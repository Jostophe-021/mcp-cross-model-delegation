# First live experiment

English | [Français](../fr/first-experiment.md)

This is a **manual, opt-in** experiment. Gemini and Anthropic API calls can incur charges. The offline quickstart does not start them. Use only synthetic or redistributable tasks and check provider data policies first.

1. Read the [methodology](methodology.md) and inspect [`basic.jsonl`](../../benchmarks/datasets/basic.jsonl). State a narrow question and prespecify quality, evidence, latency, and failure metrics. Six synthetic tasks are a software smoke test, not a representative sample.
2. Record `v1.0.0` and `git rev-parse HEAD`. Keep the dataset file and version. Choose exact provider/model IDs, API settings, policy, evaluator, seed, repetitions, and a budget. Configure keys only in your own environment.
3. Run `uv run crossmodel bench run benchmarks/datasets/basic.jsonl` to check the path without API calls. Inspect the printed run directory's `manifest.json`, `results.jsonl`, and `summary.json`.
4. Only after accepting the announced call count and possible charges, run a live comparison, for example `uv run crossmodel bench run benchmarks/datasets/basic.jsonl --live --provider gemini --orchestrator anthropic --repetitions 3 --shuffle --seed 42`. V1 makes one call per condition; it does not make a second orchestrator synthesis call.
5. Preserve the full manifest, raw **non-sensitive** results, summary, and limitations. Default results omit task/context/answer; `--save-responses` is opt-in and can expose data. Unknown token or cost fields are unavailable, not zero. Report dataset provenance, sample size, evaluator weaknesses, model drift, and failed calls.

The manifest records project version, Git SHA, dataset hash/version, providers and model IDs, policy, seed, and repetitions. Record any model settings or provider-side changes separately with the date. The seed controls local condition order, not model determinism. Use held-out tasks and independent review before making performance claims. Share a safe configuration through [Discussions](../../SUPPORT.md) to invite reproduction.
