"""The only provider implementation in the research preview."""

from typing import Any

from contracts import ProviderCapabilities


class GeminiProvider:
    name = "gemini"

    def __init__(self, model: str, client: Any):
        self.model = model
        self.client = client

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(structured_output=True, evidence_extraction=True)

    def _generation_config(self, max_output_tokens: int) -> dict:
        return {"thinking_level": "low", "max_output_tokens": max_output_tokens}

    def delegate(self, prompt: str, max_output_tokens: int, timeout_seconds: float) -> str:
        response = self.client.interactions.create(
            model=self.model,
            input=prompt,
            store=False,
            timeout=timeout_seconds,
            generation_config=self._generation_config(max_output_tokens),
        )
        return getattr(response, "output_text", None)

    def extract_findings(
        self, prompt: str, schema: dict, max_output_tokens: int, timeout_seconds: float
    ) -> str:
        response = self.client.interactions.create(
            model=self.model,
            input=prompt,
            store=False,
            timeout=timeout_seconds,
            generation_config=self._generation_config(max_output_tokens),
            response_format=[
                {"type": "text", "mime_type": "application/json", "schema": schema}
            ],
        )
        return getattr(response, "output_text", None)
