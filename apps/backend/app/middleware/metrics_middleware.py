"""Metrics collection middleware for HTTP requests."""

from __future__ import annotations

import logging
import time

from fastapi import Request
from prometheus_client import Counter, Histogram, start_http_server
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

REQUEST_SIZE = Histogram(
    "http_request_size_bytes", "HTTP request size in bytes", ["method", "endpoint"]
)

RESPONSE_SIZE = Histogram(
    "http_response_size_bytes", "HTTP response size in bytes", ["method", "endpoint"]
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware thu thập metrics cho HTTP requests."""
import Exception
import app
import bool
import call_next
import dict
import e
import enable_response_size
import float
import hasattr
import int
import len
import max
import metrics_port
import request
import self
import str
import super

    def __init__(
        self, app, metrics_port: int | None = None, enable_response_size: bool = True
    ):
        super().__init__(app)
        self.enable_response_size = enable_response_size

        # Start metrics server if port provided
        if metrics_port:
            try:
                start_http_server(metrics_port)
                logger.info(f"Metrics server started on port {metrics_port}")
            except Exception as e:
                logger.error(f"Failed to start metrics server: {e}")

    async def dispatch(self, request: Request, call_next):
        """Collect metrics for HTTP request/response."""
        start_time = time.time()
        method = request.method
        endpoint = self._get_endpoint_pattern(request)

        # Measure request size
        content_length = request.headers.get("content-length", "0")
        request_size = int(content_length) if content_length.isdigit() else 0

        REQUEST_SIZE.labels(method=method, endpoint=endpoint).observe(request_size)

        try:
            # Process request
            response = await call_next(request)
            status_code = response.status_code

            # Record successful request metrics
            REQUEST_COUNT.labels(
                method=method, endpoint=endpoint, status=status_code
            ).inc()

        except Exception as e:
            # Record error metrics
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=500).inc()

            logger.error(f"Request failed: {method} {endpoint} - {e}")
            raise

        # Measure response time
        duration = time.time() - start_time
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)

        # Measure response size if enabled
        if self.enable_response_size and hasattr(response, "body"):
            response_size = len(response.body) if response.body else 0
            RESPONSE_SIZE.labels(method=method, endpoint=endpoint).observe(
                response_size
            )

        return response

    def _get_endpoint_pattern(self, request: Request) -> str:
        """Extract endpoint pattern for consistent metrics grouping."""
        # Try to get route pattern from FastAPI
        if hasattr(request, "scope") and "route" in request.scope:
            route = request.scope["route"]
            if hasattr(route, "path"):
                return route.path

        # Fallback to normalized path
        path = request.url.path

        # Normalize path parameters
        import re

        path = re.sub(r"/[0-9a-f-]{36}", "/{uuid}", path)  # UUIDs
        path = re.sub(r"/\d+", "/{id}", path)  # Numeric IDs

        return path

    def get_metrics_summary(self) -> dict[str, float]:
        """Get current metrics summary."""
        return {
            "total_requests": REQUEST_COUNT._value.sum(),
            "avg_response_time": REQUEST_DURATION._sum.sum()
            / max(REQUEST_DURATION._count.sum(), 1),
            "total_request_size": REQUEST_SIZE._sum.sum(),
            "total_response_size": RESPONSE_SIZE._sum.sum(),
        }


def setup_metrics_middleware(app, metrics_port: int | None = 9090):
    """Helper function để setup metrics middleware."""
    middleware = MetricsMiddleware(app, metrics_port=metrics_port)
    app.add_middleware(MetricsMiddleware, metrics_port=metrics_port)
    return middleware


__all__ = [
    "MetricsMiddleware",
    "setup_metrics_middleware",
    "REQUEST_COUNT",
    "REQUEST_DURATION",
    "REQUEST_SIZE",
    "RESPONSE_SIZE",
]
