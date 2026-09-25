# Related work

English | [Français](../fr/related-work.md)

Generic cross-model delegation predates this project. These maintained upstream descriptions were checked on 25 September 2026; their features can change. The links are starting points for comparison, not endorsements or claims of priority.

| Project | Verified scope | Relationship to this repository |
| --- | --- | --- |
| [Gemini MCP Tool](https://github.com/jamubc/gemini-mcp-tool) | An MCP tool connecting an assistant to a Gemini CLI or successor backend for analysis. | A concrete Gemini bridge. This repository calls configured provider APIs through a bounded Python contract and records routing/evaluation decisions. |
| [PAL MCP Server](https://github.com/BeehiveInnovations/pal-mcp-server) | MCP tools for working with multiple model providers and custom endpoints. | Cross-model collaboration exists already. This repository concentrates on explicit constraint filtering, local quotation checks, and reproducible benchmark artifacts. |
| [LiteLLM Router](https://github.com/BerriAI/litellm-docs/blob/main/docs/routing.md) | Routing and load balancing over model deployments with configurable strategies. | This repository has a smaller, research-oriented router that filters declared privacy/capability constraints and can consume benchmark history. |
| [promptfoo](https://github.com/promptfoo/promptfoo/blob/main/site/docs/configuration/guide.md) | Configurable prompts, providers, test cases, and assertions for LLM evaluation. | It is a broader evaluation system. This repository couples its limited evaluations to its own delegation, route trace, and local evidence check. |

The intended contribution is a **reproducible loop** connecting bounded delegation, measurement, constraint-first routing, execution, evidence verification, and evaluation. V1 does not establish superior quality, cost, latency, or security relative to these projects. See [methodology](methodology.md) for the tests needed to evaluate such claims.
