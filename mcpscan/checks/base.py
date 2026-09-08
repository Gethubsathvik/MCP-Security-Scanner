from __future__ import annotations

from abc import ABC, abstractmethod

from mcpscan.models import Finding, MCPManifest


class Check(ABC):
    check_id: str
    title: str

    @abstractmethod
    def run(self, manifest: MCPManifest) -> list[Finding]:
        """Return findings for a manifest without invoking any server tools."""