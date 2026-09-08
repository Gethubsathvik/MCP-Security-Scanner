from __future__ import annotations

import asyncio
import json
import os
import shlex
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from mcpscan import __version__
from mcpscan.checks import DEFAULT_CHECKS
from mcpscan.checks.base import Check
from mcpscan.client import MCPClient
from mcpscan.models import Severity
from mcpscan.report import render_terminal, write_json
from mcpscan.scanner import Scanner

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Passively audit an MCP server manifest.")
console = Console()


def _load_checks(selected: str | None) -> tuple[Check, ...]:
    if not selected:
        return DEFAULT_CHECKS
    names = [name.strip() for name in selected.split(",") if name.strip()]
    registry = {check.check_id: check for check in DEFAULT_CHECKS}
    missing = [name for name in names if name not in registry]
    if missing:
        raise typer.BadParameter(f"Unknown check(s): {', '.join(missing)}")
    return tuple(registry[name] for name in names)


@app.command()
def list_checks() -> None:
    """Print available check IDs and titles."""
    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="bold")
    for check in DEFAULT_CHECKS:
        table.add_row(check.check_id, check.title)
    console.print(table)


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
    checks: Annotated[Optional[str], typer.Option("--checks", help="Comma-separated check IDs to run.")] = None,
) -> None:
    """Connect, introspect, and run passive checks without calling tools."""
    if transport not in {"stdio", "http"}:
        raise typer.BadParameter("must be 'stdio' or 'http'", param_hint="--transport")
    if transport == "stdio":
        command_parts = shlex.split(target, posix=os.name != 'nt')
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
        selected_checks = _load_checks(checks)
        report = asyncio.run(Scanner(checks=selected_checks).scan(client, severity_threshold))
    except Exception as exc:
        raise typer.Exit(code=1) from typer.echo(f"[red]Scan failed:[/] {exc}", err=True)
    render_terminal(report, console)
    if output:
        write_json(report, output)
        console.print(f"\n[green]JSON report written to[/] {output}")


@app.command("version")
def version() -> None:
    """Print the scanner version."""
    console.print(__version__)


if __name__ == "__main__":
    app()