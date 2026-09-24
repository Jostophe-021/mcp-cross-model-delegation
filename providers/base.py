"""Small provider contract; new providers need no changes to the MCP layer."""

from typing import Protocol

from contracts import ProviderCapabilities


class DelegationProvider(Protocol):
    name: str
    model: str

    def capabilities(self) -> ProviderCapabilities: ...

    def delegate(self, prompt: str, max_output_tokens: int, timeout_seconds: float) -> str: ...

    def extract_findings(
        self, prompt: str, schema: dict, max_output_tokens: int, timeout_seconds: float
    ) -> str: ...
