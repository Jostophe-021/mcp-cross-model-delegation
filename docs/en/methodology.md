# Research methodology

English | [Français](../fr/methodology.md)

## Research questions and hypotheses

V1 supplies measurement tools, not answers. Each question below needs a preregistered dataset, baseline, and independent analysis:

1. When does delegation improve task quality?
2. When does delegation reduce orchestrator context usage?
3. What latency does delegation introduce?
4. What additional cost does delegation introduce?
5. Does structured evidence improve verification?
6. Can an orchestrator detect errors introduced by a secondary model?
7. How robust is TASK/CONTEXT separation against prompt injection?
8. Which provider performs best for which task categories?
9. Can benchmark-informed routing outperform a fixed routing policy?
10. How do privacy, cost, and latency constraints change the chosen route?

Possible hypotheses should be stated before experiments. The repository claims no answer to these questions.

## Experimental conditions and datasets

The CLI supports `orchestrator_only`, `fixed_delegation`, `structured_delegation`, and `routed_delegation` on the same JSONL dataset. V1 executes one call per condition; it does not implement a second orchestrator synthesis call. `FakeProvider` runs are software checks, not LLM evidence. Live API runs require `--live` and configured keys. The small committed dataset is synthetic and redistributable. The deterministic long-context generator records its seed, version, character count, and unknown token count.

Use separate task categories, repetitions, fixed model IDs, and a held-out evaluation set. If router weights are chosen on the same benchmark used to assess the router, the result is vulnerable to benchmark overfitting. Keep training history and holdout evaluation separate in later studies.

## Metrics, routing policies, and evaluation

Records include model/provider, routing reason codes, latency, success/error, source hash, fallback, and evaluator results. Token usage and cost remain `null` until directly measured or a dated pricing configuration is supplied. Historical latency is not guaranteed future latency. `manual` is a baseline, `rules` is deterministic, and `benchmark_weighted` scores only metrics known for every eligible candidate. Privacy and strict cost/latency constraints filter before any score.

Deterministic evaluators are exact string, numeric, local evidence verification, structured shape, and synthetic injection task preservation. They have narrow meanings: exact match does not prove semantic correctness, and verified quotation does not prove a claim is true. The tested model is never its sole judge. LLM-as-a-judge is future, opt-in research and should identify a separate judge and rubric.

## Reproducibility and privacy

Each run stores project version, Git SHA when available, dataset version, timestamp, model IDs, providers, conditions, seed, repetitions, policy, and weights. Keep raw **non-sensitive** results and a summary for any publishable study, plus known limitations. V1 omits prompts and responses from result files by default and stores a SHA-256 of the exact context used. `--save-responses` is only suitable for redistributable data. The code enables no custom telemetry.

## Threats to validity and limitations

Model aliases may move, providers update models, outputs vary stochastically, tokenizers differ, regions and APIs differ, rate limits intervene, safety policies alter responses, evaluators are biased, datasets may be contaminated, samples are small, temporal effects matter, and routing can overfit a benchmark. The included dataset is too small for substantive model comparisons. Do not report a universal winner or infer savings from fake-provider timings.
