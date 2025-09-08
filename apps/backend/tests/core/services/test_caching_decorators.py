from __future__ import annotations

import asyncio
import os
import time
from typing import Any, Dict, List, Optional

import psutil
import pytest
from apps.backend.core.caching.decorators import CircuitBreakerCache, cache_result
from apps.backend.core.observability.logging import get_logger
import ConnectionError
import Exception
import RuntimeError
import ValueError
import bool
import data
import delay
import dict
import float
import hasattr
import int
import key
import len
import list
import optional
import range
import self
import should_error
import size
import str
import sum
import value
import x
import y

"""Unit tests for caching decorators functionality.
This module contains comprehensive unit tests for caching decorators
including cache_result, CircuitBreakerCache, and compression utilities.
"""


class TestCacheResultDecorator:
    """Test cases for cache_result decorator."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.logger = get_logger(__name__)

    def teardown_method(self) -> None:
        """Clean up after each test method."""

    @pytest.mark.asyncio
    async def test_cache_result_basic_caching(self) -> None:
        """Test basic caching functionality."""
        call_count = 0

        @cache_result(ttl_seconds=60)
        async def expensive_function(x: int, y: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.01)  # Simulate work
            return x + y

        result1 = await expensive_function(2, 3)
        assert result1 == 5
        assert call_count == 1
        result2 = await expensive_function(2, 3)
        assert result2 == 5
        assert call_count == 1  # Should not increase
        result3 = await expensive_function(3, 4)
        assert result3 == 7
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_cache_result_with_ttl(self) -> None:
        """Test cache expiration with TTL."""
        call_count = 0

        @cache_result(ttl_seconds=0.1)  # Very short TTL
        async def short_lived_cache(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = await short_lived_cache(5)
        assert result1 == 10
        assert call_count == 1
        result2 = await short_lived_cache(5)
        assert result2 == 10
        assert call_count == 1
        await asyncio.sleep(0.15)
        result3 = await short_lived_cache(5)
        assert result3 == 10
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_cache_result_with_complex_args(self) -> None:
        """Test caching with complex argument types."""
        call_count = 0

        @cache_result(ttl_seconds=60)
        async def complex_args_function(
            data: dict[str, Any], items: list[int], optional: str | None = None
        ) -> dict[str, Any]:
            nonlocal call_count
            call_count += 1
            return {
                "data": data,
                "sum": sum(items),
                "optional": optional,
                "call_count": call_count,
            }

        args1 = ({"key": "value"}, [1, 2, 3], "test")
        args2 = ({"key": "value"}, [1, 2, 3], "test")  # Same args
        args3 = ({"key": "different"}, [1, 2, 3], "test")  # Different args
        result1 = await complex_args_function(*args1)
        assert result1["sum"] == 6
        assert result1["call_count"] == 1
        result2 = await complex_args_function(*args2)
        assert result2["sum"] == 6
        assert result2["call_count"] == 1  # Should be cached value
        result3 = await complex_args_function(*args3)
        assert result3["sum"] == 6
        assert result3["call_count"] == 2

    @pytest.mark.asyncio
    async def test_cache_result_error_handling(self) -> None:
        """Test error handling in cached functions."""
        call_count = 0

        @cache_result(ttl_seconds=60)
        async def error_function(should_error: bool) -> str:
            nonlocal call_count
            call_count += 1
            if should_error:
                raise ValueError("Test error")
            return "success"

        result1 = await error_function(False)
        assert result1 == "success"
        assert call_count == 1
        result2 = await error_function(False)
        assert result2 == "success"
        assert call_count == 1
        with pytest.raises(ValueError, match="Test error"):
            await error_function(True)
        assert call_count == 2
        with pytest.raises(ValueError, match="Test error"):
            await error_function(True)
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_cache_result_with_compression(self) -> None:
        """Test caching with compression enabled."""
        call_count = 0

        @cache_result(ttl_seconds=60, compress=True)
        async def large_data_function(size: int) -> str:
            nonlocal call_count
            call_count += 1
            return "x" * size  # Large string

        result1 = await large_data_function(1000)
        assert len(result1) == 1000
        assert call_count == 1
        result2 = await large_data_function(1000)
        assert len(result2) == 1000
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_cache_result_concurrent_access(self) -> None:
        """Test concurrent access to cached function."""
        call_count = 0

        @cache_result(ttl_seconds=60)
        async def concurrent_function(delay: float) -> str:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(delay)
            return f"result_{call_count}"

        async def call_function():
            return await concurrent_function(0.05)

        tasks = [call_function() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        assert len(set(results)) == 1
        assert call_count == 1


class TestCircuitBreakerCache:
    """Test cases for CircuitBreakerCache class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.logger = get_logger(__name__)
        self.cache = CircuitBreakerCache(
            failure_threshold=3, recovery_timeout=1.0, expected_exception=Exception
        )

    def teardown_method(self) -> None:
        """Clean up after each test method."""

    @pytest.mark.asyncio
    async def test_initialization(self) -> None:
        """Test CircuitBreakerCache initialization."""
        assert self.cache is not None
        assert hasattr(self.cache, "_failure_count")
        assert hasattr(self.cache, "_last_failure_time")
        assert hasattr(self.cache, "_state")

    @pytest.mark.asyncio
    async def test_successful_operation(self) -> None:
        """Test successful operation through circuit breaker."""

        async def successful_operation():
            return "success"

        result = await self.cache.call(successful_operation)
        assert result == "success"
        assert self.cache._failure_count == 0
        assert self.cache._state == "closed"

    @pytest.mark.asyncio
    async def test_failure_handling(self) -> None:
        """Test failure handling and circuit opening."""

        async def failing_operation():
            raise ValueError("Test failure")

        with pytest.raises(ValueError):
            await self.cache.call(failing_operation)
        assert self.cache._failure_count == 1
        assert self.cache._state == "closed"
        with pytest.raises(ValueError):
            await self.cache.call(failing_operation)
        assert self.cache._failure_count == 2
        assert self.cache._state == "closed"
        with pytest.raises(ValueError):
            await self.cache.call(failing_operation)
        assert self.cache._failure_count == 3
        assert self.cache._state == "open"

    @pytest.mark.asyncio
    async def test_circuit_open_behavior(self) -> None:
        """Test behavior when circuit is open."""

        async def failing_operation():
            raise ValueError("Test failure")

        for _ in range(3):
            try:
                await self.cache.call(failing_operation)
            except ValueError:
                pass
        assert self.cache._state == "open"
        with pytest.raises(Exception):  # Should raise circuit breaker exception
            await self.cache.call(failing_operation)

    @pytest.mark.asyncio
    async def test_circuit_recovery(self) -> None:
        """Test circuit recovery after timeout."""

        async def failing_operation():
            raise ValueError("Test failure")

        for _ in range(3):
            try:
                await self.cache.call(failing_operation)
            except ValueError:
                pass
        assert self.cache._state == "open"
        await asyncio.sleep(1.1)

        async def successful_operation():
            return "recovered"

        result = await self.cache.call(successful_operation)
        assert result == "recovered"
        assert self.cache._state == "closed"
        assert self.cache._failure_count == 0

    @pytest.mark.asyncio
    async def test_half_open_state(self) -> None:
        """Test half-open state behavior."""

        async def failing_operation():
            raise ValueError("Test failure")

        for _ in range(3):
            try:
                await self.cache.call(failing_operation)
            except ValueError:
                pass
        assert self.cache._state == "open"
        await asyncio.sleep(1.1)
        with pytest.raises(ValueError):
            await self.cache.call(failing_operation)
        assert self.cache._state == "open"  # Back to open
        await asyncio.sleep(1.1)

        async def successful_operation():
            return "success"

        result = await self.cache.call(successful_operation)
        assert result == "success"
        assert self.cache._state == "closed"

    @pytest.mark.asyncio
    async def test_different_exception_types(self) -> None:
        """Test circuit breaker with different exception types."""
        cache = CircuitBreakerCache(failure_threshold=2, expected_exception=ValueError)

        async def value_error_operation():
            raise ValueError("Value error")

        async def runtime_error_operation():
            raise RuntimeError("Runtime error")

        with pytest.raises(ValueError):
            await cache.call(value_error_operation)
        assert cache._failure_count == 1
        with pytest.raises(RuntimeError):
            await cache.call(runtime_error_operation)
        assert cache._failure_count == 1  # Should not increase

    @pytest.mark.asyncio
    async def test_configuration_management(self) -> None:
        """Test configuration management for circuit breaker."""
        config = {
            "circuit_breaker": {
                "failure_threshold": 5,
                "recovery_timeout": 2.0,
                "expected_exception": "ConnectionError",
            }
        }
        await self.cache.configure(config)


