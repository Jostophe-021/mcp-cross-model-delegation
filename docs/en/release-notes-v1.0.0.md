# Proposed v1.0.0 release notes

**Tag:** `v1.0.0`
**Title:** v1.0.0 — Stable Cross-Model Routing & Evaluation Framework

This release introduces optional Gemini and Anthropic providers behind one small provider contract. It adds constraint-first, explainable routing with `manual`, `rules`, and `benchmark_weighted` policies; local quotation verification; a reproducible benchmark runner; a CLI; and generic MCP tools. The Gemini V0.1 tool names remain available as compatibility aliases. The server keeps local-first defaults and does not expose an unauthenticated public listener.

This release provides the framework and reproducible synthetic validation. It does not claim that cross-model delegation improves quality, cost or latency without measured experiments. Live API experiments require explicit opt-in and separate API access.

Publish these notes only after PR approval, merge, release checks, and creation of the tag and OCI image. The matching [French notes](../fr/release-notes-v1.0.0.md) are part of the release draft.
