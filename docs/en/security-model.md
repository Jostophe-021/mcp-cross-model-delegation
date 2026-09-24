# Security model and threat table

English | [Français](../fr/security-model.md)

**A model boundary is not a security boundary by itself.** Prompt separation mitigates accidental mixing; it cannot guarantee resistance to adversarial prompt injection. The MCP endpoint is local and unauthenticated. Only the operator can decide whether text may be sent to Google.

| Risk | Current mitigation | Remaining limitation |
| --- | --- | --- |
| Instructions hidden in CONTEXT | TASK and CONTEXT are separate JSON fields; prompt explicitly subordinates CONTEXT | Models may still follow malicious text; test and verify |
| Sensitive-context exfiltration | Tool descriptions warn callers; no automatic app or file reads | The caller can still send confidential text to Google |
| Compromised or unavailable provider | Timeout, fixed sanitized errors, no automatic retry | Provider can be slow, wrong, or malicious |
| Hallucinated answer or evidence | Structured evidence fields and orchestrator verification requirement | Evidence is model-generated, not independently validated |
| Invalid JSON or shape | Schema request and strict local shape/type checks | A valid-looking answer can still be factually false |
| Payload leakage through logs | No prompt or response logging/custom telemetry in this app | Client, runtime, network, and provider may log independently |
| Accidental public MCP bind | Explicit loopback allowlist; no public bind without authentication | A local user or process can access the endpoint |
| Committed secrets | `.gitignore`, example-only `.env.example`, CI secret scan | Ignore rules do not prevent deliberate `git add -f`; review history |
| Compromised dependency | Pinned direct dependencies, lockfile, dependency audit workflow | Supply-chain risk remains; update and review dependencies |
| Unverified secondary answer | README and tool descriptions require verification | An orchestrator may fail to verify |

Error objects expose fixed codes and messages, never exception strings, prompts, contexts, keys, or stack traces. Input and output limits bound workload but are not a spending limit. `store=False` prevents storage of the Interaction object for that request under the current Gemini API; other provider processing and policies still apply. Consult [Google's logging documentation](https://ai.google.dev/gemini-api/docs/logs-datasets) and your account terms.

Before connecting a remote product, decide how MCP client identity, authentication, transport encryption, authorization, and logs will be handled. The optional [OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) keeps the MCP listener private but does not remove the Google data-sharing decision. Do not expose `0.0.0.0:8000` by editing the guard without an appropriate security design.
