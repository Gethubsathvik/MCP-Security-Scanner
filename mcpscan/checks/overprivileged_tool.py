from __future__ import annotations

import re

from mcpscan.checks._helpers import compact, item_name
from mcpscan.checks.base import Check
from mcpscan.models import Finding, MCPManifest, Severity


class OverprivilegedToolCheck(Check):
    check_id = "overprivileged-tool"
    title = "Overprivileged tool"

    _broad_capabilities = (
        (
            re.compile(r"\b(shell|command|exec(?:ute)?|subprocess|terminal)\b", re.I),
            "shell execution",
        ),
        (
            re.compile(
                r"\b(write|delete|remove|modify|rename|chmod).{0,30}\b(file|folder|directory|filesystem)\b",
                re.I,
            ),
            "filesystem mutation",
        ),
        (
            re.compile(
                r"\b(arbitrary|any|raw|unrestricted).{0,30}\b(network|http|url|request)\b", re.I
            ),
            "unrestricted network access",
        ),
    )
    _scope_keys = {
        "path",
        "paths",
        "directory",
        "filename",
        "url",
        "host",
        "command",
        "allowlist",
        "resource",
    }

    def run(self, manifest: MCPManifest) -> list[Finding]:
        findings: list[Finding] = []
        for tool in manifest.tools:
            description = str(tool.get("description", ""))
            schema = tool.get("inputSchema") or {}
            properties = schema.get("properties") or {}
            text = f"{tool.get('name', '')} {description}"
            for pattern, capability in self._broad_capabilities:
                match = pattern.search(text)
                if not match:
                    continue
                scoped = {
                    name
                    for name, definition in properties.items()
                    if name in self._scope_keys
                    and isinstance(definition, dict)
                    and any(
                        key in definition
                        for key in ("enum", "pattern", "const", "minLength", "maxLength")
                    )
                }
                if scoped or re.search(
                    r"\b(allowlist|approved|sandbox|project directory|restricted)\b",
                    description,
                    re.I,
                ):
                    continue
                severity: Severity = "critical" if capability == "shell execution" else "high"
                findings.append(
                    Finding(
                        check_id=self.check_id,
                        severity=severity,
                        target=item_name(tool),
                        description=f"Tool implies broad {capability} without a narrowing parameter.",
                        evidence=compact(description or tool),
                        remediation="Limit the capability to an explicit allowlist or narrowly scoped parameter.",
                    )
                )
                break
        return findings
