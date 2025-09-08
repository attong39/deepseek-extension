# Author: Duy BG VN
# ZETA AI - Automated Testing Script

"""Comprehensive automated testing suite.

Provides automated testing capabilities including unit tests,
integration tests, performance tests, and security tests.
"""

import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class TestType(Enum):
    """Types of tests available."""

    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    SMOKE = "smoke"


class TestStatus(Enum):
    """Test execution status."""

    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TestResult:
    """Individual test result."""

    test_name: str
    test_type: TestType
    status: TestStatus
    duration_seconds: float
    start_time: datetime
    end_time: datetime | None = None

    # Test details
    assertions_count: int = 0
    failures_count: int = 0
    errors_count: int = 0

    # Output
    stdout: str | None = None
    stderr: str | None = None
    error_message: str | None = None

    # Coverage
    coverage_percent: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["test_type"] = self.test_type.value
        result["status"] = self.status.value
        result["start_time"] = self.start_time.isoformat()
        if self.end_time:
            result["end_time"] = self.end_time.isoformat()
        return result


@dataclass
class TestSuite:
    """Test suite configuration."""

    name: str
    test_type: TestType
    test_directory: str
    test_pattern: str = "test_*.py"

    # pytest configuration
    pytest_args: list[str] = None
    coverage_enabled: bool = True
    coverage_min_threshold: float = 80.0

    # Environment settings
    env_vars: dict[str, str] = None
    setup_commands: list[str] = None
    teardown_commands: list[str] = None

    # Timeout settings
    timeout_seconds: int = 300

    def __post_init__(self):
        """Initialize default values."""
        if self.pytest_args is None:
            self.pytest_args = ["-v", "--tb=short"]

        if self.env_vars is None:
            self.env_vars = {}

        if self.setup_commands is None:
            self.setup_commands = []

        if self.teardown_commands is None:
            self.teardown_commands = []


@dataclass
class TestReport:
    """Overall test execution report."""

    suite_name: str
    start_time: datetime
    end_time: datetime | None = None

    # Results
    results: list[TestResult] = None

    # Summary
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    error_tests: int = 0

    # Coverage
    overall_coverage: float | None = None

    # Performance
    total_duration: float = 0.0

    def __post_init__(self):
        """Initialize default values."""
        if self.results is None:
            self.results = []

    def calculate_summary(self) -> None:
        """Calculate test summary statistics."""
        self.total_tests = len(self.results)
        self.passed_tests = sum(1 for r in self.results if r.status == TestStatus.PASSED)
        self.failed_tests = sum(1 for r in self.results if r.status == TestStatus.FAILED)
        self.skipped_tests = sum(1 for r in self.results if r.status == TestStatus.SKIPPED)
        self.error_tests = sum(1 for r in self.results if r.status == TestStatus.ERROR)

        if self.end_time and self.start_time:
            self.total_duration = (self.end_time - self.start_time).total_seconds()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["start_time"] = self.start_time.isoformat()
        if self.end_time:
            result["end_time"] = self.end_time.isoformat()
        result["results"] = [r.to_dict() for r in self.results]
        return result


