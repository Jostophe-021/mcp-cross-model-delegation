# Security policy

English | [Français](SECURITY.fr.md)

## Reporting

Please use GitHub's **private vulnerability reporting** for this repository if it is enabled. If no private channel is available, open a public issue containing only a minimal, non-sensitive request to establish a private reporting channel. Do not post exploit details, API keys, real prompts, user data, or private infrastructure information in a public issue or pull request. No security email address is claimed here.

## Scope and current risks

This is an experimental preview, not a hardened service. The primary risks are indirect prompt injection in CONTEXT, accidental sharing of sensitive text with a third-party provider, output hallucination or manipulation, an invalid structured response, a compromised dependency, a misconfigured public listener, and accidental secret or payload logging. The default loopback bind, size limits, no custom telemetry, `store=False`, fixed error responses, and fake-client tests reduce some risks but do not eliminate them. A model boundary is not a security boundary by itself.

Do not expose the MCP endpoint publicly without suitable authentication and transport security. Do not use secondary-model answers as the sole basis for high-impact decisions. Provider policies and the client/host logging environment also matter. See the [threat table](docs/en/security-model.md).
