# Generic deployment example

English | [Français](../fr/deployment-example.md)

The recommended first run is local Python plus a local MCP client. A generic always-on design can use a small VM, a containerized MCP server, and a secret manager. This is an **architecture example**, not an automated deployment or a promise of free hosting. Check current cloud pricing, egress, storage, and model API charges before provisioning anything.

```text
Compatible remote MCP client
    | (optional private tunnel)
    v
Small VM: tunnel client -> 127.0.0.1:8000/mcp
                         -> Gemini API over outbound HTTPS
Secret manager -> process environment at runtime
```

Use a dedicated service identity with access only to the example secret it needs, private firewall defaults, outbound HTTPS, and no inbound MCP port. Supply the API key at runtime from a secret manager such as `YOUR_SECRET_NAME`; do not pass it as a Docker build argument or commit it to a file. Start the server with its loopback default. If a tunnel client shares the VM network namespace, it can reach that loopback address. Secure its own control-plane credential separately and rotate it according to the provider's guidance. Avoid writing secrets or full prompts to logs.

[OpenAI Secure MCP Tunnel](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels) is one optional transport for supported OpenAI clients. Its official guide describes creating a tunnel in your own account, running `tunnel-client` where it can reach the local MCP server, and selecting Tunnel in a developer-mode app. Follow that guide for current commands and permissions; this repository deliberately contains no tunnel identifier, endpoint, or production credential. The private tunnel does not satisfy public plugin submission requirements.

Before accepting traffic, test `/mcp` through the intended client, confirm the server is bound to loopback, inspect container restart behavior, review provider data policies, and configure a budget alert while understanding that alerts do not enforce a hard cap. A remote listener requires a separate authentication and transport-security design. For local development, follow the [README](../../README.md) instead of creating cloud resources.
