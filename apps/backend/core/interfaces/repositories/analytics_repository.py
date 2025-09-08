"""Analytics repository interface.

Repository interface cho analytics domain theo Clean Architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import dict
import list
import str


class AnalyticsRepository(ABC):
    """Repository interface cho analytics operations."""

    @abstractmethod
    async def record_event(self, event_type: str, data: dict[str, Any]) -> str:
        """Record an analytics event."""
        ...

    @abstractmethod
    async def get_metrics(
        self,
        metric_name: str,
        start_date: Any | None = None,
        end_date: Any | None = None,
    ) -> list[dict[str, Any]]:
        """Get metrics data for a specific metric."""
        ...

    @abstractmethod
    async def aggregate_data(
        self, aggregation_type: str, filters: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Aggregate analytics data."""
        ...


__all__ = ["AnalyticsRepository"]
