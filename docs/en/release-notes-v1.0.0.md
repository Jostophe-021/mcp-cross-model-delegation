# v1.0.0 — Stable Cross-Model Routing & Evaluation Framework

MCP Cross-Model Delegation is a small, local-first framework for measuring, comparing, routing, and verifying bounded work across language models.

## Included in this release

- Optional Gemini and Anthropic provider adapters, plus a deterministic `FakeProvider` for offline validation.
- Constraint-first routing with `manual`, `rules`, and `benchmark_weighted` policies, explainable `RoutingDecision` records, privacy-aware constraints, and explicit fallback tracing.
- Local quotation verification against the supplied context.
- A reproducible benchmark runner with deterministic evaluators, CLI commands, and generic MCP tools. The V0.1 Gemini tool names remain as compatibility aliases.
- English and French documentation, local-first security defaults, OCI metadata and SPDX SBOM release workflow, and MCP Registry-ready metadata.

The five-minute offline demo is `uv run crossmodel bench run benchmarks/datasets/basic.jsonl` after `uv sync --locked --extra all --extra test`. It needs no API key. Live provider calls require separate credentials and explicit opt-in.

**This release provides the framework and reproducible synthetic validation. It does not claim that cross-model delegation improves quality, cost, latency or token usage without measured experiments.**
