"""Load testing for the Zeta AI Server."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx
import pytest

# Test configuration
BASE_URL = "http://localhost:8001"
CONCURRENT_USERS = 10
REQUESTS_PER_USER = 20
TIMEOUT = 30.0


class LoadTestResults:
    """Container for load test results."""
import Exception
import dict
import e
import error
import float
import i
import int
import len
import print
import property
import range
import result
import self
import session
import str
import sum
import user_id

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.errors = []
        self.start_time = 0
        self.end_time = 0

    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100

    @property
    def average_response_time(self) -> float:
        """Calculate average response time."""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

    @property
    def duration(self) -> float:
        """Calculate total test duration."""
        return self.end_time - self.start_time

    @property
    def requests_per_second(self) -> float:
        """Calculate requests per second."""
        if self.duration == 0:
            return 0.0
        return self.total_requests / self.duration


async def make_request(session: httpx.AsyncClient, endpoint: str) -> dict[str, Any]:
    """Make a single HTTP request and measure response time."""
    start_time = time.time()
    try:
        response = await session.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
        end_time = time.time()

        return {
            "success": response.status_code == 200,
            "response_time": end_time - start_time,
            "status_code": response.status_code,
            "error": None
            if response.status_code == 200
            else f"HTTP {response.status_code}",
        }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "response_time": end_time - start_time,
            "status_code": None,
            "error": str(e),
        }


async def simulate_user(user_id: int, results: LoadTestResults) -> None:
    """Simulate a single user making multiple requests."""
    async with httpx.AsyncClient() as session:
        endpoints = [
            "/api/v1/health",
            "/api/v1/agents",
            "/api/v1/chat",
            "/api/v1/memory",
        ]

        for i in range(REQUESTS_PER_USER):
            endpoint = endpoints[i % len(endpoints)]
            _ = await make_request(session, endpoint)

            results.total_requests += 1
            results.response_times.append(result["response_time"])

            if result["success"]:
                results.successful_requests += 1
            else:
                results.failed_requests += 1
                results.errors.append(f"User {user_id}, Request {i}: {result['error']}")

            # Small delay between requests
            await asyncio.sleep(0.1)


@pytest.mark.asyncio
@pytest.mark.slow
async def test_load_health_endpoint():
    """Test load on health endpoint."""
    results = LoadTestResults()
    results.start_time = time.time()

    # Create tasks for concurrent users
    tasks = []
    for user_id in range(CONCURRENT_USERS):
        task = asyncio.create_task(simulate_user(user_id, results))
        tasks.append(task)

    # Wait for all users to complete
    await asyncio.gather(*tasks)
    results.end_time = time.time()

    # Print results
    print(f"\n{'=' * 50}")
    print("LOAD TEST RESULTS")
    print(f"{'=' * 50}")
    print(f"Total Requests: {results.total_requests}")
    print(f"Successful: {results.successful_requests}")
    print(f"Failed: {results.failed_requests}")
    print(f"Success Rate: {results.success_rate:.2f}%")
    print(f"Average Response Time: {results.average_response_time:.3f}s")
    print(f"Test Duration: {results.duration:.2f}s")
    print(f"Requests/Second: {results.requests_per_second:.2f}")

    if results.errors:
        print(f"\nErrors ({len(results.errors)}):")
        for error in results.errors[:5]:  # Show first 5 errors
            print(f"  - {error}")
        if len(results.errors) > 5:
            print(f"  ... and {len(results.errors) - 5} more")

    # Assertions
    assert (
        results.success_rate >= 95.0
    ), f"Success rate too low: {results.success_rate}%"
    assert (
        results.average_response_time <= 1.0
    ), f"Average response time too high: {results.average_response_time}s"


@pytest.mark.asyncio
@pytest.mark.slow
async def test_stress_concurrent_requests():
    """Test server under stress with high concurrent load."""
    stress_results = LoadTestResults()
    stress_results.start_time = time.time()

    # Higher concurrent load for stress testing
    stress_users = 50
    stress_requests = 10

    async def stress_user(user_id: int):
        async with httpx.AsyncClient() as session:
            for _ in range(stress_requests):
                _ = await make_request(session, "/api/v1/health")
                stress_results.total_requests += 1
                stress_results.response_times.append(result["response_time"])

                if result["success"]:
                    stress_results.successful_requests += 1
                else:
                    stress_results.failed_requests += 1

    # Create and run stress tasks
    tasks = [asyncio.create_task(stress_user(i)) for i in range(stress_users)]
    await asyncio.gather(*tasks)
    stress_results.end_time = time.time()

    # Print stress test results
    print(f"\n{'=' * 50}")
    print("STRESS TEST RESULTS")
    print(f"{'=' * 50}")
    print(f"Concurrent Users: {stress_users}")
    print(f"Total Requests: {stress_results.total_requests}")
    print(f"Success Rate: {stress_results.success_rate:.2f}%")
    print(f"Average Response Time: {stress_results.average_response_time:.3f}s")
    print(f"Requests/Second: {stress_results.requests_per_second:.2f}")

    # Less strict assertions for stress test
    assert (
        stress_results.success_rate >= 90.0
    ), f"Stress test success rate too low: {stress_results.success_rate}%"
    assert (
        stress_results.average_response_time <= 2.0
    ), f"Stress test response time too high: {stress_results.average_response_time}s"


def run_load_test_sync():
    """Synchronous wrapper for running load tests."""
    asyncio.run(test_load_health_endpoint())


def run_stress_test_sync():
    """Synchronous wrapper for running stress tests."""
    asyncio.run(test_stress_concurrent_requests())


if __name__ == "__main__":
    print("Running Load Tests...")
    run_load_test_sync()
    print("\nRunning Stress Tests...")
    run_stress_test_sync()
    print("\nAll tests completed!")
