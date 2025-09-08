"""


Enhanced Performance Monitoring Middleware





Provides comprehensive performance tracking including:


- Request timing and throughput metrics


- Database query performance monitoring


- Memory and CPU usage tracking


- Cache performance metrics


- Error rate monitoring


- Real-time performance alerts


"""

from __future__ import annotations

import logging
import os
import time
from collections import defaultdict, deque
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
import Exception
import ImportError
import alert_thresholds
import app
import bool
import call_next
import dict
import e
import endpoint
import float
import getattr
import globals
import hasattr
import hash
import hit
import int
import key
import len
import list
import m
import max
import min
import operation
import operation_name
import query
import request
import row_count
import self
import sorted
import str
import sum
import super
import times
import window_minutes

try:
    import psutil

    HAS_PSUTIL = True


except ImportError:
    HAS_PSUTIL = False


from fastapi import APIRouter, FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)
_NOT_ATTACHED = "performance middleware not attached"


@dataclass
class RequestMetrics:
    """Individual request performance metrics."""

    timestamp: datetime

    method: str

    endpoint: str

    status_code: int

    duration_ms: float

    memory_mb: float

    cpu_percent: float

    request_size_kb: float

    response_size_kb: float

    user_id: str | None = None

    error_message: str | None = None


@dataclass
class PerformanceStats:
    """Aggregated performance statistics."""

    total_requests: int = 0

    successful_requests: int = 0

    failed_requests: int = 0

    average_response_time: float = 0.0

    p95_response_time: float = 0.0

    p99_response_time: float = 0.0

    requests_per_second: float = 0.0

    error_rate: float = 0.0

    average_memory_mb: float = 0.0

    average_cpu_percent: float = 0.0

    peak_memory_mb: float = 0.0

    peak_cpu_percent: float = 0.0

    active_connections: int = 0

    cache_hit_rate: float = 0.0

    database_query_time: float = 0.0


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Enhanced performance monitoring middleware."""

    def __init__(
        self, app: Any, alert_thresholds: dict[str, float] | None = None
    ) -> None:
        """Initialize performance monitoring middleware.





        import re  # noqa: PLC0415


            app: FastAPI application


            alert_thresholds: Performance alert thresholds


        """

        super().__init__(app)

        # Default alert thresholds

        self.alert_thresholds = alert_thresholds or {
            "response_time_ms": 1000.0,  # Alert if response time > 1s
            "error_rate_percent": 5.0,  # Alert if error rate > 5%
            "memory_mb": 1024.0,  # Alert if memory usage > 1GB
            "cpu_percent": 80.0,  # Alert if CPU usage > 80%
        }

        # Metrics storage (using deque for efficient rotation)

        self.request_metrics: deque[RequestMetrics] = deque(maxlen=10000)

        self.endpoint_stats: defaultdict[str, list[float]] = defaultdict(list)

        # Real-time tracking

        self.active_requests = 0

        self.start_time = datetime.now()

        self.last_alert_times: defaultdict[str, datetime] = defaultdict(
            lambda: datetime.min
        )

        # Performance counters

        self.total_requests = 0

        self.total_errors = 0

        # Memory baseline

        self.process = psutil.Process()

        self.baseline_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        logger.info("Performance monitoring middleware initialized")

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request with comprehensive performance monitoring."""

        request_start = time.perf_counter()

        # Track active requests

        self.active_requests += 1

        self.total_requests += 1

        # Get request size

        content_length = request.headers.get("content-length", "0")

        request_size_kb = (
            float(content_length) / 1024 if content_length.isdigit() else 0.0
        )

        # Extract user info if available

        user_id = getattr(request.state, "user_id", None)

        try:
            # Process request

            response = await call_next(request)

            # Calculate metrics

            duration = time.perf_counter() - request_start

            duration_ms = duration * 1000

            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB

            end_cpu = self.process.cpu_percent()

            # Get response size

            response_size_kb = 0.0

            if hasattr(response, "headers") and "content-length" in response.headers:
                response_size_kb = float(response.headers["content-length"]) / 1024

            # Create metrics record

            metrics = RequestMetrics(
                timestamp=datetime.now(),
                method=request.method,
                endpoint=self._normalize_endpoint(request.url.path),
                status_code=response.status_code,
                duration_ms=duration_ms,
                memory_mb=end_memory,
                cpu_percent=end_cpu,
                request_size_kb=request_size_kb,
                response_size_kb=response_size_kb,
                user_id=user_id,
            )

            # Store metrics

            self._store_metrics(metrics)

            # Check for performance alerts

            await self._check_alerts(metrics)

            # Add performance headers

            response.headers["X-Response-Time"] = f"{duration:.3f}s"

            response.headers["X-Memory-Usage"] = f"{end_memory:.1f}MB"

            response.headers["X-Request-Count"] = str(self.total_requests)

            return response

        except Exception as e:
            # Track error

            self.total_errors += 1

            duration = time.perf_counter() - request_start

            duration_ms = duration * 1000

            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB

            end_cpu = self.process.cpu_percent()

            # Create error metrics record

            metrics = RequestMetrics(
                timestamp=datetime.now(),
                method=request.method,
                endpoint=self._normalize_endpoint(request.url.path),
                status_code=500,
                duration_ms=duration_ms,
                memory_mb=end_memory,
                cpu_percent=end_cpu,
                request_size_kb=request_size_kb,
                response_size_kb=0.0,
                user_id=user_id,
                error_message=str(e),
            )

            # Store error metrics

            self._store_metrics(metrics)

            logger.error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    "duration_ms": duration_ms,
                    "memory_mb": end_memory,
                    "error": str(e),
                },
                exc_info=True,
            )

            raise

        finally:
            self.active_requests -= 1

    def _normalize_endpoint(self, path: str) -> str:
        """Normalize endpoint path for metrics grouping."""
        # Replace UUIDs and IDs with placeholders
        import re  # noqa: PLC0415

        # Replace UUIDs
        path = re.sub(
            r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "/{uuid}",
            path,
        )

        # Replace numeric IDs
        path = re.sub(r"/\d+", "/{id}", path)

        return path

    def _store_metrics(self, metrics: RequestMetrics) -> None:
        """Store metrics for analysis."""

        self.request_metrics.append(metrics)

        # Store endpoint-specific timing for percentile calculations

        self.endpoint_stats[metrics.endpoint].append(metrics.duration_ms)

        # Keep only recent endpoint stats (last 1000 requests per endpoint)

        if len(self.endpoint_stats[metrics.endpoint]) > 1000:
            self.endpoint_stats[metrics.endpoint] = self.endpoint_stats[
                metrics.endpoint
            ][-1000:]

    async def _check_alerts(self, metrics: RequestMetrics) -> None:
        """Check for performance alerts."""

        now = datetime.now()

        alert_cooldown = timedelta(minutes=5)  # Don't spam alerts

        # Response time alert

        if (
            metrics.duration_ms > self.alert_thresholds["response_time_ms"]
            and now - self.last_alert_times["response_time"] > alert_cooldown
        ):
            logger.warning(
                "PERFORMANCE ALERT: Slow response time detected",
                extra={
                    "endpoint": metrics.endpoint,
                    "duration_ms": metrics.duration_ms,
                    "threshold_ms": self.alert_thresholds["response_time_ms"],
                },
            )

            self.last_alert_times["response_time"] = now

        # Memory usage alert

        if (
            metrics.memory_mb > self.alert_thresholds["memory_mb"]
            and now - self.last_alert_times["memory"] > alert_cooldown
        ):
            logger.warning(
                "PERFORMANCE ALERT: High memory usage detected",
                extra={
                    "memory_mb": metrics.memory_mb,
                    "threshold_mb": self.alert_thresholds["memory_mb"],
                    "baseline_mb": self.baseline_memory,
                },
            )

            self.last_alert_times["memory"] = now

        # CPU usage alert

        if (
            metrics.cpu_percent > self.alert_thresholds["cpu_percent"]
            and now - self.last_alert_times["cpu"] > alert_cooldown
        ):
            logger.warning(
                "PERFORMANCE ALERT: High CPU usage detected",
                extra={
                    "cpu_percent": metrics.cpu_percent,
                    "threshold_percent": self.alert_thresholds["cpu_percent"],
                },
            )

            self.last_alert_times["cpu"] = now

        # Error rate alert

        error_rate = (self.total_errors / self.total_requests) * 100

        if (
            error_rate > self.alert_thresholds["error_rate_percent"]
            and now - self.last_alert_times["error_rate"] > alert_cooldown
        ):
            logger.warning(
                "PERFORMANCE ALERT: High error rate detected",
                extra={
                    "error_rate_percent": error_rate,
                    "threshold_percent": self.alert_thresholds["error_rate_percent"],
                    "total_errors": self.total_errors,
                    "total_requests": self.total_requests,
                },
            )

            self.last_alert_times["error_rate"] = now

    def get_performance_stats(self, window_minutes: int = 5) -> PerformanceStats:
        """Get aggregated performance statistics.





        Args:


            window_minutes: Time window for statistics calculation





        Returns:


            Aggregated performance statistics


        """

        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)

        recent_metrics = [m for m in self.request_metrics if m.timestamp >= cutoff_time]

        if not recent_metrics:
            return PerformanceStats()

        # Calculate basic stats

        total_requests = len(recent_metrics)

        successful_requests = sum(
            1 for m in recent_metrics if 200 <= m.status_code < 400
        )

        failed_requests = total_requests - successful_requests

        # Response time statistics

        response_times = [m.duration_ms for m in recent_metrics]

        avg_response_time = sum(response_times) / len(response_times)

        # Calculate percentiles

        sorted_times = sorted(response_times)

        p95_index = int(len(sorted_times) * 0.95)

        p99_index = int(len(sorted_times) * 0.99)

        p95_response_time = sorted_times[p95_index] if sorted_times else 0.0

        p99_response_time = sorted_times[p99_index] if sorted_times else 0.0

        # Requests per second

        time_span = window_minutes * 60

        requests_per_second = total_requests / time_span if time_span > 0 else 0.0

        # Error rate

        error_rate = (
            (failed_requests / total_requests) * 100 if total_requests > 0 else 0.0
        )

        # Resource usage

        memory_values = [m.memory_mb for m in recent_metrics]

        cpu_values = [m.cpu_percent for m in recent_metrics if m.cpu_percent > 0]

        avg_memory = sum(memory_values) / len(memory_values) if memory_values else 0.0

        avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0.0

        peak_memory = max(memory_values) if memory_values else 0.0

        peak_cpu = max(cpu_values) if cpu_values else 0.0

        return PerformanceStats(
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            average_response_time=avg_response_time,
            p95_response_time=p95_response_time,
            p99_response_time=p99_response_time,
            requests_per_second=requests_per_second,
            error_rate=error_rate,
            average_memory_mb=avg_memory,
            average_cpu_percent=avg_cpu,
            peak_memory_mb=peak_memory,
            peak_cpu_percent=peak_cpu,
            active_connections=self.active_requests,
        )

    def get_endpoint_stats(self) -> dict[str, dict[str, float]]:
        """Get per-endpoint performance statistics."""

        endpoint_stats = {}

        for endpoint, times in self.endpoint_stats.items():
            if not times:
                continue

            sorted_times = sorted(times)

            count = len(times)

            endpoint_stats[endpoint] = {
                "count": count,
                "avg_ms": sum(times) / count,
                "min_ms": min(times),
                "max_ms": max(times),
                "p50_ms": sorted_times[int(count * 0.5)],
                "p95_ms": sorted_times[int(count * 0.95)],
                "p99_ms": sorted_times[int(count * 0.99)],
            }

        return endpoint_stats

    def get_system_metrics(self) -> dict[str, Any]:
        """Get current system performance metrics."""

        try:
            memory_info = self.process.memory_info()

            cpu_percent = self.process.cpu_percent()

            # System-wide metrics

            system_memory = psutil.virtual_memory()

            system_cpu = psutil.cpu_percent(interval=None)

            return {
                "process": {
                    "memory_mb": memory_info.rss / 1024 / 1024,
                    "memory_percent": self.process.memory_percent(),
                    "cpu_percent": cpu_percent,
                    "threads": self.process.num_threads(),
                    "connections": len(self.process.connections()),
                },
                "system": {
                    "memory_total_gb": system_memory.total / 1024 / 1024 / 1024,
                    "memory_available_gb": system_memory.available / 1024 / 1024 / 1024,
                    "memory_percent": system_memory.percent,
                    "cpu_percent": system_cpu,
                    "cpu_count": psutil.cpu_count(),
                },
                "application": {
                    "uptime_seconds": (
                        datetime.now() - self.start_time
                    ).total_seconds(),
                    "total_requests": self.total_requests,
                    "total_errors": self.total_errors,
                    "active_requests": self.active_requests,
                    "error_rate_percent": (
                        (self.total_errors / self.total_requests) * 100
                        if self.total_requests > 0
                        else 0.0
                    ),
                },
            }

        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")

            return {}

    def reset_metrics(self) -> None:
        """Reset all collected metrics."""

        self.request_metrics.clear()

        self.endpoint_stats.clear()

        self.total_requests = 0

        self.total_errors = 0

        self.start_time = datetime.now()

        logger.info("Performance metrics reset")


