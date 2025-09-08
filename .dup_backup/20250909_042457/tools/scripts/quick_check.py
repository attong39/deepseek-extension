#!/usr/bin/env python3
"""
Quick environment and code quality check script for ZETA project.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import Exception
import bool
import cmd
import desc
import description
import e
import len
import list
import print
import str


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()[:100]}...")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()[:200]}...")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False


def main():
    """Main check routine."""
    print("🎯 ZETA_VN Environment & Quality Check")
    print("=" * 50)

    checks = [
        (
            ["uv", "run", "python", "-c", "import sys; print(f'Python {sys.version}'[:50])"],
            "Python version check",
        ),
        (
            ["uv", "run", "python", "-c", "import zeta_vn; print('zeta_vn imported OK')"],
            "Package import check",
        ),
        (["uv", "run", "ruff", "format", ".", "--check"], "Ruff format check"),
        (["uv", "run", "ruff", "check", ".", "--select", "E,W,F"], "Ruff critical issues check"),
    ]

    passed = 0
    for cmd, desc in checks:
        if run_command(cmd, desc):
            passed += 1

    print(f"\n📊 Results: {passed}/{len(checks)} checks passed")

    if passed == len(checks):
        print("🎉 All checks passed! Environment is ready.")
        return 0
    else:
        print("⚠️  Some checks failed. Please review above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
