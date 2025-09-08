#!/usr/bin/env python3
"""
Performance monitoring script for Zeta AI.

Monitors API response times, database query performance,
memory usage, and system metrics with alerting.
"""

import asyncio
import json
import logging
import statistics
import time
from datetime import datetime, timedelta
from pathlib import Path

import aiohttp
import asyncpg
import redis.asyncio as redis
from pydantic import BaseModel, Field
import Exception
import ImportError
import ValueError
import abs
import api_metrics
import change
import db_metrics
import dict
import e
import endpoint
import f
import float
import int
import isinstance
import len
import list
import m
import max
import metric
import metric_name
import min
import monitor
import op_name
import open
import operation
import print
import query
import query_name
import range
import redis_metrics
import response
import self
import str
import sum
import trend
import tuple


class PerformanceConfig(BaseModel):
    """Performance monitoring configuration."""

    # Service endpoints
    api_base_url: str = "http://localhost:8000"
    database_url: str = "postgresql://user:pass@localhost:5432/zeta_db"
    redis_url: str = "redis://localhost:6379"

    # Monitoring settings
    check_interval: int = Field(default=30, description="Check interval in seconds")
    sample_size: int = Field(default=10, description="Number of samples per metric")

    # Performance thresholds
    api_response_threshold: float = Field(default=2.0, description="API response time threshold (seconds)")
    db_query_threshold: float = Field(default=1.0, description="DB query time threshold (seconds)")
    memory_threshold: float = Field(default=80.0, description="Memory usage threshold (%)")
    cpu_threshold: float = Field(default=75.0, description="CPU usage threshold (%)")

    # Alert settings
    alert_webhook_url: str | None = None
    metrics_retention_days: int = Field(default=7, description="Metrics retention period")


class PerformanceMetric(BaseModel):
    """Performance metric data point."""

    name: str
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = "normal"  # "normal", "warning", "critical"
    details: dict = Field(default_factory=dict)


