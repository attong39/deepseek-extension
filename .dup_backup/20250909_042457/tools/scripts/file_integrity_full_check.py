#!/usr/bin/env python3
"""
File Integrity Guard - tổng hợp runner cho tất cả checks.

Chạy cả 3 lớp kiểm tra:
1. Auto-fix regression guard
2. Module symbol verification
3. Used-but-missing imports

Usage: uv run python scripts/file_integrity_full_check.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import Exception
import SystemExit
import dict
import e
import int
import print
import report_file
import script_name
import str
import tuple

ART = Path(".artifacts")


def run_script(script_name: str) -> tuple[int, str]:
    """Chạy một script và trả về exit code + output."""
    try:
        result = subprocess.run(  # noqa: S603
            [sys.executable, "-m", f"scripts.{script_name}"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running {script_name}: {e}"


def load_summary(report_file: Path) -> dict:
    """Load summary từ JSON report."""
    if not report_file.exists():
        return {"total": 0, "high": 0, "medium": 0, "low": 0}

    try:
        data = json.loads(report_file.read_text(encoding="utf-8"))
        return data.get("summary", {"total": 0, "high": 0, "medium": 0, "low": 0})
    except Exception:
        return {"total": 0, "high": 0, "medium": 0, "low": 0}


def main() -> int:
    """Run all file integrity checks."""
    print("🔍 Running File Integrity Guard - Enhanced Full Check")
    print("=" * 60)

    # Step 0: Generate expectations
    print("\n0️⃣ Generating Expectations from PROJECT_MAP...")
    _, _ = run_script("generate_expectations_from_project_map")

    # Step 1: Completeness scoring
    print("\n1️⃣ Per-file Completeness Analysis...")
    _, _ = run_script("completeness_score")
    completeness_summary = load_summary(ART / "completeness_report.json")

    # Step 2: Auto-fix regression
    print("\n2️⃣ Auto-fix Regression Guard...")
    _, _ = run_script("auto_fix_regression_guard")
    regression_summary = load_summary(ART / "auto_fix_regression.json")

    # Step 3: Restoration patches (if needed)
    if regression_summary.get("high", 0) > 0:
        print("\n🔧 Generating Restoration Patches...")
        _, _ = run_script("restore_candidate_patch")

    # Step 4: Module symbols
    print("\n3️⃣ Module Symbol Verification...")
    _, _ = run_script("verify_module_symbols")
    symbol_summary = load_summary(ART / "module_symbol_report.json")

    # Step 5: Used but missing
    print("\n4️⃣ Used-but-Missing Imports...")
    _, _ = run_script("used_but_missing")
    import_summary = load_summary(ART / "used_but_missing.json")

    # Step 6: Directory scaffolding
    print("\n5️⃣ Directory Scaffolding...")
    _, _ = run_script("scaffold_missing_dirs")

    # Step 7: Module scaffolding (existing)
    print("\n6️⃣ Module Scaffolding Suggestions...")
    _, _ = run_script("scaffold_missing_modules")

    # Summary
    print("\n" + "=" * 60)
    print("📊 ENHANCED FINAL SUMMARY")
    print("=" * 60)

    total_high = (
        completeness_summary.get("high", 0)
        + regression_summary.get("high", 0)
        + symbol_summary.get("high", 0)
        + import_summary.get("high", 0)
    )

    total_issues = (
        completeness_summary.get("total", 0)
        + regression_summary.get("total", 0)
        + symbol_summary.get("total", 0)
        + import_summary.get("total", 0)
    )

    avg_completeness = completeness_summary.get("avg_score", 0)

    print(
        f"� Completeness:        {completeness_summary.get('high', 0)} HIGH / "
        f"{completeness_summary.get('total', 0)} files (avg: {avg_completeness:.1f})"
    )
    print(
        f"�📈 Auto-fix Regression: {regression_summary.get('high', 0)} HIGH / "
        f"{regression_summary.get('total', 0)} total"
    )
    print(f"🔍 Module Symbols:      {symbol_summary.get('high', 0)} HIGH / " f"{symbol_summary.get('total', 0)} total")
    print(f"📦 Import Issues:       {import_summary.get('high', 0)} HIGH / " f"{import_summary.get('total', 0)} total")
    print("📁 Scaffolding:         Generated in .artifacts/scaffold_*.md")

    if regression_summary.get("high", 0) > 0:
        print("🔧 Restore Patches:     Available in .artifacts/restore_patches/")

    print(f"\n🎯 TOTAL: {total_high} HIGH severity issues / {total_issues} total issues")

    # Completeness threshold check (70.0 default)
    threshold = 70.0
    completeness_fail = avg_completeness < threshold

    # Final verdict
    if total_high > 0 or completeness_fail:
        print("\n❌ FAILED: Critical issues found!")
        if total_high > 0:
            print(f"   📊 {total_high} HIGH severity integrity issues")
        if completeness_fail:
            print(f"   📉 Average completeness {avg_completeness:.1f} below threshold {threshold}")
        print(f"   📄 Review {ART}/*.json for details")
        print(f"   📁 Check {ART}/restore_patches/ for recovery options")
        return 1
    elif total_issues > 0:
        print("\n⚠️  WARNING: Non-critical issues found")
        print(f"   📊 {total_issues} total issues requiring attention")
        print(f"   📄 Review {ART}/*.json for improvements")
        return 0
    else:
        print("\n✅ SUCCESS: All file integrity checks passed!")
        print(f"   📊 Average completeness: {avg_completeness:.1f}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
