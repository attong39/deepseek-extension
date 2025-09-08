"""
Analytics Controller Module

Orchestrates analytics/metrics queries across services/adapters.
Framework-agnostic: usable by API, CLI, WS. No direct DB/HTTP calls.

Author: duy_bg_vn
"""

from __future__ import annotations

import logging
from typing import Any, Protocol
import Exception
import ValueError
import analytics
import dict
import exc
import isinstance
import period
import self
import str

# Use project logger (assumes project-wide logger config)
logger = logging.getLogger("zeta_vn.app.controllers.analytics")

class AnalyticsService(Protocol):
    """
    Protocol for analytics service.

    Defines the required interface for analytics services.
    """

    async def get_metrics(self, *, period: str) -> dict[str, Any]:
        """
        Get aggregated metrics for a given period.

        Args:
            period (str): Time period for metrics (e.g., '24h', '7d').

        Returns:
            Dict[str, Any]: Aggregated metrics data.

        Raises:
            Exception: For service errors.
        """
        ...


class AnalyticsController:
    """
    Controller for querying metrics/analytics aggregated by services.

    Typical wiring:
        svc = container.analytics_service()
        ctl = AnalyticsController(analytics=svc)
    """

    def __init__(self, analytics: AnalyticsService) -> None:
        """
        Initialize AnalyticsController.

        Args:
            analytics (AnalyticsService): Analytics service instance.

        Raises:
            ValueError: If analytics is not provided.
        """
        if analytics is None:
            logger.error("Analytics service must not be None.")
            raise ValueError("Analytics service must not be None.")
        self._analytics: AnalyticsService = analytics

    async def metrics(self, period: str = "24h") -> dict[str, Any]:
        """
        Query metrics for a given period.

        Args:
            period (str, optional): Time period for metrics. Defaults to "24h".

        Returns:
            Dict[str, Any]: Aggregated metrics data.

        Raises:
            ValueError: If period is invalid.
            Exception: For unexpected errors.
        """
        if not isinstance(period, str) or not period:
            logger.error("Invalid period: %r", period)
            raise ValueError("Period must be a non-empty string.")

        logger.debug("AnalyticsController.metrics period=%s", period)
        try:
            metrics = await self._analytics.get_metrics(period=period)
            logger.info("Metrics queried successfully for period=%s", period)
            return metrics
        except Exception as exc:
            logger.exception("Failed to query metrics: %s", exc)
            raise

# End of file
