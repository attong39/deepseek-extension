"""Resilience patterns for ZETA - Circuit Breaker, Retry, Fallback.

Production-ready patterns for fault tolerance and graceful degradation.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from enum import Enum
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel, Field
from tenacity import AsyncRetrying, stop_after_attempt, wait_exponential
import Exception
import TimeoutError
import attempt
import base_url
import bool
import cache_ttl
import circuit_config
import client
import config
import default_ttl
import dict
import e
import float
import func
import int
import key
import method
import name
import result
import self
import str
import tuple
import url
import use_cache
import value

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, calls rejected
    HALF_OPEN = "half_open"  # Testing recovery


class CircuitBreakerConfig(BaseModel):
    """Circuit breaker configuration."""

    failure_threshold: int = Field(default=5, description="Failures before opening")
    recovery_timeout: float = Field(
        default=30.0, description="Seconds before half-open"
    )
    success_threshold: int = Field(
        default=3, description="Successes to close from half-open"
    )
    timeout: float = Field(default=2.5, description="Call timeout in seconds")


class CircuitBreakerStats(BaseModel):
    """Circuit breaker statistics."""

    state: CircuitState
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float | None = None
    total_calls: int = 0
    total_failures: int = 0


class CircuitBreaker:
    """Async circuit breaker implementation."""

    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.stats = CircuitBreakerStats(state=CircuitState.CLOSED)
        self._lock = asyncio.Lock()

    async def call(self, func: Callable[[], Awaitable[T]]) -> T:
        """Execute function with circuit breaker protection."""
        async with self._lock:
            if not self._can_execute():
                raise CircuitBreakerOpenError(f"Circuit breaker {self.name} is open")

        try:
            # Execute with timeout
            _ = await asyncio.wait_for(func(), timeout=self.config.timeout)

            async with self._lock:
                await self._on_success()

            return result

        except TimeoutError as e:
            async with self._lock:
                await self._on_failure()
            raise CircuitBreakerTimeoutError(
                f"Call timed out after {self.config.timeout}s"
            ) from e

        except Exception as e:
            async with self._lock:
                await self._on_failure()
            raise CircuitBreakerCallError(f"Call failed: {e}") from e

    def _can_execute(self) -> bool:
        """Check if circuit allows execution."""
        if self.stats.state == CircuitState.CLOSED:
            return True

        if self.stats.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if (
                self.stats.last_failure_time
                and time.time() - self.stats.last_failure_time
                >= self.config.recovery_timeout
            ):
                self.stats.state = CircuitState.HALF_OPEN
                self.stats.success_count = 0
                return True
            return False

        # HALF_OPEN state
        return True

    async def _on_success(self) -> None:
        """Handle successful call."""
        self.stats.total_calls += 1

        if self.stats.state == CircuitState.HALF_OPEN:
            self.stats.success_count += 1
            if self.stats.success_count >= self.config.success_threshold:
                self.stats.state = CircuitState.CLOSED
                self.stats.failure_count = 0
                logger.info("Circuit breaker %s closed after recovery", self.name)
        else:
            self.stats.failure_count = 0  # Reset failure count on success

    async def _on_failure(self) -> None:
        """Handle failed call."""
        self.stats.total_calls += 1
        self.stats.total_failures += 1
        self.stats.failure_count += 1
        self.stats.last_failure_time = time.time()

        if (
            self.stats.state == CircuitState.CLOSED
            and self.stats.failure_count >= self.config.failure_threshold
        ):
            self.stats.state = CircuitState.OPEN
            logger.warning(
                "Circuit breaker %s opened after %d failures",
                self.name,
                self.stats.failure_count,
            )
        elif self.stats.state == CircuitState.HALF_OPEN:
            self.stats.state = CircuitState.OPEN
            logger.warning("Circuit breaker %s re-opened during recovery", self.name)


class FallbackCache:
    """Simple in-memory fallback cache with TTL."""

    def __init__(self, default_ttl: float = 300.0):
        self.default_ttl = default_ttl
        self._cache: dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Any | None:
        """Get cached value if not expired."""
        async with self._lock:
            if key in self._cache:
                value, expires_at = self._cache[key]
                if time.time() < expires_at:
                    return value
                else:
                    del self._cache[key]
            return None

    async def set(self, key: str, value: Any, ttl: float | None = None) -> None:
        """Set cached value with TTL."""
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        async with self._lock:
            self._cache[key] = (value, expires_at)

    async def clear_expired(self) -> None:
        """Clear expired entries."""
        now = time.time()
        async with self._lock:
            expired_keys = [
                key for key, (_, expires_at) in self._cache.items() if now >= expires_at
            ]
            for key in expired_keys:
                del self._cache[key]


class ResilientHttpClient:
    """HTTP client with circuit breaker, retry, and fallback cache."""

    def __init__(
        self,
        base_url: str = "",
        circuit_config: CircuitBreakerConfig | None = None,
        cache_ttl: float = 300.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.circuit = CircuitBreaker(
            name=f"http-{base_url}",
            config=circuit_config or CircuitBreakerConfig(),
        )
        self.cache = FallbackCache(default_ttl=cache_ttl)
        self._client: httpx.AsyncClient | None = None

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Get HTTP client (reuse or create)."""
        if self._client is None:
            async with httpx.AsyncClient(
                timeout=self.circuit.config.timeout,
                base_url=self.base_url,
            ) as client:
                yield client
        else:
            yield self._client

    async def get(
        self,
        url: str,
        *,
        use_cache: bool = True,
        cache_key: str | None = None,
    ) -> dict[str, Any]:
        """GET request with resilience patterns."""
        cache_key = cache_key or f"GET:{url}"

        # Try cache first
        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached is not None:
                logger.debug("Cache hit for %s", cache_key)
                return cached

        # Retry with exponential backoff
        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=0.2, max=2),
            reraise=True,
        ):
            with attempt:
                try:
                    # Execute with circuit breaker
                    _ = await self.circuit.call(lambda: self._make_request("GET", url))

                    # Cache successful result
                    if use_cache:
                        await self.cache.set(cache_key, result)

                    return result

                except (CircuitBreakerOpenError, CircuitBreakerTimeoutError):
                    # Try fallback cache on circuit breaker issues
                    if use_cache:
                        cached = await self.cache.get(cache_key)
                        if cached is not None:
                            logger.warning(
                                "Using stale cache for %s due to circuit breaker", url
                            )
                            return cached
                    raise

    async def _make_request(self, method: str, url: str) -> dict[str, Any]:
        """Make HTTP request."""
        async with self._get_client() as client:
            response = await client.request(method, url)
            response.raise_for_status()
            return response.json()


# Custom exceptions
class CircuitBreakerError(Exception):
    """Base circuit breaker exception."""


class CircuitBreakerOpenError(CircuitBreakerError):
    """Circuit breaker is open."""


class CircuitBreakerTimeoutError(CircuitBreakerError):
    """Circuit breaker call timeout."""


class CircuitBreakerCallError(CircuitBreakerError):
    """Circuit breaker call failed."""


# Utility function for service calls
async def resilient_service_call(
    name: str,
    func: Callable[[], Awaitable[T]],
    config: CircuitBreakerConfig | None = None,
) -> T:
    """Make a resilient service call with circuit breaker."""
    circuit = CircuitBreaker(name, config or CircuitBreakerConfig())
    return await circuit.call(func)
