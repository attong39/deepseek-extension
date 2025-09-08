#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
import counts
import dict
import i
import int
import issue
import issues
import k
import key
import len
import lines
import list
import output_path
import project_root
import self
import str
import tuple
import v


class ReportManager:
    def __init__(self, project_root: Path) -> None:
        self.report_dir = project_root / "reports" / "ai-monitor"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def save_issues_report(self, issues: list[dict[str, Any]], run_id: str | None = None) -> tuple[Path, Path]:
        if run_id is None:
            run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        json_report = {
            "timestamp": datetime.now().isoformat(),
            "run_id": run_id,
            "issues": issues,
            "summary": {
                "total_issues": len(issues),
                "by_type": self._count_by_key(issues, "type"),
                "by_severity": self._count_by_key(issues, "severity"),
            },
        }

        json_path = self.report_dir / f"issues_{run_id}.json"
        json_path.write_text(json.dumps(json_report, indent=2), encoding="utf-8")

        md_path = self.report_dir / f"issues_{run_id}.md"
        self._generate_markdown_report(issues, md_path)
        return json_path, md_path

    def _count_by_key(self, issues: list[dict[str, Any]], key: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        for i in issues:
            val = str(i.get(key, "unknown"))
            counts[val] = counts.get(val, 0) + 1
        return counts

    def _generate_markdown_report(self, issues: list[dict[str, Any]], output_path: Path) -> None:
        lines: list[str] = []
        lines.append("# AI Monitor Issues Report\n")
        lines.append(f"Generated: {datetime.now().isoformat()}\n\n")
        lines.append("## Summary\n")
        lines.append(f"- Total issues: {len(issues)}\n")
        by_type = self._count_by_key(issues, "type")
        for k, v in by_type.items():
            lines.append(f"- {k}: {v}\n")
        lines.append("\n## Detailed Issues\n")
        for issue in issues:
            lines.append(f"### {issue.get('type','unknown')} (Severity: {issue.get('severity','n/a')})\n")
            lines.append(f"- File: {issue.get('file_path','n/a')}\n")
            lines.append(f"- Description: {issue.get('description','')}\n\n")
        output_path.write_text("".join(lines), encoding="utf-8")
