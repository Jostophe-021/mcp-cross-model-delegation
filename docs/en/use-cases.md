# Use cases

English | [Français](../fr/use-cases.md)

| Use case | V1 status | What V1 actually provides |
| --- | --- | --- |
| Long-context offloading | Available | Bounded text delegation; no claim of savings. |
| Independent second opinion | Available | Manual second-provider call; the caller checks it. |
| Evidence-backed extraction | Available | Structured findings and local quotation offsets/hash. |
| Cross-provider comparison | Available | Same benchmark primitives for Gemini/Anthropic/Fake. |
| Prompt-injection research | Available | Synthetic dataset and narrow deterministic evaluator. |
| Secondary-model error detection | Possible extension | Synthetic wrong-answer fixture; no orchestrator correction experiment yet. |
| Cost-constrained routing | Available | Strict caps reject unknown cost unless explicitly allowed. |
| Latency-constrained routing | Available | Historical measured latency filter; no future guarantee. |
| Privacy-constrained routing | Available | Caller-declared modes and provider allowlists. |
| Future model scheduling | Future research | No scheduler or adaptive learning in V1. |

These constraints can help evaluate enterprise requirements for cost, latency, capabilities, provider approval, and privacy. V1 is not a complete enterprise IAM or policy platform. A local OpenAI-compatible adapter for Ollama, vLLM, or LM Studio is a plausible next extension; it is not included yet.
