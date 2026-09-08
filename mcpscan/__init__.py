"""mcpscan: passive security checks for MCP server manifests."""

from mcpscan.client import MCPClient
from mcpscan.models import Finding, MCPManifest, ScanReport, Severity
from mcpscan.report import render_terminal, write_json
from mcpscan.scanner import Scanner

__version__ = "0.1.0"

__all__ = [
    "Scanner",
    "MCPClient",
    "MCPManifest",
    "ScanReport",
    "Finding",
    "Severity",
    "render_terminal",
    "write_json",
    "__version__",
]
