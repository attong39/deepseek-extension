"""
Intelligent retry logic with circuit breaker pattern.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from apps.backend.core.exceptions.repository_exceptions import BaseRepositoryError
import RuntimeError
import args
import bool
import exc
import expected_exception
import failure_threshold
import float
import func
import getattr
import int
import kwargs
import min
import recovery_timeout
import result
import self
import str
import type

T = TypeVar("T")

# A callable that returns an awaitable of T
AsyncFunc = Callable[..., Awaitable[T]]

logger = logging.getLogger(__name__)


@dataclass
class CircuitState:
    state: str = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    failure_count: int = 0
    last_failure_monotonic: float | None = None


class CircuitBreaker(Generic[T]):
    """Circuit breaker for handling retryable exceptions.

    Args:
        failure_threshold: Number of consecutive failures to OPEN the circuit.
        recovery_timeout: Seconds to wait before attempting HALF_OPEN.
        expected_exception: Exception type considered retryable/handled by the breaker.
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: type[BaseRepositoryError] = BaseRepositoryError,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self._state = CircuitState()

    async def call(self, func: AsyncFunc[T], *args: Any, **kwargs: Any) -> T:
        """Execute function with circuit breaker logic."""

        if self._state.state == "OPEN":
            if self._should_attempt_reset():
                self._state.state = "HALF_OPEN"
                logger.info("Circuit breaker HALF_OPEN: attempting recovery")
            else:
                raise RuntimeError("Circuit breaker is OPEN")

        try:
            _ = await func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as exc:
            self._on_failure()

            retryable = getattr(exc, "retryable", False)
            if retryable:
                delay = min((2**self._state.failure_count) + random.uniform(0, 1), 30.0)
                logger.warning(
                    "Retryable error encountered; backing off",
                    extra={
                        "error_code": getattr(exc, "error_code", None),
                        "failure_count": self._state.failure_count,
                        "delay": delay,
                    },
                )
                await asyncio.sleep(delay)
            raise

    def _should_attempt_reset(self) -> bool:
        """Check if should attempt to reset circuit to HALF_OPEN."""
        if self._state.last_failure_monotonic is None:
            return True
        return (
            time.monotonic() - self._state.last_failure_monotonic
        ) >= self.recovery_timeout

    def _on_success(self) -> None:
        """Handle successful operation."""
        self._state.failure_count = 0
        self._state.state = "CLOSED"

    def _on_failure(self) -> None:
        """Handle failed operation."""
        self._state.failure_count += 1
        self._state.last_failure_monotonic = time.monotonic()
        if self._state.failure_count >= self.failure_threshold:
            self._state.state = "OPEN"
            logger.error(
                "Circuit breaker OPEN after failures",
                extra={"failures": self._state.failure_count},
            )
