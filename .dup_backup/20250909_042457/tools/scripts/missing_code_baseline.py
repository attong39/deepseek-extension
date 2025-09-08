#!/usr/bin/env python3
"""
Tạo và cập nhật baseline từ missing code audit report.

Baseline được dùng để "đóng băng" backlog hiện tại và chỉ bắt lỗi mới.
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
import len
import print
import set
import sum


def main() -> int:
    """Main entry point for baseline creation."""
    artifacts_dir = Path(".artifacts")
    baseline_file = Path("contracts/missing_code_baseline.json")
    report_file = artifacts_dir / "missing_code_report.json"

    if not report_file.exists():
        print("[baseline] ❌ Missing .artifacts/missing_code_report.json")
        print("[baseline] Run 'uv run python scripts/missing_code_audit.py' first")
        return 2

    try:
        # Load current report
        report_data = json.loads(report_file.read_text(encoding="utf-8"))

        # Ensure contracts directory exists
        baseline_file.parent.mkdir(parents=True, exist_ok=True)

        # Create baseline với chỉ thông tin cần thiết để identify issues
        baseline = {
            "created_at": "2025-08-29T00:00:00Z",  # Timestamp cho tracking
            "summary": report_data.get("summary", {}),
            "total_files_scanned": len(set(i["path"] for i in report_data.get("issues", []))),
            "baseline_version": "1.0",
            "issues": [
                {
                    "path": issue["path"],
                    "line": issue["line"],
                    "kind": issue["kind"],
                    "severity": issue["severity"],
                }
                for issue in report_data.get("issues", [])
            ],
        }

        # Write baseline
        baseline_file.write_text(json.dumps(baseline, indent=2, ensure_ascii=False), encoding="utf-8")

        # Summary
        total_issues = len(baseline["issues"])
        high_issues = sum(1 for i in baseline["issues"] if i["severity"] == "HIGH")
        medium_issues = sum(1 for i in baseline["issues"] if i["severity"] == "MEDIUM")
        low_issues = sum(1 for i in baseline["issues"] if i["severity"] == "LOW")

        print(f"[baseline] ✅ Created {baseline_file}")
        print("[baseline] 📊 Baseline Summary:")
        print(f"  Total issues: {total_issues}")
        print(f"  HIGH: {high_issues} 🚨")
        print(f"  MEDIUM: {medium_issues} ⚠️")
        print(f"  LOW: {low_issues} ℹ️")
        print(f"  Files scanned: {baseline['total_files_scanned']}")

        print("\n[baseline] 💡 Next steps:")
        print("  1. Commit this baseline to freeze current backlog")
        print("  2. Enable PR diff-gate: scripts/missing_code_diff_gate.py")
        print("  3. Set reduction targets in configs/missing_code_policy.yml")

        return 0

    except Exception as e:
        print(f"[baseline] ❌ Error creating baseline: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
