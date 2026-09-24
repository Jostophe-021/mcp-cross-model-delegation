"""Execute a routing decision once; optionally fall back after retryable failures."""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import asdict

from contracts import DelegationRequest, DelegationResult, ExecutionTrace
from evidence import EvidenceVerifier, source_hash
from gateway import Gateway, Settings, _text, safe_call
from routing import Router, RoutingPolicy

logger = logging.getLogger("crossmodel")


def execute(request: DelegationRequest, router: Router, policy: RoutingPolicy,
            settings: Settings, *, structured: bool = False) -> tuple[DelegationResult | None,
                                                                     ExecutionTrace]:
    started = time.monotonic()
    request_id = uuid.uuid4().hex
    # Validate before routing, including context length; hash the exact context sent onward.
    task = _text("task", request.task, settings.max_task_chars)
    context = _text("context", request.context, settings.max_context_chars, False)
    validated = DelegationRequest(task, context, request.required_capabilities,
                                  request.constraints, request.metadata)
    decision = router.route(validated, policy)
    names = (decision.provider, *decision.fallback_chain)
    last_error = None
    fallback_reason = None
    for index, name in enumerate(names):
        provider = router.providers[name]
        gateway = Gateway(provider, settings)
        operation = (lambda: gateway.extract_findings(task, context)) if structured else (
            lambda: gateway.delegate(task, context))
        result = safe_call(operation)
        if "error_code" not in result:
            findings = []
            if structured:
                verifier = EvidenceVerifier()
                for finding in result["findings"]:
                    item = dict(finding)
                    item["verification"] = asdict(verifier.verify(item["evidence"], context))
                    findings.append(item)
            trace = ExecutionTrace(request_id, decision, decision.provider, name, index > 0,
                                   fallback_reason, time.monotonic() - started, None,
                                   source_hash(context))
            logger.info(json.dumps({"request_id": request_id, "operation": "extract" if structured
                                    else "delegate", "provider": name, "model": provider.model,
                                    "routing_policy": policy.name,
                                    "duration": trace.latency_total, "status": "ok"}))
            return (DelegationResult(result.get("answer", result.get("summary", "")),
                                     name, provider.model, tuple(findings)), trace)
        last_error = result["error_code"]
        if index == 0:
            fallback_reason = last_error
        if not result["retryable"]:
            break
    trace = ExecutionTrace(request_id, decision, decision.provider, name, index > 0,
                           fallback_reason if index > 0 else None,
                           time.monotonic() - started, last_error, source_hash(context))
    logger.info(json.dumps({"request_id": request_id, "operation": "extract" if structured
                            else "delegate", "provider": decision.provider,
                            "model": decision.model, "routing_policy": policy.name,
                            "duration": trace.latency_total, "status": last_error}))
    return None, trace
