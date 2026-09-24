from types import SimpleNamespace

from providers.anthropic import AnthropicProvider


class FakeMessages:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(stop_reason="end_turn", content=[
            SimpleNamespace(type="text", text="ok")])


def test_anthropic_uses_messages_without_implicit_retries():
    messages = FakeMessages()
    provider = AnthropicProvider("claude-haiku-4-5-20251001", SimpleNamespace(messages=messages))
    assert provider.delegate("prompt", 123, 7) == "ok"
    assert messages.calls[0]["model"] == provider.model
    assert messages.calls[0]["timeout"] == 7
    assert messages.calls[0]["max_tokens"] == 123
    assert messages.calls[0]["messages"] == [{"role": "user", "content": "prompt"}]


def test_anthropic_structured_schema_is_compatible():
    messages = FakeMessages()
    provider = AnthropicProvider("test", SimpleNamespace(messages=messages))
    provider.extract_findings("prompt", {"type": "object", "properties": {"items": {
        "type": "array", "maxItems": 20, "items": {"type": "object", "properties": {}}
    }}}, 123, 7)
    schema = messages.calls[0]["output_config"]["format"]["schema"]
    assert schema["additionalProperties"] is False
    assert "maxItems" not in schema["properties"]["items"]
    assert schema["properties"]["items"]["items"]["additionalProperties"] is False
