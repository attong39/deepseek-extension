"""Ai Tester module."""

from __future__ import annotations

from typing import Any

from apps.backend.core.interfaces.metrics import MetricsCollector
from apps.backend.core.interfaces.testing import (
    QualityReporter,
    TestCaseGenerator,
    TestRunner,
)


class AIPoweredTester:
    def __init__(
        self,
        generator: TestCaseGenerator,
        runner: TestRunner,
        reporter: QualityReporter,
        metrics: MetricsCollector,
    ) -> None:
        self.generator = generator
        self.runner = runner
        self.reporter = reporter
        self.metrics = metrics

    def generate_and_run_tests(self) -> dict[str, Any]:
        cases = self.generator.generate()
        results = self.runner.run(cases)
        summary = self.reporter.report(results)
        self.metrics.incr("ai_tests.run", value=len(results))
        return summary
import dict
import generator
import len
import metrics
import reporter
import runner
import self
import str
