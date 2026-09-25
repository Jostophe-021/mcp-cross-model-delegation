"""Loopback-only MCP server exposing bounded, read-only delegation tools."""

import json
import os
from dataclasses import asdict
from pathlib import Path

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from contracts import DelegationRequest, RoutingConstraints
from execution import execute
from gateway import ConfigurationError, Settings, safe_call
from providers import configured_providers
from routing import BenchmarkWeightedPolicy, ManualPolicy, Router, RulesPolicy

server = MCPServer(
    "Cross-Model Delegation",
    instructions=(
        "Send only data the user authorizes to share with the configured third-party provider. "
        "Verify secondary-model output before important decisions. These tools handle text; "
        "they do not read applications, email, or Drive, and do not execute code."
    ),
)


def _configured_history() -> dict:
    path = os.getenv("CROSSMODEL_HISTORY_PATH")
    if not path:
        return {}
    try:
        history = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(history, dict) or any(
            not isinstance(metrics, dict) for metrics in history.values()
        ):
            raise ValueError("Invalid benchmark history")
        return history
    except (OSError, ValueError) as error:
        raise ConfigurationError("Invalid benchmark history") from error


def _run(task: str, context: str, provider: str | None, policy: str,
         constraints: dict | None, *, structured: bool = False) -> dict:
    if policy not in {"manual", "rules", "benchmark_weighted"}:
        raise ValueError("Invalid policy")
    try:
        limits = RoutingConstraints(**(constraints or {}))
    except TypeError as error:
        raise ValueError("Invalid constraints") from error
    providers = configured_providers()
    chosen = (provider or os.getenv("DEFAULT_PROVIDER") or
              ("gemini" if "gemini" in providers else next(iter(providers), "gemini")))
    selected_policy = (ManualPolicy(chosen) if policy == "manual" else RulesPolicy()
                       if policy == "rules" else BenchmarkWeightedPolicy())
    router = Router(providers, _configured_history() if policy == "benchmark_weighted" else {})
    result, trace = execute(DelegationRequest(task, context, constraints=limits), router,
                            selected_policy, Settings.from_env(), structured=structured)
    if result is None:
        return {"error_code": trace.error_code, "message": "The delegated model request failed.",
                "retryable": trace.error_code == "MODEL_TEMPORARILY_UNAVAILABLE",
                "trace": asdict(trace)}
    payload = {"model": result.model, "provider": result.provider,
               "answer": result.answer, "trace": asdict(trace)}
    if structured:
        payload["summary"] = result.answer
        payload["findings"] = result.findings
    return payload


@server.tool(
    title="Delegate a bounded task",
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True, destructiveHint=False),
)
def delegate_task(task: str, context: str = "", provider: str | None = None,
                  policy: str = "manual", constraints: dict | None = None) -> dict:
    """Delegate authorized text; automatic routing requires an explicit policy."""
    return safe_call(lambda: _run(task, context, provider, policy, constraints))


@server.tool(
    title="Extract locally verified findings",
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True, destructiveHint=False),
)
def extract_findings(question: str, context: str, provider: str | None = None,
                     policy: str = "manual", constraints: dict | None = None) -> dict:
    """Extract quotations and verify their offsets against the caller's context."""
    return safe_call(lambda: _run(question, context, provider, policy, constraints,
                                  structured=True))


@server.tool(
    title="Delegate a bounded task to Gemini (compatibility alias)",
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True, destructiveHint=False),
)
def gemini_delegate_task(task: str, context: str = "") -> dict:
    """Send authorized text to Gemini for a bounded intellectual task.

    Never send confidential or personal data without appropriate authorization.
    Gemini cannot act in user applications, and its answer needs verification.
    """
    return delegate_task(task, context, provider="gemini", policy="manual")


@server.tool(
    title="Extract evidence-backed findings with Gemini (compatibility alias)",
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True, destructiveHint=False),
)
def gemini_extract_findings(question: str, context: str) -> dict:
    """Extract up to 20 findings from authorized text; evidence is verified locally.

    This tool cannot fetch email, Drive, or app data and cannot execute code.
    Treat the secondary model as fallible and check important findings yourself.
    """
    return extract_findings(question, context, provider="gemini", policy="manual")


def main() -> None:
    host = os.getenv("MCP_HOST", "127.0.0.1")
    if host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Refusing a network-visible bind without client authentication")
    try:
        port = int(os.getenv("PORT", "8000"))
    except ValueError as error:
        raise SystemExit("PORT must be an integer") from error
    if not 1 <= port <= 65535:
        raise SystemExit("PORT is outside the valid range")
    server.run(
        transport="streamable-http",
        host=host,
        port=port,
        stateless_http=True,
        json_response=True,
    )


if __name__ == "__main__":
    main()
