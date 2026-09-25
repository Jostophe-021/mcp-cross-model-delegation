"""Deterministic synthetic long-context dataset generator."""

import json
import random
from pathlib import Path

GENERATOR_VERSION = "1"
SIZES = {"small": 1_000, "medium": 10_000, "large": 90_000}


def generate(path: Path, size: str, seed: int) -> None:
    if size not in SIZES:
        raise ValueError("Unknown size")
    rng = random.Random(seed)
    words = ("alpha", "beta", "gamma", "delta")
    context = ""
    while len(context) < SIZES[size] - 40:
        context += rng.choice(words) + " "
    context = context[:SIZES[size] - 22] + " Marker color: amber."
    row = {"id": f"long-{size}-{seed}", "category": "long_context",
           "task": "Return the marker color only.", "context": context,
           "reference_answer": "amber", "evaluator": "exact_match",
           "tags": ["synthetic", "generated"], "fake_answer": "amber",
           "fake_structured": '{"summary":"amber","findings":[]}',
           "generator_version": GENERATOR_VERSION, "seed": seed,
           "characters": len(context), "tokens": None, "dataset_version": "1"}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(row) + "\n", encoding="utf-8")
