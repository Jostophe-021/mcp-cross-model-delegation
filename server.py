"""Loopback-only MCP server exposing bounded, read-only delegation tools."""

import os

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from gateway import make_gateway, safe_call

server = MCPServer(
    "Cross-Model Delegation",
    instructions=(
        "Send only data the user authorizes to share with the configured third-party provider. "
        "Verify secondary-model output before important decisions. These tools handle text; "
        "they do not read applications, email, or Drive, and do not execute code."
    ),
)


@server.tool(
    title="Delegate a bounded task to Gemini",
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True, destructiveHint=False),
)
def gemini_delegate_task(task: str, context: str = "") -> dict:
    """Send authorized text to Gemini for a bounded intellectual task.

    Never send confidential or personal data without appropriate authorization.
    Gemini cannot act in user applications, and its answer needs verification.
    """
    return safe_call(lambda: make_gateway().delegate(task, context))


@server.tool(
    title="Extract evidence-backed findings with Gemini",
    annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True, destructiveHint=False),
)
def gemini_extract_findings(question: str, context: str) -> dict:
    """Extract up to 20 findings from authorized text; evidence is not verified.

    This tool cannot fetch email, Drive, or app data and cannot execute code.
    Treat the secondary model as fallible and check important findings yourself.
    """
    return safe_call(lambda: make_gateway().extract_findings(question, context))


if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "127.0.0.1")
    if host not in {"127.0.0.1", "localhost"}:
        raise SystemExit("Refusing a network-visible bind without client authentication")
    try:
        port = int(os.getenv("PORT", "8000"))
    except ValueError as error:
        raise SystemExit("PORT must be an integer") from error
    if not 1 <= port <= 65535:
        raise SystemExit("PORT is outside the valid range")
    server.run(
        transport="streamable-http",
        host=host,
        port=port,
        stateless_http=True,
        json_response=True,
    )
