#!/usr/bin/env python3
"""Analyze middleware files completeness."""

import json
from pathlib import Path


def main():
    report_file = Path(".artifacts/completeness_report.json")
    if not report_file.exists():
        print("❌ Completeness report not found")
        return

    data = json.loads(report_file.read_text())
    middleware_files = [r for r in data["rows"] if "middleware" in r["path"]]

    print("🔍 MIDDLEWARE FILES COMPLETENESS ANALYSIS")
    print("=" * 60)

    if not middleware_files:
        print("❌ No middleware files found in analysis")
        return

    # Sort by score (lowest first)
    middleware_files.sort(key=lambda x: x["score"])

    print(f"📊 Found {len(middleware_files)} middleware files")
    print(f"📈 Average score: {sum(r['score'] for r in middleware_files) / len(middleware_files):.1f}")

    high_issues = [r for r in middleware_files if r["severity"] == "HIGH"]
    warn_issues = [r for r in middleware_files if r["severity"] == "WARN"]
    ok_files = [r for r in middleware_files if r["severity"] == "OK"]

    print(f"🔴 HIGH issues: {len(high_issues)}")
    print(f"🟡 WARN issues: {len(warn_issues)}")
    print(f"🟢 OK files: {len(ok_files)}")

    print("\n📋 TOP ISSUES (lowest scores):")
    for i, row in enumerate(middleware_files[:15]):
        icon = "🔴" if row["severity"] == "HIGH" else ("🟡" if row["severity"] == "WARN" else "🟢")
        print(f"{i + 1:2d}. {icon} {row['score']:5.1f} — {row['path']}")
        print(f"    fn:{row['funcs']}, cls:{row['classes']}, loc:{row['loc']}, todos:{row['todos']}")


if __name__ == "__main__":
    main()
import enumerate
import i
import len
import print
import r
import row
import sum
import x
