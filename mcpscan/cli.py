from __future__ import annotations

import asyncio
import json
import shlex
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from mcpscan.client import MCPClient
from mcpscan.models import Severity
from mcpscan.report import render_terminal, write_json
from mcpscan.scanner import Scanner

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Passively audit an MCP server manifest.")
console = Console()


@app.command()
def scan(
    target: Annotated[str, typer.Argument(help="stdio command or HTTP/SSE endpoint to inspect.")],
    transport: Annotated[str, typer.Option("--transport", "-t", help="Connection transport: stdio or http.")] = "stdio",
    output: Annotated[Optional[Path], typer.Option("--output", "-o", help="Write the full report as JSON.")] = None,
    severity_threshold: Annotated[Severity, typer.Option("--severity-threshold", help="Only show findings at or above this level.")] = "info",
    cwd: Annotated[Optional[Path], typer.Option("--cwd", help="Working directory for a stdio server.")] = None,
    auth_header: Annotated[Optional[str], typer.Option("--auth-header", help="Declared remote auth header name, for exposure checks.")] = None,
    cors: Annotated[Optional[str], typer.Option("--cors", help="Declared CORS policy signal, e.g. restricted or *.")] = None,
    rate_limit_signal: Annotated[Optional[str], typer.Option("--rate-limit-signal", help="Documented rate limit signal for an HTTP target.")] = None,
) -> None:
    """Connect, introspect, and run passive checks without calling tools."""
    if transport not in {"stdio", "http"}:
        raise typer.BadParameter("must be 'stdio' or 'http'", param_hint="--transport")
    if transport == "stdio":
        command_parts = shlex.split(target)
        if not command_parts:
            raise typer.BadParameter("stdio target cannot be empty")
        client = MCPClient(target=target, transport="stdio", command=command_parts[0], args=command_parts[1:], cwd=str(cwd) if cwd else None)
    else:
        client = MCPClient(
            target=target,
            transport="http",
            remote_signals={"auth_header": auth_header, "cors": cors, "rate_limit_signal": rate_limit_signal},
        )
    try:
        report = asyncio.run(Scanner().scan(client, severity_threshold))
    except Exception as exc:
        raise typer.Exit(code=1) from typer.echo(f"[red]Scan failed:[/] {exc}", err=True)
    render_terminal(report, console)
    if output:
        write_json(report, output)
        console.print(f"\n[green]JSON report written to[/] {output}")


@app.command("version")
def version() -> None:
    """Print the scanner version."""
    from mcpscan import __version__

    console.print(__version__)


if __name__ == "__main__":
    app()