class TestCachingIntegration:
    """Integration tests for caching components."""

    @pytest.mark.asyncio
    async def test_cache_with_circuit_breaker(self) -> None:
        """Test cache decorator with circuit breaker."""
        call_count = 0

        @cache_result(ttl_seconds=60)
        async def unreliable_operation():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise ConnectionError("Network error")
            return "success"

        cache = CircuitBreakerCache(failure_threshold=3)
        for _ in range(2):
            with pytest.raises(ConnectionError):
                await cache.call(unreliable_operation)
        result = await cache.call(unreliable_operation)
        assert result == "success"
        result = await cache.call(unreliable_operation)
        assert result == "success"
        assert call_count == 3  # Only 3 actual calls

    @pytest.mark.asyncio
    async def test_performance_comparison(self) -> None:
        """Test performance comparison with and without caching."""
        call_count = 0

        async def expensive_operation():
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)  # Simulate expensive operation
            return "expensive_result"

        @cache_result(ttl_seconds=60)
        async def cached_expensive_operation():
            return await expensive_operation()

        start_time = time.time()
        for _ in range(3):
            await expensive_operation()
        uncached_time = time.time() - start_time
        call_count = 0
        start_time = time.time()
        for _ in range(3):
            await cached_expensive_operation()
        cached_time = time.time() - start_time
        assert cached_time < uncached_time
        assert call_count == 1  # Only one actual call

    @pytest.mark.asyncio
    async def test_memory_usage_with_compression(self) -> None:
        """Test memory usage with compression enabled."""
        process = psutil.Process(os.getpid())

        @cache_result(ttl_seconds=60, compress=True)
        async def large_data_operation(size: int):
            return "x" * size

        initial_memory = process.memory_info().rss
        for size in [10000, 20000, 30000]:
            await large_data_operation(size)
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        assert memory_increase < 10 * 1024 * 1024  # Less than 10MB


