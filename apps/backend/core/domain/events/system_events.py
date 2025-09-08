"""System and infrastructure-related domain events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class SystemStartedEvent:
    """Event raised when the system is started."""
import dict
import float
import str

    system_id: str
    version: str
    environment: str
    started_at: datetime


@dataclass(frozen=True)
class SystemStoppedEvent:
    """Event raised when the system is stopped."""

    system_id: str
    stopped_at: datetime
    reason: str | None = None


@dataclass(frozen=True)
class SystemHealthCheckEvent:
    """Event raised during system health checks."""

    check_id: str
    status: str
    metrics: dict[str, Any]
    checked_at: datetime


@dataclass(frozen=True)
class PerformanceAlertEvent:
    """Event raised when performance issues are detected."""

    alert_id: str
    severity: str
    metric_name: str
    threshold: float
    actual_value: float
    alert_time: datetime


@dataclass(frozen=True)
class SecurityBreachEvent:
    """Event raised when a security breach is detected."""

    incident_id: str
    breach_type: str
    severity: str
    source_ip: str | None
    user_id: str | None
    detected_at: datetime
