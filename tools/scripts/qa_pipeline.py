from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
import Exception
import bool
import check_func
import coverage
import description
import e
import fix
import init_file
import len
import list
import name
import print
import self
import str
import verbose

"""QA Pipeline Script for Zeta VN Project.
This script runs comprehensive quality assurance checks including:
- Code formatting and linting (ruff)
- Type checking (mypy)
- Unit tests (pytest)
- Security scanning (bandit)
- Dependency auditing (pip-audit)
- Dead code detection (vulture)
Usage:
    python scripts/qa_pipeline.py [--fix] [--verbose] [--coverage]
Options:
    --fix       Auto-fix formatting issues
    --verbose   Show detailed output
    --coverage  Run tests with coverage report
"""


class QAPipeline:
    """Quality Assurance Pipeline for Zeta VN."""

    def __init__(self, verbose: bool = False, fix: bool = False, coverage: bool = False):
        self.verbose = verbose
        self.fix = fix
        self.coverage = coverage
        self.project_root = Path(__file__).parent.parent

    def run_command(self, cmd: list[str], description: str) -> bool:
        """Run a command and return success status."""
        if self.verbose:
            print(f"\n🔧 {description}")
            print(f"Command: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=not self.verbose, text=True, check=False)
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ {description} - PASSED")
                else:
                    print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description} - FAILED")
                if not self.verbose:
                    print(f"Error output: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ {description} - ERROR: {e}")
            return False

    def check_uv_availability(self) -> bool:
        """Check if uv is available."""
        return self.run_command(["uv", "--version"], "Checking uv availability")

    def format_code(self) -> bool:
        """Format code with ruff."""
        if self.fix:
            return self.run_command(["uv", "run", "ruff", "format", "."], "Formatting code with ruff")
        else:
            return self.run_command(
                ["uv", "run", "ruff", "format", "--check", "."],
                "Checking code formatting with ruff",
            )

    def lint_code(self) -> bool:
        """Lint code with ruff."""
        return self.run_command(["uv", "run", "ruff", "check", "."], "Linting code with ruff")

    def type_check(self) -> bool:
        """Type check with mypy."""
        return self.run_command(["uv", "run", "mypy", "zeta_vn", "--show-error-codes"], "Type checking with mypy")

    def run_tests(self) -> bool:
        """Run unit tests with pytest."""
        cmd = ["uv", "run", "pytest"]
        if self.coverage:
            cmd.extend(
                [
                    "--cov=zeta_vn",
                    "--cov-report=html",
                    "--cov-report=term-missing",
                    "--cov-fail-under=80",
                ]
            )
        else:
            cmd.append("-q")
        return self.run_command(cmd, "Running unit tests with pytest")

    def security_scan(self) -> bool:
        """Security scan with bandit."""
        return self.run_command(["uv", "run", "bandit", "-q", "-r", "zeta_vn"], "Security scanning with bandit")

    def audit_dependencies(self) -> bool:
        """Audit dependencies with pip-audit."""
        return self.run_command(["uv", "run", "pip-audit"], "Auditing dependencies with pip-audit")

    def check_dead_code(self) -> bool:
        """Check for dead code with vulture."""
        return self.run_command(["uv", "run", "vulture", "zeta_vn"], "Checking for dead code with vulture")

    def validate_project_structure(self) -> bool:
        """Validate project structure and imports."""
        success = True
        required_inits = [
            "zeta_vn/__init__.py",
            "zeta_vn/core/__init__.py",
            "zeta_vn/core/domain/__init__.py",
            "zeta_vn/core/domain/aggregates/__init__.py",
            "zeta_vn/tests/__init__.py",
            "zeta_vn/tests/unit/__init__.py",
            "zeta_vn/tests/unit/domain/__init__.py",
        ]
        for init_file in required_inits:
            if not (self.project_root / init_file).exists():
                print(f"❌ Missing required file: {init_file}")
                success = False
            else:
                if self.verbose:
                    print(f"✅ Found: {init_file}")
        if success:
            print("✅ Project structure validation passed")
        else:
            print("❌ Project structure validation failed")
        return success

    def run_all_checks(self) -> bool:
        """Run all QA checks."""
        print("🚀 Starting Zeta VN QA Pipeline")
        print("=" * 50)
        checks = [
            ("UV Availability", self.check_uv_availability),
            ("Project Structure", self.validate_project_structure),
            ("Code Formatting", self.format_code),
            ("Code Linting", self.lint_code),
            ("Type Checking", self.type_check),
            ("Unit Tests", self.run_tests),
            ("Security Scan", self.security_scan),
            ("Dependency Audit", self.audit_dependencies),
            ("Dead Code Check", self.check_dead_code),
        ]
        results = []
        for name, check_func in checks:
            result = check_func()
            results.append((name, result))
        print("\n" + "=" * 50)
        print("📊 QA Pipeline Summary:")
        passed = 0
        total = len(results)
        for name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"  {name}: {status}")
            if result:
                passed += 1
        success_rate = (passed / total) * 100
        print(f"\nOverall: {passed}/{total} checks passed ({success_rate:.1f}%)")
        if passed == total:
            print("🎉 All QA checks passed! Code is ready for production.")
            return True
        else:
            print("⚠️  Some QA checks failed. Please review and fix issues.")
            return False


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Zeta VN QA Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/qa_pipeline.py                    # Run all checks
  python scripts/qa_pipeline.py --fix             # Auto-fix formatting
  python scripts/qa_pipeline.py --verbose         # Detailed output
  python scripts/qa_pipeline.py --coverage        # With coverage report
        """,
    )
    parser.add_argument("--fix", action="store_true", help="Auto-fix formatting issues")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage report")
    args = parser.parse_args()
    pipeline = QAPipeline(verbose=args.verbose, fix=args.fix, coverage=args.coverage)
    success = pipeline.run_all_checks()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
