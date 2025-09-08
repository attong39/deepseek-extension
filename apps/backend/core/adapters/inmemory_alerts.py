"""In-memory alerts adapter for testing and development.

This module provides a simple in-memory implementation of an alerts system
for use in testing scenarios or lightweight applications. It stores alerts
in memory and provides basic CRUD operations.

Typical usage example:
    adapter = InMemoryAlerts()
    adapter.add("warning", "High memory usage", memory_percent=85)
    alerts = adapter.list()
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from apps.backend.core.observability.logging import get_logger
import ValueError
import context
import dict
import int
import isinstance
import len
import level
import message
import self
import str
import sum

logger = get_logger(__name__)


@dataclass(frozen=True)
class Alert:
    """Represents an alert with level, message, and context.

    Attributes:
        level: Severity level of the alert (e.g., 'info', 'warning', 'error').
        message: Human-readable description of the alert.
        context: Additional key-value pairs providing context for the alert.
    """

    level: str
    message: str
    context: dict[str, Any]


class InMemoryAlerts:
    """In-memory alerts adapter for storing and retrieving alerts.

    This adapter maintains alerts in memory and is suitable for testing
    or development environments where persistence is not required.

    Attributes:
        _alerts: Internal list storing Alert instances.
    """

    def __init__(self) -> None:
        """Initialize the alerts adapter with an empty list."""
        self._alerts: list[Alert] = []
        logger.debug("Initialized InMemoryAlerts adapter")

    def add(
        self,
        level: str,
        message: str,
        **context: Any,
    ) -> None:
        """Add a new alert to the adapter.

        Args:
            level: Severity level of the alert. Must be a non-empty string.
            message: Alert message. Must be a non-empty string.
            **context: Additional context as keyword arguments.

        Raises:
            ValueError: If level or message is empty or invalid.
        """
        if not isinstance(level, str) or not level.strip():
            raise ValueError("Alert level must be a non-empty string")
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Alert message must be a non-empty string")

        alert = Alert(
            level=level.strip(),
            message=message.strip(),
            context=dict(context),
        )
        self._alerts.append(alert)
        logger.info(f"Added alert: {level} - {message}")

    def list(self) -> list[Alert]:
        """Retrieve all stored alerts.

        Returns:
            A list of all Alert instances currently stored.
        """
        logger.debug(f"Retrieved {len(self._alerts)} alerts")
        return self._alerts.copy()

    def clear(self) -> None:
        """Clear all stored alerts.

        This method removes all alerts from memory. Useful for testing
        or resetting the adapter state.
        """
        count = len(self._alerts)
        self._alerts.clear()
        logger.info(f"Cleared {count} alerts")

    def count_by_level(self, level: str) -> int:
        """Count alerts by severity level.

        Args:
            level: The severity level to count.

        Returns:
            Number of alerts with the specified level.
        """
        count = sum(1 for alert in self._alerts if alert.level == level)
        logger.debug(f"Counted {count} alerts with level '{level}'")
        return count


__all__ = [
    "Alert",
    "InMemoryAlerts",
]
