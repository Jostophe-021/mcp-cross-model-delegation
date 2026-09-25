"""Inspect a privacy-constrained route without network access."""

from contracts import DelegationRequest, RoutingConstraints
from providers.fake import FakeProvider
from routing import Router, RulesPolicy

router = Router({"local": FakeProvider(), "external": FakeProvider(external=True)})
request = DelegationRequest("Synthetic task", constraints=RoutingConstraints(
    privacy_mode="local_only"))
print(router.inspect(request))
print(router.route(request, RulesPolicy()))
