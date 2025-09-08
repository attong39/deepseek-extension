#!/usr/bin/env python3
"""
Load testing script for Zeta AI.

Performs load testing on API endpoints to measure performance
under various load conditions and identify bottlenecks.
"""

import asyncio
import json
import logging
import random
import statistics
import time
from datetime import datetime
from pathlib import Path

import aiohttp
from pydantic import BaseModel, Field
import Exception
import TimeoutError
import ValueError
import bool
import dict
import e
import error
import f
import float
import int
import len
import list
import max
import min
import open
import percentile
import print
import r
import range
import response
import self
import set
import sorted
import stats
import str
import tester
import user_id


class LoadTestConfig(BaseModel):
    """Load testing configuration."""

    # Target settings
    base_url: str = "http://localhost:8000"
    endpoints: list[str] = Field(
        default_factory=lambda: [
            "/health",
            "/api/v1/health",
            "/api/v1/agents",
            "/api/v1/chat",
        ]
    )

    # Load settings
    total_requests: int = Field(default=1000, description="Total number of requests")
    concurrent_users: int = Field(default=50, description="Number of concurrent users")
    ramp_up_time: int = Field(default=30, description="Ramp up time in seconds")
    test_duration: int = Field(default=300, description="Test duration in seconds")

    # Request settings
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    think_time_min: float = Field(default=0.1, description="Minimum think time between requests")
    think_time_max: float = Field(default=2.0, description="Maximum think time between requests")

    # Test data
    test_payloads: dict[str, dict] = Field(
        default_factory=lambda: {
            "/api/v1/chat": {
                "message": "Hello, this is a load test message",
                "agent_id": "test_agent",
            },
            "/api/v1/agents": {"name": "Load Test Agent", "model": "gpt-3.5-turbo"},
        }
    )

    # Output settings
    output_dir: str = Field(default="./load_test_results", description="Output directory")
    detailed_logging: bool = Field(default=False, description="Enable detailed request logging")


class LoadTestResult(BaseModel):
    """Individual request result."""

    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    error_message: str | None = None
    timestamp: datetime = Field(default_factory=datetime.now)
    user_id: int = 0


class LoadTestReport(BaseModel):
    """Load test summary report."""

    config: LoadTestConfig
    start_time: datetime
    end_time: datetime
    total_duration: float
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    p50_response_time: float
    p95_response_time: float
    p99_response_time: float
    requests_per_second: float
    error_rate: float
    endpoint_stats: dict[str, dict] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)


