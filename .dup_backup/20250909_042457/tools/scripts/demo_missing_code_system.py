#!/usr/bin/env python3
"""
Demo script để chạy thử toàn bộ hệ thống missing code audit.
Chạy cả missing code audit và conformance check, hiển thị kết quả.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import Exception
import category
import cmd
import conformance_exit
import count
import description
import e
import enumerate
import f
import file
import i
import int
import issue
import kind
import len
import list
import max_issues
import min
import missing_code_exit
import open
import print
import report_path
import report_type
import sorted
import str
import test_exit
import tuple
import x


def run_command(cmd: list[str], description: str) -> tuple[int, str]:
    """Chạy command và trả về exit code và output."""
    print(f"\n🔄 {description}")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        return result.returncode, result.stdout

    except Exception as e:
        print(f"❌ Error running command: {e}")
        return 1, str(e)


def display_report_summary(report_path: Path, report_type: str) -> None:
    """Hiển thị tóm tắt báo cáo."""
    if not report_path.exists():
        print(f"❌ {report_type} report not found at {report_path}")
        return

    try:
        with open(report_path, encoding="utf-8") as f:
            data = json.load(f)

        print(f"\n📊 {report_type} Report Summary")
        print("=" * 50)

        if report_type == "Missing Code":
            summary = data.get("summary", {})
            print(f"Total issues: {summary.get('total', 0)}")
            print(f"HIGH severity: {summary.get('high', 0)} 🚨")
            print(f"MEDIUM severity: {summary.get('medium', 0)} ⚠️")
            print(f"LOW severity: {summary.get('low', 0)} ℹ️")

            if "by_kind" in data:
                print("\nTop issue types:")
                for kind, count in sorted(data["by_kind"].items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"  {kind}: {count}")

        elif report_type == "Conformance":
            summary = data.get("summary", {})
            print(f"Total problems: {summary.get('total_problems', 0)}")
            print(f"HIGH severity: {summary.get('high_severity', 0)} 🚨")
            print(f"MEDIUM severity: {summary.get('medium_severity', 0)} ⚠️")
            print(f"LOW severity: {summary.get('low_severity', 0)} ℹ️")

            if "by_category" in data:
                print("\nProblem categories:")
                for category, count in data["by_category"].items():
                    print(f"  {category}: {count}")

    except Exception as e:
        print(f"❌ Error reading report: {e}")


def show_sample_issues(report_path: Path, max_issues: int = 5) -> None:
    """Hiển thị một số issue mẫu."""
    if not report_path.exists():
        return

    try:
        with open(report_path, encoding="utf-8") as f:
            data = json.load(f)

        issues = data.get("issues", [])
        high_issues = [i for i in issues if i.get("severity") == "HIGH"]

        if high_issues:
            print(f"\n🚨 Sample HIGH severity issues (showing {min(max_issues, len(high_issues))}):")
            for i, issue in enumerate(high_issues[:max_issues], 1):
                path = issue.get("path", "unknown")
                line = issue.get("line", 0)
                message = issue.get("message", "no message")
                snippet = issue.get("snippet", "")

                print(f"{i}. {path}:{line}")
                print(f"   {message}")
                if snippet and len(snippet) < 100:
                    print(f"   Code: {snippet}")
                print()

    except Exception as e:
        print(f"❌ Error showing sample issues: {e}")


def main() -> int:
    """Main demo function."""
    print("🎯 MISSING CODE AUDIT SYSTEM DEMO")
    print("=" * 60)
    print("Hệ thống phát hiện thiếu code và kiểm tra conformance")
    print()

    # Ensure artifacts directory exists
    artifacts_dir = Path(".artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    # 1. Run missing code audit
    missing_code_exit, _ = run_command(
        ["uv", "run", "python", "scripts/missing_code_audit.py"],
        "Running missing code audit (Python + TypeScript)",
    )

    # 2. Run conformance check
    conformance_exit, _ = run_command(
        ["uv", "run", "python", "scripts/check_conformance.py"],
        "Running Protocol ↔ Adapter conformance check",
    )

    # 3. Display reports
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    missing_code_report = artifacts_dir / "missing_code_report.json"
    conformance_report = artifacts_dir / "conformance_report.json"

    display_report_summary(missing_code_report, "Missing Code")
    display_report_summary(conformance_report, "Conformance")

    # 4. Show sample issues
    show_sample_issues(missing_code_report)

    # 5. Run tests
    print("\n" + "=" * 60)
    print("RUNNING TESTS")
    print("=" * 60)

    test_exit, _ = run_command(["uv", "run", "pytest", "zeta_vn/tests/tools/", "-v"], "Running audit tool tests")

    # 6. Overall status
    print("\n" + "=" * 60)
    print("OVERALL STATUS")
    print("=" * 60)

    total_exit_code = 0

    if missing_code_exit != 0:
        print("❌ Missing code audit found HIGH severity issues")
        total_exit_code = 1
    else:
        print("✅ Missing code audit passed")

    if conformance_exit != 0:
        print("❌ Conformance check found HIGH severity issues")
        total_exit_code = 1
    else:
        print("✅ Conformance check passed")

    if test_exit != 0:
        print("❌ Some tests failed")
        total_exit_code = 1
    else:
        print("✅ All tests passed")

    # 7. Next steps
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)

    if total_exit_code == 0:
        print("🎉 All checks passed! System is healthy.")
        print()
        print("💡 To maintain code quality:")
        print("1. Add @implements decorator to new adapters")
        print("2. Run audit before committing: scripts/missing_code_audit.py")
        print("3. Enable CI workflow: .github/workflows/missing-code.yml")
    else:
        print("⚠️ Issues found - recommended actions:")
        print()
        print("1. Fix HIGH severity issues first")
        print("2. Run quick fix: uv run python scripts/quick_fix_stubs.py")
        print("3. Review generated reports in .artifacts/")
        print("4. Add @implements decorator to Protocol implementations")
        print("5. Re-run audit to verify fixes")

    print("\n📁 Generated files:")
    for file in artifacts_dir.glob("*.json"):
        print(f"  {file}")

    return total_exit_code


if __name__ == "__main__":
    exit_code = main()
    print(f"\nDemo completed with exit code: {exit_code}")
    sys.exit(exit_code)
