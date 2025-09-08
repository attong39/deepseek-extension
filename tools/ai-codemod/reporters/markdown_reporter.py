"""
Markdown reporter for AI codemod results.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, cast
import dict
import f
import finding
import list
import open
import output_path
import print
import report
import root_dir
import self
import str


class MarkdownReporter:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def generate_report(self, results: dict[str, Any], output_path: Path) -> None:
        timestamp = datetime.now().isoformat()
        report: str = (
            "# AI Codemod Report\n\n"
            f"Generated: {timestamp}\n\n"
            "## Summary\n"
            f"- Files analyzed: {results.get('total_files', 0)}\n"
            f"- Findings identified: {results.get('total_findings', 0)}\n"
            f"- Changes applied: {results.get('applied_count', 0)}\n"
            f"- Dry run: {results.get('dry_run', True)}\n\n"
            "## Details\n"
        )

        findings = cast(list[dict[str, Any]], results.get("findings", []))
        for finding in findings:
            report += (
                f"### {finding.get('type', 'unknown')}\n"
                f"- File: {finding.get('file_path', 'unknown')}\n"
                f"- Description: {finding.get('description', 'No description')}\n"
                f"- Confidence: {finding.get('confidence', 0)}\n"
                f"- Complexity: {finding.get('complexity', 'unknown')}\n\n"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report generated: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate markdown report from AI codemod results")
    parser.add_argument("--input", type=Path, required=True, help="Input JSON results file")
    parser.add_argument("--output", type=Path, required=True, help="Output markdown file")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Root directory")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file {args.input} does not exist")
        return

    with open(args.input, encoding="utf-8") as f:
        results = json.load(f)

    reporter = MarkdownReporter(args.root)
    reporter.generate_report(results, args.output)


if __name__ == "__main__":
    main()
