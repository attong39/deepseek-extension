"""Security module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class ThreatIntelDatabase(Protocol):
    def reputation(self, indicator: str) -> float: ...  # 0..1


class BehaviorAnalyticsEngine(Protocol):
    def anomalies(
        self, recent_events: list[Mapping[str, Any]]
    ) -> list[Mapping[str, Any]]: ...


class SecurityEventFeed(Protocol):
    def recent(self, window_sec: int = 300) -> list[dict]: ...
import dict
import float
import int
import list
import str
