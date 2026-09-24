# Benchmarks

English | [Français](README.fr.md)

This directory defines a **planned** measurement format; it contains no experimental result. The [JSON schema](benchmark_schema.json) records a benchmark ID, task, context size, project version, models, provider, strategy, public configuration, latency, token usage, estimated cost, result, reference answer, evaluation, errors, and timestamp. Use `null` with `unavailable` when a value is not reported; never fill missing usage with a fabricated zero.

Only synthetic, public, or explicitly redistributable tasks may be committed. Do not store real user prompts, credentials, private infrastructure, or client data. If a future runner processes sensitive data under separate governance, store only non-sensitive aggregate metrics by default.

The planned comparisons are orchestrator-only, free-form delegation, structured delegation, context-size groups, deliberately wrong secondary answers in **synthetic** tests, prompt injection, evidence fidelity, and future cross-provider runs. Record evaluators and rubrics. The tested model must not be the sole judge of itself. See the [research roadmap](../docs/en/research-roadmap.md).
