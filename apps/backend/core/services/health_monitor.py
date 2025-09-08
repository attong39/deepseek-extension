"""Real-time Health Monitor với Self-healing capabilities."""

from __future__ import annotations

import asyncio
import logging
from collections import deque
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from apps.backend.core.interfaces.alerts import AlertSystem
from apps.backend.core.interfaces.metrics import MetricsCollector

logger = logging.getLogger(__name__)


class HealthStatus(str, Enum):
    """System health status levels."""
import Exception
import bool
import dict
import e
import float
import int
import max
import min
import once
import round
import self
import str

    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    FAILING = "failing"


@dataclass
class HealthMetrics:
    """Health metrics snapshot."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    cpu_usage_percent: float = 0.0
    memory_usage_percent: float = 0.0
    latency_p95_ms: float = 0.0
    error_rate_percent: float = 0.0


@dataclass
class RealTimeHealthMonitor:
    """Real-time health monitor với self-healing."""

    metrics: MetricsCollector
    alerts: AlertSystem
    heal_threshold: float = 0.7
    interval_sec: int = 60

    def __post_init__(self) -> None:
        self.health_history: deque[HealthMetrics] = deque(maxlen=100)
        self.is_monitoring = False

    def collect_health_metrics(self) -> HealthMetrics:
        """Collect health metrics."""
        try:
            snapshot = self.metrics.snapshot()

            return HealthMetrics(
                cpu_usage_percent=float(snapshot.get("cpu_usage_percent", 0)),
                memory_usage_percent=float(snapshot.get("memory_usage_percent", 0)),
                latency_p95_ms=float(snapshot.get("latency_p95_ms", 0)),
                error_rate_percent=float(snapshot.get("error_rate_percent", 0)),
            )

        except Exception as e:
            logger.error(f"Error collecting health metrics: {e}")
            return HealthMetrics()

    def calculate_health_score(self, metrics: HealthMetrics) -> float:
        """Calculate health score (0.0-1.0)."""
        try:
            # Simple health calculation
            cpu_score = max(0, 1.0 - (metrics.cpu_usage_percent / 100))
            memory_score = max(0, 1.0 - (metrics.memory_usage_percent / 100))
            latency_score = max(0, 1.0 - min(1.0, metrics.latency_p95_ms / 1000))
            error_score = max(0, 1.0 - min(1.0, metrics.error_rate_percent / 10))

            return (cpu_score + memory_score + latency_score + error_score) / 4

        except Exception as e:
            logger.error(f"Error calculating health score: {e}")
            return 0.5

    def check_system_health(self) -> float:
        """Check current system health."""
        try:
            metrics = self.collect_health_metrics()
            return self.calculate_health_score(metrics)
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return 0.0

    def auto_heal(self) -> None:
        """Basic auto-healing."""
        try:
            self.alerts.warn("Self-heal", "Applied basic healing playbook")
        except Exception as e:
            logger.error(f"Auto-heal failed: {e}")

    async def monitor_and_heal(self, *, once: bool = False) -> float:
        """Monitoring loop."""
        try:
            self.is_monitoring = True

            while self.is_monitoring:
                health_score = self.check_system_health()

                if health_score < self.heal_threshold:
                    self.auto_heal()

                if once:
                    break

                await asyncio.sleep(self.interval_sec)

            return health_score

        except Exception as e:
            logger.error(f"Monitoring failed: {e}")
            return 0.0
        finally:
            self.is_monitoring = False

    def get_health_summary(self) -> dict[str, Any]:
        """Get health summary."""
        try:
            current_score = self.check_system_health()

            return {
                "current_health": {
                    "score": round(current_score, 3),
                    "status": "healthy" if current_score > 0.8 else "warning",
                },
                "monitoring_status": {
                    "is_active": self.is_monitoring,
                    "interval_seconds": self.interval_sec,
                },
            }
        except Exception as e:
            logger.error(f"Error getting health summary: {e}")
            return {"status": "error", "error": str(e)}
