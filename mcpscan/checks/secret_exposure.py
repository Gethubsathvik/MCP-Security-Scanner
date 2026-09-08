from __future__ import annotations

import re

from mcpscan.checks._helpers import compact, item_name, manifest_items
from mcpscan.checks.base import Check
from mcpscan.models import Finding, MCPManifest


class SecretExposureCheck(Check):
    check_id = "secret-exposure"
    title = "Secret exposure"
    _patterns = (
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        re.compile(r"\b(?:sk|pk|rk)-live-[A-Za-z0-9_-]{12,}\b", re.I),
        re.compile(
            r"\b(?:api[_ -]?key|secret|token|password|credential)\s*[:=]\s*[\"']?[\w/+.-]{12,}",
            re.I,
        ),
        re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}\b", re.I),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    )

    def run(self, manifest: MCPManifest) -> list[Finding]:
        findings: list[Finding] = []
        for category, item in manifest_items(manifest):
            searchable = compact(item, 1000)
            match = next(
                (
                    pattern.search(searchable)
                    for pattern in self._patterns
                    if pattern.search(searchable)
                ),
                None,
            )
            if match:
                findings.append(
                    Finding(
                        check_id=self.check_id,
                        severity="critical",
                        target=item_name(item),
                        description=f"Possible hardcoded credential found in {category} metadata.",
                        evidence=compact(match.group(0)),
                        remediation="Remove the credential, rotate it immediately, and load secrets through a secure runtime mechanism.",
                    )
                )
        return findings
