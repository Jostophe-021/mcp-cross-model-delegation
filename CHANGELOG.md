# Changelog

## 1.0.0 — 2026-09-25

- Stabilizes the small Provider, RoutingConstraints, RoutingDecision, DelegationResult, and benchmark record contracts.
- Adds Anthropic and deterministic Fake providers alongside Gemini.
- Adds explicit manual, rules, and benchmark-weighted routing after constraint filtering.
- Adds local quotation verification with offsets and SHA-256 source hashes.
- Adds a reproducible sequential benchmark runner, deterministic evaluators, CLI, and generic MCP tools.
- Retains both Gemini MCP tool names as compatibility aliases.
- Prepares optional SDK extras, CI package/Docker checks, and V1 OCI SBOM release workflow.

V1 stabilizes these contracts because they are the minimum common interface needed to measure, compare, route, and verify bounded work. Future incompatible changes follow Semantic Versioning.

## 0.1.0 — Experimental Research Preview

- Initial Gemini MCP bridge, local-only bind, TASK/CONTEXT separation, sanitized errors, tests, and research plan.
