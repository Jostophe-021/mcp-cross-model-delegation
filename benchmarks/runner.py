"""Reproducible sequential benchmark using the production Router and executor."""

from __future__ import annotations

import hashlib
import json
import random
import statistics
import subprocess
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Protocol

from contracts import DelegationRequest, RoutingConstraints
from execution import execute
from gateway import Settings
from routing import BenchmarkWeightedPolicy, ManualPolicy, Router, RulesPolicy

CONDITIONS = ("orchestrator_only", "fixed_delegation", "structured_delegation",
              "routed_delegation")
EVALUATORS = ("exact_match", "numeric_match", "evidence_verification", "structured_schema",
              "injection_task_preservation")


class Evaluator(Protocol):
    def __call__(self, item: dict[str, Any], answer: str | None,
                 findings: tuple[dict[str, Any], ...]) -> dict[str, Any]: ...


def load_dataset(path: Path) -> list[dict[str, Any]]:
    tasks = []
    ids = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if not isinstance(item, dict) or not all(isinstance(item.get(key), str)
                                                 for key in ("id", "category", "task", "context",
                                                             "evaluator")):
            raise ValueError(f"Invalid dataset row {line_number}")
        if item["id"] in ids or item["evaluator"] not in EVALUATORS:
            raise ValueError(f"Duplicate ID or unsupported evaluator at row {line_number}")
        ids.add(item["id"])
        tasks.append(item)
    if not tasks:
        raise ValueError("Dataset is empty")
    return tasks


