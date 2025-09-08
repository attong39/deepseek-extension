"""AI-Powered Testing and Quality Validation.

Tự động generate test cases, run tests và analyze quality metrics.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.testing import (
import Exception
import dict
import e
import historical_results
import int
import len
import list
import max
import max_iterations
import min
import r
import result
import round
import self
import str
import sum
    QualityReporter,
    TestCaseGenerator,
    TestRunner,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class AIPoweredTester:
    """AI-powered automated tester với intelligent test generation."""

    generator: TestCaseGenerator
    runner: TestRunner
    reporter: QualityReporter

    def generate_and_run_tests(self) -> dict[str, Any]:
        """Generate test cases và run comprehensive testing."""
        try:
            logger.info("Starting AI-powered test generation and execution")

            # Generate intelligent test cases
            logger.debug("Generating test cases...")
            cases = self.generator.generate()
            logger.info(f"Generated {len(cases)} test cases")

            if not cases:
                logger.warning("No test cases generated")
                return {
                    "status": "no_tests",
                    "cases": 0,
                    "summary": {"error": "No test cases generated"},
                }

            # Execute test cases
            logger.debug("Running test cases...")
            results = self.runner.run(cases)
            logger.info(f"Executed {len(results)} test cases")

            # Generate quality report
            logger.debug("Generating quality report...")
            summary = self.reporter.report(results)
            logger.info("Quality analysis complete")

            # Calculate test metrics
            passed_tests = sum(1 for r in results if r.get("status") == "passed")
            failed_tests = sum(1 for r in results if r.get("status") == "failed")
            pass_rate = (passed_tests / len(results)) * 100 if results else 0

            logger.info(
                f"Test execution summary: {passed_tests} passed, {failed_tests} failed ({pass_rate:.1f}% pass rate)"
            )

            return {
                "status": "completed",
                "cases": len(cases),
                "results": {
                    "total": len(results),
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "pass_rate_percent": round(pass_rate, 2),
                },
                "summary": summary,
                "quality_metrics": self._extract_quality_metrics(summary),
            }

        except Exception as e:
            logger.error(f"Error in test generation and execution: {e}")
            return {"status": "error", "error": str(e), "cases": 0}

    def _extract_quality_metrics(self, summary: dict) -> dict[str, Any]:
        """Extract key quality metrics from test summary."""
        try:
            return {
                "coverage_percent": summary.get("coverage", 0),
                "code_quality_score": summary.get("quality_score", 0),
                "security_issues": summary.get("security_issues", 0),
                "performance_score": summary.get("performance_score", 0),
                "maintainability_index": summary.get("maintainability", 0),
            }
        except Exception as e:
            logger.error(f"Error extracting quality metrics: {e}")
            return {}

    def run_continuous_testing(self, max_iterations: int = 5) -> dict[str, Any]:
        """Run continuous testing with iterative improvements."""
        logger.info(
            f"Starting continuous testing cycle (max {max_iterations} iterations)"
        )

        all_results = []
        iteration = 0

        try:
            while iteration < max_iterations:
                iteration += 1
                logger.info(f"Running testing iteration {iteration}/{max_iterations}")

                _ = self.generate_and_run_tests()
                all_results.append({"iteration": iteration, "result": result})

                # Check if quality is sufficient to stop early
                if result.get("status") == "completed":
                    pass_rate = result.get("results", {}).get("pass_rate_percent", 0)
                    if pass_rate >= 95.0:  # High pass rate threshold
                        logger.info(
                            f"Early termination: achieved {pass_rate}% pass rate"
                        )
                        break

                logger.debug(f"Iteration {iteration} complete")

            # Aggregate results
            total_cases = sum(r["result"].get("cases", 0) for r in all_results)
            avg_pass_rate = (
                sum(
                    r["result"].get("results", {}).get("pass_rate_percent", 0)
                    for r in all_results
                    if r["result"].get("status") == "completed"
                )
                / len(
                    [r for r in all_results if r["result"].get("status") == "completed"]
                )
                if all_results
                else 0
            )

            logger.info(
                f"Continuous testing complete: {iteration} iterations, {total_cases} total cases, {avg_pass_rate:.1f}%% avg pass rate"
            )

            return {
                "status": "completed",
                "iterations": iteration,
                "total_cases": total_cases,
                "average_pass_rate": round(avg_pass_rate, 2),
                "detailed_results": all_results,
            }

        except Exception as e:
            logger.error(f"Error in continuous testing: {e}")
            return {
                "status": "error",
                "error": str(e),
                "iterations": iteration,
                "partial_results": all_results,
            }

    def analyze_test_trends(self, historical_results: list[dict]) -> dict[str, Any]:
        """Analyze testing trends over time."""
        try:
            if not historical_results:
                return {"status": "no_data"}

            logger.debug(
                f"Analyzing trends from {len(historical_results)} historical results"
            )

            # Extract pass rates over time
            pass_rates = []
            for result in historical_results:
                if result.get("status") == "completed":
                    pass_rate = result.get("results", {}).get("pass_rate_percent", 0)
                    pass_rates.append(pass_rate)

            if not pass_rates:
                return {"status": "no_valid_data"}

            # Calculate trend metrics
            avg_pass_rate = sum(pass_rates) / len(pass_rates)
            min_pass_rate = min(pass_rates)
            max_pass_rate = max(pass_rates)

            # Simple trend calculation (last 3 vs first 3)
            trend = "stable"
            if len(pass_rates) >= 6:
                recent_avg = sum(pass_rates[-3:]) / 3
                early_avg = sum(pass_rates[:3]) / 3
                if recent_avg > early_avg + 5:
                    trend = "improving"
                elif recent_avg < early_avg - 5:
                    trend = "declining"

            logger.info(
                f"Trend analysis: {trend} trend, {avg_pass_rate:.1f}%% avg pass rate"
            )

            return {
                "status": "analyzed",
                "trend": trend,
                "metrics": {
                    "average_pass_rate": round(avg_pass_rate, 2),
                    "min_pass_rate": round(min_pass_rate, 2),
                    "max_pass_rate": round(max_pass_rate, 2),
                    "total_samples": len(pass_rates),
                },
            }

        except Exception as e:
            logger.error(f"Error analyzing test trends: {e}")
            return {"status": "error", "error": str(e)}

    def get_testing_status(self) -> dict[str, Any]:
        """Get current testing system status."""
        try:
            return {
                "generator_ready": self.generator is not None,
                "runner_ready": self.runner is not None,
                "reporter_ready": self.reporter is not None,
                "system_status": "operational",
                "capabilities": [
                    "ai_test_generation",
                    "automated_execution",
                    "quality_analysis",
                    "continuous_testing",
                    "trend_analysis",
                ],
            }
        except Exception as e:
            logger.error(f"Error getting testing status: {e}")
            return {"status": "error", "error": str(e)}
