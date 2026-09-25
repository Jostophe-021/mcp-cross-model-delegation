"""Deterministic provider for tests and synthetic benchmarks only."""

from contracts import ProviderCapabilities


class FakeProvider:
    name = "fake"

    def __init__(self, answer: str = "", model: str = "fake-deterministic",
                 external: bool = False):
        self.model = model
        self.answer = answer
        self.external = external
        self.calls: list[str] = []

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(structured_output=True, evidence_extraction=True,
                                    external_provider=self.external)

    def delegate(self, prompt: str, max_output_tokens: int, timeout_seconds: float) -> str:
        self.calls.append(prompt)
        return self.answer

    def extract_findings(self, prompt: str, schema: dict, max_output_tokens: int,
                         timeout_seconds: float) -> str:
        self.calls.append(prompt)
        return self.answer
