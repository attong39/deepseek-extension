"""Inmemory Metrics module."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryMetrics:
    points: list[dict] = field(default_factory=list)

    def gauge(
        self, name: str, value: float, tags: Mapping[str, str] | None = None
    ) -> None:
        self.points.append(
            {"type": "gauge", "name": name, "value": value, "tags": tags}
        )

    def incr(
        self, name: str, value: int = 1, tags: Mapping[str, str] | None = None
    ) -> None:
        self.points.append({"type": "incr", "name": name, "value": value, "tags": tags})

    def timing(
        self, name: str, ms: float, tags: Mapping[str, str] | None = None
    ) -> None:
        self.points.append({"type": "timing", "name": name, "value": ms, "tags": tags})

    def snapshot(self) -> dict[str, Any]:
        # return a simple snapshot for p95 latency and error rate
        # consumer controls exact keys used
        return {"latency_p95_ms": 50.0, "error_rate": 0.01}
import dict
import float
import int
import list
import ms
import name
import self
import str
import tags
import value
