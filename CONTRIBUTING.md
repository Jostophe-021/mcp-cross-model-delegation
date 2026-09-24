# Contributing

English | [Français](CONTRIBUTING.fr.md)

This is an experimental research preview. Small, testable changes and explicit assumptions are preferred.

1. Install Python 3.12+ and `uv`; run `uv sync --extra test`.
2. Run `uv run pytest -q` and `uv run ruff check gateway.py server.py providers tests` before proposing a change. Unit tests must never require a real API key or network call.
3. Open an issue describing the problem, expected behavior, security or research impact, and a minimal **synthetic** example. Propose changes through a focused pull request.
4. To add a provider, implement `DelegationProvider` in a new module under `providers/`, keep SDK calls isolated, validate configuration, avoid payload logging, and add fake-client tests. Do not add unrelated providers to this preview merely for completeness.
5. To add a benchmark, specify the task source and redistribution rights, strategy, reference answer, evaluator, measured versus estimated fields, and how another researcher can reproduce it. Use synthetic or redistributable data only. Do not claim unmeasured results.
6. Never commit `.env`, keys, tokens, logs, personal data, or private infrastructure identifiers. Run secret scanning before sending a pull request. For vulnerabilities, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

Substantive documentation changes must eventually be reflected in **both English and French**. Contributions can start in one language, but official releases should preserve parity, especially for security and data-sharing information.
