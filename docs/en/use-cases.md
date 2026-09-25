# Use cases

English | [Français](../fr/use-cases.md)

## Available in V1

- **Bounded delegation and second opinion:** send caller-supplied TASK and CONTEXT to Gemini or Anthropic, then inspect the returned answer. The caller decides whether and how to use it.
- **Evidence-backed extraction:** request structured findings and verify quotations against the supplied context locally. This checks quotation location, not factual truth.
- **Long-context delegation:** pass a bounded long text to a configured provider; token or cost savings are unmeasured.
- **Gemini/Anthropic comparison:** run the same redistributable dataset under explicitly selected conditions, with manifest and result records.
- **Explicit routing constraints:** filter by declared privacy mode, allowlist, capabilities, and known historical cost/latency before choosing a provider.
- **Prompt-injection research:** use the small synthetic fixture and deterministic evaluator as infrastructure for further study, not as proof of resistance.
- **Benchmark infrastructure and MCP tools:** run offline with FakeProvider or opt into real API calls; expose bounded delegation to compatible MCP clients on loopback.

## Possible extensions

- OpenAI and local or OpenAI-compatible secondary providers.
- Larger, independently sourced datasets and additional evaluation methods.
- More advanced scheduling and adaptive experiments.

V1 is not a complete enterprise IAM system, autonomous agent, or security boundary. See the [methodology](methodology.md) and [extension guide](extending.md).
