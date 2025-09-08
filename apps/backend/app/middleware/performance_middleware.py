"""
API Performance Middleware for High-Throughput Applications.

Implements rate limiting, compression, and monitoring middleware
following COMPREHENSIVE_UPGRADE_PLAN.md Phase 1.2.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
import Exception
import ImportError
import any
import app
import bool
import burst_allowed
import burst_info
import burst_limit
import call_next
import compression_level
import content_length
import content_type
import ct
import data
import default_rate_limit
import dict
import e
import enable_metrics
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
import minimum_size
import minute_limit
import percentile
import print
import rate_info
import redis_url
import request
import self
import slow_request_threshold
import sorted
import str
import sum
import super
import times
import tuple
import window

try:
    import redis.asyncio as redis  # noqa: PLC0415

    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Distributed rate limiting middleware with Redis backend."""

    def __init__(
        self,
        app: FastAPI,
        redis_url: str = "redis://localhost:6379",
        default_rate_limit: int = 1000,  # requests per minute
        burst_limit: int = 100,  # requests per 10 seconds
    ) -> None:
        super().__init__(app)
        self.redis_url = redis_url
        self.default_rate_limit = default_rate_limit
        self.burst_limit = burst_limit
        self._redis: redis.Redis[str] | None = None

    async def get_redis(self) -> redis.Redis[str]:
        """Get or create Redis connection."""
        if self._redis is None:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)
        return self._redis

    async def check_rate_limit(
        self,
        client_id: str,
        endpoint: str,
        limit: int,
        window: int,
    ) -> tuple[bool, dict[str, Any]]:
        """Check if request is within rate limit.

        Args:
            client_id: Unique identifier for the client
            endpoint: API endpoint being accessed
            limit: Number of requests allowed
            window: Time window in seconds

        Returns:
            Tuple of (allowed, rate_limit_info)
        """
        redis_client = await self.get_redis()
        key = f"rate_limit:{client_id}:{endpoint}"

        # Use sliding window with Redis
        now = time.time()
        pipeline = redis_client.pipeline()

        # Remove expired entries
        pipeline.zremrangebyscore(key, 0, now - window)

        # Count current requests
        pipeline.zcard(key)

        # Add current request
        pipeline.zadd(key, {str(now): now})

        # Set expiry
        pipeline.expire(key, window)

        results = await pipeline.execute()
        current_count = results[1]

        allowed = current_count < limit

        if not allowed:
            # Remove the request we just added if not allowed
            await redis_client.zrem(key, str(now))

        rate_limit_info = {
            "limit": limit,
            "remaining": max(0, limit - current_count),
            "reset_time": int(now + window),
            "window": window,
        }

        return allowed, rate_limit_info

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

    def get_endpoint_limits(self, path: str, method: str) -> tuple[int, int]:
        """Get rate limits for specific endpoint.

        Returns:
            Tuple of (requests_per_minute, burst_limit_per_10s)
        """
        # High-traffic endpoints with stricter limits
        if path.startswith("/api/v1/chat/stream"):
            return 100, 20  # Lower limits for streaming
        elif path.startswith("/api/v1/agents"):
            return 500, 50  # Moderate limits for agent operations
        elif path.startswith("/api/v1/auth"):
            return 30, 10  # Strict limits for auth endpoints
        elif path.startswith("/api/v1/upload"):
            return 50, 10  # Strict limits for uploads

        # Default limits
        return self.default_rate_limit, self.burst_limit

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process request through rate limiting."""
        start_time = time.time()

        # Skip rate limiting for health checks and internal endpoints
        if request.url.path in ["/health", "/metrics", "/docs", "/openapi.json"]:
            response = await call_next(request)
            return response

        try:
            client_id = self.get_client_id(request)
            path = request.url.path
            method = request.method

            # Get endpoint-specific limits
            minute_limit, burst_limit = self.get_endpoint_limits(path, method)

            # Check minute-based rate limit
            allowed, rate_info = await self.check_rate_limit(
                client_id, f"{method}:{path}", minute_limit, 60
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
            burst_allowed, burst_info = await self.check_rate_limit(
                client_id, f"burst:{method}:{path}", burst_limit, 10
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

            # Add rate limit headers to successful responses
            response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
            response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
            response.headers["X-RateLimit-Reset"] = str(rate_info["reset_time"])

            # Add performance metrics
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = f"{process_time:.4f}"

            return response

        except Exception as e:
            # Log error and allow request to proceed
            print(f"Rate limiting error: {e}")
            response = await call_next(request)
            return response


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Performance monitoring and optimization middleware."""

    def __init__(
        self,
        app: FastAPI,
        enable_metrics: bool = True,
        slow_request_threshold: float = 1.0,  # seconds
    ) -> None:
        super().__init__(app)
        self.enable_metrics = enable_metrics
        self.slow_request_threshold = slow_request_threshold
        self.request_counts: dict[str, int] = {}
        self.response_times: dict[str, list[float]] = {}

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

            if self.enable_metrics:
                # Update metrics
                self.request_counts[endpoint_key] = (
                    self.request_counts.get(endpoint_key, 0) + 1
                )

                if endpoint_key not in self.response_times:
                    self.response_times[endpoint_key] = []

                self.response_times[endpoint_key].append(process_time)

                # Keep only last 1000 measurements per endpoint
                if len(self.response_times[endpoint_key]) > 1000:
                    self.response_times[endpoint_key] = self.response_times[
                        endpoint_key
                    ][-1000:]

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
                metrics[endpoint] = {
                    "count": self.request_counts.get(endpoint, 0),
                    "avg_response_time": sum(times) / len(times),
                    "min_response_time": min(times),
                    "max_response_time": max(times),
                    "p95_response_time": self._percentile(times, 95),
                    "p99_response_time": self._percentile(times, 99),
                }

        return metrics

    def _percentile(self, data: list[float], percentile: int) -> float:
        """Calculate percentile of response times."""
        if not data:
            return 0.0

        sorted_data = sorted(data)
        index = int((percentile / 100) * len(sorted_data))
        if index >= len(sorted_data):
            index = len(sorted_data) - 1

        return sorted_data[index]


