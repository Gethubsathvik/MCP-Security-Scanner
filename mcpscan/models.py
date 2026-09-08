from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

Severity = Literal["critical", "high", "medium", "low", "info"]
Transport = Literal["stdio", "http"]


class MCPManifest(BaseModel):
    """The protocol data collected from an MCP server."""

    target: str
    transport: Transport
    tools: list[dict[str, Any]] = Field(default_factory=list)
    resources: list[dict[str, Any]] = Field(default_factory=list)
    prompts: list[dict[str, Any]] = Field(default_factory=list)
    server_info: dict[str, Any] = Field(default_factory=dict)
    remote_signals: dict[str, Any] = Field(default_factory=dict)


class Finding(BaseModel):
    check_id: str
    severity: Severity
    target: str
    description: str
    evidence: str
    remediation: str


class ScanReport(BaseModel):
    target: str
    transport: Transport
    findings: list[Finding]
    scanned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tools_scanned: int = 0
    resources_scanned: int = 0
    prompts_scanned: int = 0
    score: int = 0

    @property
    def counts(self) -> dict[str, int]:
        return {
            severity: sum(f.severity == severity for f in self.findings)
            for severity in ("critical", "high", "medium", "low", "info")
        }
