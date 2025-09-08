"""Metrics module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class MetricsCollector(Protocol):
    def gauge(
        self, name: str, value: float, tags: Mapping[str, str] | None = None
    ) -> None: ...

    def incr(
        self, name: str, value: int = 1, tags: Mapping[str, str] | None = None
    ) -> None: ...

    def timing(
        self, name: str, ms: float, tags: Mapping[str, str] | None = None
    ) -> None: ...

    def snapshot(self) -> dict[str, Any]: ...


class BottleneckDetector(Protocol):
    def detect(
        self, metrics: Mapping[str, Any]
    ) -> list[str]: ...  # ["cpu","memory","network"]
import dict
import float
import int
import list
import str