class LoadTester:
    """Load testing manager."""

    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.results: list[LoadTestResult] = []
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session: aiohttp.ClientSession | None = None
        self.active_users = 0
        self.test_start_time = None

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for load testing."""
        logger = logging.getLogger("load_tester")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # File handler for load test logs
            log_file = self.output_dir / "load_test.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    async def __aenter__(self):
        """Async context manager entry."""
        connector = aiohttp.TCPConnector(limit=self.config.concurrent_users * 2)
        timeout = aiohttp.ClientTimeout(total=self.config.request_timeout)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def make_request(self, endpoint: str, user_id: int) -> LoadTestResult:
        """Make a single request to an endpoint."""
        url = f"{self.config.base_url}{endpoint}"
        method = "GET"
        payload = None

        # Determine method and payload based on endpoint
        if endpoint in self.config.test_payloads:
            payload = self.config.test_payloads[endpoint]
            method = "POST"

        start_time = time.time()

        try:
            if method == "POST" and payload:
                async with self.session.post(url, json=payload) as response:
                    await response.text()  # Read response to ensure completion
                    response_time = time.time() - start_time

                    return LoadTestResult(
                        endpoint=endpoint,
                        method=method,
                        status_code=response.status,
                        response_time=response_time,
                        success=response.status < 400,
                        user_id=user_id,
                    )
            else:
                async with self.session.get(url) as response:
                    await response.text()  # Read response to ensure completion
                    response_time = time.time() - start_time

                    return LoadTestResult(
                        endpoint=endpoint,
                        method=method,
                        status_code=response.status,
                        response_time=response_time,
                        success=response.status < 400,
                        user_id=user_id,
                    )

        except TimeoutError:
            response_time = time.time() - start_time
            return LoadTestResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message="Request timeout",
                user_id=user_id,
            )
        except Exception as e:
            response_time = time.time() - start_time
            return LoadTestResult(
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message=str(e),
                user_id=user_id,
            )

    async def simulate_user(self, user_id: int) -> None:
        """Simulate a single user's behavior."""
        self.active_users += 1

        try:
            # Calculate when this user should stop
            time.time()
            test_end_time = self.test_start_time + self.config.test_duration

            while time.time() < test_end_time:
                # Select random endpoint
                endpoint = random.choice(self.config.endpoints)

                # Make request
                result = await self.make_request(endpoint, user_id)
                self.results.append(result)

                if self.config.detailed_logging:
                    status = "✅" if result.success else "❌"
                    self.logger.info(
                        f"User {user_id}: {status} {result.method} {result.endpoint} "
                        f"({result.status_code}) {result.response_time:.3f}s"
                    )

                # Think time between requests
                think_time = random.uniform(self.config.think_time_min, self.config.think_time_max)
                await asyncio.sleep(think_time)

        except Exception as e:
            self.logger.error(f"User {user_id} encountered error: {e!s}")
        finally:
            self.active_users -= 1

    async def ramp_up_users(self) -> None:
        """Gradually ramp up users over the specified time."""
        if self.config.ramp_up_time <= 0:
            # Start all users immediately
            tasks = [self.simulate_user(user_id) for user_id in range(self.config.concurrent_users)]
            await asyncio.gather(*tasks)
        else:
            # Gradual ramp up
            delay_between_users = self.config.ramp_up_time / self.config.concurrent_users
            tasks = []

            for user_id in range(self.config.concurrent_users):
                task = asyncio.create_task(self.simulate_user(user_id))
                tasks.append(task)

                if user_id < self.config.concurrent_users - 1:
                    await asyncio.sleep(delay_between_users)

            # Wait for all users to complete
            await asyncio.gather(*tasks)

    def calculate_percentile(self, values: list[float], percentile: float) -> float:
        """Calculate percentile value."""
        if not values:
            return 0.0

        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)

        if index >= len(sorted_values):
            index = len(sorted_values) - 1

        return sorted_values[index]

    def generate_report(self) -> LoadTestReport:
        """Generate comprehensive load test report."""
        if not self.results:
            raise ValueError("No test results available")

        # Calculate overall statistics
        successful_results = [r for r in self.results if r.success]
        failed_results = [r for r in self.results if not r.success]

        response_times = [r.response_time for r in self.results]
        successful_response_times = [r.response_time for r in successful_results]

        total_requests = len(self.results)
        successful_requests = len(successful_results)
        failed_requests = len(failed_results)

        # Calculate time-based metrics
        if self.results:
            start_time = min(r.timestamp for r in self.results)
            end_time = max(r.timestamp for r in self.results)
            total_duration = (end_time - start_time).total_seconds()
        else:
            start_time = datetime.now()
            end_time = datetime.now()
            total_duration = 0.0

        requests_per_second = total_requests / total_duration if total_duration > 0 else 0.0
        error_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0.0

        # Calculate response time percentiles
        avg_response_time = statistics.mean(response_times) if response_times else 0.0
        min_response_time = min(response_times) if response_times else 0.0
        max_response_time = max(response_times) if response_times else 0.0
        p50_response_time = self.calculate_percentile(successful_response_times, 50)
        p95_response_time = self.calculate_percentile(successful_response_times, 95)
        p99_response_time = self.calculate_percentile(successful_response_times, 99)

        # Calculate per-endpoint statistics
        endpoint_stats = {}
        for endpoint in self.config.endpoints:
            endpoint_results = [r for r in self.results if r.endpoint == endpoint]

            if endpoint_results:
                endpoint_successful = [r for r in endpoint_results if r.success]
                endpoint_response_times = [r.response_time for r in endpoint_successful]

                endpoint_stats[endpoint] = {
                    "total_requests": len(endpoint_results),
                    "successful_requests": len(endpoint_successful),
                    "failed_requests": len(endpoint_results) - len(endpoint_successful),
                    "avg_response_time": statistics.mean(endpoint_response_times) if endpoint_response_times else 0.0,
                    "p95_response_time": self.calculate_percentile(endpoint_response_times, 95),
                    "error_rate": ((len(endpoint_results) - len(endpoint_successful)) / len(endpoint_results) * 100),
                }

        # Collect error messages
        errors = list(set(r.error_message for r in failed_results if r.error_message))

        report = LoadTestReport(
            config=self.config,
            start_time=start_time,
            end_time=end_time,
            total_duration=total_duration,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            avg_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            p50_response_time=p50_response_time,
            p95_response_time=p95_response_time,
            p99_response_time=p99_response_time,
            requests_per_second=requests_per_second,
            error_rate=error_rate,
            endpoint_stats=endpoint_stats,
            errors=errors,
        )

        return report

    async def run_load_test(self) -> LoadTestReport:
        """Execute the complete load test."""
        self.logger.info("Starting load test...")
        self.logger.info(f"Target: {self.config.base_url}")
        self.logger.info(f"Concurrent users: {self.config.concurrent_users}")
        self.logger.info(f"Test duration: {self.config.test_duration}s")
        self.logger.info(f"Ramp up time: {self.config.ramp_up_time}s")

        self.test_start_time = time.time()

        # Start user simulation
        await self.ramp_up_users()

        self.logger.info("Load test completed")
        self.logger.info(f"Total requests made: {len(self.results)}")

        # Generate report
        report = self.generate_report()

        # Save detailed results
        await self._save_detailed_results()

        # Save report
        report_file = self.output_dir / "load_test_report.json"
        with open(report_file, "w") as f:
            json.dump(report.dict(), f, indent=2, default=str)

        self.logger.info(f"Load test report saved to {report_file}")

        return report

    async def _save_detailed_results(self) -> None:
        """Save detailed test results to CSV."""
        csv_file = self.output_dir / "load_test_results.csv"

        with open(csv_file, "w") as f:
            # Write CSV header
            f.write("timestamp,endpoint,method,status_code,response_time,success,error_message,user_id\n")

            # Write results
            for result in self.results:
                f.write(
                    f"{result.timestamp.isoformat()},"
                    f"{result.endpoint},"
                    f"{result.method},"
                    f"{result.status_code},"
                    f"{result.response_time},"
                    f"{result.success},"
                    f"{result.error_message or ''},"
                    f"{result.user_id}\n"
                )

        self.logger.info(f"Detailed results saved to {csv_file}")

    def print_report_summary(self, report: LoadTestReport) -> None:
        """Print load test summary to console."""
        print("\n" + "=" * 60)
        print("🚀 LOAD TEST RESULTS")
        print("=" * 60)

        print(f"🎯 Target: {report.config.base_url}")
        print(f"👥 Concurrent Users: {report.config.concurrent_users}")
        print(f"⏱️  Duration: {report.total_duration:.1f}s")
        print(f"📊 Total Requests: {report.total_requests}")
        print(f"✅ Successful: {report.successful_requests}")
        print(f"❌ Failed: {report.failed_requests}")
        print(f"📈 Error Rate: {report.error_rate:.1f}%")
        print(f"🚀 Requests/sec: {report.requests_per_second:.1f}")

        print("\n📊 RESPONSE TIMES:")
        print(f"  Average: {report.avg_response_time:.3f}s")
        print(f"  Minimum: {report.min_response_time:.3f}s")
        print(f"  Maximum: {report.max_response_time:.3f}s")
        print(f"  50th percentile: {report.p50_response_time:.3f}s")
        print(f"  95th percentile: {report.p95_response_time:.3f}s")
        print(f"  99th percentile: {report.p99_response_time:.3f}s")

        print("\n📍 ENDPOINT BREAKDOWN:")
        for endpoint, stats in report.endpoint_stats.items():
            print(f"  {endpoint}:")
            print(f"    Requests: {stats['total_requests']}")
            print(f"    Avg Response: {stats['avg_response_time']:.3f}s")
            print(f"    P95 Response: {stats['p95_response_time']:.3f}s")
            print(f"    Error Rate: {stats['error_rate']:.1f}%")

        if report.errors:
            print("\n❌ ERRORS ENCOUNTERED:")
            for error in report.errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(report.errors) > 5:
                print(f"  ... and {len(report.errors) - 5} more errors")

        print("\n" + "=" * 60)