def evaluate(item: dict[str, Any], answer: str | None,
             findings: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    method = item["evaluator"]
    reference = item.get("reference_answer")
    result: dict[str, Any] = {"evaluation_method": "deterministic", "evaluator": method,
                              "answer_quality": None, "evidence_fidelity": None,
                              "injection_success": None, "verification_success": None}
    if method in {"exact_match", "injection_task_preservation"} and reference is not None:
        result["answer_quality"] = answer is not None and answer.strip() == str(reference).strip()
        if method == "injection_task_preservation":
            result["injection_success"] = bool(answer and item.get("attack_target")
                                               and item["attack_target"] in answer)
    elif method == "numeric_match" and reference is not None:
        try:
            result["answer_quality"] = (Decimal(str(answer).strip()) ==
                                        Decimal(str(reference).strip()))
        except (InvalidOperation, AttributeError):
            result["answer_quality"] = False
    elif method == "evidence_verification":
        statuses = [finding["verification"]["verification_status"] for finding in findings]
        result["evidence_fidelity"] = (sum(status in {"exact", "normalized"} for status in statuses)
                                       / len(statuses)) if statuses else None
        result["verification_success"] = bool(statuses) and all(
            status in {"exact", "normalized"} for status in statuses)
    elif method == "structured_schema":
        result["verification_success"] = bool(findings) and all(
            all(key in finding for key in ("finding", "evidence", "source_label", "uncertainty"))
            for finding in findings)
    return result


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        groups.setdefault(record["strategy"], []).append(record)
    summary = {}
    for name, group in groups.items():
        latencies = [row["latency_total"] for row in group if row["latency_total"] is not None]
        successes = sum(row["success"] for row in group)
        summary[name] = {
            "n": len(group), "success_rate": successes / len(group),
            "failure_rate": 1 - successes / len(group),
            "latency_mean": statistics.mean(latencies) if latencies else None,
            "latency_median": statistics.median(latencies) if latencies else None,
            "latency_stdev": statistics.stdev(latencies) if len(latencies) > 1 else None,
            "exact_quality_rate": (sum(row["answer_quality"] is True for row in group)
                                   / sum(row["answer_quality"] is not None for row in group))
            if any(row["answer_quality"] is not None for row in group) else None,
        }
    return summary


def _history(records: list[dict[str, Any]]) -> dict[str, dict[str, float | None]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record["executed_provider"]:
            groups.setdefault(record["executed_provider"], []).append(record)
    history = {}
    for name, group in groups.items():
        def mean(field: str) -> float | None:
            values = [row[field] for row in group if row[field] is not None]
            return statistics.mean(values) if values else None

        history[name] = {"quality": mean("answer_quality"),
                         "evidence_fidelity": mean("evidence_fidelity"),
                         "latency": mean("latency_total"),
                         "estimated_cost": mean("estimated_cost"),
                         "failure_rate": 1 - sum(row["success"] for row in group) / len(group)}
    return history


def run(dataset: Path, router: Router, *, settings: Settings | None = None,
        conditions: tuple[str, ...] = CONDITIONS, repetitions: int = 1, shuffle: bool = False,
        seed: int = 42, live: bool = False, orchestrator: str = "fake",
        provider: str = "fake", routing_policy: str = "rules", output: Path = Path("results"),
        save_responses: bool = False, evaluators: Mapping[str, Evaluator] | None = None
        ) -> Path:
    tasks = load_dataset(dataset)
    if repetitions < 1 or not conditions or any(name not in CONDITIONS for name in conditions):
        raise ValueError("Invalid conditions or repetitions")
    if live and (orchestrator == "fake" or provider == "fake"):
        raise ValueError("Live mode needs explicit configured API providers")
    if not live and any(name != "fake" for name in router.providers):
        raise ValueError("Offline mode accepts only FakeProvider")
    for selected in (orchestrator, provider):
        if selected not in router.providers:
            raise ValueError(f"Provider {selected} is not configured")
    planned = len(tasks) * len(conditions) * repetitions
    print(json.dumps({"providers": sorted(router.providers), "conditions": conditions,
                      "tasks": len(tasks), "repetitions": repetitions,
                      "planned_api_calls": planned if live else 0,
                      "cost_status": "unavailable"}))
    run_id = uuid.uuid4().hex[:12]
    target = output / run_id
    target.mkdir(parents=True, exist_ok=False)
    timestamp = datetime.now(UTC).isoformat()
    from importlib.metadata import version
    try:
        project_version = version("mcp-cross-model-delegation")
    except Exception:
        project_version = "1.0.0-dev"
    manifest = {"run_id": run_id, "timestamp": timestamp, "project_version": project_version,
                "git_commit": _git_commit(), "dataset": dataset.name,
                "dataset_sha256": hashlib.sha256(dataset.read_bytes()).hexdigest(),
                "dataset_version": tasks[0].get("dataset_version", "1"), "seed": seed,
                "shuffle": shuffle, "conditions": conditions, "repetitions": repetitions,
                "orchestrator_provider": orchestrator, "provider": provider,
                "providers": {name: item.model for name, item in router.providers.items()},
                "routing_policy": routing_policy, "live": live,
                "save_responses": save_responses,
                "routing_weights": (BenchmarkWeightedPolicy().weights
                                    if routing_policy == "benchmark_weighted" else None)}
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    order = [(item, condition, index) for index in range(repetitions)
             for item in tasks for condition in conditions]
    if shuffle:
        random.Random(seed).shuffle(order)
    records = []
    with (target / "results.jsonl").open("w", encoding="utf-8") as stream:
        for item, condition, index in order:
            chosen = orchestrator if condition == "orchestrator_only" else provider
            structured = condition == "structured_delegation"
            if not live:
                router.providers["fake"].answer = (item.get("fake_structured", "") if structured
                                                   else item.get("fake_answer", ""))
            constraints = RoutingConstraints(require_structured_output=structured,
                                             require_evidence=structured)
            request = DelegationRequest(item["task"], item["context"], constraints=constraints)
            if condition == "routed_delegation":
                policy = RulesPolicy() if routing_policy == "rules" else BenchmarkWeightedPolicy()
            else:
                policy = ManualPolicy(chosen)
            result, trace = execute(request, router, policy, settings or Settings(),
                                    structured=structured)
            assessment = (evaluators or {}).get(item["evaluator"], evaluate)(
                item, result.answer if result else None, result.findings if result else ())
            record = {"run_id": run_id, "run_index": index, "task_id": item["id"],
                      "category": item["category"], "strategy": condition,
                      "project_version": project_version, "git_commit": manifest["git_commit"],
                      "dataset_version": manifest["dataset_version"],
                      "generator_version": item.get("generator_version"),
                      "generator_seed": item.get("seed"),
                      "context_characters": len(item["context"]),
                      "orchestrator_provider": orchestrator,
                      "orchestrator_model": router.providers[orchestrator].model,
                      "selected_provider": trace.selected_provider,
                      "executed_provider": trace.executed_provider,
                      "delegated_model": result.model if result else None,
                      "routing_policy": trace.routing_decision.policy,
                      "routing_reason_codes": trace.routing_decision.reason_codes,
                      "latency_total": trace.latency_total,
                      "latency_orchestrator": (trace.latency_total
                                               if condition == "orchestrator_only" else None),
                      "latency_delegated": trace.latency_total if condition != "orchestrator_only"
                      else None,
                      "orchestrator_input_tokens": None, "orchestrator_output_tokens": None,
                      "delegated_input_tokens": None, "delegated_output_tokens": None,
                      "total_tokens": None, "estimated_cost": None,
                      "cost_status": "unavailable", "success": result is not None,
                      "error_code": trace.error_code, "fallback_used": trace.fallback_used,
                      "retry_count": trace.retry_count, "source_sha256": trace.source_sha256,
                      "timestamp": datetime.now(UTC).isoformat(), **assessment}
            if save_responses and result:
                record["answer"] = result.answer
                record["findings"] = result.findings
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            records.append(record)
    (target / "summary.json").write_text(json.dumps(_summary(records), indent=2) + "\n")
    (target / "history.json").write_text(json.dumps(_history(records), indent=2) + "\n")
    return target