class MockRedis:
    """Mock Redis client for testing."""

    def __init__(self):
        self.data = {}

    async def get(self, key: str) -> str | None:
        """Mock get operation."""
        return self.data.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        """Mock set operation."""
        self.data[key] = value
        return True

    async def delete(self, key: str) -> int:
        """Mock delete operation."""
        if key in self.data:
            del self.data[key]
            return 1
        return 0


if __name__ == "__main__":
    pytest.main([__file__])
__all__ = [
    "MockRedis",
    "TestCacheResultDecorator",
    "TestCachingIntegration",
    "TestCircuitBreakerCache",
    "args1",
    "args2",
    "args3",
    "cache",
    "cached_expensive_operation",
    "cached_time",
    "call_count",
    "call_function",
    "complex_args_function",
    "concurrent_function",
    "config",
    "delete",
    "error_function",
    "expensive_function",
    "expensive_operation",
    "failing_operation",
    "final_memory",
    "get",
    "initial_memory",
    "large_data_function",
    "large_data_operation",
    "memory_increase",
    "process",
    "result",
    "result1",
    "result2",
    "result3",
    "results",
    "runtime_error_operation",
    "set",
    "setup_method",
    "short_lived_cache",
    "start_time",
    "successful_operation",
    "tasks",
    "teardown_method",
    "test_cache_result_basic_caching",
    "test_cache_result_concurrent_access",
    "test_cache_result_error_handling",
    "test_cache_result_with_complex_args",
    "test_cache_result_with_compression",
    "test_cache_result_with_ttl",
    "test_cache_with_circuit_breaker",
    "test_circuit_open_behavior",
    "test_circuit_recovery",
    "test_configuration_management",
    "test_different_exception_types",
    "test_failure_handling",
    "test_half_open_state",
    "test_initialization",
    "test_memory_usage_with_compression",
    "test_performance_comparison",
    "test_successful_operation",
    "uncached_time",
    "unreliable_operation",
    "value_error_operation",
]