class PerformanceMonitor:
    """Performance monitoring manager."""

    def __init__(self, config: PerformanceConfig):
        self.config = config
        self.logger = self._setup_logging()
        self.session: aiohttp.ClientSession | None = None
        self.metrics_history: dict[str, list[PerformanceMetric]] = {}

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for performance monitoring."""
        logger = logging.getLogger("performance_monitor")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # File handler for performance logs
            log_dir = Path("./logs")
            log_dir.mkdir(exist_ok=True)

            file_handler = logging.FileHandler(log_dir / "performance_monitor.log")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def measure_api_performance(self) -> list[PerformanceMetric]:
        """Measure API endpoint performance."""
        endpoints = ["/health", "/api/v1/health", "/api/v1/agents", "/api/v1/chat"]

        metrics = []

        for endpoint in endpoints:
            url = f"{self.config.api_base_url}{endpoint}"
            response_times = []

            # Take multiple samples
            for _ in range(self.config.sample_size):
                start_time = time.time()
                try:
                    async with self.session.get(url) as response:
                        response_time = time.time() - start_time
                        if response.status < 500:  # Don't count server errors
                            response_times.append(response_time)

                        await asyncio.sleep(0.1)  # Small delay between requests

                except Exception as e:
                    self.logger.warning(f"API request failed for {endpoint}: {e!s}")
                    continue

            if response_times:
                avg_response_time = statistics.mean(response_times)
                max_response_time = max(response_times)
                min_response_time = min(response_times)

                status = "normal"
                if avg_response_time > self.config.api_response_threshold:
                    status = "warning"
                if avg_response_time > self.config.api_response_threshold * 2:
                    status = "critical"

                metrics.append(
                    PerformanceMetric(
                        name=f"api_response_time_{endpoint.replace('/', '_')}",
                        value=avg_response_time,
                        unit="seconds",
                        status=status,
                        details={
                            "max": max_response_time,
                            "min": min_response_time,
                            "samples": len(response_times),
                            "endpoint": endpoint,
                        },
                    )
                )

        return metrics

    async def measure_database_performance(self) -> list[PerformanceMetric]:
        """Measure database query performance."""
        metrics = []

        try:
            conn = await asyncpg.connect(self.config.database_url)

            try:
                # Test queries with timing
                test_queries = [
                    ("simple_select", "SELECT 1"),
                    ("table_count", "SELECT count(*) FROM information_schema.tables"),
                    ("connection_stats", "SELECT count(*) FROM pg_stat_activity"),
                ]

                for query_name, query in test_queries:
                    query_times = []

                    for _ in range(min(5, self.config.sample_size)):
                        start_time = time.time()
                        try:
                            await conn.fetchval(query)
                            query_time = time.time() - start_time
                            query_times.append(query_time)
                        except Exception as e:
                            self.logger.warning(f"Query failed {query_name}: {e!s}")
                            continue

                    if query_times:
                        avg_query_time = statistics.mean(query_times)

                        status = "normal"
                        if avg_query_time > self.config.db_query_threshold:
                            status = "warning"
                        if avg_query_time > self.config.db_query_threshold * 3:
                            status = "critical"

                        metrics.append(
                            PerformanceMetric(
                                name=f"db_query_time_{query_name}",
                                value=avg_query_time,
                                unit="seconds",
                                status=status,
                                details={"query": query, "samples": len(query_times)},
                            )
                        )

                # Database connection stats
                stats_query = """
                SELECT
                    count(*) as total_connections,
                    sum(case when state = 'active' then 1 else 0 end) as active_connections,
                    sum(case when state = 'idle' then 1 else 0 end) as idle_connections
                FROM pg_stat_activity
                WHERE datname = current_database()
                """

                stats = await conn.fetchrow(stats_query)

                metrics.append(
                    PerformanceMetric(
                        name="db_total_connections",
                        value=float(stats["total_connections"]),
                        unit="count",
                        details={
                            "active": stats["active_connections"],
                            "idle": stats["idle_connections"],
                        },
                    )
                )

            finally:
                await conn.close()

        except Exception as e:
            self.logger.error(f"Database performance check failed: {e!s}")
            metrics.append(
                PerformanceMetric(
                    name="db_connection_error",
                    value=1.0,
                    unit="boolean",
                    status="critical",
                    details={"error": str(e)},
                )
            )

        return metrics

    async def measure_redis_performance(self) -> list[PerformanceMetric]:
        """Measure Redis performance."""
        metrics = []

        try:
            redis_client = redis.from_url(self.config.redis_url)

            try:
                # Test Redis operations
                operations = [
                    ("ping", lambda: redis_client.ping()),
                    ("set_get", lambda: self._test_redis_set_get(redis_client)),
                ]

                for op_name, operation in operations:
                    op_times = []

                    for _ in range(self.config.sample_size):
                        start_time = time.time()
                        try:
                            await operation()
                            op_time = time.time() - start_time
                            op_times.append(op_time)
                        except Exception as e:
                            self.logger.warning(f"Redis operation failed {op_name}: {e!s}")
                            continue

                    if op_times:
                        avg_op_time = statistics.mean(op_times)

                        metrics.append(
                            PerformanceMetric(
                                name=f"redis_{op_name}_time",
                                value=avg_op_time,
                                unit="seconds",
                                details={"samples": len(op_times)},
                            )
                        )

                # Redis info metrics
                info = await redis_client.info()

                metrics.extend(
                    [
                        PerformanceMetric(
                            name="redis_connected_clients",
                            value=float(info.get("connected_clients", 0)),
                            unit="count",
                        ),
                        PerformanceMetric(
                            name="redis_used_memory",
                            value=float(info.get("used_memory", 0)),
                            unit="bytes",
                        ),
                        PerformanceMetric(
                            name="redis_keyspace_hits",
                            value=float(info.get("keyspace_hits", 0)),
                            unit="count",
                        ),
                        PerformanceMetric(
                            name="redis_keyspace_misses",
                            value=float(info.get("keyspace_misses", 0)),
                            unit="count",
                        ),
                    ]
                )

            finally:
                await redis_client.close()

        except Exception as e:
            self.logger.error(f"Redis performance check failed: {e!s}")
            metrics.append(
                PerformanceMetric(
                    name="redis_connection_error",
                    value=1.0,
                    unit="boolean",
                    status="critical",
                    details={"error": str(e)},
                )
            )

        return metrics

    async def _test_redis_set_get(self, redis_client) -> None:
        """Test Redis SET/GET operations."""
        test_key = f"perf_test_{int(time.time())}"
        test_value = "performance_test_value"

        await redis_client.set(test_key, test_value)
        result = await redis_client.get(test_key)
        await redis_client.delete(test_key)

        if result.decode() != test_value:
            raise ValueError("Redis SET/GET test failed")

    def measure_system_performance(self) -> list[PerformanceMetric]:
        """Measure system performance metrics."""
        metrics = []

        try:
            import psutil

            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            status = "normal"
            if cpu_percent > self.config.cpu_threshold:
                status = "warning"
            if cpu_percent > self.config.cpu_threshold * 1.2:
                status = "critical"

            metrics.append(
                PerformanceMetric(
                    name="system_cpu_percent",
                    value=cpu_percent,
                    unit="percent",
                    status=status,
                )
            )

            # Memory metrics
            memory = psutil.virtual_memory()
            mem_status = "normal"
            if memory.percent > self.config.memory_threshold:
                mem_status = "warning"
            if memory.percent > self.config.memory_threshold * 1.1:
                mem_status = "critical"

            metrics.extend(
                [
                    PerformanceMetric(
                        name="system_memory_percent",
                        value=memory.percent,
                        unit="percent",
                        status=mem_status,
                    ),
                    PerformanceMetric(
                        name="system_memory_available",
                        value=memory.available / (1024**3),
                        unit="gb",
                    ),
                ]
            )

            # Disk metrics
            disk = psutil.disk_usage("/")
            metrics.extend(
                [
                    PerformanceMetric(name="system_disk_percent", value=disk.percent, unit="percent"),
                    PerformanceMetric(name="system_disk_free", value=disk.free / (1024**3), unit="gb"),
                ]
            )

        except ImportError:
            self.logger.warning("psutil not available for system metrics")
        except Exception as e:
            self.logger.error(f"System performance check failed: {e!s}")

        return metrics

    def calculate_trend(self, metric_name: str) -> tuple[str, float]:
        """Calculate performance trend for a metric."""
        if metric_name not in self.metrics_history:
            return "unknown", 0.0

        history = self.metrics_history[metric_name]
        if len(history) < 2:
            return "stable", 0.0

        # Get recent values (last hour)
        recent_time = datetime.now() - timedelta(minutes=60)
        recent_values = [m.value for m in history if m.timestamp > recent_time]

        if len(recent_values) < 2:
            return "stable", 0.0

        # Calculate trend
        first_half = recent_values[: len(recent_values) // 2]
        second_half = recent_values[len(recent_values) // 2 :]

        if not first_half or not second_half:
            return "stable", 0.0

        avg_first = statistics.mean(first_half)
        avg_second = statistics.mean(second_half)

        if avg_first == 0:
            return "stable", 0.0

        change_percent = ((avg_second - avg_first) / avg_first) * 100

        if abs(change_percent) < 5:
            return "stable", change_percent
        elif change_percent > 0:
            return "increasing", change_percent
        else:
            return "decreasing", change_percent

    def store_metrics(self, metrics: list[PerformanceMetric]) -> None:
        """Store metrics in history."""
        for metric in metrics:
            if metric.name not in self.metrics_history:
                self.metrics_history[metric.name] = []

            self.metrics_history[metric.name].append(metric)

            # Keep only recent metrics
            cutoff_time = datetime.now() - timedelta(days=self.config.metrics_retention_days)
            self.metrics_history[metric.name] = [
                m for m in self.metrics_history[metric.name] if m.timestamp > cutoff_time
            ]

    async def run_performance_checks(self) -> list[PerformanceMetric]:
        """Run all performance checks."""
        self.logger.info("Running performance checks...")

        all_metrics = []

        # Run checks concurrently
        api_metrics, db_metrics, redis_metrics = await asyncio.gather(
            self.measure_api_performance(),
            self.measure_database_performance(),
            self.measure_redis_performance(),
            return_exceptions=True,
        )

        # Add successful metrics
        for metrics in [api_metrics, db_metrics, redis_metrics]:
            if isinstance(metrics, list):
                all_metrics.extend(metrics)

        # Add system metrics
        system_metrics = self.measure_system_performance()
        all_metrics.extend(system_metrics)

        # Store metrics
        self.store_metrics(all_metrics)

        return all_metrics

    async def generate_performance_report(self) -> dict:
        """Generate performance summary report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "metrics": [],
            "trends": {},
            "alerts": [],
        }

        # Run performance checks
        current_metrics = await self.run_performance_checks()

        # Add current metrics to report
        report["metrics"] = [metric.dict() for metric in current_metrics]

        # Calculate trends
        for metric_name in self.metrics_history.keys():
            trend, change = self.calculate_trend(metric_name)
            report["trends"][metric_name] = {
                "direction": trend,
                "change_percent": change,
            }

        # Identify performance issues
        for metric in current_metrics:
            if metric.status in ("warning", "critical"):
                report["alerts"].append(
                    {
                        "metric": metric.name,
                        "status": metric.status,
                        "value": metric.value,
                        "message": f"{metric.name} is {metric.status}: {metric.value} {metric.unit}",
                    }
                )

        # Summary statistics
        total_metrics = len(current_metrics)
        warning_count = sum(1 for m in current_metrics if m.status == "warning")
        critical_count = sum(1 for m in current_metrics if m.status == "critical")

        report["summary"] = {
            "total_metrics": total_metrics,
            "normal_count": total_metrics - warning_count - critical_count,
            "warning_count": warning_count,
            "critical_count": critical_count,
            "overall_status": "critical" if critical_count > 0 else "warning" if warning_count > 0 else "normal",
        }

        return report


