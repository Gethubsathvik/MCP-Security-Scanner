---
name: MCP SDK v2 migration
description: Compatibility note for the official Python MCP SDK used by mcpscan.
---

The project uses the MCP Python SDK 2.x line. Demo servers must use `mcp.server.mcpserver.MCPServer`; the former `mcp.server.fastmcp.FastMCP` import belongs to the v1 API and fails at runtime.

**Why:** The dependency resolver selected the current SDK, whose v2 migration renamed FastMCP and changed server registration APIs.

**How to apply:** Keep demo and fixture servers on the v2 `MCPServer` API unless the dependency is intentionally pinned below 2. Client introspection should continue to use the official `ClientSession` transport wrappers.