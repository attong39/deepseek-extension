#!/usr/bin/env python3
"""
🧪 TESTING SAFETY FRAMEWORK - Comprehensive Test Management

Framework để đảm bảo testing an toàn và đầy đủ.
"""

from __future__ import annotations

import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
import Exception
import bool
import dict
import e
import f
import int
import isinstance
import len
import list
import max
import min
import print
import project_root
import self
import str
import sub_result
import sub_type
import sum
import test_type
import xml_file


class TestSafetyManager:
    """Comprehensive testing safety manager."""

    def __init__(self, project_root: Path = Path.cwd()) -> None:
        self.project_root = project_root
        self.reports_dir = project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)

    def run_unit_tests(self) -> dict[str, Any]:
        """Run unit tests with coverage."""
        print("🧪 Running unit tests...")

        try:
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "pytest",
                    "zeta_vn/tests/unit/",
                    "--cov=zeta_vn",
                    "--cov-report=json:reports/coverage.json",
                    "--cov-report=html:reports/coverage_html",
                    "--junit-xml=reports/unit_tests.xml",
                    "-v",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            # Parse results
            test_results = {
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

            # Parse coverage if available
            coverage_file = self.reports_dir / "coverage.json"
            if coverage_file.exists():
                with coverage_file.open() as f:
                    coverage_data = json.load(f)
                test_results["coverage"] = coverage_data.get("totals", {}).get("percent_covered", 0)

            return test_results

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def run_integration_tests(self) -> dict[str, Any]:
        """Run integration tests."""
        print("🔗 Running integration tests...")

        try:
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "pytest",
                    "zeta_vn/tests/integration/",
                    "--junit-xml=reports/integration_tests.xml",
                    "-v",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def run_api_tests(self) -> dict[str, Any]:
        """Run API tests."""
        print("🌐 Running API tests...")

        try:
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "pytest",
                    "zeta_vn/tests/api/",
                    "--junit-xml=reports/api_tests.xml",
                    "-v",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def run_security_tests(self) -> dict[str, Any]:
        """Run security tests."""
        print("🔒 Running security tests...")

        security_results = {}

        # Bandit security scan
        try:
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "bandit",
                    "-r",
                    "zeta_vn",
                    "--format",
                    "json",
                    "-o",
                    "reports/bandit_report.json",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            security_results["bandit"] = {
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
            }

        except Exception as e:
            security_results["bandit"] = {"status": "error", "message": str(e)}

        # Dependency vulnerability check
        try:
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "pip-audit",
                    "--format",
                    "json",
                    "--output",
                    "reports/pip_audit.json",
                ],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            security_results["pip_audit"] = {
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
            }

        except Exception as e:
            security_results["pip_audit"] = {"status": "error", "message": str(e)}

        return security_results

    def run_performance_tests(self) -> dict[str, Any]:
        """Run performance tests."""
        print("⚡ Running performance tests...")

        try:
            # Look for performance test files
            perf_test_files = list(self.project_root.glob("**/test_*_performance.py"))

            if not perf_test_files:
                return {"status": "skipped", "message": "No performance test files found"}

            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "pytest",
                    "--benchmark-only",
                    "--benchmark-json=reports/benchmark.json",
                    "-v",
                ]
                + [str(f) for f in perf_test_files],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            return {
                "status": "passed" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def analyze_test_results(self) -> dict[str, Any]:
        """Analyze all test results."""
        analysis = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "error_tests": 0,
            "coverage_percentage": 0,
            "test_files": [],
        }

        # Parse XML test reports
        xml_reports = list(self.reports_dir.glob("*_tests.xml"))

        for xml_file in xml_reports:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                # Parse JUnit XML format
                if root.tag == "testsuite":
                    tests = int(root.get("tests", 0))
                    failures = int(root.get("failures", 0))
                    errors = int(root.get("errors", 0))

                    analysis["total_tests"] += tests
                    analysis["failed_tests"] += failures
                    analysis["error_tests"] += errors
                    analysis["passed_tests"] += tests - failures - errors

                    analysis["test_files"].append(
                        {
                            "file": xml_file.name,
                            "tests": tests,
                            "failures": failures,
                            "errors": errors,
                        }
                    )

            except Exception as e:
                print(f"⚠️ Could not parse {xml_file}: {e}")

        # Get coverage data
        coverage_file = self.reports_dir / "coverage.json"
        if coverage_file.exists():
            try:
                with coverage_file.open() as f:
                    coverage_data = json.load(f)
                analysis["coverage_percentage"] = coverage_data.get("totals", {}).get("percent_covered", 0)
            except Exception:
                pass

        return analysis

    def generate_test_report(self) -> dict[str, Any]:
        """Generate comprehensive test report."""
        print("📊 Generating test safety report...")

        report = {
            "unit_tests": self.run_unit_tests(),
            "integration_tests": self.run_integration_tests(),
            "api_tests": self.run_api_tests(),
            "security_tests": self.run_security_tests(),
            "performance_tests": self.run_performance_tests(),
            "analysis": self.analyze_test_results(),
        }

        # Calculate overall test score
        scores = []

        for test_type, result in report.items():
            if test_type == "analysis":
                continue

            if isinstance(result, dict):
                if result.get("status") == "passed":
                    scores.append(100)
                elif result.get("status") == "failed":
                    scores.append(0)
                elif result.get("status") == "skipped":
                    scores.append(75)  # Neutral score for skipped
                else:
                    scores.append(0)  # Error
            else:
                # Handle security tests (nested dict)
                sub_scores = []
                for sub_result in result.values():
                    if sub_result.get("status") == "passed":
                        sub_scores.append(100)
                    elif sub_result.get("status") == "failed":
                        sub_scores.append(0)
                    else:
                        sub_scores.append(0)
                scores.append(sum(sub_scores) / len(sub_scores) if sub_scores else 0)

        overall_score = sum(scores) / len(scores) if scores else 0

        # Add coverage bonus/penalty
        coverage = report["analysis"]["coverage_percentage"]
        if coverage >= 80:
            overall_score += 10
        elif coverage < 60:
            overall_score -= 10

        report["overall_score"] = min(100, max(0, overall_score))

        # Determine status
        if overall_score >= 90:
            report["status"] = "excellent"
        elif overall_score >= 75:
            report["status"] = "good"
        elif overall_score >= 60:
            report["status"] = "fair"
        else:
            report["status"] = "needs_improvement"

        return report

    def save_report(self, report: dict[str, Any]) -> None:
        """Save test report."""
        report_file = self.reports_dir / "test_safety_report.json"
        with report_file.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📄 Test report saved to: {report_file}")

    def print_summary(self, report: dict[str, Any]) -> bool:
        """Print test summary."""
        print("\n" + "=" * 60)
        print("🧪 TEST SAFETY REPORT")
        print("=" * 60)
        print(f"📊 Overall Score: {report['overall_score']:.1f}/100 ({report['status'].upper()})")

        analysis = report["analysis"]
        print(f"🧪 Total Tests: {analysis['total_tests']}")
        print(f"✅ Passed: {analysis['passed_tests']}")
        print(f"❌ Failed: {analysis['failed_tests']}")
        print(f"🚨 Errors: {analysis['error_tests']}")
        print(f"📊 Coverage: {analysis['coverage_percentage']:.1f}%")

        print("\n📋 Test Categories:")
        for test_type, result in report.items():
            if test_type in ["analysis", "overall_score", "status"]:
                continue

            if isinstance(result, dict):
                status = result.get("status", "unknown")
                emoji = "✅" if status == "passed" else "❌" if status == "failed" else "⚠️"
                print(f"  {emoji} {test_type.replace('_', ' ').title()}: {status}")
            else:
                # Handle nested results (security tests)
                print(f"  🔒 {test_type.replace('_', ' ').title()}:")
                for sub_type, sub_result in result.items():
                    sub_status = sub_result.get("status", "unknown")
                    emoji = "✅" if sub_status == "passed" else "❌" if sub_status == "failed" else "⚠️"
                    print(f"    {emoji} {sub_type}: {sub_status}")

        print("=" * 60)

        return report["overall_score"] >= 75

    def run_all_tests(self) -> bool:
        """Run complete test suite."""
        print("🚀 Starting comprehensive test suite...")

        report = self.generate_test_report()
        self.save_report(report)
        return self.print_summary(report)


def main() -> None:
    """Main entry point."""
    manager = TestSafetyManager()

    if len(sys.argv) > 1 and sys.argv[1] == "--unit-only":
        # Run only unit tests
        result = manager.run_unit_tests()
        success = result.get("status") == "passed"
    else:
        # Run full test suite
        success = manager.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
