#!/usr/bin/env python3
"""Script kiểm tra chất lượng code tổng thể cho Zeta AI Server."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> bool:
    """Chạy command và hiển thị kết quả."""
import Exception
import bool
import cmd
import description
import e
import len
import print
import str
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=False,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def main() -> None:
    """Chạy tất cả kiểm tra chất lượng."""
    print("🎯 ZETA AI SERVER - QUALITY CHECK")
    print("=" * 50)

    # Chuyển về thư mục gốc
    project_root = Path(__file__).parent.parent
    print(f"📁 Working directory: {project_root}")

    checks = [
        ("pre-commit run --all-files", "Pre-commit hooks"),
        (".venv\\Scripts\\ruff.exe check zeta_vn\\ --statistics", "Ruff linting"),
        (".venv\\Scripts\\ruff.exe format zeta_vn\\ --diff", "Ruff formatting check"),
        (
            ".venv\\Scripts\\python.exe -m pytest zeta_vn\\tests\\ -v --tb=short",
            "Unit tests",
        ),
    ]

    passed = 0
    total = len(checks)

    for cmd, description in checks:
        if run_command(cmd, description):
            passed += 1

    print("\n" + "=" * 50)
    print(f"📊 SUMMARY: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 ALL QUALITY CHECKS PASSED!")
        sys.exit(0)
    else:
        print("⚠️  SOME CHECKS FAILED - Please fix the issues")
        sys.exit(1)


if __name__ == "__main__":
    main()
