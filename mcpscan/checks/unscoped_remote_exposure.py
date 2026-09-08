from __future__ import annotations

from mcpscan.checks.base import Check
from mcpscan.models import Finding, MCPManifest


class UnscopedRemoteExposureCheck(Check):
    check_id = "unscoped-remote-exposure"
    title = "Unscoped remote exposure"

    def run(self, manifest: MCPManifest) -> list[Finding]:
        if manifest.transport != "http":
            return []
        signals = manifest.remote_signals
        findings: list[Finding] = []
        if not signals.get("auth_header"):
            findings.append(
                Finding(
                    check_id=self.check_id,
                    severity="high",
                    target=manifest.target,
                    description="Remote MCP endpoint has no declared authentication header.",
                    evidence="auth_header: absent",
                    remediation="Require an authenticated, least-privilege credential before accepting MCP sessions.",
                )
            )
        if str(signals.get("cors", "")).lower() in {"*", "allow-all", "permissive"}:
            findings.append(
                Finding(
                    check_id=self.check_id,
                    severity="medium",
                    target=manifest.target,
                    description="Remote endpoint declares permissive cross-origin access.",
                    evidence=f"cors: {signals.get('cors')}",
                    remediation="Restrict allowed origins to the smallest set of trusted clients.",
                )
            )
        if not signals.get("rate_limit_signal"):
            findings.append(
                Finding(
                    check_id=self.check_id,
                    severity="medium",
                    target=manifest.target,
                    description="No rate-limit signal was provided for the remote endpoint.",
                    evidence="rate_limit_signal: absent",
                    remediation="Add server-side rate limiting and document the enforced limit.",
                )
            )
        return findings