async def main():
    """Main performance monitoring function."""
    try:
        # Load configuration
        config = PerformanceConfig()

        # Parse command line arguments
        import argparse

        parser = argparse.ArgumentParser(description="Zeta AI Performance Monitor")
        parser.add_argument("--report", action="store_true", help="Generate performance report")
        parser.add_argument("--output", help="Output file for report")

        args = parser.parse_args()

        async with PerformanceMonitor(config) as monitor:
            if args.report:
                # Generate report
                report = await monitor.generate_performance_report()

                if args.output:
                    with open(args.output, "w") as f:
                        json.dump(report, f, indent=2)
                    print(f"Performance report saved to {args.output}")
                else:
                    print(json.dumps(report, indent=2))

                # Exit with error code if critical issues found
                return 1 if report["summary"]["critical_count"] > 0 else 0
            else:
                # Run performance checks
                metrics = await monitor.run_performance_checks()

                print("\n=== Performance Check Results ===")
                for metric in metrics:
                    status_icon = {"normal": "✅", "warning": "⚠️", "critical": "❌"}
                    print(f"{status_icon.get(metric.status, '❓')} {metric.name}: {metric.value:.3f} {metric.unit}")

                return 0

    except Exception as e:
        logging.error(f"Performance monitoring error: {e!s}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))
