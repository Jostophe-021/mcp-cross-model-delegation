import pytest

from contracts import DelegationRequest, RoutingConstraints
from providers.fake import FakeProvider
from routing import BenchmarkWeightedPolicy, ManualPolicy, NoEligibleProvider, Router, RulesPolicy


def test_manual_privacy_and_unknown_cost_filter_before_ranking():
    router = Router({"external": FakeProvider(external=True), "local": FakeProvider()})
    request = DelegationRequest("task", constraints=RoutingConstraints(privacy_mode="local_only"))
    assert router.route(request, RulesPolicy()).provider == "local"
    with pytest.raises(NoEligibleProvider):
        router.route(request, ManualPolicy("external"))
    with pytest.raises(NoEligibleProvider):
        router.route(DelegationRequest("task", constraints=RoutingConstraints(max_cost=1)),
                     RulesPolicy())
    allowed = DelegationRequest("task", constraints=RoutingConstraints(max_cost=1,
                                                                  allow_unknown_cost=True))
    assert router.route(allowed, ManualPolicy("local")).provider == "local"


def test_approved_providers_and_capabilities():
    router = Router({"a": FakeProvider(), "b": FakeProvider(external=True)})
    request = DelegationRequest("task", constraints=RoutingConstraints(
        privacy_mode="approved_providers", approved_providers=("b",),
        require_structured_output=True, require_evidence=True))
    assert router.route(request, RulesPolicy()).provider == "b"


def test_benchmark_weights_and_explainable_fallback():
    history = {
        "a": {"quality": .9, "evidence_fidelity": .9, "latency": .1,
              "estimated_cost": .1, "failure_rate": 0.0},
        "b": {"quality": .5, "evidence_fidelity": .5, "latency": .1,
              "estimated_cost": .1, "failure_rate": 0.0},
    }
    router = Router({"a": FakeProvider(), "b": FakeProvider()}, history)
    request = DelegationRequest("task", constraints=RoutingConstraints(fallback_allowed=True))
    decision = router.route(request, BenchmarkWeightedPolicy())
    assert decision.provider == "a"
    assert decision.fallback_chain == ("b",)
    assert decision.weights["quality"] == 1.0
    assert "best_historical_score" in decision.reason_codes


def test_disallowed_provider_cannot_win_with_higher_score():
    history = {name: {"quality": quality, "evidence_fidelity": 1,
                      "latency": 0, "estimated_cost": 0, "failure_rate": 0}
               for name, quality in (("external", 1), ("local", .1))}
    router = Router({"external": FakeProvider(external=True),
                     "local": FakeProvider()}, history)
    request = DelegationRequest("task", constraints=RoutingConstraints(privacy_mode="local_only"))
    assert router.route(request, BenchmarkWeightedPolicy()).provider == "local"
