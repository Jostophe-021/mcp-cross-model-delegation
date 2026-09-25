"""Filter first, then rank eligible providers with reproducible policies."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Protocol

from contracts import DelegationRequest, RoutingDecision
from providers.base import DelegationProvider


class NoEligibleProvider(Exception):
    code = "NO_ELIGIBLE_PROVIDER"


class RoutingPolicy(Protocol):
    name: str

    def rank(self, eligible: list[str], request: DelegationRequest,
             history: Mapping[str, dict[str, float | None]]) -> tuple[list[str], tuple[str, ...],
                                                               dict[str, float]]: ...


@dataclass(frozen=True)
class ManualPolicy:
    provider: str
    name: str = "manual"

    def rank(self, eligible: list[str], request: DelegationRequest,
             history: Mapping[str, dict[str, float | None]]) -> tuple[list[str], tuple[str, ...],
                                                               dict[str, float]]:
        if self.provider not in eligible:
            raise NoEligibleProvider(self.provider)
        return ([self.provider] + [name for name in eligible if name != self.provider],
                ("manual_selection",), {})


@dataclass(frozen=True)
class RulesPolicy:
    name: str = "rules"

    def rank(self, eligible: list[str], request: DelegationRequest,
             history: Mapping[str, dict[str, float | None]]) -> tuple[list[str], tuple[str, ...],
                                                               dict[str, float]]:
        return sorted(eligible), ("eligible_by_constraints", "stable_name_order"), {}


DEFAULT_WEIGHTS = {
    "quality": 1.0,
    "evidence_fidelity": 1.0,
    "latency": -0.2,
    "estimated_cost": -0.2,
    "failure_rate": -0.5,
}


@dataclass(frozen=True)
class BenchmarkWeightedPolicy:
    weights: dict[str, float] = field(default_factory=lambda: dict(DEFAULT_WEIGHTS))
    name: str = "benchmark_weighted"

    def rank(self, eligible: list[str], request: DelegationRequest,
             history: Mapping[str, dict[str, float | None]]) -> tuple[list[str], tuple[str, ...],
                                                               dict[str, float]]:
        if not history:
            raise NoEligibleProvider("benchmark history unavailable")
        common = {key: weight for key, weight in self.weights.items()
                  if all(history.get(name, {}).get(key) is not None for name in eligible)}
        if not common:
            raise NoEligibleProvider("comparable benchmark history unavailable")
        def score(name: str) -> float:
            metrics = history.get(name, {})
            return sum(weight * float(metrics[key]) for key, weight in common.items())

        ranked = sorted(eligible, key=lambda name: (-score(name), name))
        return (ranked, ("supports_required_capabilities", "best_historical_score"),
                common)


class Router:
    def __init__(self, providers: Mapping[str, DelegationProvider],
                 history: Mapping[str, dict[str, float | None]] | None = None):
        self.providers = dict(providers)
        self.history = history or {}

    def inspect(self, request: DelegationRequest) -> dict[str, list[str]]:
        constraints = request.constraints
        reasons = {}
        for name, provider in self.providers.items():
            capabilities = provider.capabilities()
            metrics = self.history.get(name, {})
            rejected = []
            if (constraints.allowed_providers is not None
                    and name not in constraints.allowed_providers):
                rejected.append("not_allowed")
            if constraints.privacy_mode == "local_only" and capabilities.external_provider:
                rejected.append("external_provider_forbidden")
            if (constraints.privacy_mode == "approved_providers"
                    and name not in constraints.approved_providers):
                rejected.append("not_approved")
            if constraints.require_structured_output and not capabilities.structured_output:
                rejected.append("structured_output_unavailable")
            if constraints.require_evidence and not capabilities.evidence_extraction:
                rejected.append("evidence_extraction_unavailable")
            if any(not getattr(capabilities, required, False)
                   for required in request.required_capabilities):
                rejected.append("required_capability_unavailable")
            cost = metrics.get("estimated_cost")
            if (constraints.max_cost is not None and
                    (cost is None and not constraints.allow_unknown_cost
                     or cost is not None and cost > constraints.max_cost)):
                rejected.append("cost_unknown_or_above_limit")
            latency = metrics.get("latency")
            if constraints.max_latency is not None and (latency is None or
                                                        latency > constraints.max_latency):
                rejected.append("latency_unknown_or_above_limit")
            reasons[name] = rejected
        return reasons

    def route(self, request: DelegationRequest, policy: RoutingPolicy) -> RoutingDecision:
        rejected = self.inspect(request)
        eligible = [name for name, reasons in rejected.items() if not reasons]
        if not eligible:
            raise NoEligibleProvider("No provider satisfies the constraints")
        ranking, reasons, weights = policy.rank(eligible, request, self.history)
        selected = ranking[0]
        return RoutingDecision(selected, self.providers[selected].model, policy.name, reasons,
                               tuple(ranking[1:]),
                               tuple(ranking[1:]) if request.constraints.fallback_allowed else (),
                               weights)
