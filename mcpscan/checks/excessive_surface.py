from __future__ import annotations

from mcpscan.checks._helpers import compact
from mcpscan.checks.base import Check
from mcpscan.models import Finding, MCPManifest


class ExcessiveSurfaceCheck(Check):
    check_id = "excessive-tool-surface"
    title = "Excessive tool surface"

    def run(self, manifest: MCPManifest) -> list[Finding]:
        count = len(manifest.tools)
        if count <= 12:
            return []
        names = [str(tool.get("name", "")) for tool in manifest.tools]
        return [
            Finding(
                check_id=self.check_id,
                severity="info",
                target=manifest.target,
                description=f"Server exposes {count} tools, which is a large agent-facing attack surface.",
                evidence=compact(names),
                remediation="Remove unused tools and split unrelated capabilities across separately permissioned servers.",
            )
        ]
