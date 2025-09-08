"""
Performance Testing Suite

Comprehensive performance testing including load testing, stress testing,
and performance regression testing for the Zeta AI server.
"""

from __future__ import annotations

import asyncio
import logging
import random
import statistics
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import aiohttp
import pytest

from core.services.performance.profiler import PerformanceProfiler
import Exception
import ValueError
import all
import base_url
import bool
import dict
import e
import float
import i
import int
import isinstance
import len
import list
import load_result
import max
import min
import print
import r
import range
import request_id
import response
import response_time
import result
import self
import session
import sorted
import str
import tuple

logger = logging.getLogger(__name__)


@dataclass
class LoadTestConfig:
    """Configuration for load testing."""

    base_url: str
    total_requests: int = 1000
    concurrent_requests: int = 10
    request_delay_ms: int = 0
    timeout_seconds: int = 30
    ramp_up_seconds: int = 0
    endpoints: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class LoadTestResult:
    """Results from load testing."""

    total_requests: int
    successful_requests: int
    failed_requests: int
    total_duration_seconds: float
    average_response_time_ms: float
    min_response_time_ms: float
    max_response_time_ms: float
    p50_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    requests_per_second: float
    error_rate_percent: float
    errors: list[str] = field(default_factory=list)
    response_times: list[float] = field(default_factory=list)
    timestamps: list[datetime] = field(default_factory=list)


@dataclass
class EndpointTestCase:
    """Test case for an individual endpoint."""

    name: str
    method: str
    path: str
    headers: dict[str, str] | None = None
    payload: dict[str, Any] | None = None
    expected_status: int = 200
    weight: float = 1.0  # Relative frequency of this endpoint in load testing


