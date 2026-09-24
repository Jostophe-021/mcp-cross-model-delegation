import pytest

import gateway
import server


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
    class FakeGateway:
        def delegate(self, task, context):
            return {"model": "fake", "answer": f"{task}:{context}"}

    monkeypatch.setattr(server, "make_gateway", FakeGateway)
    assert server.gemini_delegate_task("test", "data") == {"model": "fake", "answer": "test:data"}
