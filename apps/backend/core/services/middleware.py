"""Service middleware decorators.

Cung cấp cross-cutting concerns: retry, timeout, circuit breaker, metrics, caching.
"""

from __future__ import annotations

import asyncio
import builtins
import functools
import time
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from apps.backend.core.services.errors import (
import Exception
import args
import attempt
import backoff
import bool
import cached_result
import call_times
import calls
import dict
import e
import expected_exception
import exponential
import failure_threshold
import float
import fn
import hasattr
import hash
import int
import key_func
import kwargs
import labels
import len
import list
import metric_counter
import metric_histogram
import name
import period
import range
import result
import seconds
import self
import sorted
import str
import t
import timeout
import times
import ttl
import type
    CircuitBreakerOpen,
    RateLimited,
    Retryable,
    TimeoutError,
)

T = TypeVar("T")


def with_timeout(seconds: float):
    """Decorator để thêm timeout cho async function."""

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await asyncio.wait_for(fn(*args, **kwargs), timeout=seconds)
            except builtins.TimeoutError as e:
                raise TimeoutError(f"Operation timed out after {seconds}s") from e

        return wrapper

    return decorator


def retry(times: int = 3, backoff: float = 0.1, exponential: bool = True):
    """Decorator để retry failed operations."""

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            delay = backoff
            last_exception = None

            for attempt in range(times):
                try:
                    return await fn(*args, **kwargs)
                except Retryable as e:
                    last_exception = e
                    if attempt == times - 1:
                        raise

                    await asyncio.sleep(delay)
                    if exponential:
                        delay *= 2
                except Exception:
                    # Non-retryable error
                    raise

            # Should not reach here
            raise last_exception or Exception("Retry failed")

        return wrapper

    return decorator


def instrument(
    metric_counter: Any = None,
    metric_histogram: Any = None,
    name: str = "",
    labels: dict[str, str] | None = None,
):
    """Decorator để thêm metrics instrumentation."""

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        method_name = name or fn.__name__
        metric_labels = labels or {}

        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            start_time = time.perf_counter()

            try:
                _ = await fn(*args, **kwargs)

                # Success metrics
                if metric_counter:
                    metric_counter.labels(
                        **metric_labels, method=method_name, status="success"
                    ).inc()

                return result

            except Exception as e:
                # Error metrics
                if metric_counter:
                    error_type = type(e).__name__
                    metric_counter.labels(
                        **metric_labels,
                        method=method_name,
                        status="error",
                        error_type=error_type,
                    ).inc()
                raise

            finally:
                # Duration metrics
                if metric_histogram:
                    duration = time.perf_counter() - start_time
                    metric_histogram.labels(
                        **metric_labels, method=method_name
                    ).observe(duration)

        return wrapper

    return decorator


def cached(ttl: int | None = None, key_func: Callable[..., str] | None = None):
    """Decorator để cache kết quả function."""

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            # Extract cache from first argument (usually service instance)
            if args and hasattr(args[0], "cache"):
                cache = args[0].cache

                # Generate cache key
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    # Default key generation
                    cache_key = f"{fn.__module__}.{fn.__name__}:{hash(str(args[1:]) + str(sorted(kwargs.items())))}"

                # Try to get from cache
                try:
                    await cache.get(cache_key)
                    if cached_result is not None:
                        return cached_result
                except Exception:
                    # Cache error, continue with normal execution
                    pass

                # Execute function
                _ = await fn(*args, **kwargs)

                # Store in cache
                try:
                    await cache.set(cache_key, result, ttl=ttl)
                except Exception:
                    # Cache error, ignore
                    pass

                return result
            else:
                # No cache available, execute normally
                return await fn(*args, **kwargs)

        return wrapper

    return decorator


class CircuitBreaker:
    """Simple circuit breaker implementation."""

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        expected_exception: type[Exception] = Exception,
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time: float | None = None
        self.state = "closed"  # closed, open, half-open

    def __call__(self, fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            if self.state == "open":
                if (
                    self.last_failure_time
                    and time.time() - self.last_failure_time >= self.timeout
                ):
                    self.state = "half-open"
                else:
                    raise CircuitBreakerOpen("Circuit breaker is open")

            try:
                _ = await fn(*args, **kwargs)

                # Success - reset failure count
                if self.state == "half-open":
                    self.state = "closed"
                self.failure_count = 0

                return result

            except self.expected_exception:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "open"

                raise

        return wrapper


def rate_limit(calls: int, period: float):
    """Simple rate limiting decorator."""

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        call_times: list[float] = []

        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> T:
            now = time.time()

            # Clean old calls
            call_times[:] = [t for t in call_times if now - t < period]

            # Check rate limit
            if len(call_times) >= calls:
                raise RateLimited(
                    f"Rate limit exceeded: {calls} calls per {period} seconds"
                )

            # Record this call
            call_times.append(now)

            return await fn(*args, **kwargs)

        return wrapper

    return decorator
