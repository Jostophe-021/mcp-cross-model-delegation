import pytest

import gateway
import server
from providers.fake import FakeProvider


@pytest.mark.parametrize("status", [429, 500, 502, 503, 504])
def test_transient_errors_are_sanitized(status):
    class ProviderError(Exception):
        status_code = status

    def fail():
        raise ProviderError("secret prompt and credential")

    result = gateway.safe_call(fail)
    assert result["error_code"] == "MODEL_TEMPORARILY_UNAVAILABLE"
    assert result["retryable"] is True
    assert "secret prompt" not in str(result)


def test_timeout_is_sanitized():
    def fail():
        raise TimeoutError("secret prompt")

    assert gateway.safe_call(fail)["error_code"] == "MODEL_TEMPORARILY_UNAVAILABLE"


def test_configuration_and_input_errors_are_distinct():
    assert gateway.safe_call(lambda: gateway._text("task", "", 10))["error_code"] == "INVALID_INPUT"

    def no_config():
        raise gateway.ConfigurationError("secret prompt")

    assert gateway.safe_call(no_config)["error_code"] == "CONFIGURATION_ERROR"


def test_mcp_tool_uses_injected_gateway_without_network(monkeypatch):
    provider = FakeProvider("done")
    monkeypatch.setattr(server, "configured_providers", lambda: {"gemini": provider})
    result = server.gemini_delegate_task("test", "data")
    assert result["answer"] == "done"
    assert result["trace"]["routing_decision"]["policy"] == "manual"
    assert server.delegate_task("test", "data", provider="gemini")["answer"] == "done"
    assert server.delegate_task("test", "data", provider="missing")["error_code"] == (
        "NO_ELIGIBLE_PROVIDER")


def test_legacy_extract_verifies_evidence(monkeypatch):
    provider = FakeProvider('{"summary":"ok","findings":[{"finding":"count","evidence":'
                            '"12 tickets","source_label":"context","uncertainty":"none"}]}')
    monkeypatch.setattr(server, "configured_providers", lambda: {"gemini": provider})
    result = server.gemini_extract_findings("Count?", "Monday: 12 tickets.")
    assert result["findings"][0]["verification"]["verification_status"] == "exact"