class TestRunner:
    """Automated test execution engine."""

    def __init__(self, project_root: str = "."):
        """Initialize test runner.

        Args:
            project_root: Root directory of the project
        """
        self.project_root = Path(project_root)
        self.test_results: list[TestReport] = []

        # Default test suites
        self.test_suites = {
            TestType.UNIT: TestSuite(
                name="Unit Tests",
                test_type=TestType.UNIT,
                test_directory="zeta_vn/tests/unit",
                pytest_args=[
                    "-v",
                    "--tb=short",
                    "--cov=zeta_vn",
                    "--cov-report=term-missing",
                ],
            ),
            TestType.INTEGRATION: TestSuite(
                name="Integration Tests",
                test_type=TestType.INTEGRATION,
                test_directory="zeta_vn/tests/integration",
                pytest_args=["-v", "--tb=short"],
            ),
            TestType.E2E: TestSuite(
                name="End-to-End Tests",
                test_type=TestType.E2E,
                test_directory="zeta_vn/tests/e2e",
                pytest_args=["-v", "--tb=short"],
                timeout_seconds=600,
            ),
            TestType.SMOKE: TestSuite(
                name="Smoke Tests",
                test_type=TestType.SMOKE,
                test_directory="zeta_vn/tests/smoke",
                pytest_args=["-v", "--tb=short", "-m", "smoke"],
            ),
        }

    def add_test_suite(self, test_suite: TestSuite) -> None:
        """Add a custom test suite.

        Args:
            test_suite: Test suite configuration
        """
        self.test_suites[test_suite.test_type] = test_suite
        logger.info(f"Added test suite: {test_suite.name}")

    async def setup_test_environment(self, test_suite: TestSuite) -> bool:
        """Setup test environment.

        Args:
            test_suite: Test suite to setup for

        Returns:
            True if setup successful
        """
        try:
            # Run setup commands
            for command in test_suite.setup_commands:
                logger.info(f"Running setup command: {command}")

                process = await asyncio.create_subprocess_shell(
                    command,
                    cwd=self.project_root,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                stdout, stderr = await process.communicate()

                if process.returncode != 0:
                    logger.error(f"Setup command failed: {command}")
                    logger.error(f"Error: {stderr.decode()}")
                    return False

            logger.info(f"Test environment setup completed for {test_suite.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to setup test environment: {e}")
            return False

    async def teardown_test_environment(self, test_suite: TestSuite) -> None:
        """Teardown test environment.

        Args:
            test_suite: Test suite to teardown
        """
        try:
            # Run teardown commands
            for command in test_suite.teardown_commands:
                logger.info(f"Running teardown command: {command}")

                process = await asyncio.create_subprocess_shell(
                    command,
                    cwd=self.project_root,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                await process.communicate()

            logger.info(f"Test environment teardown completed for {test_suite.name}")

        except Exception as e:
            logger.error(f"Failed to teardown test environment: {e}")

    async def run_pytest(self, test_suite: TestSuite) -> TestResult:
        """Run pytest for a test suite.

        Args:
            test_suite: Test suite to run

        Returns:
            Test execution result
        """
        start_time = datetime.now()

        # Prepare pytest command
        test_dir = self.project_root / test_suite.test_directory

        if not test_dir.exists():
            logger.warning(f"Test directory not found: {test_dir}")
            return TestResult(
                test_name=test_suite.name,
                test_type=test_suite.test_type,
                status=TestStatus.SKIPPED,
                duration_seconds=0.0,
                start_time=start_time,
                end_time=datetime.now(),
                error_message=f"Test directory not found: {test_dir}",
            )

        # Build pytest command
        cmd = ["python", "-m", "pytest"] + test_suite.pytest_args + [str(test_dir)]

        # Prepare environment
        env = os.environ.copy()
        env.update(test_suite.env_vars)
        env["PYTHONPATH"] = str(self.project_root)

        logger.info(f"Running: {' '.join(cmd)}")

        try:
            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *cmd,
                cwd=self.project_root,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=test_suite.timeout_seconds)
            except TimeoutError:
                process.kill()
                await process.wait()

                return TestResult(
                    test_name=test_suite.name,
                    test_type=test_suite.test_type,
                    status=TestStatus.ERROR,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                    start_time=start_time,
                    end_time=datetime.now(),
                    error_message=f"Test execution timed out after {test_suite.timeout_seconds} seconds",
                )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            stdout_str = stdout.decode("utf-8") if stdout else ""
            stderr_str = stderr.decode("utf-8") if stderr else ""

            # Parse pytest output for results
            passed_count, failed_count, skipped_count, error_count = self._parse_pytest_output(stdout_str)

            # Determine status
            if process.returncode == 0:
                status = TestStatus.PASSED
            elif failed_count > 0 or error_count > 0:
                status = TestStatus.FAILED
            else:
                status = TestStatus.ERROR

            # Extract coverage if available
            coverage_percent = self._extract_coverage(stdout_str)

            result = TestResult(
                test_name=test_suite.name,
                test_type=test_suite.test_type,
                status=status,
                duration_seconds=duration,
                start_time=start_time,
                end_time=end_time,
                assertions_count=passed_count + failed_count,
                failures_count=failed_count,
                errors_count=error_count,
                stdout=stdout_str,
                stderr=stderr_str,
                coverage_percent=coverage_percent,
            )

            logger.info(f"Test completed: {test_suite.name} - {status.value} ({duration:.2f}s)")
            return result

        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            return TestResult(
                test_name=test_suite.name,
                test_type=test_suite.test_type,
                status=TestStatus.ERROR,
                duration_seconds=duration,
                start_time=start_time,
                end_time=end_time,
                error_message=str(e),
            )

    def _parse_pytest_output(self, output: str) -> tuple[int, int, int, int]:
        """Parse pytest output to extract test counts.

        Args:
            output: Pytest stdout output

        Returns:
            Tuple of (passed, failed, skipped, errors)
        """
        passed = failed = skipped = errors = 0

        # Look for result summary line
        lines = output.split("\n")
        for line in lines:
            if "passed" in line or "failed" in line or "error" in line:
                # Parse patterns like "5 passed, 2 failed, 1 skipped"
                if "passed" in line:
                    try:
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part == "passed" and i > 0:
                                passed = int(parts[i - 1])
                            elif part == "failed" and i > 0:
                                failed = int(parts[i - 1])
                            elif part == "skipped" and i > 0:
                                skipped = int(parts[i - 1])
                            elif part == "error" and i > 0:
                                errors = int(parts[i - 1])
                    except (ValueError, IndexError):
                        continue

        return passed, failed, skipped, errors

    def _extract_coverage(self, output: str) -> float | None:
        """Extract coverage percentage from pytest output.

        Args:
            output: Pytest stdout output

        Returns:
            Coverage percentage or None
        """
        lines = output.split("\n")
        for line in lines:
            if "TOTAL" in line and "%" in line:
                # Look for coverage total line
                parts = line.split()
                for part in parts:
                    if part.endswith("%"):
                        try:
                            return float(part[:-1])
                        except ValueError:
                            continue

        return None

    async def run_performance_tests(self) -> TestResult:
        """Run performance tests using locust or similar.

        Returns:
            Performance test result
        """
        start_time = datetime.now()

        try:
            # Simple performance test using requests
            import httpx

            logger.info("Running performance tests...")

            # Test basic API endpoint performance
            url = "http://localhost:8000/api/v1/health"
            total_requests = 100
            successful_requests = 0
            response_times = []

            async with httpx.AsyncClient() as client:
                for i in range(total_requests):
                    try:
                        start = time.time()
                        response = await client.get(url, timeout=5.0)
                        end = time.time()

                        response_times.append(end - start)
                        if response.status_code == 200:
                            successful_requests += 1

                    except Exception:
                        continue

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Calculate performance metrics
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            success_rate = (successful_requests / total_requests) * 100

            # Determine status based on performance criteria
            if success_rate >= 95 and avg_response_time <= 1.0:
                status = TestStatus.PASSED
                message = f"Performance test passed: {success_rate:.1f}% success rate, {avg_response_time:.3f}s avg response time"
            else:
                status = TestStatus.FAILED
                message = f"Performance test failed: {success_rate:.1f}% success rate, {avg_response_time:.3f}s avg response time"

            return TestResult(
                test_name="Performance Tests",
                test_type=TestType.PERFORMANCE,
                status=status,
                duration_seconds=duration,
                start_time=start_time,
                end_time=end_time,
                assertions_count=total_requests,
                failures_count=total_requests - successful_requests,
                stdout=message,
            )

        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            return TestResult(
                test_name="Performance Tests",
                test_type=TestType.PERFORMANCE,
                status=TestStatus.ERROR,
                duration_seconds=duration,
                start_time=start_time,
                end_time=end_time,
                error_message=str(e),
            )

    async def run_security_tests(self) -> TestResult:
        """Run security tests using bandit or similar tools.

        Returns:
            Security test result
        """
        start_time = datetime.now()

        try:
            logger.info("Running security tests...")

            # Run bandit security scanner
            cmd = ["python", "-m", "bandit", "-r", "zeta_vn", "-f", "json"]

            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *cmd,
                cwd=self.project_root,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            stdout_str = stdout.decode("utf-8") if stdout else ""
            stderr_str = stderr.decode("utf-8") if stderr else ""

            # Parse bandit output
            try:
                if stdout_str:
                    bandit_results = json.loads(stdout_str)
                    issues_count = len(bandit_results.get("results", []))
                    high_severity_count = sum(
                        1 for issue in bandit_results.get("results", []) if issue.get("issue_severity") == "HIGH"
                    )

                    if high_severity_count > 0:
                        status = TestStatus.FAILED
                        message = f"Security test failed: {high_severity_count} high severity issues found"
                    elif issues_count > 0:
                        status = TestStatus.PASSED
                        message = f"Security test passed with warnings: {issues_count} low/medium issues found"
                    else:
                        status = TestStatus.PASSED
                        message = "Security test passed: No issues found"
                else:
                    status = TestStatus.PASSED
                    message = "Security test passed: No issues found"
                    issues_count = 0
                    high_severity_count = 0

            except json.JSONDecodeError:
                status = TestStatus.ERROR
                message = "Failed to parse security test results"
                issues_count = 0
                high_severity_count = 0

            return TestResult(
                test_name="Security Tests",
                test_type=TestType.SECURITY,
                status=status,
                duration_seconds=duration,
                start_time=start_time,
                end_time=end_time,
                assertions_count=1,
                failures_count=high_severity_count,
                stdout=message,
                stderr=stderr_str,
            )

        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            return TestResult(
                test_name="Security Tests",
                test_type=TestType.SECURITY,
                status=TestStatus.ERROR,
                duration_seconds=duration,
                start_time=start_time,
                end_time=end_time,
                error_message=str(e),
            )

    async def run_test_suite(self, test_type: TestType) -> TestReport:
        """Run a specific test suite.

        Args:
            test_type: Type of test to run

        Returns:
            Test execution report
        """
        if test_type not in self.test_suites:
            raise ValueError(f"Unknown test type: {test_type}")

        test_suite = self.test_suites[test_type]
        report = TestReport(suite_name=test_suite.name, start_time=datetime.now())

        logger.info(f"Starting test suite: {test_suite.name}")

        try:
            # Setup test environment
            if not await self.setup_test_environment(test_suite):
                report.end_time = datetime.now()
                report.results.append(
                    TestResult(
                        test_name=test_suite.name,
                        test_type=test_type,
                        status=TestStatus.ERROR,
                        duration_seconds=0.0,
                        start_time=report.start_time,
                        end_time=report.end_time,
                        error_message="Failed to setup test environment",
                    )
                )
                report.calculate_summary()
                return report

            # Run tests based on type
            if test_type == TestType.PERFORMANCE:
                result = await self.run_performance_tests()
            elif test_type == TestType.SECURITY:
                result = await self.run_security_tests()
            else:
                result = await self.run_pytest(test_suite)

            report.results.append(result)

        finally:
            # Teardown test environment
            await self.teardown_test_environment(test_suite)

            report.end_time = datetime.now()
            report.calculate_summary()

        logger.info(f"Test suite completed: {test_suite.name} - {report.passed_tests}/{report.total_tests} passed")
        return report

    async def run_all_tests(self, test_types: list[TestType] | None = None) -> list[TestReport]:
        """Run all or specified test suites.

        Args:
            test_types: Optional list of test types to run

        Returns:
            List of test reports
        """
        if test_types is None:
            test_types = list(self.test_suites.keys())

        reports = []

        for test_type in test_types:
            try:
                report = await self.run_test_suite(test_type)
                reports.append(report)
                self.test_results.append(report)
            except Exception as e:
                logger.error(f"Failed to run test suite {test_type}: {e}")

                # Create error report
                error_report = TestReport(
                    suite_name=f"{test_type.value} Tests",
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                )
                error_report.results.append(
                    TestResult(
                        test_name=f"{test_type.value} Tests",
                        test_type=test_type,
                        status=TestStatus.ERROR,
                        duration_seconds=0.0,
                        start_time=error_report.start_time,
                        error_message=str(e),
                    )
                )
                error_report.calculate_summary()
                reports.append(error_report)

        return reports

    async def generate_report(self, reports: list[TestReport], output_file: str | None = None) -> None:
        """Generate comprehensive test report.

        Args:
            reports: List of test reports
            output_file: Optional output file path
        """
        try:
            # Calculate overall statistics
            total_tests = sum(report.total_tests for report in reports)
            total_passed = sum(report.passed_tests for report in reports)
            total_failed = sum(report.failed_tests for report in reports)
            total_errors = sum(report.error_tests for report in reports)
            total_skipped = sum(report.skipped_tests for report in reports)

            overall_duration = sum(report.total_duration for report in reports)

            # Create report data
            report_data = {
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_suites": len(reports),
                    "total_tests": total_tests,
                    "passed_tests": total_passed,
                    "failed_tests": total_failed,
                    "error_tests": total_errors,
                    "skipped_tests": total_skipped,
                    "success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
                    "total_duration_seconds": overall_duration,
                },
                "suites": [report.to_dict() for report in reports],
            }

            # Write to file
            if output_file is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                reports_dir = Path("storage/reports")
                reports_dir.mkdir(parents=True, exist_ok=True)
                output_file = reports_dir / f"test_report_{timestamp}.json"

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2)

            logger.info(f"Test report generated: {output_file}")

            # Print summary
            print(f"\n{'=' * 60}")
            print("TEST EXECUTION SUMMARY")
            print(f"{'=' * 60}")
            print(f"Total Suites: {len(reports)}")
            print(f"Total Tests: {total_tests}")
            print(f"Passed: {total_passed}")
            print(f"Failed: {total_failed}")
            print(f"Errors: {total_errors}")
            print(f"Skipped: {total_skipped}")
            print(f"Success Rate: {(total_passed / total_tests * 100):.1f}%" if total_tests > 0 else "N/A")
            print(f"Total Duration: {overall_duration:.2f}s")
            print(f"Report File: {output_file}")
            print(f"{'=' * 60}")

        except Exception as e:
            logger.error(f"Failed to generate test report: {e}")


async def main():
    """Main function for running automated tests."""
    import argparse

    parser = argparse.ArgumentParser(description="ZETA AI Automated Testing Suite")
    parser.add_argument(
        "--types",
        nargs="+",
        choices=["unit", "integration", "e2e", "performance", "security", "smoke"],
        help="Test types to run",
    )
    parser.add_argument("--output", help="Output file for test report")
    parser.add_argument("--project-root", default=".", help="Project root directory")

    args = parser.parse_args()

    # Create test runner
    runner = TestRunner(args.project_root)

    # Determine test types to run
    if args.types:
        test_types = [TestType(t) for t in args.types]
    else:
        test_types = [TestType.UNIT, TestType.INTEGRATION, TestType.SMOKE]

    logger.info(f"Running test types: {[t.value for t in test_types]}")

    try:
        # Run tests
        reports = await runner.run_all_tests(test_types)

        # Generate report
        await runner.generate_report(reports, args.output)

        # Determine exit code
        total_failed = sum(report.failed_tests + report.error_tests for report in reports)
        return 0 if total_failed == 0 else 1

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
