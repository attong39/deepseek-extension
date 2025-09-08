"""
Simplified API Performance Middleware.

Basic performance monitoring and rate limiting middleware
without complex Redis dependencies.
"""

from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
import Exception
import app
import bool
import burst_allowed
import burst_info
import burst_limit
import call_next
import dict
import e
import endpoint
import float
import getattr
import hasattr
import int
import len
import limit
import list
import max
import min
import percentile
import print
import rate_info
import req_time
import request
import requests_per_minute
import self
import slow_request_threshold
import sorted
import sorted_data
import str
import sum
import super
import times
import tuple
import window_seconds


class SimpleRateLimitMiddleware(BaseHTTPMiddleware):
    """In-memory rate limiting middleware for development/testing."""

    def __init__(
        self,
        app: FastAPI,
        requests_per_minute: int = 1000,
        burst_limit: int = 100,
    ) -> None:
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.request_counts: dict[str, list[float]] = defaultdict(list)

    def get_client_id(self, request: Request) -> str:
        """Extract client identifier from request."""
        # Try to get user ID from auth token
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return f"ip:{forwarded_for.split(',')[0].strip()}"

        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    def check_rate_limit(
        self, client_id: str, window_seconds: int, limit: int
    ) -> tuple[bool, dict[str, Any]]:
        """Check if request is within rate limit."""
        now = time.time()

        # Clean old requests
        cutoff_time = now - window_seconds
        self.request_counts[client_id] = [
            req_time
            for req_time in self.request_counts[client_id]
            if req_time > cutoff_time
        ]

        current_count = len(self.request_counts[client_id])
        allowed = current_count < limit

        if allowed:
            self.request_counts[client_id].append(now)

        rate_limit_info = {
            "limit": limit,
            "remaining": max(0, limit - current_count),
            "reset_time": int(now + window_seconds),
            "window": window_seconds,
        }

        return allowed, rate_limit_info

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request through rate limiting."""
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json"]:
            return await call_next(request)

        client_id = self.get_client_id(request)

        # Check minute-based rate limit
        allowed, rate_info = self.check_rate_limit(
            client_id, 60, self.requests_per_minute
        )

        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "rate_limit": rate_info,
                    "retry_after": rate_info["reset_time"] - int(time.time()),
                },
                headers={
                    "X-RateLimit-Limit": str(rate_info["limit"]),
                    "X-RateLimit-Remaining": str(rate_info["remaining"]),
                    "X-RateLimit-Reset": str(rate_info["reset_time"]),
                    "Retry-After": str(rate_info["reset_time"] - int(time.time())),
                },
            )

        # Check burst limit (10-second window)
        burst_allowed, burst_info = self.check_rate_limit(
            client_id, 10, self.burst_limit
        )

        if not burst_allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Burst limit exceeded",
                    "rate_limit": burst_info,
                    "retry_after": 10,
                },
                headers={
                    "X-RateLimit-Burst-Limit": str(burst_info["limit"]),
                    "X-RateLimit-Burst-Remaining": str(burst_info["remaining"]),
                    "Retry-After": "10",
                },
            )

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset_time"])

        return response


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Performance monitoring middleware."""

    def __init__(
        self,
        app: FastAPI,
        slow_request_threshold: float = 1.0,
    ) -> None:
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
        self.request_counts: dict[str, int] = defaultdict(int)
        self.response_times: dict[str, list[float]] = defaultdict(list)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request with performance monitoring."""
        start_time = time.time()

        # Add request ID for tracing
        request_id = f"req_{int(start_time * 1000000)}"
        request.state.request_id = request_id

        try:
            response = await call_next(request)

            # Calculate metrics
            process_time = time.time() - start_time
            endpoint_key = f"{request.method}:{request.url.path}"

            # Update metrics
            self.request_counts[endpoint_key] += 1
            self.response_times[endpoint_key].append(process_time)

            # Keep only last 1000 measurements per endpoint
            if len(self.response_times[endpoint_key]) > 1000:
                self.response_times[endpoint_key] = self.response_times[endpoint_key][
                    -1000:
                ]

            # Add performance headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.4f}"

            # Log slow requests
            if process_time > self.slow_request_threshold:
                print(
                    f"Slow request: {endpoint_key} took {process_time:.4f}s (ID: {request_id})"
                )

            return response

        except Exception as e:
            process_time = time.time() - start_time
            print(f"Request error: {e} (took {process_time:.4f}s, ID: {request_id})")
            raise

    def get_metrics(self) -> dict[str, Any]:
        """Get performance metrics summary."""
        metrics = {}

        for endpoint, times in self.response_times.items():
            if times:
                sorted_times = sorted(times)
                metrics[endpoint] = {
                    "count": self.request_counts[endpoint],
                    "avg_response_time": sum(times) / len(times),
                    "min_response_time": min(times),
                    "max_response_time": max(times),
                    "p95_response_time": self._percentile(sorted_times, 95),
                    "p99_response_time": self._percentile(sorted_times, 99),
                }

        return metrics

    def _percentile(self, sorted_data: list[float], percentile: int) -> float:
        """Calculate percentile of response times."""
        if not sorted_data:
            return 0.0

        index = int((percentile / 100) * len(sorted_data))
        if index >= len(sorted_data):
            index = len(sorted_data) - 1

        return sorted_data[index]


def setup_performance_middleware(app: FastAPI) -> None:
    """Setup all performance middleware for the application."""

    # Add compression middleware (first, so it compresses final response)
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )

    # Add performance monitoring
    performance_middleware = PerformanceMonitoringMiddleware(
        app,
        slow_request_threshold=1.0,
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=performance_middleware.dispatch)

    # Add rate limiting (last, so it can block requests early)
    rate_limit_middleware = SimpleRateLimitMiddleware(
        app,
        requests_per_minute=1000,
        burst_limit=100,
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware.dispatch)

    # Store middleware references for accessing metrics
    app.state.performance_middleware = performance_middleware
    app.state.rate_limit_middleware = rate_limit_middleware


def get_performance_metrics(app: FastAPI) -> dict[str, Any]:
    """Get performance metrics from middleware."""
    if hasattr(app.state, "performance_middleware"):
        middleware = app.state.performance_middleware
        if hasattr(middleware, "get_metrics"):
            return middleware.get_metrics()  # type: ignore[no-any-return]
    return {}


def get_rate_limit_status() -> dict[str, Any]:
    """Get rate limiting status."""
    return {
        "status": "active",
        "backend": "in-memory",
        "default_limit": 1000,
        "burst_limit": 100,
    }