# Global middleware instance for access from other modules


_performance_middleware: PerformanceMonitoringMiddleware | None = None


def get_performance_middleware() -> PerformanceMonitoringMiddleware | None:
    """Get the global performance middleware instance."""
    return _performance_middleware


def set_performance_middleware(middleware: PerformanceMonitoringMiddleware) -> None:
    """Set the global performance middleware instance."""
    globals()["_performance_middleware"] = middleware


@asynccontextmanager
async def performance_timer(operation_name: str) -> AsyncIterator[None]:
    """Context manager for timing specific operations.





    Args:


        operation_name: Name of the operation being timed





    Usage:


        async with performance_timer("database_query"):


            _ = await db.query()


    """

    start_time = time.perf_counter()

    try:
        yield

    finally:
        duration = time.perf_counter() - start_time

        logger.info(
            f"Operation completed: {operation_name}",
            extra={"operation": operation_name, "duration_ms": duration * 1000},
        )


def log_database_query(query: str, duration_ms: float, row_count: int = 0) -> None:
    """Log database query performance.





    Args:


        query: SQL query (sanitized)


        duration_ms: Query duration in milliseconds


        row_count: Number of rows returned/affected


    """

    logger.info(
        "Database query executed",
        extra={
            "query_type": query.split()[0].upper() if query else "UNKNOWN",
            "duration_ms": duration_ms,
            "row_count": row_count,
            "slow_query": duration_ms > 100,  # Flag slow queries
        },
    )


