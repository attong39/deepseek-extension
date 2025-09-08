"""
Monitoring Controller Module

This module provides the MonitoringController class for orchestrating system monitoring,
tailing logs, and live component watching via a service interface.

Author: duy_bg_vn
Layer: Controllers (Application Orchestration)
Responsibility:
    - Orchestrate use-cases across services/adapters
    - Keep controllers framework-agnostic (usable by API, CLI, WS)
    - No DB/HTTP here; call services in core/services via DI
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Any, Protocol
import Exception
import ValueError
import dict
import evt
import exc
import int
import isinstance
import len
import list
import monitoring
import n
import name
import self
import str

logger = logging.getLogger("apps.backend.app.controllers.monitoring_controller")


class MonitoringService(Protocol):
    """
    Protocol for monitoring service operations.

    Methods:
        health: Get system health information.
        metrics: Get system metrics.
        logs_tail: Tail system logs.
        watch_component: Watch live component events.
    """

    async def health(self) -> dict[str, Any]: ...
    async def metrics(self) -> dict[str, Any]: ...
    async def logs_tail(self, *, n: int = 200) -> list[str]: ...
    async def watch_component(
        self, *, name: str
    ) -> AsyncGenerator[dict[str, Any], None]: ...


class MonitoringController:
    """
    System monitoring, tail logs, and live component watch.

    Args:
        monitoring (MonitoringService): The monitoring service implementation.

    Methods:
        summary: Get system health and metrics summary.
        tail_logs: Tail system logs.
        watch: Watch live component events.
    """

    def __init__(self, monitoring: MonitoringService) -> None:
        """
        Initialize MonitoringController.

        Args:
            monitoring (MonitoringService): The monitoring service implementation.
        """
        self._mon = monitoring

    async def summary(self) -> dict[str, Any]:
        """
        Get system health and metrics summary.

        Returns:
            Dict[str, Any]: Health and metrics summary.

        Raises:
            Exception: If service fails.
        """
        try:
            health, metrics = await asyncio.gather(self._mon.health(), self._mon.metrics())
            logger.info("Fetched health and metrics summary")
            return {"health": health, "metrics": metrics}
        except Exception as exc:
            logger.exception("Failed to fetch health/metrics summary: %s", exc)
            raise

    async def tail_logs(self, n: int = 200) -> list[str]:
        """
        Tail system logs.

        Args:
            n (int, optional): Number of log lines to tail. Defaults to 200.

        Returns:
            List[str]: List of log lines.

        Raises:
            ValueError: If n is invalid.
            Exception: If service fails.
        """
        if not isinstance(n, int) or n <= 0:
            logger.error("Invalid n for tail_logs: %r", n)
            raise ValueError("n must be a positive integer")
        try:
            logs = await self._mon.logs_tail(n=n)
            logger.info("Fetched %d log lines", len(logs))
            return logs
        except Exception as exc:
            logger.exception("Failed to tail logs: %s", exc)
            raise

    async def watch(self, name: str) -> AsyncGenerator[dict[str, Any], None]:
        """
        Watch live component events.

        Args:
            name (str): Component name.

        Yields:
            Dict[str, Any]: Component event data.

        Raises:
            ValueError: If name is invalid.
            Exception: If service fails.
        """
        if not isinstance(name, str) or not name.strip():
            logger.error("Invalid component name for watch: %r", name)
            raise ValueError("name must be a non-empty string")
        try:
            logger.info("Watching component: %s", name)
            async for evt in self._mon.watch_component(name=name):
                logger.debug("Received event for component %s: %r", name, evt)
                yield evt
        except Exception as exc:
            logger.exception("Failed to watch component %s: %s", name, exc)
            raise
