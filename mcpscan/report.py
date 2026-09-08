from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mcpscan.models import ScanReport

SEVERITY_STYLE = {
    "critical": "bold red",
    "high": "red",
    "medium": "yellow",
    "low": "cyan",
    "info": "dim",
}


def render_terminal(report: ScanReport, console: Console | None = None) -> None:
    console = console or Console()
    counts = report.counts
    summary = "  ".join(f"[{SEVERITY_STYLE[level]}]{level.title()}: {counts[level]}[/]" for level in counts if counts[level])
    console.print()
    console.print(Panel(
        f"[bold]Target[/] {report.target}\n[bold]Transport[/] {report.transport}    [bold]Risk score[/] {report.score}/100\n"
        f"[bold]Introspected[/] {report.tools_scanned} tools, {report.resources_scanned} resources, {report.prompts_scanned} prompts\n\n{summary or '[green]No findings[/]' }",
        title="mcpscan security report",
        border_style="blue",
    ))
    if not report.findings:
        console.print("[green]PASS[/] No registered checks produced a finding.")
        return
    table = Table(show_header=True, header_style="bold")
    table.add_column("Severity", width=10)
    table.add_column("Check", width=30)
    table.add_column("Target", width=24)
    table.add_column("Finding")
    for finding in report.findings:
        table.add_row(
            Text(finding.severity.upper(), style=SEVERITY_STYLE[finding.severity]),
            finding.check_id,
            finding.target,
            f"{finding.description}\n[dim]Fix: {finding.remediation}[/]",
        )
    console.print(table)


def write_json(report: ScanReport, output: Path) -> None:
    output.write_text(json.dumps(report.model_dump(mode="json"), indent=2) + "\n", encoding="utf-8")