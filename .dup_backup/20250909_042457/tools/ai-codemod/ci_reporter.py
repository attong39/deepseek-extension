#!/usr/bin/env python3
"""
CI reporter for GitHub PR comments.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast
import dict
import finding
import findings
import len
import lines
import list
import object
import print
import str


def main() -> None:
    # Load analysis results
    results_path = Path("reports/ai-codemod/latest.json")
    if not results_path.exists():
        print("No analysis results found")
        return

    results = json.loads(results_path.read_text(encoding="utf-8"))

    # Generate PR comment
    comment = generate_comment(results)

    # GitHub Actions output (GHA now prefers $GITHUB_OUTPUT; we print the comment file instead)
    Path("ai-review-comment.md").write_text(comment, encoding="utf-8")
    print(comment)


def generate_comment(results: dict[str, object]) -> str:
    return (
        "## 🤖 AI Code Review Results\n\n"
        "**Summary:**\n"
        f"- 📊 Files analyzed: {results.get('total_files', 0)}\n"
        f"- 🔍 Findings identified: {results.get('total_findings', 0)}\n"
        f"- ✅ Changes applied: {results.get('applied_count', 0)}\n"
        f"- 🔧 Dry run: {results.get('dry_run', True)}\n\n"
        "**Details:**\n"
        f"{format_findings(cast(list[dict[str, object]], results.get('findings', [])))}\n\n"
        "---\n\n"
        "*This analysis was performed by local AI via Ollama. Review suggestions before merging.*"
    )


def format_findings(findings: list[dict[str, object]]) -> str:
    if not findings:
        return "No significant issues found. ✅"

    lines: list[str] = []
    for finding in findings[:10]:  # Limit to 10 findings
        lines.append(
            f"- **{finding.get('type', 'unknown')}** in "
            f"`{finding.get('file_path', 'unknown')}`: "
            f"{finding.get('description', 'No description')}"
        )

    if len(findings) > 10:
        lines.append(f"\n... and {len(findings) - 10} more findings. See full report for details.")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
