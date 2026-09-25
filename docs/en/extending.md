# Extend V1

English | [Français](../fr/extending.md)

The contracts below are in [`providers/base.py`](../../providers/base.py), [`routing.py`](../../routing.py), and [`benchmarks/runner.py`](../../benchmarks/runner.py). Keep provider SDK calls isolated; use synthetic data and fake clients in tests.

## Add a provider

Implement `DelegationProvider` in a new module. No Router change is needed when you pass the instance explicitly:

```python
from contracts import ProviderCapabilities
from routing import Router

class LocalExample:
    name = "local_example"
    model = "example-model"

    def capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(structured_output=False, external_provider=False)

    def delegate(self, prompt: str, max_output_tokens: int, timeout_seconds: float) -> str:
        return "synthetic answer"

    def extract_findings(self, prompt: str, schema: dict,
                         max_output_tokens: int, timeout_seconds: float) -> str:
        raise NotImplementedError("structured extraction is unavailable")

router = Router({"local_example": LocalExample()})
```

This is a local contract example, not a production adapter. The built-in CLI/MCP provider loader does **not** discover arbitrary classes automatically; wire a new adapter there only if you want it exposed through those entry points. Report capabilities truthfully: routing may reject extraction before calling the provider.

## Add a routing policy

`Router.route(request, policy)` accepts a `RoutingPolicy` object after filtering by constraints. `rank` receives only eligible provider names and returns a nonempty ordered list, reason codes, and score weights:

```python
class ReverseNamePolicy:
    name = "reverse_name"

    def rank(self, eligible, request, history):
        return sorted(eligible, reverse=True), ("reverse_name_order",), {}
```

Use it with `router.route(request, ReverseNamePolicy())`. The built-in CLI/MCP policy selector currently accepts only `manual`, `rules`, and `benchmark_weighted`; a custom policy requires direct Python use or a deliberate CLI/MCP integration change. The policy must never reintroduce a provider excluded by constraints.

## Add an evaluator

`benchmarks.runner.run(..., evaluators={"exact_match": custom})` can override an existing evaluator **for a direct Python run**. A callable receives `(item, answer, findings)` and returns result fields such as `answer_quality` and `verification_success`:

```python
def custom(item, answer, findings):
    return {"evaluation_method": "custom", "evaluator": "exact_match",
            "answer_quality": answer == item.get("reference_answer"),
            "evidence_fidelity": None, "injection_success": None,
            "verification_success": None}
```

V1 `load_dataset` accepts only names in `EVALUATORS`. Adding a **new** evaluator name requires registering it there and updating the CLI path if desired. A mapping alone cannot add a new JSONL evaluator name. Describe the method and validate it on independent cases before interpreting results.

## Add a dataset

Create UTF-8 JSONL with one object per line, unique `id`, and string `category`, `task`, `context`, and supported `evaluator`. For example:

```json
{"id":"sum-1","category":"arithmetic","task":"Calculate 2 + 2.","context":"","evaluator":"numeric_match","reference_answer":"4","fake_answer":"4","dataset_version":"1"}
```

Then run `uv run crossmodel bench run path/to/dataset.jsonl` for the offline software check. The V1 runner supplies `fake_answer` in offline mode; it is not evidence of model performance. Record provenance, redistribution rights, version, reference answers, evaluator limits, and any prompt-injection fixtures. See the [benchmark format](../../benchmarks/README.md) and [methodology](methodology.md).
