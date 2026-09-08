from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from mcpscan.checks import DEFAULT_CHECKS
from mcpscan.checks.base import Check
from mcpscan.client import MCPClient
from mcpscan.models import Finding, MCPManifest, ScanReport, Severity

SEVERITY_SCORE = {"critical": 10, "high": 7, "medium": 4, "low": 2, "info": 1}
SEVERITY_RANK = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass
class Scanner:
    checks: Iterable[Check] = DEFAULT_CHECKS

    def scan_manifest(self, manifest: MCPManifest, severity_threshold: Severity = "info") -> ScanReport:
        findings = [finding for check in self.checks for finding in check.run(manifest)]
        threshold_rank = SEVERITY_RANK[severity_threshold]
        findings = [finding for finding in findings if SEVERITY_RANK[finding.severity] >= threshold_rank]
        findings.sort(key=lambda finding: (-SEVERITY_RANK[finding.severity], finding.target, finding.check_id))
        return ScanReport(
            target=manifest.target,
            transport=manifest.transport,
            findings=findings,
            tools_scanned=len(manifest.tools),
            resources_scanned=len(manifest.resources),
            prompts_scanned=len(manifest.prompts),
            score=min(100, sum(SEVERITY_SCORE[finding.severity] for finding in findings)),
        )

    async def scan(self, client: MCPClient, severity_threshold: Severity = "info") -> ScanReport:
        return self.scan_manifest(await client.introspect(), severity_threshold)