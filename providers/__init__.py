"""Secondary-model providers; SDKs load only for configured providers."""

import os

from providers.base import DelegationProvider

GEMINI_DEFAULT = "gemini-3.5-flash-lite"
ANTHROPIC_DEFAULT = "claude-haiku-4-5-20251001"


def provider_status() -> dict[str, dict[str, str | bool]]:
    return {
        "gemini": {"model": os.getenv("GEMINI_MODEL", GEMINI_DEFAULT),
                   "configured": bool(os.getenv("GEMINI_API_KEY")), "structured_output": True},
        "anthropic": {"model": os.getenv("ANTHROPIC_MODEL", ANTHROPIC_DEFAULT),
                      "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
                      "structured_output": True},
    }


def configured_providers() -> dict[str, DelegationProvider]:
    providers: dict[str, DelegationProvider] = {}
    status = provider_status()
    if status["gemini"]["configured"]:
        from google import genai
        from google.genai import types

        from providers.gemini import GeminiProvider

        providers["gemini"] = GeminiProvider(str(status["gemini"]["model"]),
            genai.Client(api_key=os.environ["GEMINI_API_KEY"],
                         http_options=types.HttpOptions(
                             retry_options=types.HttpRetryOptions(attempts=1))))
    if status["anthropic"]["configured"]:
        from anthropic import Anthropic

        from providers.anthropic import AnthropicProvider

        # The SDK otherwise retries transient failures twice by default.
        providers["anthropic"] = AnthropicProvider(
            str(status["anthropic"]["model"]),
            Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=0))
    return providers
