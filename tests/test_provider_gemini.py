from types import SimpleNamespace

from providers.gemini import GeminiProvider


class FakeInteractions:
    def __init__(self, output):
        self.output = output
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(output_text=self.output)


def test_gemini_calls_are_stateless_and_bounded():
    interactions = FakeInteractions("answer")
    provider = GeminiProvider("gemini-test-model", SimpleNamespace(interactions=interactions))
    assert provider.delegate("prompt", 512, 15) == "answer"
    call = interactions.calls[0]
    assert call["store"] is False
    assert call["timeout"] == 15
    assert call["generation_config"]["max_output_tokens"] == 512
    assert call["input"] == "prompt"


def test_gemini_structured_output_uses_schema():
    interactions = FakeInteractions('{"summary":"ok","findings":[]}')
    provider = GeminiProvider("gemini-test-model", SimpleNamespace(interactions=interactions))
    schema = {"type": "object"}
    provider.extract_findings("prompt", schema, 512, 15)
    assert interactions.calls[0]["response_format"] == [
        {"type": "text", "mime_type": "application/json", "schema": schema}
    ]
    assert interactions.calls[0]["store"] is False
