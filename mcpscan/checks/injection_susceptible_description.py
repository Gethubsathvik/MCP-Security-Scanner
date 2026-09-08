from __future__ import annotations

import re

from mcpscan.checks._helpers import compact, item_name, manifest_items
from mcpscan.checks.base import Check
from mcpscan.models import Finding, MCPManifest


class InjectionSusceptibleDescriptionCheck(Check):
    check_id = "injection-susceptible-description"
    title = "Injection-susceptible description"

    _patterns = (
        re.compile(r"\b(ignore|disregard|forget|override)\b.{0,50}\b(instruction|previous|system|safety|rule)", re.I),
        re.compile(r"\b(system prompt|developer message|secret instructions|do not reveal)\b", re.I),
        re.compile(r"<\/?(?:system|instruction|prompt|tool)[^>]*>", re.I),
        re.compile(r"\b(must|always)\b.{0,45}\b(send|upload|share|reveal|exfiltrate)\b", re.I),
    )

    def run(self, manifest: MCPManifest) -> list[Finding]:
        findings: list[Finding] = []
        for category, item in manifest_items(manifest):
            description = str(item.get("description", ""))
            for pattern in self._patterns:
                if pattern.search(description):
                    findings.append(
                        Finding(
                            check_id=self.check_id,
                            severity="high",
                            target=item_name(item),
                            description=f"{category.title()} description contains instruction-like text that may steer an agent.",
                            evidence=compact(description),
                            remediation="Keep descriptions factual and move behavior into validated server-side logic.",
                        )
                    )
                    break
        return findings