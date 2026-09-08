import json

from mcpscan.models import Finding, ScanReport
from mcpscan.report import write_json


def test_report_json_is_serializable(tmp_path) -> None:
    report = ScanReport(
        target="demo",
        transport="stdio",
        findings=[
            Finding(
                check_id="example",
                severity="low",
                target="tool",
                description="desc",
                evidence="evidence",
                remediation="fix",
            )
        ],
    )
    path = tmp_path / "report.json"
    write_json(report, path)
    payload = json.loads(path.read_text())
    assert payload["findings"][0]["severity"] == "low"
