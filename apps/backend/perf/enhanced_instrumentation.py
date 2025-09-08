"""
Enhanced performance instrumentation với advanced metrics collection.

Features:
- Extended system metrics (disk I/O, network, GC)
- Distributed tracing correlation
- JSON structured logging với trace context
- Dynamic sampling based on load
- Environment-specific metric profiles
"""

from __future__ import annotations

import asyncio
import gc
import logging
import threading
import time
from typing import TYPE_CHECKING

from prometheus_client import (
import Exception
import ImportError
import TypeError
import ValueError
import active
import app
import c
import call_next
import current
import duration_seconds
import enumerate
import exc
import float
import gen
import generation
import hasattr
import idle
import int
import last
import len
import list
import locals
import query_type
import request
import str
import task
import user_agent
import zip
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

if TYPE_CHECKING:
    from fastapi import FastAPI, Request, Response

logger = logging.getLogger("zeta.perf.enhanced_instrumentation")

# ================= Core HTTP Metrics =================
# Use unique metric names để avoid collisions với existing metrics
HTTP_REQUESTS_ENHANCED_TOTAL = Counter(
    "http_requests_enhanced_total",
    "Total HTTP requests (enhanced)",
    ["method", "route", "status_code", "user_agent_type"],
)

HTTP_REQUEST_DURATION_ENHANCED = Histogram(
    "http_request_duration_enhanced_seconds",
    "HTTP request duration (enhanced)",
    ["method", "route", "status_code_class"],
    buckets=[
        0.001,
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
        10.0,
    ],
)

HTTP_REQUEST_SIZE_ENHANCED = Histogram(
    "http_request_size_enhanced_bytes",
    "HTTP request size (enhanced)",
    ["method", "route"],
    buckets=[100, 1000, 10000, 100000, 1000000],
)

HTTP_RESPONSE_SIZE_ENHANCED = Histogram(
    "http_response_size_enhanced_bytes",
    "HTTP response size (enhanced)",
    ["method", "route", "status_code_class"],
    buckets=[100, 1000, 10000, 100000, 1000000],
)

# ================= Advanced System Metrics =================
# Memory & GC (unique names)
ENHANCED_MEMORY_USAGE_BYTES = Gauge(
    "enhanced_process_memory_usage_bytes", "Process memory usage in bytes"
)
ENHANCED_MEMORY_USAGE_PERCENT = Gauge(
    "enhanced_process_memory_usage_percent", "Process memory usage percentage"
)
ENHANCED_GC_COLLECTIONS_TOTAL = Counter(
    "enhanced_gc_collections_total", "Total garbage collections", ["generation"]
)
ENHANCED_GC_COLLECTION_TIME = Histogram(
    "enhanced_gc_collection_seconds", "GC collection time", ["generation"]
)

# CPU & Threading
CPU_USAGE_PERCENT = Gauge("process_cpu_usage_percent", "Process CPU usage percentage")
THREAD_COUNT = Gauge("process_threads_active", "Active thread count")
ASYNC_TASKS_ACTIVE = Gauge("async_tasks_active", "Active async tasks")

# Disk I/O (optional psutil)
DISK_IO_BYTES = Counter(
    "disk_io_bytes_total", "Disk I/O bytes", ["operation"]
)  # read/write
DISK_IO_OPERATIONS = Counter(
    "disk_io_operations_total", "Disk I/O operations", ["operation"]
)
DISK_IO_TIME = Histogram("disk_io_seconds", "Disk I/O time", ["operation"])

# Network I/O (optional psutil)
NETWORK_BYTES = Counter(
    "network_bytes_total", "Network bytes", ["direction"]
)  # sent/received
NETWORK_PACKETS = Counter("network_packets_total", "Network packets", ["direction"])
NETWORK_CONNECTIONS = Gauge(
    "network_connections_active", "Active network connections", ["type"]
)

# Database connections (if available)
DB_CONNECTIONS_ACTIVE = Gauge("db_connections_active", "Active database connections")
DB_CONNECTIONS_IDLE = Gauge("db_connections_idle", "Idle database connections")
DB_QUERY_DURATION = Histogram(
    "db_query_seconds", "Database query duration", ["query_type"]
)

# Application metrics
REQUEST_QUEUE_DEPTH = Gauge("request_queue_depth", "HTTP request queue depth")
ACTIVE_REQUESTS = Gauge("http_requests_active", "Currently active HTTP requests")


def _get_user_agent_type(user_agent: str) -> str:
    """Classify user agent to reduce cardinality."""
    if not user_agent:
        return "unknown"

    ua_lower = user_agent.lower()
    if "bot" in ua_lower or "crawler" in ua_lower or "spider" in ua_lower:
        return "bot"
    elif "mobile" in ua_lower or "android" in ua_lower or "iphone" in ua_lower:
        return "mobile"
    elif "postman" in ua_lower or "insomnia" in ua_lower or "curl" in ua_lower:
        return "api_client"
    else:
        return "browser"


def _get_status_code_class(status_code: int) -> str:
    """Get status code class to reduce cardinality."""
    if 200 <= status_code < 300:
        return "2xx"
    elif 300 <= status_code < 400:
        return "3xx"
    elif 400 <= status_code < 500:
        return "4xx"
    elif 500 <= status_code < 600:
        return "5xx"
    else:
        return "other"


def _get_route_path(request: Request) -> str:
    """
    Get route path for metrics (cardinality-safe).
    Enhanced với parameter detection.
    """
    try:
        route = request.scope.get("route")
        if route and hasattr(route, "path"):
            return route.path
    except Exception as exc:
        logger.debug("Failed to get route path: %s", exc)

    # Fallback: sanitize URL path
    path = str(request.url.path)

    # Truncate very long paths
    if len(path) > 100:
        path = path[:100] + "..."

    # Replace common ID patterns to reduce cardinality
    import re

    # Replace UUIDs
    path = re.sub(
        r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        "/{uuid}",
        path,
    )
    # Replace numeric IDs
    path = re.sub(r"/\d+", "/{id}", path)

    return path


def _start_enhanced_resource_monitoring() -> None:
    """Start enhanced background monitoring thread."""

    def _enhanced_resource_poller():
        try:
            import os

            import psutil

            process = psutil.Process(os.getpid())
            logger.info("Started enhanced resource monitoring with psutil")

            # Track GC generations
            gc_counts_last = [0, 0, 0]

            while True:
                try:
                    # === Memory metrics ===
                    memory_info = process.memory_info()
                    ENHANCED_MEMORY_USAGE_BYTES.set(memory_info.rss)

                    try:
                        memory_percent = process.memory_percent()
                        ENHANCED_MEMORY_USAGE_PERCENT.set(memory_percent)
                    except Exception as exc:
                        logger.debug("Failed to get memory percentage: %s", exc)

                    # === CPU metrics ===
                    cpu_percent = process.cpu_percent(interval=1.0)
                    CPU_USAGE_PERCENT.set(cpu_percent)

                    # === Threading metrics ===
                    thread_count = process.num_threads()
                    THREAD_COUNT.set(thread_count)

                    # Active async tasks (approximation)
                    try:
                        loop = asyncio.get_running_loop()
                        task_count = len(
                            [
                                task
                                for task in asyncio.all_tasks(loop)
                                if not task.done()
                            ]
                        )
                        ASYNC_TASKS_ACTIVE.set(task_count)
                    except Exception:
                        pass

                    # === Disk I/O metrics ===
                    try:
                        io_counters = process.io_counters()
                        DISK_IO_BYTES.labels(
                            operation="read"
                        )._value._value = io_counters.read_bytes
                        DISK_IO_BYTES.labels(
                            operation="write"
                        )._value._value = io_counters.write_bytes
                        DISK_IO_OPERATIONS.labels(
                            operation="read"
                        )._value._value = io_counters.read_count
                        DISK_IO_OPERATIONS.labels(
                            operation="write"
                        )._value._value = io_counters.write_count
                    except Exception as exc:
                        logger.debug("Failed to get I/O counters: %s", exc)

                    # === Network metrics ===
                    try:
                        # Get system-wide network stats (process-level not available)
                        net_io = psutil.net_io_counters()
                        if net_io:
                            NETWORK_BYTES.labels(
                                direction="sent"
                            )._value._value = net_io.bytes_sent
                            NETWORK_BYTES.labels(
                                direction="received"
                            )._value._value = net_io.bytes_recv
                            NETWORK_PACKETS.labels(
                                direction="sent"
                            )._value._value = net_io.packets_sent
                            NETWORK_PACKETS.labels(
                                direction="received"
                            )._value._value = net_io.packets_recv
                    except Exception as exc:
                        logger.debug("Failed to get network counters: %s", exc)

                    # === Connection metrics ===
                    try:
                        connections = process.connections()
                        tcp_count = len(
                            [c for c in connections if c.type.name == "SOCK_STREAM"]
                        )
                        udp_count = len(
                            [c for c in connections if c.type.name == "SOCK_DGRAM"]
                        )
                        NETWORK_CONNECTIONS.labels(type="tcp").set(tcp_count)
                        NETWORK_CONNECTIONS.labels(type="udp").set(udp_count)
                    except Exception as exc:
                        logger.debug("Failed to get connection info: %s", exc)

                    # === Garbage collection metrics ===
                    try:
                        gc_counts = gc.get_count()
                        for gen, (current, last) in enumerate(
                            zip(gc_counts, gc_counts_last, strict=False)
                        ):
                            if current != last:
                                ENHANCED_GC_COLLECTIONS_TOTAL.labels(
                                    generation=str(gen)
                                ).inc(current - last)
                        gc_counts_last = list(gc_counts)
                    except Exception as exc:
                        logger.debug("Failed to get GC counts: %s", exc)

                    # === Runtime state metrics ===
                    try:
                        from apps.backend.perf.config import get_runtime

                        runtime = get_runtime()
                        # Using existing metrics from base instrumentation
                        from apps.backend.perf.instrumentation import (
                            RUNTIME_STATE_GAUGE,
                        )

                        RUNTIME_STATE_GAUGE.labels(feature="enabled").set(
                            1 if runtime.enabled else 0
                        )
                        RUNTIME_STATE_GAUGE.labels(feature="tracing").set(
                            1 if runtime.tracing_enabled else 0
                        )
                    except Exception as exc:
                        logger.debug("Failed to update runtime state metrics: %s", exc)

                    # TODO: Replace blocking sleep with async await asyncio.sleep(5)  # Poll every 5 seconds

                except Exception as exc:
                    logger.warning("Enhanced resource monitoring error: %s", exc)
                    # TODO: Replace blocking sleep with async await asyncio.sleep(15)  # Longer delay on error

        except ImportError:
            logger.info("psutil not available - enhanced resource monitoring disabled")
        except Exception as exc:
            logger.warning("Failed to start enhanced resource monitoring: %s", exc)

    thread = threading.Thread(
        target=_enhanced_resource_poller,
        name="perf-enhanced-monitor",
        daemon=True,
    )
    thread.start()


def instrument_fastapi_enhanced(app: FastAPI) -> None:
    """
    Enhanced FastAPI instrumentation với comprehensive metrics.

    Args:
        app: FastAPI application instance
    """

    @app.middleware("http")
    async def enhanced_metrics_middleware(request: Request, call_next) -> Response:
        """Enhanced HTTP metrics middleware với detailed tracking."""
        start_time = time.perf_counter()

        # Track active requests
        ACTIVE_REQUESTS.inc()

        try:
            # Get request metadata
            method = request.method
            route_path = _get_route_path(request)
            user__ = request.headers.get("user-agent", "")
            user_agent_type = _get_user_agent_type(user_agent)

            # Request size
            content_length = request.headers.get("content-length", "0")
            try:
                request_size = int(content_length)
                HTTP_REQUEST_SIZE_ENHANCED.labels(
                    method=method, route=route_path
                ).observe(request_size)
            except (ValueError, TypeError):
                pass

            # Process request
            response = await call_next(request)

            # Calculate metrics
            duration = time.perf_counter() - start_time
            status_code = response.status_code
            status_code_class = _get_status_code_class(status_code)

            # Response size
            response_size = 0
            if hasattr(response, "headers") and "content-length" in response.headers:
                try:
                    response_size = int(response.headers["content-length"])
                except (ValueError, TypeError):
                    pass

            # Record metrics
            HTTP_REQUESTS_ENHANCED_TOTAL.labels(
                method=method,
                route=route_path,
                status_code=str(status_code),
                user_agent_type=user_agent_type,
            ).inc()

            HTTP_REQUEST_DURATION_ENHANCED.labels(
                method=method,
                route=route_path,
                status_code_class=status_code_class,
            ).observe(duration)

            if response_size > 0:
                HTTP_RESPONSE_SIZE_ENHANCED.labels(
                    method=method,
                    route=route_path,
                    status_code_class=status_code_class,
                ).observe(response_size)

            return response

        except Exception as exc:
            logger.error("Enhanced metrics middleware error: %s", exc)
            # Return error response if request processing failed
            if "response" not in locals():
                from fastapi import Response

                response = Response(status_code=500, content="Internal Server Error")
            return response
        finally:
            ACTIVE_REQUESTS.dec()

    @app.get("/metrics/enhanced")
    async def enhanced_prometheus_metrics():
        """Enhanced Prometheus metrics endpoint with additional metadata."""
        try:
            metrics_data = generate_latest()

            # Add custom metadata
            metadata_lines = [
                "# HELP zeta_performance_monitoring_info Performance monitoring metadata",
                "# TYPE zeta_performance_monitoring_info gauge",
                'zeta_performance_monitoring_info{version="2.0",enhanced="true"} 1',
            ]

            enhanced_data = (
                "\n".join(metadata_lines) + "\n" + metrics_data.decode("utf-8")
            )

            from fastapi import Response

            return Response(
                content=enhanced_data,
                media_type=CONTENT_TYPE_LATEST,
            )
        except Exception as exc:
            logger.error("Failed to generate enhanced metrics: %s", exc)
            from fastapi import Response

            return Response(
                content="# Failed to generate enhanced metrics\n",
                media_type=CONTENT_TYPE_LATEST,
                status_code=500,
            )

    # Start enhanced resource monitoring
    _start_enhanced_resource_monitoring()

    logger.info("Enhanced FastAPI performance instrumentation enabled")


# Utility functions for external integration
def record_database_query(query_type: str, duration_seconds: float) -> None:
    """Record database query metrics."""
    DB_QUERY_DURATION.labels(query_type=query_type).observe(duration_seconds)


def update_db_connection_pool(active: int, idle: int) -> None:
    """Update database connection pool metrics."""
    DB_CONNECTIONS_ACTIVE.set(active)
    DB_CONNECTIONS_IDLE.set(idle)


def record_gc_time(generation: int, duration_seconds: float) -> None:
    """Record garbage collection time."""
    ENHANCED_GC_COLLECTION_TIME.labels(generation=str(generation)).observe(
        duration_seconds
    )