class PerformanceTestSuite:
    """Comprehensive performance testing suite."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize performance test suite.

        Args:
            base_url: Base URL for the API server
        """
        self.base_url = base_url.rstrip("/")
        self.profiler = PerformanceProfiler()

        # Default test endpoints
        self.default_endpoints = [
            EndpointTestCase("health_check", "GET", "/health"),
            EndpointTestCase("api_health", "GET", "/api/v1/health/status"),
            EndpointTestCase("performance_stats", "GET", "/api/v1/performance/stats"),
            EndpointTestCase("system_metrics", "GET", "/api/v1/performance/system"),
            EndpointTestCase("agents_list", "GET", "/api/v1/agents"),
            EndpointTestCase("memory_status", "GET", "/api/v1/memory/status"),
        ]

        logger.info(f"Performance test suite initialized for {self.base_url}")

    async def run_load_test(
        self,
        config: LoadTestConfig,
        endpoints: list[EndpointTestCase] | None = None,
    ) -> LoadTestResult:
        """Run comprehensive load testing.

        Args:
            config: Load test configuration
            endpoints: Optional list of endpoints to test

        Returns:
            Load test results
        """
        endpoints = endpoints or self.default_endpoints
        if not endpoints:
            raise ValueError("No endpoints provided for load testing")

        logger.info(
            f"Starting load test: {config.total_requests} requests, "
            f"{config.concurrent_requests} concurrent"
        )

        start_time = time.perf_counter()
        errors = []

        # Create weighted endpoint list for random selection
        weighted_endpoints = []
        for endpoint in endpoints:
            count = int(endpoint.weight * 100)  # Convert weight to count
            weighted_endpoints.extend([endpoint] * count)

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=config.timeout_seconds)
        ) as session:
            # Create semaphore for concurrency control
            semaphore = asyncio.Semaphore(config.concurrent_requests)

            # Generate all requests
            tasks = []
            for i in range(config.total_requests):
                endpoint = random.choice(weighted_endpoints)
                task = self._make_request(session, semaphore, endpoint, config, i)
                tasks.append(task)

                # Add ramp-up delay
                if config.ramp_up_seconds > 0:
                    delay = (config.ramp_up_seconds * i) / config.total_requests
                    await asyncio.sleep(delay / 1000)  # Convert to seconds

            # Execute all requests
            request_results = await asyncio.gather(*tasks, return_exceptions=True)

        end_time = time.perf_counter()
        total_duration = end_time - start_time

        # Process results
        response_times = []
        successful_requests = 0
        failed_requests = 0
        timestamps = []

        for result in request_results:
            if isinstance(result, Exception):
                errors.append(str(result))
                failed_requests += 1
            elif isinstance(result, tuple):
                response_time, timestamp, success = result
                response_times.append(response_time)
                timestamps.append(timestamp)
                if success:
                    successful_requests += 1
                else:
                    failed_requests += 1

        # Calculate statistics
        if response_times:
            sorted_times = sorted(response_times)
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p50_response_time = statistics.median(response_times)
            p95_index = int(len(sorted_times) * 0.95)
            p99_index = int(len(sorted_times) * 0.99)
            p95_response_time = (
                sorted_times[p95_index]
                if p95_index < len(sorted_times)
                else max_response_time
            )
            p99_response_time = (
                sorted_times[p99_index]
                if p99_index < len(sorted_times)
                else max_response_time
            )
        else:
            avg_response_time = min_response_time = max_response_time = 0
            p50_response_time = p95_response_time = p99_response_time = 0

        requests_per_second = (
            config.total_requests / total_duration if total_duration > 0 else 0
        )
        error_rate = (
            (failed_requests / config.total_requests) * 100
            if config.total_requests > 0
            else 0
        )

        _ = LoadTestResult(
            total_requests=config.total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            total_duration_seconds=total_duration,
            average_response_time_ms=avg_response_time,
            min_response_time_ms=min_response_time,
            max_response_time_ms=max_response_time,
            p50_response_time_ms=p50_response_time,
            p95_response_time_ms=p95_response_time,
            p99_response_time_ms=p99_response_time,
            requests_per_second=requests_per_second,
            error_rate_percent=error_rate,
            errors=errors,
            response_times=response_times,
            timestamps=timestamps,
        )

        logger.info(
            f"Load test completed: {successful_requests}/{config.total_requests} successful, "
            f"{requests_per_second:.1f} RPS, {avg_response_time:.1f}ms avg response time"
        )

        return result

    async def _make_request(
        self,
        session: aiohttp.ClientSession,
        semaphore: asyncio.Semaphore,
        endpoint: EndpointTestCase,
        config: LoadTestConfig,
        request_id: int,
    ) -> tuple[float, datetime, bool]:
        """Make a single HTTP request.

        Returns:
            Tuple of (response_time_ms, timestamp, success)
        """
        async with semaphore:
            url = f"{self.base_url}{endpoint.path}"
            headers = endpoint.headers or {}

            start_time = time.perf_counter()
            timestamp = datetime.now()

            try:
                # Add request delay if configured
                if config.request_delay_ms > 0:
                    await asyncio.sleep(config.request_delay_ms / 1000)

                async with session.request(
                    endpoint.method,
                    url,
                    headers=headers,
                    json=endpoint.payload,
                ) as response:
                    await response.text()  # Consume response body
                    end_time = time.perf_counter()
                    response_time_ms = (end_time - start_time) * 1000

                    success = response.status == endpoint.expected_status
                    return response_time_ms, timestamp, success

            except Exception as e:
                end_time = time.perf_counter()
                response_time_ms = (end_time - start_time) * 1000
                logger.error(f"Request {request_id} failed: {e}")
                return response_time_ms, timestamp, False


# Pytest fixtures for testing
@pytest.fixture
def performance_suite():
    """Pytest fixture for performance test suite."""
    return PerformanceTestSuite()


@pytest.fixture
def mock_api():
    """Mock API for local testing."""

    class MockAPI:
        async def simulate_work(self, duration: float = 0.01):
            """Simulate API work."""
            await asyncio.sleep(duration)
            return {"status": "ok", "duration": duration}

    return MockAPI()


