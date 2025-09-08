"""Script to run quality gates: ruff, mypy, pytest.

This script runs all quality checks in sequence and reports the results.
Used for CI/CD pipelines and local development.

Usage:
    python scripts/run_quality_gates.py
    python scripts/run_quality_gates.py --fix  # Auto-fix formatting issues
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import Exception
import bool
import cmd
import cwd
import e
import error
import list
import name
import output
import print
import str
import title
import tuple


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[bool, str, str]:
    """Run a command and return success status with output.

    Args:
        cmd: Command to run as list of strings.
        cwd: Working directory for the command.

    Returns:
        Tuple of (success, stdout, stderr).
    """
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'=' * 60}")
    print(f"🚀 {title}")
    print(f"{'=' * 60}")


def print_result(success: bool, output: str, error: str) -> None:
    """Print command result."""
    if success:
        print("✅ PASSED")
        if output.strip():
            print(output)
    else:
        print("❌ FAILED")
        if error.strip():
            print("STDERR:", error)
        if output.strip():
            print("STDOUT:", output)


def run_quality_check(name: str, cmd: list[str], cwd: Path) -> bool:
    """Run a single quality check and return success status."""
    print_section(name)
    success, output, error = run_command(cmd, cwd)
    print_result(success, output, error)
    return success


def run_formatting_check(cwd: Path, auto_fix: bool) -> bool:
    """Run code formatting check."""
    if auto_fix:
        return run_quality_check("Code Formatting (Ruff)", ["uv", "run", "ruff", "format", "."], cwd)
    else:
        success = run_quality_check("Code Formatting (Ruff)", ["uv", "run", "ruff", "format", "--check", "."], cwd)
        if not success and not auto_fix:
            print("💡 Tip: Run with --fix to auto-format code")
        return success


def main() -> None:
    """Run all quality gates."""
    project_root = Path(__file__).parent.parent
    all_passed = True

    # Check if we're in auto-fix mode
    auto_fix = "--fix" in sys.argv

    print("🔍 Running Quality Gates for zeta_vn project")
    print(f"📁 Project root: {project_root}")

    # Run all checks
    checks = [
        ("Code Linting (Ruff)", ["uv", "run", "ruff", "check", "."]),
        ("Type Checking (MyPy)", ["uv", "run", "mypy", "."]),
        (
            "Unit Tests (Pytest)",
            [
                "uv",
                "run",
                "pytest",
                "--cov=zeta_vn",
                "--cov-report=html:htmlcov",
                "--cov-report=term-missing",
                "-v",
            ],
        ),
        ("Security Check (Bandit)", ["uv", "run", "bandit", "-r", "zeta_vn", "-f", "txt"]),
        ("Dependency Audit (pip-audit)", ["uv", "run", "pip-audit"]),
        ("Dead Code Detection (Vulture)", ["uv", "run", "vulture", "zeta_vn"]),
    ]

    # Formatting check
    if not run_formatting_check(project_root, auto_fix):
        all_passed = False

    # Other checks
    for name, cmd in checks:
        if not run_quality_check(name, cmd, project_root):
            all_passed = False

    # Final result
    print_section("FINAL RESULT")
    if all_passed:
        print("🎉 ALL QUALITY GATES PASSED!")
        print("✅ Code is ready for production")
        if auto_fix:
            print("🔧 Auto-formatting completed")
    else:
        print("💥 SOME QUALITY GATES FAILED!")
        print("❌ Please fix the issues above before committing")
        if not auto_fix:
            print("💡 Try running with --fix to auto-format, or fix issues manually")
        sys.exit(1)


if __name__ == "__main__":
    main()
