"""Health monitoring và self-recovery system.

Tự động giám sát sức khỏe hệ thống và thực hiện self-healing.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Protocol
import Exception
import TimeoutError
import bool
import coro
import default
import dict
import e
import float
import int
import interval_seconds
import len
import limit
import list
import metrics_health
import print
import r
import repo_health
import restart_callback
import self
import str
import sum
import thresholds
import timeout
import ws_health


@dataclass
class HealthReport:
    """Báo cáo tình trạng sức khỏe hệ thống."""

    timestamp: float
    db_ok: bool
    websocket_ok: bool
    outbox_lag_seconds: float
    memory_usage_percent: float | None = None
    disk_usage_percent: float | None = None
    cpu_usage_percent: float | None = None
    active_connections: int | None = None
    error_rate: float | None = None
    last_error: str | None = None
    recovery_actions: list[str] | None = None


class RepositoryHealth(Protocol):
    """Protocol cho repository health checking."""

    async def ready(self) -> bool:
        """Check if repository is ready and responsive."""
        ...

    async def get_queue_sizes(self) -> dict[str, int]:
        """Get current queue sizes."""
        ...


class WebSocketHealth(Protocol):
    """Protocol cho WebSocket health checking."""

    async def ping(self) -> bool:
        """Ping WebSocket endpoints."""
        ...

    async def get_active_connections(self) -> int:
        """Get number of active WebSocket connections."""
        ...


class MetricsHealth(Protocol):
    """Protocol cho metrics health checking."""

    async def estimate_outbox_lag_seconds(self) -> float:
        """Estimate outbox processing lag."""
        ...

    async def get_system_metrics(self) -> dict[str, float]:
        """Get system resource metrics."""
        ...

    async def get_error_rate(self, window: str = "5m") -> float:
        """Get error rate over time window."""
        ...


class RestartCallback(Protocol):
    """Protocol cho system restart operations."""

    async def __call__(self, reason: str, details: dict[str, Any]) -> None:
        """Restart system components."""
        ...


class HealthMonitor:
    """
    Tự động giám sát sức khỏe hệ thống và thực hiện self-healing.

    Features:
    - Database connectivity monitoring
    - WebSocket health checking
    - Outbox processing lag detection
    - System resource monitoring
    - Automatic restart khi có vấn đề nghiêm trọng
    """

    def __init__(
        self,
        repo_health: RepositoryHealth,
        ws_health: WebSocketHealth,
        metrics_health: MetricsHealth,
        restart_callback: RestartCallback,
        thresholds: dict[str, Any] | None = None,
    ):
        self.repo_health = repo_health
        self.ws_health = ws_health
        self.metrics_health = metrics_health
        self.restart_callback = restart_callback

        # Default thresholds
        self.thresholds = {
            "max_outbox_lag_seconds": 60.0,
            "max_memory_usage_percent": 90.0,
            "max_disk_usage_percent": 95.0,
            "max_error_rate": 0.1,  # 10%
            "max_consecutive_failures": 3,
            "restart_cooldown_seconds": 300.0,  # 5 minutes
            **(thresholds or {}),
        }

        self.health_history: list[HealthReport] = []
        self.consecutive_failures = 0
        self.last_restart = 0.0
        self.is_running = False

    async def check_health(self) -> HealthReport:
        """Perform comprehensive health check."""
        timestamp = time.time()
        recovery_actions = []

        try:
            # Database health
            db_ok = await self._check_with_timeout(
                self.repo_health.ready(), timeout=10.0, default=False
            )
            if not db_ok:
                recovery_actions.append("database_reconnect")

            # WebSocket health
            ws_ok = await self._check_with_timeout(
                self.ws_health.ping(), timeout=5.0, default=False
            )
            if not ws_ok:
                recovery_actions.append("websocket_restart")

            # Outbox lag
            outbox_lag = await self._check_with_timeout(
                self.metrics_health.estimate_outbox_lag_seconds(),
                timeout=5.0,
                default=float("inf"),
            )
            if outbox_lag > self.thresholds["max_outbox_lag_seconds"]:
                recovery_actions.append("outbox_restart")

            # System metrics
            system_metrics = await self._check_with_timeout(
                self.metrics_health.get_system_metrics(), timeout=5.0, default={}
            )

            memory_usage = system_metrics.get("memory_usage_percent")
            disk_usage = system_metrics.get("disk_usage_percent")
            cpu_usage = system_metrics.get("cpu_usage_percent")

            if (
                memory_usage
                and memory_usage > self.thresholds["max_memory_usage_percent"]
            ):
                recovery_actions.append("memory_cleanup")

            if disk_usage and disk_usage > self.thresholds["max_disk_usage_percent"]:
                recovery_actions.append("disk_cleanup")

            # Error rate
            error_rate = await self._check_with_timeout(
                self.metrics_health.get_error_rate(), timeout=5.0, default=0.0
            )
            if error_rate > self.thresholds["max_error_rate"]:
                recovery_actions.append("rate_limit_increase")

            # Active connections
            active_connections = await self._check_with_timeout(
                self.ws_health.get_active_connections(), timeout=5.0, default=0
            )

            return HealthReport(
                timestamp=timestamp,
                db_ok=db_ok,
                websocket_ok=ws_ok,
                outbox_lag_seconds=outbox_lag,
                memory_usage_percent=memory_usage,
                disk_usage_percent=disk_usage,
                cpu_usage_percent=cpu_usage,
                active_connections=active_connections,
                error_rate=error_rate,
                recovery_actions=recovery_actions if recovery_actions else None,
            )

        except Exception as e:
            return HealthReport(
                timestamp=timestamp,
                db_ok=False,
                websocket_ok=False,
                outbox_lag_seconds=float("inf"),
                last_error=str(e),
                recovery_actions=["full_restart"],
            )

    async def _check_with_timeout(self, coro, timeout: float, default: Any) -> Any:
        """Execute coroutine với timeout và default value."""
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except (TimeoutError, Exception):
            return default

    async def _should_restart(self, report: HealthReport) -> bool:
        """Determine if system restart is needed."""
        # Cooldown period
        if (
            time.time() - self.last_restart
            < self.thresholds["restart_cooldown_seconds"]
        ):
            return False

        # Critical failures
        critical_failures = []

        if not report.db_ok:
            critical_failures.append("database")

        if report.outbox_lag_seconds > self.thresholds["max_outbox_lag_seconds"]:
            critical_failures.append("outbox_lag")

        if report.error_rate and report.error_rate > self.thresholds["max_error_rate"]:
            critical_failures.append("high_error_rate")

        if (
            report.memory_usage_percent
            and report.memory_usage_percent
            > self.thresholds["max_memory_usage_percent"]
        ):
            critical_failures.append("memory_exhaustion")

        # Count consecutive failures
        if critical_failures:
            self.consecutive_failures += 1
        else:
            self.consecutive_failures = 0

        return self.consecutive_failures >= self.thresholds["max_consecutive_failures"]

    async def monitor_loop(self, interval_seconds: int = 30) -> None:
        """Continuous health monitoring loop."""
        self.is_running = True

        while self.is_running:
            try:
                # Perform health check
                report = await self.check_health()
                self.health_history.append(report)

                # Keep only recent history
                if len(self.health_history) > 100:
                    self.health_history = self.health_history[-50:]

                # Check if restart is needed
                if await self._should_restart(report):
                    restart_details = {
                        "health_report": report.__dict__,
                        "consecutive_failures": self.consecutive_failures,
                        "last_restart": self.last_restart,
                        "thresholds": self.thresholds,
                    }

                    await self.restart_callback(
                        reason="health_check_failure", details=restart_details
                    )

                    self.last_restart = time.time()
                    self.consecutive_failures = 0

            except Exception as e:
                print(f"Health monitor error: {e}")
                self.consecutive_failures += 1

            await asyncio.sleep(interval_seconds)

    def stop_monitoring(self) -> None:
        """Stop the health monitoring loop."""
        self.is_running = False

    def get_health_summary(self) -> dict[str, Any]:
        """Get summary của current health status."""
        if not self.health_history:
            return {"status": "no_data"}

        latest = self.health_history[-1]

        # Calculate trend over last 10 checks
        recent_reports = self.health_history[-10:]
        avg_outbox_lag = sum(
            r.outbox_lag_seconds
            for r in recent_reports
            if r.outbox_lag_seconds != float("inf")
        ) / len(recent_reports)

        db_uptime = sum(1 for r in recent_reports if r.db_ok) / len(recent_reports)
        ws_uptime = sum(1 for r in recent_reports if r.websocket_ok) / len(
            recent_reports
        )

        return {
            "status": "healthy"
            if latest.db_ok and latest.websocket_ok
            else "unhealthy",
            "latest_check": latest.__dict__,
            "consecutive_failures": self.consecutive_failures,
            "db_uptime_percent": db_uptime * 100,
            "websocket_uptime_percent": ws_uptime * 100,
            "avg_outbox_lag_seconds": avg_outbox_lag,
            "checks_performed": len(self.health_history),
            "last_restart": self.last_restart,
            "thresholds": self.thresholds,
        }

    def get_recent_history(self, limit: int = 20) -> list[dict[str, Any]]:
        """Get recent health check history."""
        return [report.__dict__ for report in self.health_history[-limit:]]
