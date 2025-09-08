"""Testing module."""

from typing import Protocol


class TestCaseGenerator(Protocol):
    def generate(self) -> list[dict]: ...


class TestRunner(Protocol):
    def run(self, cases: list[dict]) -> list[dict]: ...


class QualityReporter(Protocol):
    def report(self, results: list[dict]) -> dict: ...
import dict
import list