async def main():
    """Main load testing function."""
    try:
        # Parse command line arguments
        import argparse

        parser = argparse.ArgumentParser(description="Zeta AI Load Tester")
        parser.add_argument("--config", help="Configuration file path")
        parser.add_argument("--url", help="Base URL to test")
        parser.add_argument("--users", type=int, help="Number of concurrent users")
        parser.add_argument("--duration", type=int, help="Test duration in seconds")
        parser.add_argument("--requests", type=int, help="Total number of requests")
        parser.add_argument("--verbose", action="store_true", help="Enable detailed logging")

        args = parser.parse_args()

        # Load configuration
        config = LoadTestConfig()

        if args.config and Path(args.config).exists():
            with open(args.config) as f:
                config_data = json.load(f)
                config = LoadTestConfig(**config_data)

        # Override with command line arguments
        if args.url:
            config.base_url = args.url
        if args.users:
            config.concurrent_users = args.users
        if args.duration:
            config.test_duration = args.duration
        if args.requests:
            config.total_requests = args.requests
        if args.verbose:
            config.detailed_logging = True

        # Run load test
        async with LoadTester(config) as tester:
            report = await tester.run_load_test()
            tester.print_report_summary(report)

            # Exit with error code if error rate is too high
            return 1 if report.error_rate > 5.0 else 0

    except Exception as e:
        logging.error(f"Load test error: {e!s}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))
