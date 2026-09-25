"""Synthetic local example; replace FakeProvider only after choosing a data policy."""

from contracts import DelegationRequest
from execution import execute
from gateway import Settings
from providers.fake import FakeProvider
from routing import ManualPolicy, Router

router = Router({"fake": FakeProvider("20")})
result, trace = execute(DelegationRequest("Calculate 12 + 8."), router,
                        ManualPolicy("fake"), Settings())
print(result.answer, trace.routing_decision.reason_codes)
