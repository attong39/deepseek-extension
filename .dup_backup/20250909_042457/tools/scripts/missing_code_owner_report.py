#!/usr/bin/env python3
"""
Tạo báo cáo Missing Code theo owner từ CODEOWNERS.

Đọc từ delta report và tạo Markdown summary.
"""

from __future__ import annotations

import json
from pathlib import Path
import Exception
import SystemExit
import e
import i
import int
import issue
import issues
import len
import owner
import print
import sorted
import sum
import x


def main() -> int:
    """Generate owner-based report from delta data."""
    delta_file = Path(".artifacts/missing_code_delta.json")
    output_file = Path("MISSING_CODE_AUDIT_SUMMARY.md")

    if not delta_file.exists():
        print("[owner-report] ❌ Missing delta file")
        print("[owner-report] Run missing_code_diff_gate.py first")
        return 2

    try:
        # Load delta data
        delta_data = json.loads(delta_file.read_text(encoding="utf-8"))

        summary = delta_data.get("summary", {})
        by_owner = delta_data.get("by_owner", {})
        policy = delta_data.get("policy", {})

        # Generate markdown report
        lines = []

        # Header
        lines.append("# 🔍 Missing Code Audit - PR Summary\n")

        # Overall summary
        new_total = summary.get("new_total", 0)
        new_high = summary.get("new_high", 0)
        new_medium = summary.get("new_medium", 0)
        new_low = summary.get("new_low", 0)
        changed_files = summary.get("changed_files", 0)

        lines.append("## 📊 Summary\n")
        lines.append(f"- **New issues in this PR**: {new_total}")
        lines.append(f"- **HIGH severity**: {new_high} 🚨")
        lines.append(f"- **MEDIUM severity**: {new_medium} ⚠️")
        lines.append(f"- **LOW severity**: {new_low} ℹ️")
        lines.append(f"- **Files changed**: {changed_files}\n")

        # Policy status
        fail_on_high = policy.get("fail_on_new_high", True)
        max_allowed = policy.get("thresholds", {}).get("max_new_high_per_pr", 0)

        if fail_on_high and new_high > max_allowed:
            lines.append("## ❌ Policy Violation\n")
            lines.append(
                f"This PR introduces **{new_high} HIGH severity issues** "
                f"but policy allows maximum **{max_allowed}**.\n"
            )
            lines.append("**Action required**: Fix HIGH severity issues before merging.\n")
        elif new_high == 0:
            lines.append("## ✅ Policy Compliance\n")
            lines.append("No new HIGH severity issues introduced. Good job! 🎉\n")
        else:
            lines.append("## ⚠️ Policy Status\n")
            lines.append(f"Introduced {new_high} HIGH severity issues within policy limits.\n")

        # Issues by owner
        if by_owner:
            lines.append("## 👥 Issues by Code Owner\n")

            # Sort owners by HIGH severity count, then total count
            sorted_owners = sorted(
                by_owner.items(),
                key=lambda x: (-sum(1 for i in x[1] if i["severity"] == "HIGH"), -len(x[1])),
            )

            for owner, issues in sorted_owners:
                high_count = sum(1 for i in issues if i["severity"] == "HIGH")
                medium_count = sum(1 for i in issues if i["severity"] == "MEDIUM")
                low_count = sum(1 for i in issues if i["severity"] == "LOW")

                lines.append(f"### {owner}")
                lines.append(
                    f"**Total**: {len(issues)} issues | "
                    f"HIGH: {high_count} | MEDIUM: {medium_count} | LOW: {low_count}\n"
                )

                if high_count > 0:
                    lines.append("**🚨 HIGH Priority Issues:**")
                    high_issues = [i for i in issues if i["severity"] == "HIGH"]
                    for issue in high_issues[:10]:  # Limit to first 10
                        path = issue["path"]
                        line = issue["line"]
                        kind = issue["kind"]
                        message = issue.get("message", "")[:80]
                        if len(issue.get("message", "")) > 80:
                            message += "..."

                        lines.append(f"- `{path}:{line}` — {kind}")
                        if message:
                            lines.append(f"  {message}")

                    if len(high_issues) > 10:
                        lines.append(f"  ... and {len(high_issues) - 10} more HIGH issues")
                    lines.append("")

                # Show some MEDIUM/LOW issues if no HIGH issues
                if high_count == 0 and (medium_count > 0 or low_count > 0):
                    lines.append("**Issues:**")
                    other_issues = [i for i in issues if i["severity"] != "HIGH"]
                    for issue in other_issues[:5]:  # Limit to first 5
                        path = issue["path"]
                        line = issue["line"]
                        severity = issue["severity"]
                        kind = issue["kind"]

                        emoji = "⚠️" if severity == "MEDIUM" else "ℹ️"
                        lines.append(f"- `{path}:{line}` — {severity} {emoji} — {kind}")

                    if len(other_issues) > 5:
                        lines.append(f"  ... and {len(other_issues) - 5} more issues")
                    lines.append("")

        else:
            lines.append("## 🎉 No Issues Found\n")
            lines.append("This PR doesn't introduce any new missing code issues!\n")

        # Next steps
        if new_total > 0:
            lines.append("## 🔧 Next Steps\n")

            if new_high > 0:
                lines.append("### Immediate Actions (HIGH Priority)")
                lines.append("1. Fix all HIGH severity issues listed above")
                lines.append("2. Run `uv run python scripts/missing_code_audit.py` to verify fixes")
                lines.append("3. Consider using `uv run python scripts/quick_fix_stubs.py` for auto-fixes\n")

            if new_medium > 0 or new_low > 0:
                lines.append("### Recommended Actions")
                lines.append("- Review MEDIUM severity issues for potential improvements")
                lines.append("- Consider fixing LOW severity issues for better code quality")
                lines.append("- Add proper type hints and documentation\n")

            lines.append("### Resources")
            lines.append("- 📚 [Missing Code Audit Guide](docs/MISSING_CODE_AUDIT_SYSTEM.md)")
            lines.append("- 🔧 [Quick Fix Scripts](scripts/)")
            lines.append("- 📝 [Policy Configuration](configs/missing_code_policy.yml)\n")

        # Footer
        lines.append("---")
        lines.append("*Generated by Missing Code Audit System*")
        lines.append("*Report: `.artifacts/missing_code_delta.json`*")

        # Write output
        content = "\n".join(lines)
        output_file.write_text(content, encoding="utf-8")

        print(f"[owner-report] ✅ Generated: {output_file}")
        print(f"[owner-report] 📊 Issues by {len(by_owner)} owners")

        return 0

    except Exception as e:
        print(f"[owner-report] ❌ Error generating report: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
