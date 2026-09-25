import json
from pathlib import Path

from jsonschema import Draft202012Validator

import cli
from benchmarks.runner import evaluate, load_dataset, run
from contracts import DelegationRequest, RoutingConstraints
from execution import execute
from gateway import Settings
from providers.fake import FakeProvider
from routing import ManualPolicy, Router


def test_fallback_traced_only_for_retryable_error():
    class TimeoutProvider(FakeProvider):
        name = "first"

        def delegate(self, prompt, max_output_tokens, timeout_seconds):
            raise TimeoutError("private context")

    router = Router({"first": TimeoutProvider(), "second": FakeProvider("ok")})
    request = DelegationRequest("task", "secret", constraints=RoutingConstraints(
        fallback_allowed=True))
    result, trace = execute(request, router, ManualPolicy("first"), Settings())
    assert result.answer == "ok"
    assert trace.selected_provider == "first"
    assert trace.executed_provider == "second"
    assert trace.fallback_used is True
    assert trace.fallback_reason == "MODEL_TEMPORARILY_UNAVAILABLE"
    assert "secret" not in str(trace)


def test_dataset_parser_and_runner(tmp_path):
    dataset = Path(__file__).parents[1] / "benchmarks/datasets/basic.jsonl"
    assert len(load_dataset(dataset)) == 6
    output = run(dataset, Router({"fake": FakeProvider()}), output=tmp_path,
                 repetitions=2, shuffle=True, seed=42)
    manifest = json.loads((output / "manifest.json").read_text())
    records = [json.loads(line) for line in (output / "results.jsonl").read_text().splitlines()]
    summary = json.loads((output / "summary.json").read_text())
    history = json.loads((output / "history.json").read_text())
    assert len(records) == 48
    schema = json.loads((dataset.parent.parent / "result_schema.json").read_text())
    assert all(Draft202012Validator(schema).is_valid(record) for record in records)
    assert manifest["seed"] == 42
    assert records[0]["total_tokens"] is None
    assert records[0]["source_sha256"]
    assert "task" not in records[0] and "context" not in records[0]
    assert summary["fixed_delegation"]["n"] == 12
    assert history["fake"]["estimated_cost"] is None


def test_evaluators_are_deterministic():
    assert evaluate({"evaluator": "numeric_match", "reference_answer": "20"}, "20.0", ())[
        "answer_quality"] is True
    assert evaluate({"evaluator": "exact_match", "reference_answer": "yes"}, "no", ())[
        "answer_quality"] is False


def test_cli_doctor_and_providers_have_no_keys(monkeypatch, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "private-test-key")
    assert cli.main(["doctor"]) == 0
    assert "private-test-key" not in capsys.readouterr().out
    assert cli.main(["providers"]) == 0
    output = capsys.readouterr().out
    assert '"configured": true' in output
    assert "private-test-key" not in output
