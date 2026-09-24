"""One small command-line entry point for serving, inspection, and benchmarks."""

from __future__ import annotations

import argparse
import json
import os
import platform
from dataclasses import asdict
from pathlib import Path

from benchmarks.runner import CONDITIONS, run
from contracts import DelegationRequest, RoutingConstraints
from providers import configured_providers, provider_status
from providers.fake import FakeProvider
from routing import BenchmarkWeightedPolicy, ManualPolicy, NoEligibleProvider, Router, RulesPolicy


def _history(path: str | None) -> dict:
    return json.loads(Path(path).read_text()) if path else {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="crossmodel")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("serve")
    commands.add_parser("doctor")
    commands.add_parser("providers")
    route = commands.add_parser("route")
    route_sub = route.add_subparsers(dest="route_command", required=True)
    explain = route_sub.add_parser("explain")
    explain.add_argument("--provider")
    explain.add_argument("--policy", choices=("manual", "rules", "benchmark_weighted"),
                         default="manual")
    explain.add_argument("--constraints", default="{}", help="JSON RoutingConstraints object")
    explain.add_argument("--history")
    bench = commands.add_parser("bench")
    bench_sub = bench.add_subparsers(dest="bench_command", required=True)
    bench_run = bench_sub.add_parser("run")
    bench_run.add_argument("dataset", type=Path)
    bench_run.add_argument("--live", action="store_true")
    bench_run.add_argument("--provider", default="fake")
    bench_run.add_argument("--orchestrator", default="fake")
    bench_run.add_argument("--condition", action="append", choices=CONDITIONS)
    bench_run.add_argument("--repetitions", type=int, default=1)
    bench_run.add_argument("--shuffle", action="store_true")
    bench_run.add_argument("--seed", type=int, default=42)
    bench_run.add_argument("--policy", choices=("rules", "benchmark_weighted"), default="rules")
    bench_run.add_argument("--history")
    bench_run.add_argument("--output", type=Path, default=Path("results"))
    bench_run.add_argument("--save-responses", action="store_true")
    bench_report = bench_sub.add_parser("report")
    bench_report.add_argument("run_directory", type=Path)
    bench_generate = bench_sub.add_parser("generate")
    bench_generate.add_argument("output", type=Path)
    bench_generate.add_argument("--size", choices=("small", "medium", "large"),
                                default="small")
    bench_generate.add_argument("--seed", type=int, default=42)
    args = parser.parse_args(argv)
    if args.command == "serve":
        from server import main as serve
        serve()
        return 0
    if args.command == "doctor":
        status = provider_status()
        report = {"python": platform.python_version(), "package_version": "1.0.0-dev",
                  "mcp_host": os.getenv("MCP_HOST", "127.0.0.1"),
                  "mcp_bind_safe": os.getenv("MCP_HOST", "127.0.0.1") in
                  {"127.0.0.1", "localhost"},
                  "providers": status, "benchmark_directory":
                  "present" if Path("benchmarks/datasets").is_dir() else "missing"}
        print(json.dumps(report, indent=2))
        return 0 if report["mcp_bind_safe"] else 1
    if args.command == "providers":
        print(json.dumps(provider_status(), indent=2))
        return 0
    if args.command == "route":
        try:
            constraints = RoutingConstraints(**json.loads(args.constraints))
            providers = configured_providers()
            router = Router(providers, _history(args.history))
            request = DelegationRequest("routing inspection", constraints=constraints)
            default = (args.provider or os.getenv("DEFAULT_PROVIDER") or
                       ("gemini" if "gemini" in providers else next(iter(providers), "gemini")))
            policy = (ManualPolicy(default)
                      if args.policy == "manual" else RulesPolicy() if args.policy == "rules"
                      else BenchmarkWeightedPolicy())
            inspection = router.inspect(request)
            decision = router.route(request, policy)
            components = {name: {key: weight * router.history.get(name, {}).get(key, 0)
                                 for key, weight in decision.weights.items()}
                          for name in inspection if not inspection[name] and
                          all(router.history.get(name, {}).get(key) is not None
                              for key in decision.weights)}
            print(json.dumps({"eligible": [name for name, reasons in inspection.items()
                                           if not reasons], "rejected": {name: reasons for name,
                                           reasons in inspection.items() if reasons},
                              "decision": asdict(decision), "score_components": components},
                             indent=2))
            return 0
        except (ValueError, TypeError, NoEligibleProvider) as error:
            print(json.dumps({"error_code": "NO_ELIGIBLE_PROVIDER" if isinstance(
                error, NoEligibleProvider) else "INVALID_INPUT"}))
            return 1
    if args.bench_command == "report":
        print((args.run_directory / "summary.json").read_text())
        return 0
    if args.bench_command == "generate":
        from benchmarks.generate import generate
        generate(args.output, args.size, args.seed)
        print(args.output)
        return 0
    try:
        providers = configured_providers() if args.live else {"fake": FakeProvider()}
        output = run(args.dataset, Router(providers, _history(args.history)),
                     conditions=tuple(args.condition or CONDITIONS), repetitions=args.repetitions,
                     shuffle=args.shuffle, seed=args.seed, live=args.live,
                     orchestrator=args.orchestrator, provider=args.provider,
                     routing_policy=args.policy, output=args.output,
                     save_responses=args.save_responses)
        print(output)
        return 0
    except (ValueError, OSError, NoEligibleProvider) as error:
        print(f"Benchmark failed: {type(error).__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
