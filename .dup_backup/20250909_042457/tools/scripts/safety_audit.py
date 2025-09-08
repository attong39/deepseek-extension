#!/usr/bin/env python3
"""
🛡️ SAFETY AUDIT SCRIPT - Comprehensive Project Health Check

Kiểm tra toàn diện tình trạng an toàn của dự án.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import Exception
import bool
import check_name
import check_result
import cmd
import dict
import e
import f
import int
import isinstance
import len
import line
import list
import output_file
import print
import project_root
import py_file
import self
import str
import sub_check


class SafetyAuditor:
    """Comprehensive project safety auditor."""

    def __init__(self, project_root: Path = Path.cwd()) -> None:
        self.project_root = project_root
        self.results: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "project_root": str(project_root),
            "checks": {},
            "summary": {"passed": 0, "failed": 0, "warnings": 0},
        }

    def run_command(self, cmd: list[str], check_name: str) -> dict[str, Any]:
        """Run command and capture results safely."""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=self.project_root)

            return {
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd),
            }
        except subprocess.TimeoutExpired:
            return {"status": "failed", "error": "Command timeout", "command": " ".join(cmd)}
        except Exception as e:
            return {"status": "failed", "error": str(e), "command": " ".join(cmd)}

    def check_ruff(self) -> None:
        """Check code quality with ruff."""
        print("🔍 Running Ruff check...")
        result = self.run_command(["uv", "run", "ruff", "check", ".", "--statistics"], "ruff")

        # Parse statistics if available
        if result["status"] == "failed" and result["stdout"]:
            lines = result["stdout"].strip().split("\n")
            errors = {}
            for line in lines:
                if line.strip() and not line.startswith("Found"):
                    parts = line.strip().split()
                    if len(parts) >= 2 and parts[0].isdigit():
                        count = int(parts[0])
                        error_type = parts[1]
                        errors[error_type] = count
            result["error_statistics"] = errors

        self.results["checks"]["ruff"] = result

    def check_mypy(self) -> None:
        """Check type hints with mypy."""
        print("🎯 Running MyPy check...")
        result = self.run_command(["uv", "run", "mypy", ".", "--show-error-codes"], "mypy")
        self.results["checks"]["mypy"] = result

    def check_tests(self) -> None:
        """Run test suite."""
        print("🧪 Running tests...")
        result = self.run_command(["uv", "run", "pytest", "-v", "--tb=short"], "pytest")
        self.results["checks"]["tests"] = result

    def check_security(self) -> None:
        """Security vulnerability scan."""
        print("🔒 Running security scan...")
        bandit_result = self.run_command(["uv", "run", "bandit", "-r", "zeta_vn", "--format", "json"], "bandit")

        pip_audit_result = self.run_command(["uv", "run", "pip-audit", "--format", "json"], "pip_audit")

        self.results["checks"]["security"] = {
            "bandit": bandit_result,
            "pip_audit": pip_audit_result,
        }

    def check_dependencies(self) -> None:
        """Check dependency status."""
        print("📦 Checking dependencies...")
        result = self.run_command(["uv", "pip", "list", "--format", "json"], "dependencies")

        if result["status"] == "passed":
            try:
                deps = json.loads(result["stdout"])
                result["dependency_count"] = len(deps)
                result["dependencies"] = deps
            except json.JSONDecodeError:
                result["warning"] = "Could not parse dependency list"

        self.results["checks"]["dependencies"] = result

    def check_code_coverage(self) -> None:
        """Check test coverage."""
        print("📊 Checking code coverage...")
        result = self.run_command(["uv", "run", "pytest", "--cov=zeta_vn", "--cov-report=json"], "coverage")

        if result["status"] == "passed":
            coverage_file = self.project_root / "coverage.json"
            if coverage_file.exists():
                try:
                    with coverage_file.open() as f:
                        coverage_data = json.load(f)
                    result["coverage_percent"] = coverage_data.get("totals", {}).get("percent_covered", 0)
                except Exception as e:
                    result["warning"] = f"Could not parse coverage: {e}"

        self.results["checks"]["coverage"] = result

    def analyze_file_structure(self) -> None:
        """Analyze project file structure."""
        print("📁 Analyzing file structure...")

        python_files = list(self.project_root.glob("**/*.py"))
        test_files = [f for f in python_files if "test" in str(f)]

        structure_info = {
            "total_python_files": len(python_files),
            "test_files": len(test_files),
            "test_coverage_ratio": len(test_files) / len(python_files) if python_files else 0,
            "large_files": [],
        }

        # Check for large files
        for py_file in python_files:
            try:
                size = py_file.stat().st_size
                if size > 10000:  # Files > 10KB
                    lines = len(py_file.read_text(encoding="utf-8").splitlines())
                    structure_info["large_files"].append(
                        {
                            "file": str(py_file.relative_to(self.project_root)),
                            "size_bytes": size,
                            "lines": lines,
                        }
                    )
            except Exception:
                continue

        self.results["checks"]["file_structure"] = {"status": "passed", "analysis": structure_info}

    def generate_summary(self) -> None:
        """Generate overall summary."""
        passed = 0
        failed = 0
        warnings = 0

        for check_name, check_result in self.results["checks"].items():
            if isinstance(check_result, dict):
                if check_result.get("status") == "passed":
                    passed += 1
                elif check_result.get("status") == "failed":
                    failed += 1
                if "warning" in check_result:
                    warnings += 1
            else:
                # Handle nested checks like security
                for sub_check in check_result.values():
                    if sub_check.get("status") == "passed":
                        passed += 1
                    elif sub_check.get("status") == "failed":
                        failed += 1
                    if "warning" in sub_check:
                        warnings += 1

        self.results["summary"] = {
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "total_checks": passed + failed,
            "health_score": (passed / (passed + failed)) * 100 if (passed + failed) > 0 else 0,
        }

    def save_report(self, output_file: Path = Path("safety_audit_report.json")) -> None:
        """Save detailed report."""
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"📋 Report saved to: {output_file}")

    def print_summary(self) -> None:
        """Print summary to console."""
        summary = self.results["summary"]
        print("\n" + "=" * 60)
        print("🛡️  SAFETY AUDIT SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⚠️  Warnings: {summary['warnings']}")
        print(f"📊 Health Score: {summary['health_score']:.1f}%")
        print("=" * 60)

        # Detailed breakdown
        for check_name, result in self.results["checks"].items():
            if isinstance(result, dict) and "status" in result:
                status_icon = "✅" if result["status"] == "passed" else "❌"
                print(f"{status_icon} {check_name.title()}: {result['status']}")

        return summary["health_score"] >= 80  # Return True if healthy

    def run_full_audit(self) -> bool:
        """Run complete safety audit."""
        print("🚀 Starting comprehensive safety audit...")

        # Core quality checks
        self.check_ruff()
        self.check_mypy()
        self.check_tests()

        # Security checks
        self.check_security()

        # Dependency and structure analysis
        self.check_dependencies()
        self.check_code_coverage()
        self.analyze_file_structure()

        # Generate summary
        self.generate_summary()

        # Save and display results
        self.save_report()
        return self.print_summary()


def main() -> None:
    """Main entry point."""
    auditor = SafetyAuditor()
    is_healthy = auditor.run_full_audit()

    if not is_healthy:
        print("\n⚠️  Project health score below 80%. Please review the report.")
        sys.exit(1)
    else:
        print("\n✅ Project is healthy!")
        sys.exit(0)


if __name__ == "__main__":
    main()
