import json
from pathlib import Path

from jsonschema import Draft202012Validator


def test_benchmark_schema_accepts_only_a_complete_synthetic_record():
    schema_path = Path(__file__).parents[1] / "benchmarks/benchmark_schema.json"
    schema = json.loads(schema_path.read_text())
    Draft202012Validator.check_schema(schema)
    record = {
        "benchmark_id": "synthetic-arithmetic-01",
        "project_version": "0.1.0",
        "task": "Calculate 2 + 2.",
        "context_size": {"label": "small", "characters": 0, "tokens": None},
        "orchestrator_model": "example-orchestrator",
        "delegated_model": None,
        "provider": None,
        "strategy": "orchestrator_only",
        "configuration": {},
        "latency": {"seconds": None, "status": "unavailable"},
        "token_usage": {
            "orchestrator_input": None,
            "orchestrator_output": None,
            "delegated_input": None,
            "delegated_output": None,
            "total": None,
            "status": "unavailable",
        },
        "estimated_cost": {"amount": None, "currency": "USD", "status": "unavailable"},
        "result": None,
        "reference_answer": "4",
        "evaluation": {},
        "errors": [],
        "timestamp": "2026-01-01T00:00:00Z",
    }
    validator = Draft202012Validator(schema)
    assert validator.is_valid(record)
    assert not validator.is_valid({**record, "token_usage": {}})
