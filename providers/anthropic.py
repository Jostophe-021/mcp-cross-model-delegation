"""Anthropic Messages adapter. The SDK is an optional dependency."""

from typing import Any

from contracts import ProviderCapabilities


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model: str, client: Any):
        self.model = model
        self.client = client

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(structured_output=True, evidence_extraction=True)

    def _create(self, prompt: str, max_output_tokens: int, timeout_seconds: float,
                output_config: dict | None = None) -> str:
        params: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_output_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "timeout": timeout_seconds,
        }
        if output_config is not None:
            params["output_config"] = output_config
        response = self.client.messages.create(**params)
        if response.stop_reason not in {"end_turn", "stop_sequence"}:
            return ""
        return "".join(block.text for block in response.content if block.type == "text")

    def delegate(self, prompt: str, max_output_tokens: int, timeout_seconds: float) -> str:
        return self._create(prompt, max_output_tokens, timeout_seconds)

    def extract_findings(self, prompt: str, schema: dict, max_output_tokens: int,
                         timeout_seconds: float) -> str:
        # Anthropic's strict JSON schema excludes maxItems and requires closed objects.
        def compatible(node: object) -> object:
            if isinstance(node, list):
                return [compatible(item) for item in node]
            if isinstance(node, dict):
                clean = {key: compatible(value) for key, value in node.items()
                         if key != "maxItems"}
                if clean.get("type") == "object":
                    clean["additionalProperties"] = False
                return clean
            return node

        output_config = {"format": {"type": "json_schema", "schema": compatible(schema)}}
        return self._create(prompt, max_output_tokens, timeout_seconds, output_config)
