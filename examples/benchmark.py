"""Run the committed synthetic dataset without paid APIs."""

from pathlib import Path

from benchmarks.runner import run
from providers.fake import FakeProvider
from routing import Router

print(run(Path("benchmarks/datasets/basic.jsonl"), Router({"fake": FakeProvider()})))