class CompressionMiddleware:
    """Advanced compression middleware with content-type awareness."""

    def __init__(
        self,
        app: FastAPI,
        compression_level: int = 6,
        minimum_size: int = 1000,  # Only compress responses larger than this
    ) -> None:
        self.app = app
        self.compression_level = compression_level
        self.minimum_size = minimum_size

    def should_compress(self, content_type: str, content_length: int) -> bool:
        """Determine if response should be compressed."""
        if content_length < self.minimum_size:
            return False

        # Compress text-based content
        compressible_types = [
            "application/json",
            "application/javascript",
            "text/",
            "application/xml",
            "application/rss+xml",
            "application/atom+xml",
        ]

        return any(content_type.startswith(ct) for ct in compressible_types)


def setup_performance_middleware(app: FastAPI) -> None:
    """Setup all performance middleware for the application."""

    # Add compression middleware (first, so it compresses final response)
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,
    )

    # Add performance monitoring
    performance_middleware = PerformanceMiddleware(
        app,
        enable_metrics=True,
        slow_request_threshold=1.0,
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=performance_middleware.dispatch)

    # Add rate limiting (last, so it can block requests early)
    rate_limit_middleware = RateLimitMiddleware(
        app,
        redis_url="redis://localhost:6379",
        default_rate_limit=1000,
        burst_limit=100,
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware.dispatch)

    # Store middleware references for accessing metrics
    app.state.performance_middleware = performance_middleware
    app.state.rate_limit_middleware = rate_limit_middleware


# FastAPI endpoint for monitoring
def get_performance_metrics(app: FastAPI) -> dict[str, Any]:
    """Get performance metrics from middleware."""
    if hasattr(app.state, "performance_middleware"):
        return app.state.performance_middleware.get_metrics()
    return {}


def get_rate_limit_status() -> dict[str, Any]:
    """Get rate limiting status."""
    return {
        "status": "active",
        "backend": "redis",
        "default_limit": 1000,
        "burst_limit": 100,
    }
