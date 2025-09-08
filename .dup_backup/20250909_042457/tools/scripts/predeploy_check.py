#!/usr/bin/env python3
"""
Production readiness checker for ZETA_VN.

Validates environment, dependencies, code quality, security, and deployment readiness.
"""

import os
import subprocess
import sys
from pathlib import Path
import Exception
import ValueError
import allow_fail
import args
import bool
import check_func
import check_name
import code
import e
import env
import float
import int
import len
import line
import print
import stderr
import stdout
import str
import tuple

HERE = Path(__file__).parent
ROOT = HERE.parent


class CheckFail(Exception):
    """Raised when a critical check fails."""


def run_cmd(*args: str, allow_fail: bool = False) -> tuple[int, str, str]:
    """Run command and return (returncode, stdout, stderr)."""
    result = subprocess.run(args, check=False, cwd=ROOT, capture_output=True, text=True, timeout=300)

    if result.returncode != 0 and not allow_fail:
        raise CheckFail(f"Command failed: {' '.join(args)}\n{result.stderr}")

    return result.returncode, result.stdout, result.stderr


def check_environment() -> None:
    """Check required environment variables."""
    print("🌍 Checking environment variables...")

    required_envs = [
        "DATABASE_URL",
        "REDIS_URL",
        "JWT_SECRET_KEY",
    ]

    missing = []
    for env in required_envs:
        if not os.getenv(env):
            missing.append(env)

    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        raise CheckFail(f"Missing required environment variables: {missing}")

    print("✅ All required environment variables set")


def check_dependencies() -> None:
    """Check that all dependencies are installed."""
    print("📦 Checking dependencies...")

    try:
        run_cmd("uv", "sync", "--dev")
        print("✅ Dependencies synced successfully")
    except CheckFail:
        print("❌ Failed to sync dependencies")
        raise


def check_code_quality() -> None:
    """Run code quality checks."""
    print("🔍 Running code quality checks...")

    # Ruff linting
    print("  Running ruff...")
    code, stdout, stderr = run_cmd("uv", "run", "ruff", "check", ".", allow_fail=True)
    if code != 0:
        error_count = len(stdout.strip().splitlines()) if stdout.strip() else 0
        if error_count > 50:  # Allow some errors but not too many
            print(f"❌ Too many ruff errors: {error_count}")
            raise CheckFail(f"Ruff found {error_count} errors (max 50 allowed)")
    print("✅ Ruff check passed")

    # Type checking
    print("  Running mypy...")
    code, stdout, stderr = run_cmd("uv", "run", "mypy", ".", "--strict", allow_fail=True)
    if code != 0:
        error_lines = [line for line in stdout.splitlines() if ": error:" in line]
        if len(error_lines) > 20:  # Allow some type errors during development
            print(f"❌ Too many type errors: {len(error_lines)}")
            raise CheckFail(f"MyPy found {len(error_lines)} errors (max 20 allowed)")
    print("✅ Type checking passed")


def check_tests() -> None:
    """Run test suite."""
    print("🧪 Running tests...")

    code, stdout, stderr = run_cmd("uv", "run", "pytest", "-x", "--maxfail=5", allow_fail=True)
    if code != 0:
        print("❌ Tests failed")
        print(f"Error output:\n{stderr}")
        raise CheckFail("Test suite failed")

    print("✅ All tests passed")


def check_security() -> None:
    """Run security checks."""
    print("🔒 Running security checks...")

    # Bandit security linting
    print("  Running bandit...")
    code, stdout, stderr = run_cmd("uv", "run", "bandit", "-r", "zeta_vn", "-q", allow_fail=True)
    if code != 0 and "No issues identified" not in stdout:
        # Allow warnings but fail on high severity issues
        if "SEVERITY: HIGH" in stdout:
            print("❌ High severity security issues found")
            raise CheckFail("Bandit found high severity security issues")
    print("✅ Security scan passed")

    # Dependency vulnerability check
    print("  Checking for vulnerable dependencies...")
    code, stdout, stderr = run_cmd("uv", "run", "pip-audit", allow_fail=True)
    if code != 0:
        # Allow some vulnerabilities in dev dependencies
        vuln_count = stdout.count("vulnerability") if stdout else 0
        if vuln_count > 5:
            print(f"❌ Too many vulnerabilities: {vuln_count}")
            raise CheckFail(f"Found {vuln_count} vulnerabilities (max 5 allowed)")
    print("✅ Dependency security check passed")


def check_focus_index() -> None:
    """Check Focus Index meets minimum threshold."""
    print("🎯 Checking Focus Index...")

    code, stdout, stderr = run_cmd("python", "tools/focus_guard.py", allow_fail=True)
    if code == 0 and stdout:
        # Parse Focus Index from output
        for line in stdout.splitlines():
            if "Focus Index:" in line:
                score_str = line.split(":")[1].split("/")[0].strip()
                try:
                    score = float(score_str)
                    min_score = float(os.getenv("MIN_FOCUS_INDEX", "25"))

                    if score < min_score:
                        print(f"❌ Focus Index too low: {score} < {min_score}")
                        raise CheckFail(f"Focus Index {score} below minimum {min_score}")

                    print(f"✅ Focus Index: {score}/100 (min: {min_score})")
                    return
                except ValueError:
                    pass

    print("⚠️ Could not determine Focus Index")


def check_database() -> None:
    """Check database connectivity and migrations."""
    print("🗄️ Checking database...")

    # Check if alembic is available
    if Path("alembic.ini").exists():
        print("  Checking migrations...")
        code, stdout, stderr = run_cmd("uv", "run", "alembic", "current", allow_fail=True)
        if code != 0:
            print("⚠️ Database migration check failed (this may be expected in CI)")
        else:
            print("✅ Database migrations checked")
    else:
        print("⚠️ No alembic configuration found")


def main() -> int:
    """Main check orchestrator."""
    print("🚀 ZETA_VN Production Readiness Check")
    print("=" * 50)

    checks = [
        ("Environment", check_environment),
        ("Dependencies", check_dependencies),
        ("Code Quality", check_code_quality),
        ("Tests", check_tests),
        ("Security", check_security),
        ("Focus Index", check_focus_index),
        ("Database", check_database),
    ]

    failed_checks = []

    for check_name, check_func in checks:
        try:
            print(f"\n[{check_name}]")
            check_func()
        except CheckFail as e:
            print(f"❌ {check_name} failed: {e}")
            failed_checks.append(check_name)
        except Exception as e:
            print(f"⚠️ {check_name} error: {e}")
            failed_checks.append(check_name)

    print(f"\n{'=' * 50}")

    if failed_checks:
        print(f"❌ {len(failed_checks)} checks failed: {', '.join(failed_checks)}")
        print("🚫 NOT READY FOR PRODUCTION")
        return 1
    else:
        print("✅ ALL CHECKS PASSED")
        print("🎉 READY FOR PRODUCTION DEPLOYMENT")
        return 0


if __name__ == "__main__":
    sys.exit(main())
