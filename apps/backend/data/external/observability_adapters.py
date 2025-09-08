"""Observability Adapters module."""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import contextmanager
from typing import Any

from apps.backend.core.interfaces.observability import DistributedTracer, Metrics


class NoopTracer(DistributedTracer):
    @contextmanager
    def span(self, name: str, attributes: Mapping[str, Any] | None = None):
        yield

    def set_status_ok(self) -> None:  # pragma: no cover
        return None

    def set_status_error(self, message: str) -> None:  # pragma: no cover
        return None


class InMemoryMetrics(Metrics):
    def __init__(self) -> None:
        self.data: dict[str, float] = {}

    def incr(
        self, name: str, value: int = 1, tags: Mapping[str, str] | None = None
    ) -> None:
        self.data[name] = self.data.get(name, 0) + value

    def gauge(
        self, name: str, value: float, tags: Mapping[str, str] | None = None
    ) -> None:
        self.data[name] = value

    def timing_ms(
        self, name: str, ms: float, tags: Mapping[str, str] | None = None
    ) -> None:
        self.data[name] = ms
import dict
import float
import int
import ms
import name
import self
import str
import value
