from __future__ import annotations

import os
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

from mcpscan.models import MCPManifest, Transport


def _dump(value: Any) -> dict[str, Any]:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", by_alias=True, exclude_none=True)
    return dict(value)


async def _collect(method: Callable[..., Awaitable[Any]]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    cursor: str | None = None
    while True:
        result = await method(params=types.PaginatedRequestParams(cursor=cursor) if cursor else None)
        values = getattr(result, "tools", None) or getattr(result, "resources", None) or getattr(result, "prompts", None) or []
        items.extend(_dump(value) for value in values)
        cursor = getattr(result, "nextCursor", None)
        if not cursor:
            return items


async def _introspect(read_stream: Any, write_stream: Any, target: str, transport: Transport, remote_signals: dict[str, Any]) -> MCPManifest:
    async with ClientSession(read_stream, write_stream) as session:
        initialized = await session.initialize()
        tools = await _collect(session.list_tools)
        resources = await _collect(session.list_resources)
        prompts = await _collect(session.list_prompts)
        return MCPManifest(
            target=target,
            transport=transport,
            tools=tools,
            resources=resources,
            prompts=prompts,
            server_info=_dump(getattr(initialized, "serverInfo", {})),
            remote_signals=remote_signals,
        )


@dataclass
class MCPClient:
    target: str
    transport: Transport = "stdio"
    command: str | None = None
    args: list[str] = field(default_factory=list)
    cwd: str | None = None
    env: dict[str, str] | None = None
    headers: dict[str, str] | None = None
    remote_signals: dict[str, Any] = field(default_factory=dict)

    @asynccontextmanager
    async def _connection(self) -> AsyncGenerator[tuple[Any, Any], None]:
        if self.transport == "stdio":
            if not self.command:
                raise ValueError("stdio scans require a command target")
            merged_env = {**os.environ, **(self.env or {})}
            params = StdioServerParameters(command=self.command, args=self.args, cwd=self.cwd, env=merged_env)
            async with stdio_client(params) as streams:
                yield streams
            return

        headers = self.headers or None
        if headers:
            import httpx2

            async with httpx2.AsyncClient(headers=headers) as http_client:
                async with streamable_http_client(self.target, http_client=http_client) as streams:
                    yield streams
            return

        async with streamable_http_client(self.target) as streams:
            yield streams

    async def introspect(self) -> MCPManifest:
        async with self._connection() as (read_stream, write_stream):
            try:
                return await _introspect(read_stream, write_stream, self.target, self.transport, self.remote_signals)
            except Exception as streamable_error:
                if self.transport != "http":
                    raise
                async with sse_client(self.target, headers=self.headers or {}) as streams:
                    return await _introspect(streams[0], streams[1], self.target, self.transport, self.remote_signals)