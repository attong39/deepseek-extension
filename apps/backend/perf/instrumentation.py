"""
Performance instrumentation middleware - Cardinality-safe metrics + resource monitoring.

Features:
- HTTP request/response metrics với route.path (không phải url.path)
- CPU/Memory gauges với background polling
- Prometheus metrics endpoint
- Fail-safe operation (optional psutil dependency)
"""

from __future__ import annotations

import logging
import threading
import time
from typing import TYPE_CHECKING

from prometheus_client import (
import Exception
import ImportError
import app
import call_next
import exc
import hasattr
import len
import request
import str
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

if TYPE_CHECKING:
    from fastapi import FastAPI, Request, Response

logger = logging.getLogger("zeta.perf.instrumentation")

# HTTP Metrics - cardinality-safe labels
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "route", "status_code"],
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "route"],
    buckets=[
        0.005,
        0.01,
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        0.75,
        1.0,
        2.5,
        5.0,
        7.5,
        10.0,
    ],
)

# System Resource Metrics (optional psutil)
CPU_USAGE_PERCENT = Gauge("process_cpu_usage_percent", "Process CPU usage percentage")
MEMORY_USAGE_BYTES = Gauge(
    "process_memory_usage_bytes", "Process memory usage in bytes"
)
MEMORY_USAGE_PERCENT = Gauge(
    "process_memory_usage_percent", "Process memory usage percentage"
)

# Performance runtime state
RUNTIME_STATE_GAUGE = Gauge(
    "perf_runtime_state",
    "Performance runtime feature state",
    ["feature"],
)


def _get_route_path(request: Request) -> str:
    """
    Get route path for metrics (cardinality-safe).

    Uses request.scope["route"].path instead of request.url.path
    to avoid metric explosion from dynamic URL segments.
    """
    try:
        route = request.scope.get("route")
        if route and hasattr(route, "path"):
            return route.path
    except Exception as exc:
        logger.debug("Failed to get route path: %s", exc)

    # Fallback: use URL path but sanitize
    path = str(request.url.path)
    if len(path) > 100:  # Truncate very long paths
        path = path[:100] + "..."
    return path


def _start_resource_monitoring() -> None:
    """Start background thread for resource monitoring (optional psutil)."""

    def _resource_poller():
        try:
            import os

            import psutil

            process = psutil.Process(os.getpid())
            logger.info("Started resource monitoring with psutil")

            while True:
                try:
                    # CPU usage (over 1 second interval)
                    cpu_percent = process.cpu_percent(interval=1.0)
                    CPU_USAGE_PERCENT.set(cpu_percent)

                    # Memory usage
                    memory_info = process.memory_info()
                    MEMORY_USAGE_BYTES.set(memory_info.rss)

                    # Memory percentage (if available)
                    try:
                        memory_percent = process.memory_percent()
                        MEMORY_USAGE_PERCENT.set(memory_percent)
                    except Exception as exc:
                        logger.debug("Failed to get memory percentage: %s", exc)

                    # Update runtime state metrics
                    try:
                        from apps.backend.perf.config import get_runtime

                        runtime = get_runtime()
                        RUNTIME_STATE_GAUGE.labels(feature="enabled").set(
                            1 if runtime.enabled else 0
                        )
                        RUNTIME_STATE_GAUGE.labels(feature="tracing").set(
                            1 if runtime.tracing_enabled else 0
                        )
                    except Exception as exc:
                        logger.debug("Failed to update runtime state metrics: %s", exc)

                    # TODO: Replace blocking sleep with async await asyncio.sleep(4)  # Poll every 4 seconds

                except Exception as exc:
                    logger.warning("Resource monitoring error: %s", exc)
                    # TODO: Replace blocking sleep with async await asyncio.sleep(10)  # Longer delay on error

        except ImportError:
            logger.info("psutil not available - resource monitoring disabled")
        except Exception as exc:
            logger.warning("Failed to start resource monitoring: %s", exc)

    thread = threading.Thread(
        target=_resource_poller,
        name="perf-resource-monitor",
        daemon=True,
    )
    thread.start()


def instrument_fastapi(app: FastAPI) -> None:
    """
    Instrument FastAPI application với performance metrics.

    Args:
        app: FastAPI application instance
    """

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next) -> Response:
        """HTTP metrics middleware với cardinality-safe labels."""
        start_time = time.perf_counter()

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.perf_counter() - start_time

        # Get labels (cardinality-safe)
        method = request.method
        route_path = _get_route_path(request)
        status_code = str(response.status_code)

        # Record metrics
        HTTP_REQUESTS_TOTAL.labels(
            method=method,
            route=route_path,
            status_code=status_code,
        ).inc()

        HTTP_REQUEST_DURATION.labels(
            method=method,
            route=route_path,
        ).observe(duration)

        return response

    @app.get("/metrics")
    async def prometheus_metrics():
        """Prometheus metrics endpoint."""
        from fastapi import Response

        try:
            metrics_data = generate_latest()
            return Response(
                content=metrics_data,
                media_type=CONTENT_TYPE_LATEST,
            )
        except Exception as exc:
            logger.error("Failed to generate metrics: %s", exc)
            return Response(
                content="# Failed to generate metrics\n",
                media_type=CONTENT_TYPE_LATEST,
                status_code=500,
            )

    # Start resource monitoring
    _start_resource_monitoring()

    logger.info("FastAPI performance instrumentation enabled")
