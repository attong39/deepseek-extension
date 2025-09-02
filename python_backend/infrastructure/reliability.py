"""
Infrastructure components: Circuit Breaker, Retry Service, Rate Limiter, Input Sanitizer.
Các component hỗ trợ reliability và security.
"""

import asyncio
import html
import random
import re
import time
from enum import Enum
from typing import Any, Callable, Dict, Optional

from core.domain.interfaces import (
    CircuitBreakerInterface,
    InputSanitizerInterface,
    MetricsServiceInterface,
    RateLimiterInterface,
    RetryServiceInterface,
)


class CircuitBreakerState(Enum):
    """Trạng thái của Circuit Breaker"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject all requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreakerService(CircuitBreakerInterface):
    """
    Circuit Breaker implementation để fail-fast khi service không available.
    Implement 3 states: CLOSED -> OPEN -> HALF_OPEN -> CLOSED
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: int = 60,
        metrics: Optional[MetricsServiceInterface] = None
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.metrics = metrics

        self._failure_count = 0
        self._last_failure_time = 0
        self._state = CircuitBreakerState.CLOSED
        self._next_attempt_time = 0

    @property
    def is_open(self) -> bool:
        """Kiểm tra circuit breaker có đang open không"""
        return self._state == CircuitBreakerState.OPEN

    @property
    def failure_count(self) -> int:
        """Số lượng failures hiện tại"""
        return self._failure_count

    @property
    def state(self) -> CircuitBreakerState:
        """Current state của circuit breaker"""
        return self._state

    def reset(self) -> None:
        """Reset circuit breaker về trạng thái closed"""
        self._failure_count = 0
        self._state = CircuitBreakerState.CLOSED
        self._next_attempt_time = 0

        if self.metrics:
            self.metrics.increment_counter("circuit_breaker_resets")
            self.metrics.set_gauge("circuit_breaker_state", 0)  # 0 = CLOSED

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function với circuit breaker protection"""
        current_time = time.time()

        # Check if we should transition from OPEN to HALF_OPEN
        if (self._state == CircuitBreakerState.OPEN and
            current_time >= self._next_attempt_time):
            self._state = CircuitBreakerState.HALF_OPEN
            if self.metrics:
                self.metrics.set_gauge("circuit_breaker_state", 0.5)  # 0.5 = HALF_OPEN

        # Reject request if circuit breaker is OPEN
        if self._state == CircuitBreakerState.OPEN:
            if self.metrics:
                self.metrics.increment_counter("circuit_breaker_rejections")
            raise RuntimeError("Circuit breaker is OPEN - service unavailable")

        try:
            # Execute function
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            # Success - reset failure count và transition to CLOSED
            if self._state == CircuitBreakerState.HALF_OPEN:
                self.reset()
                if self.metrics:
                    self.metrics.increment_counter("circuit_breaker_half_open_successes")
            else:
                self._failure_count = 0

            if self.metrics:
                self.metrics.increment_counter("circuit_breaker_successes")

            return result

        except Exception:
            # Failure - increment count và possibly transition to OPEN
            self._failure_count += 1
            self._last_failure_time = current_time

            if self.metrics:
                self.metrics.increment_counter("circuit_breaker_failures")

            # Transition to OPEN if threshold reached
            if (self._failure_count >= self.failure_threshold or
                self._state == CircuitBreakerState.HALF_OPEN):
                self._state = CircuitBreakerState.OPEN
                self._next_attempt_time = current_time + self.reset_timeout

                if self.metrics:
                    self.metrics.increment_counter("circuit_breaker_opens")
                    self.metrics.set_gauge("circuit_breaker_state", 1)  # 1 = OPEN

            raise


class ExponentialBackoffRetryService(RetryServiceInterface):
    """
    Retry service với exponential backoff và jitter.
    """

    def __init__(self, metrics: Optional[MetricsServiceInterface] = None):
        self.metrics = metrics

    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        **kwargs
    ) -> Any:
        """Execute function với retry logic"""

        for attempt in range(max_retries + 1):
            try:
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

                if self.metrics:
                    self.metrics.increment_counter("retry_successes", {"attempt": str(attempt)})

                return result

            except Exception:
                if self.metrics:
                    self.metrics.increment_counter("retry_attempts", {"attempt": str(attempt)})

                # Re-raise nếu đây là attempt cuối
                if attempt >= max_retries:
                    if self.metrics:
                        self.metrics.increment_counter("retry_exhausted", {"max_retries": str(max_retries)})
                    raise

                # Calculate delay với exponential backoff
                delay = min(base_delay * (exponential_base ** attempt), max_delay)

                # Add jitter để tránh thundering herd
                if jitter:
                    delay *= (0.5 + random.random() * 0.5)

                if self.metrics:
                    self.metrics.record_histogram("retry_delay_seconds", delay)

                await asyncio.sleep(delay)

        # Should never reach here
        raise RuntimeError("Retry logic error")


class TokenBucketRateLimiter(RateLimiterInterface):
    """
    Token bucket rate limiter implementation.
    """

    def __init__(self, metrics: Optional[MetricsServiceInterface] = None):
        self.metrics = metrics
        self._buckets: dict[str, dict[str, Any]] = {}

    async def is_allowed(self, key: str, limit: int, window_seconds: int) -> bool:
        """Kiểm tra xem request có được phép không"""
        current_time = time.time()

        # Initialize bucket nếu chưa có
        if key not in self._buckets:
            self._buckets[key] = {
                "tokens": limit,
                "last_refill": current_time,
                "limit": limit,
                "window_seconds": window_seconds
            }

        bucket = self._buckets[key]

        # Refill tokens dựa trên thời gian đã qua
        time_passed = current_time - bucket["last_refill"]
        tokens_to_add = (time_passed / window_seconds) * limit
        bucket["tokens"] = min(limit, bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = current_time

        # Check if có token available
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            if self.metrics:
                self.metrics.increment_counter("rate_limit_allowed", {"key": key})
            return True
        else:
            if self.metrics:
                self.metrics.increment_counter("rate_limit_rejected", {"key": key})
            return False

    async def get_remaining(self, key: str, limit: int, window_seconds: int) -> int:
        """Lấy số requests còn lại trong window"""
        current_time = time.time()

        if key not in self._buckets:
            return limit

        bucket = self._buckets[key]

        # Refill tokens
        time_passed = current_time - bucket["last_refill"]
        tokens_to_add = (time_passed / window_seconds) * limit
        bucket["tokens"] = min(limit, bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = current_time

        return int(bucket["tokens"])


class InputSanitizer(InputSanitizerInterface):
    """
    Input sanitization service cho security.
    """

    def __init__(self, metrics: Optional[MetricsServiceInterface] = None):
        self.metrics = metrics

        # Patterns để detect malicious input
        self._sql_injection_patterns = [
            r"(union\s+select)",
            r"(drop\s+table)",
            r"(insert\s+into)",
            r"(delete\s+from)",
            r"(update\s+set)",
            r"(exec\s*\()",
            r"(script\s*>)",
        ]

        self._xss_patterns = [
            r"<script[^>]*>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>",
        ]

        self._command_injection_patterns = [
            r"(;\s*rm\s)",
            r"(;\s*cat\s)",
            r"(\|\s*nc\s)",
            r"(&&\s*curl)",
            r"(`[^`]*`)",
        ]

    def sanitize_text(self, text: str) -> str:
        """Sanitize text input"""
        if not text:
            return ""

        sanitized = text

        # HTML escape
        sanitized = html.escape(sanitized, quote=True)

        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')

        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()

        # Limit length
        if len(sanitized) > 10000:
            sanitized = sanitized[:10000]
            if self.metrics:
                self.metrics.increment_counter("input_truncated")

        if self.metrics:
            self.metrics.increment_counter("input_sanitized")

        return sanitized

    def validate_input(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Validate và sanitize input data"""
        sanitized_data = {}

        for key, value in input_data.items():
            if isinstance(value, str):
                sanitized_data[key] = self.sanitize_text(value)
            elif isinstance(value, dict):
                sanitized_data[key] = self.validate_input(value)
            elif isinstance(value, list):
                sanitized_data[key] = [
                    self.sanitize_text(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                sanitized_data[key] = value

        return sanitized_data

    def is_safe_input(self, text: str) -> bool:
        """Kiểm tra input có safe không"""
        if not text:
            return True

        text_lower = text.lower()

        # Check SQL injection patterns
        for pattern in self._sql_injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                if self.metrics:
                    self.metrics.increment_counter("unsafe_input_detected", {"type": "sql_injection"})
                return False

        # Check XSS patterns
        for pattern in self._xss_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                if self.metrics:
                    self.metrics.increment_counter("unsafe_input_detected", {"type": "xss"})
                return False

        # Check command injection patterns
        for pattern in self._command_injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                if self.metrics:
                    self.metrics.increment_counter("unsafe_input_detected", {"type": "command_injection"})
                return False

        return True