# Performance tests
@pytest.mark.asyncio
async def test_basic_load_performance(performance_suite):
    """Test basic load performance."""
    config = LoadTestConfig(
        base_url=performance_suite.base_url,
        total_requests=50,
        concurrent_requests=5,
    )

    _ = await performance_suite.run_load_test(config)

    # Performance assertions
    assert (
        result.error_rate_percent < 10.0
    ), f"Error rate too high: {result.error_rate_percent:.1f}%"
    assert (
        result.average_response_time_ms < 2000
    ), f"Average response time too slow: {result.average_response_time_ms:.1f}ms"
    assert (
        result.p95_response_time_ms < 5000
    ), f"P95 response time too slow: {result.p95_response_time_ms:.1f}ms"


@pytest.mark.asyncio
async def test_concurrent_operations(mock_api):
    """Test concurrent operation performance."""

    async def simulate_work():
        return await mock_api.simulate_work(0.01)

    # Run concurrent operations
    start_time = time.perf_counter()
    tasks = [simulate_work() for _ in range(100)]
    results = await asyncio.gather(*tasks)
    end_time = time.perf_counter()

    duration = end_time - start_time

    # Verify results
    assert len(results) == 100
    assert all(r["status"] == "ok" for r in results)
    assert duration < 1.0, f"Concurrent operations took too long: {duration:.3f}s"


@pytest.mark.asyncio
async def test_memory_performance(mock_api):
    """Test memory usage during operations."""
    import os

    import psutil

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Perform memory-intensive operations
    data = []
    for _ in range(1000):
        _ = await mock_api.simulate_work(0.001)
        data.append(result)

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory

    # Memory should not increase excessively
    assert memory_increase < 50, f"Memory usage increased by {memory_increase:.1f}MB"


class TestPerformanceRegression:
    """Performance regression testing."""

    @pytest.mark.asyncio
    async def test_response_time_regression(self, performance_suite):
        """Test that response times haven't regressed."""
        config = LoadTestConfig(
            base_url=performance_suite.base_url,
            total_requests=20,
            concurrent_requests=3,
        )

        _ = await performance_suite.run_load_test(config)

        # Baseline performance expectations
        baseline_avg_ms = 1000  # 1 second baseline
        baseline_p95_ms = 2000  # 2 second P95 baseline

        assert (
            result.average_response_time_ms < baseline_avg_ms
        ), f"Average response time regression: {result.average_response_time_ms:.1f}ms > {baseline_avg_ms}ms"

        assert (
            result.p95_response_time_ms < baseline_p95_ms
        ), f"P95 response time regression: {result.p95_response_time_ms:.1f}ms > {baseline_p95_ms}ms"

    @pytest.mark.asyncio
    async def test_throughput_regression(self, performance_suite):
        """Test that throughput hasn't regressed."""
        config = LoadTestConfig(
            base_url=performance_suite.base_url,
            total_requests=50,
            concurrent_requests=10,
        )

        _ = await performance_suite.run_load_test(config)

        # Baseline throughput expectations
        baseline_rps = 5  # 5 requests per second baseline

        assert (
            result.requests_per_second > baseline_rps
        ), f"Throughput regression: {result.requests_per_second:.1f} RPS < {baseline_rps} RPS"

    @pytest.mark.asyncio
    async def test_error_rate_regression(self, performance_suite):
        """Test that error rates haven't regressed."""
        config = LoadTestConfig(
            base_url=performance_suite.base_url,
            total_requests=30,
            concurrent_requests=5,
        )

        _ = await performance_suite.run_load_test(config)

        # Baseline error rate expectations
        baseline_error_rate = 10.0  # 10% baseline error rate

        assert (
            result.error_rate_percent < baseline_error_rate
        ), f"Error rate regression: {result.error_rate_percent:.1f}% > {baseline_error_rate}%"


if __name__ == "__main__":
    # Example usage
    async def main():
        suite = PerformanceTestSuite()

        # Run load test
        config = LoadTestConfig(
            base_url="http://localhost:8000",
            total_requests=100,
            concurrent_requests=10,
        )

        await suite.run_load_test(config)
        print(f"Load test completed: {load_result.requests_per_second:.1f} RPS")
        print(f"Average response time: {load_result.average_response_time_ms:.1f}ms")
        print(f"Error rate: {load_result.error_rate_percent:.1f}%")

    asyncio.run(main())
    asyncio.run(main())