def log_cache_operation(
    operation: str, key: str, hit: bool, duration_ms: float = 0
) -> None:
    """Log cache operation performance.





    Args:


        operation: Cache operation (GET, SET, DELETE, etc.)


        key: Cache key (sanitized)


        hit: Whether it was a cache hit


        duration_ms: Operation duration in milliseconds


    """

    logger.info(
        "Cache operation",
        extra={
            "operation": operation,
            "cache_hit": hit,
            "duration_ms": duration_ms,
            "key_hash": hash(key) % 10000,  # Anonymized key identifier
        },
    )


def _build_perf_router() -> APIRouter:
    """Create an internal router exposing performance stats.

    Returns:
        APIRouter: Router with minimal, opt-in endpoints for diagnostics.
    """
    router = APIRouter()

    @router.get("/stats", tags=["Monitoring"], summary="Aggregated performance stats")
    async def perf_stats(window_minutes: int = 5) -> dict[str, Any]:
        middleware = get_performance_middleware()
        if not middleware:
            return {"enabled": False, "detail": _NOT_ATTACHED}
        stats = middleware.get_performance_stats(window_minutes=window_minutes)
        return {
            "enabled": True,
            "window_minutes": window_minutes,
            "stats": stats.__dict__,
            "endpoints": middleware.get_endpoint_stats(),
        }

    @router.get("/system", tags=["Monitoring"], summary="Process/system metrics")
    async def system_metrics() -> dict[str, Any]:
        middleware = get_performance_middleware()
        if not middleware:
            return {"enabled": False, "detail": _NOT_ATTACHED}
        return {"enabled": True, "metrics": middleware.get_system_metrics()}

    @router.post("/reset", tags=["Monitoring"], summary="Reset collected metrics")
    async def reset_metrics() -> dict[str, Any]:
        middleware = get_performance_middleware()
        if not middleware:
            return {"enabled": False, "detail": _NOT_ATTACHED}
        middleware.reset_metrics()
        return {"ok": True}

    return router


def attach(app: FastAPI) -> None:
    """Attach the performance middleware and optional internal routes.

    This hook allows the application factory to integrate performance monitoring
    without hard dependencies. Internal endpoints are gated by the environment
    variable `ENABLE_PERF_ENDPOINTS` (default: false) to avoid exposing them in
    production unintentionally.

    Args:
        app: FastAPI application instance.
    """
    # Install middleware and capture the instance used by Starlette
    if not HAS_PSUTIL:
        logger.warning(
            "Performance monitoring middleware skipped (psutil not installed)"
        )
        return

    class _Installed(PerformanceMonitoringMiddleware):
        def __init__(self, app: ASGIApp):  # type: ignore[override]
            super().__init__(app)
            set_performance_middleware(self)

    app.add_middleware(_Installed)

    # Optionally mount internal diagnostics endpoints
    if os.getenv("ENABLE_PERF_ENDPOINTS", "false").lower() == "true":
        router = _build_perf_router()
        app.include_router(router, prefix="/_internal/perf")
        logger.info("Performance endpoints enabled at /_internal/perf")
