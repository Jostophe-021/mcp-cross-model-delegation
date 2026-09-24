# Research roadmap

English | [Français](../fr/research-roadmap.md)

## Hypothesis and status vocabulary

**Hypothesis:** Delegating bounded subtasks to a secondary model may reduce orchestrator context load or improve specialized processing, but can also increase latency, cost, privacy risk, and error propagation. No outcome has been measured by this repository. Label every claim as **implemented**, **planned**, **hypothesis**, or **measured**; publish measured results only with the data, method, and uncertainty needed to reproduce them.

**V1 target:** Gemini and Anthropic providers, a deterministic FakeProvider, constraint-aware Router, three explicit policies, local evidence verification, four-condition sequential benchmark runner, deterministic evaluators, and CLI. These are software capabilities, not comparative LLM results. **Later:** local/OpenAI-compatible provider, larger public datasets, holdout evaluation, routing-policy comparison, and independent verification. No date is promised. See [methodology](methodology.md).

## Experimental conditions

| ID | Condition | Question | Status |
| --- | --- | --- | --- |
| A | Orchestrator only, one call | How does the primary model solve the task alone? | V1 runner |
| B | Fixed delegation, one call | Does bounded delegation help? | V1 runner; synthesis follow-up future |
| C | Structured delegation and local quotation verification | Does structure improve evidence handling? | V1 runner |
| D | Generated small, medium, large context | How do quality, failures, and latency scale? | V1 generator |
| E | Deliberately wrong synthetic secondary answer | Can another model detect and correct it? | Wrong-answer fixture in V1; correction study future |
| F | Malicious instructions in CONTEXT | Does the secondary model preserve TASK? | V1 synthetic fixture; broader study future |
| G | Exact/normalized quotation search | Are findings textually supported? | V1 verifier |
| H | Gemini vs Anthropic under one protocol | Which effects are provider-specific? | V1 adapters; no result claimed |

Choose task collections that are synthetic, public, or explicitly redistributable. Pre-register input groups and scoring rules where possible. Vary one experimental factor at a time, record provider model versions and settings, repeat stochastic runs, and report confidence intervals or uncertainty rather than only a winning score. Context groups should be defined relative to each model's documented input limit, not by universal arbitrary sizes.

## Metrics and evaluation

Capture answer quality, factual accuracy, evidence fidelity, hallucination rate, verification success rate, prompt-injection success rate, latency, orchestrator input/output tokens, delegated input/output tokens, total tokens, estimated cost, failure rate, retry rate, and timeout rate. Mark values as measured, estimated, or unavailable. Keep raw timing and token accounting separate from subjective quality judgments. Never fabricate usage or cost when an API does not report it.

Use human references, reference answers, and deterministic rules when suitable. An independent evaluator model or multi-judge panel can supplement them, but an LLM judge can share biases, be swayed by style, or miss the same error. The model being evaluated must not be the sole judge of its own response. Record evaluator identity, rubric, agreement, and disputed cases. Sensitive prompts must not be saved by default; use synthetic inputs or a separately governed dataset with explicit consent and retention rules.

Every run should preserve project version, Git SHA when available, dataset version, provider, model, strategy, settings, seed, repetitions, timestamp, metrics, outcome, and error category. The [runner format](../../benchmarks/README.md) provides these fields. Do not commit real user data or credentials in benchmark artifacts. A policy optimized on the same dataset can overfit its quirks; future studies should separate training history and holdout evaluation. No online self-learning or LLM router is included in V1.
