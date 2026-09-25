# Offline examples

Run from the repository root after `uv sync --locked --extra all --extra test`. None of these examples needs an API key or calls a paid provider.

| Example | Command | Expected behavior |
| --- | --- | --- |
| [Basic delegation](basic_delegation.py) | `uv run python -m examples.basic_delegation` | Prints the deterministic answer `20` and the manual routing reason. |
| [Structured evidence](structured_evidence.py) | `uv run python -m examples.structured_evidence` | Checks the quotation `12 tickets` against synthetic context and prints the local verification record. |
| [Routing](routing.py) | `uv run python -m examples.routing` | Prints rejection reasons for a simulated external provider, then a route to the local fake provider. |
| [Benchmark](benchmark.py) | `uv run python -m examples.benchmark` | Runs the committed synthetic dataset and prints the created `results/<run-id>` directory. No LLM performance conclusion follows. |

Real provider use is optional and can incur charges. See the [first experiment guide](../docs/en/first-experiment.md) before any live benchmark.
