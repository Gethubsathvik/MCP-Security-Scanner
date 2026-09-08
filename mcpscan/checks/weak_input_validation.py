from __future__ import annotations

import re
from typing import Any

from mcpscan.checks._helpers import compact, item_name
from mcpscan.checks.base import Check
from mcpscan.models import Finding, MCPManifest


class WeakInputValidationCheck(Check):
    check_id = "weak-input-validation"
    title = "Weak input validation"
    _structured_words = re.compile(r"\b(path|file|url|host|email|date|id|sql|query|command|directory|json|config)\b", re.I)

    def run(self, manifest: MCPManifest) -> list[Finding]:
        findings: list[Finding] = []
        for tool in manifest.tools:
            schema = tool.get("inputSchema") or {}
            properties: dict[str, Any] = schema.get("properties") or {}
            purpose = f"{tool.get('name', '')} {tool.get('description', '')}"
            for name, definition in properties.items():
                if not isinstance(definition, dict) or definition.get("type") != "string":
                    continue
                has_constraint = any(key in definition for key in ("pattern", "enum", "minLength", "maxLength", "format"))
                if has_constraint or not self._structured_words.search(f"{name} {purpose}"):
                    continue
                findings.append(
                    Finding(
                        check_id=self.check_id,
                        severity="medium",
                        target=item_name(tool),
                        description=f"Parameter '{name}' accepts an unconstrained string for a structured value.",
                        evidence=compact({name: definition}),
                        remediation="Add an enum, format, pattern, or length bound and validate again in the handler.",
                    )
                )
        return findings