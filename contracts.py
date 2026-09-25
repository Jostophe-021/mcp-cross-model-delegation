"""Small, stable public contracts for bounded delegation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

PrivacyMode = Literal["external_allowed", "approved_providers", "local_only"]


@dataclass(frozen=True)
class RoutingConstraints:
    allowed_providers: tuple[str, ...] | None = None
    privacy_mode: PrivacyMode = "external_allowed"
    approved_providers: tuple[str, ...] = ()
    max_cost: float | None = None
    max_latency: float | None = None
    require_structured_output: bool = False
    require_evidence: bool = False
    fallback_allowed: bool = False
    allow_unknown_cost: bool = False

    def __post_init__(self) -> None:
        if self.privacy_mode not in {"external_allowed", "approved_providers", "local_only"}:
            raise ValueError("Invalid privacy mode")
        for value in (self.max_cost, self.max_latency):
            if value is not None and (not isinstance(value, (int, float)) or value < 0):
                raise ValueError("Invalid routing limit")


@dataclass(frozen=True)
class DelegationRequest:
    task: str
    context: str = ""
    required_capabilities: tuple[str, ...] = ()
    constraints: RoutingConstraints = field(default_factory=RoutingConstraints)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProviderCapabilities:
    structured_output: bool = False
    usage_reporting: bool = False
    evidence_extraction: bool = False
    max_context_tokens: int | None = None
    external_provider: bool = True


@dataclass(frozen=True)
class RoutingDecision:
    provider: str
    model: str
    policy: str
    reason_codes: tuple[str, ...]
    alternatives: tuple[str, ...] = ()
    fallback_chain: tuple[str, ...] = ()
    weights: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class EvidenceVerification:
    evidence: str
    verification_status: Literal["exact", "normalized", "ambiguous", "not_found"]
    start: int | None
    end: int | None
    source_sha256: str


@dataclass(frozen=True)
class DelegationResult:
    answer: str
    provider: str
    model: str
    findings: tuple[dict[str, Any], ...] = ()
    usage_input_tokens: int | None = None
    usage_output_tokens: int | None = None


@dataclass(frozen=True)
class ExecutionTrace:
    request_id: str
    routing_decision: RoutingDecision
    selected_provider: str
    executed_provider: str | None
    fallback_used: bool
    fallback_reason: str | None
    latency_total: float
    error_code: str | None
    source_sha256: str
    retry_count: int = 0
