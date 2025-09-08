import Exception
import KeyboardInterrupt
import all
import any
import check
import dict
import e
import endpoint_name
import exit
import f
import float
import int
import isinstance
import len
import list
import open
import print
import round
import self
import str
import sum
import url
# Author: Duy BG VN
# ZETA AI - Health Monitoring Script

"""Application health monitoring and diagnostics.

Provides comprehensive health checks for all system components
including API endpoints, database, cache, external services.
"""

import asyncio
import json
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import httpx
import psutil

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health check status levels."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheckResult:
    """Individual health check result."""

    service_name: str
    status: HealthStatus
    response_time_ms: float
    timestamp: datetime
    message: str | None = None
    details: dict[str, Any] | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["status"] = self.status.value
        result["timestamp"] = self.timestamp.isoformat()
        return result


@dataclass
class SystemHealthReport:
    """Overall system health report."""

    overall_status: HealthStatus
    timestamp: datetime
    checks: list[HealthCheckResult]
    summary: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "overall_status": self.overall_status.value,
            "timestamp": self.timestamp.isoformat(),
            "checks": [check.to_dict() for check in self.checks],
            "summary": self.summary,
        }


class HealthMonitor:
    """Comprehensive health monitoring system."""

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize health monitor.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.timeout = self.config.get("timeout", 10.0)
        self.retry_attempts = self.config.get("retry_attempts", 3)

        # API endpoints to check
        self.api_endpoints = self.config.get(
            "api_endpoints",
            {
                "health": "http://localhost:8000/api/v1/health",
                "agents": "http://localhost:8000/api/v1/agents",
                "chat": "http://localhost:8000/api/v1/chat/health",
            },
        )

        # Database settings
        self.database_config = self.config.get(
            "database",
            {"type": "sqlite", "path": "./zeta.db", "connection_string": None},
        )

        # Cache settings
        self.cache_config = self.config.get("cache", {"type": "redis", "host": "localhost", "port": 6379})

        # External services
        self.external_services = self.config.get(
            "external_services",
            {
                "openai": {"enabled": True},
                "anthropic": {"enabled": False},
                "pinecone": {"enabled": False},
            },
        )

    async def check_api_endpoints(self) -> list[HealthCheckResult]:
        """Check all API endpoints health.

        Returns:
            List of health check results
        """
        results = []

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for endpoint_name, url in self.api_endpoints.items():
                start_time = time.time()

                try:
                    response = await client.get(url)
                    response_time = (time.time() - start_time) * 1000

                    if response.status_code == 200:
                        status = HealthStatus.HEALTHY
                        message = f"API endpoint {endpoint_name} is healthy"
                        details = {
                            "status_code": response.status_code,
                            "content_length": len(response.content),
                        }
                        error = None
                    else:
                        status = HealthStatus.DEGRADED
                        message = f"API endpoint {endpoint_name} returned status {response.status_code}"
                        details = {"status_code": response.status_code}
                        error = f"HTTP {response.status_code}"

                    result = HealthCheckResult(
                        service_name=f"api_{endpoint_name}",
                        status=status,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message=message,
                        details=details,
                        error=error,
                    )

                except httpx.TimeoutException:
                    response_time = (time.time() - start_time) * 1000
                    result = HealthCheckResult(
                        service_name=f"api_{endpoint_name}",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message=f"API endpoint {endpoint_name} timed out",
                        error="Timeout",
                    )

                except Exception as e:
                    response_time = (time.time() - start_time) * 1000
                    result = HealthCheckResult(
                        service_name=f"api_{endpoint_name}",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message=f"API endpoint {endpoint_name} failed",
                        error=str(e),
                    )

                results.append(result)
                logger.info(f"Checked {endpoint_name}: {result.status.value} ({result.response_time_ms:.2f}ms)")

        return results

    async def check_database(self) -> HealthCheckResult:
        """Check database connectivity and health.

        Returns:
            Database health check result
        """
        start_time = time.time()

        try:
            if self.database_config["type"] == "sqlite":
                # Check SQLite database
                import sqlite3

                db_path = self.database_config["path"]
                if not Path(db_path).exists():
                    return HealthCheckResult(
                        service_name="database",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=0.0,
                        timestamp=datetime.now(),
                        message="Database file not found",
                        error=f"File not found: {db_path}",
                    )

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                conn.close()

                response_time = (time.time() - start_time) * 1000

                if result:
                    return HealthCheckResult(
                        service_name="database",
                        status=HealthStatus.HEALTHY,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message="SQLite database is healthy",
                        details={"type": "sqlite", "path": db_path},
                    )
                else:
                    return HealthCheckResult(
                        service_name="database",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message="Database query failed",
                        error="No result from test query",
                    )

            elif self.database_config["type"] == "postgresql":
                # Check PostgreSQL database
                import asyncpg

                conn_string = self.database_config["connection_string"]
                if not conn_string:
                    return HealthCheckResult(
                        service_name="database",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=0.0,
                        timestamp=datetime.now(),
                        message="No PostgreSQL connection string provided",
                        error="Missing connection string",
                    )

                conn = await asyncpg.connect(conn_string)
                result = await conn.fetchval("SELECT 1")
                await conn.close()

                response_time = (time.time() - start_time) * 1000

                return HealthCheckResult(
                    service_name="database",
                    status=HealthStatus.HEALTHY,
                    response_time_ms=response_time,
                    timestamp=datetime.now(),
                    message="PostgreSQL database is healthy",
                    details={"type": "postgresql"},
                )

            else:
                return HealthCheckResult(
                    service_name="database",
                    status=HealthStatus.UNKNOWN,
                    response_time_ms=0.0,
                    timestamp=datetime.now(),
                    message=f"Unsupported database type: {self.database_config['type']}",
                    error="Unsupported database type",
                )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                service_name="database",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=response_time,
                timestamp=datetime.now(),
                message="Database health check failed",
                error=str(e),
            )

    async def check_cache(self) -> HealthCheckResult:
        """Check cache system health.

        Returns:
            Cache health check result
        """
        start_time = time.time()

        try:
            if self.cache_config["type"] == "redis":
                import redis.asyncio as redis

                host = self.cache_config["host"]
                port = self.cache_config["port"]

                client = redis.Redis(host=host, port=port, decode_responses=True)

                # Test basic operations
                await client.ping()
                await client.set("health_check", "ok", ex=60)
                result = await client.get("health_check")
                await client.delete("health_check")
                await client.aclose()

                response_time = (time.time() - start_time) * 1000

                if result == "ok":
                    return HealthCheckResult(
                        service_name="cache",
                        status=HealthStatus.HEALTHY,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message="Redis cache is healthy",
                        details={"type": "redis", "host": host, "port": port},
                    )
                else:
                    return HealthCheckResult(
                        service_name="cache",
                        status=HealthStatus.DEGRADED,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message="Redis cache operations failed",
                        error="Test operations failed",
                    )

            else:
                return HealthCheckResult(
                    service_name="cache",
                    status=HealthStatus.UNKNOWN,
                    response_time_ms=0.0,
                    timestamp=datetime.now(),
                    message=f"Unsupported cache type: {self.cache_config['type']}",
                    error="Unsupported cache type",
                )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                service_name="cache",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=response_time,
                timestamp=datetime.now(),
                message="Cache health check failed",
                error=str(e),
            )

    async def check_system_resources(self) -> list[HealthCheckResult]:
        """Check system resource health.

        Returns:
            List of system resource health checks
        """
        results = []

        try:
            # CPU check
            cpu_percent = psutil.cpu_percent(interval=1)

            if cpu_percent < 70:
                cpu_status = HealthStatus.HEALTHY
                cpu_message = f"CPU usage is normal ({cpu_percent:.1f}%)"
            elif cpu_percent < 90:
                cpu_status = HealthStatus.DEGRADED
                cpu_message = f"CPU usage is elevated ({cpu_percent:.1f}%)"
            else:
                cpu_status = HealthStatus.UNHEALTHY
                cpu_message = f"CPU usage is critical ({cpu_percent:.1f}%)"

            results.append(
                HealthCheckResult(
                    service_name="cpu",
                    status=cpu_status,
                    response_time_ms=1000.0,  # 1 second interval
                    timestamp=datetime.now(),
                    message=cpu_message,
                    details={
                        "cpu_percent": cpu_percent,
                        "cpu_count": psutil.cpu_count(),
                    },
                )
            )

            # Memory check
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            if memory_percent < 70:
                memory_status = HealthStatus.HEALTHY
                memory_message = f"Memory usage is normal ({memory_percent:.1f}%)"
            elif memory_percent < 90:
                memory_status = HealthStatus.DEGRADED
                memory_message = f"Memory usage is elevated ({memory_percent:.1f}%)"
            else:
                memory_status = HealthStatus.UNHEALTHY
                memory_message = f"Memory usage is critical ({memory_percent:.1f}%)"

            results.append(
                HealthCheckResult(
                    service_name="memory",
                    status=memory_status,
                    response_time_ms=0.0,
                    timestamp=datetime.now(),
                    message=memory_message,
                    details={
                        "memory_percent": memory_percent,
                        "total_gb": round(memory.total / (1024**3), 2),
                        "available_gb": round(memory.available / (1024**3), 2),
                    },
                )
            )

            # Disk check
            disk = psutil.disk_usage("/")
            disk_percent = (disk.used / disk.total) * 100

            if disk_percent < 80:
                disk_status = HealthStatus.HEALTHY
                disk_message = f"Disk usage is normal ({disk_percent:.1f}%)"
            elif disk_percent < 95:
                disk_status = HealthStatus.DEGRADED
                disk_message = f"Disk usage is elevated ({disk_percent:.1f}%)"
            else:
                disk_status = HealthStatus.UNHEALTHY
                disk_message = f"Disk usage is critical ({disk_percent:.1f}%)"

            results.append(
                HealthCheckResult(
                    service_name="disk",
                    status=disk_status,
                    response_time_ms=0.0,
                    timestamp=datetime.now(),
                    message=disk_message,
                    details={
                        "disk_percent": disk_percent,
                        "total_gb": round(disk.total / (1024**3), 2),
                        "free_gb": round(disk.free / (1024**3), 2),
                    },
                )
            )

        except Exception as e:
            results.append(
                HealthCheckResult(
                    service_name="system_resources",
                    status=HealthStatus.UNHEALTHY,
                    response_time_ms=0.0,
                    timestamp=datetime.now(),
                    message="System resource check failed",
                    error=str(e),
                )
            )

        return results

    async def check_external_services(self) -> list[HealthCheckResult]:
        """Check external services health.

        Returns:
            List of external service health checks
        """
        results = []

        # Check internet connectivity
        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("https://httpbin.org/get")
                response_time = (time.time() - start_time) * 1000

                if response.status_code == 200:
                    results.append(
                        HealthCheckResult(
                            service_name="internet_connectivity",
                            status=HealthStatus.HEALTHY,
                            response_time_ms=response_time,
                            timestamp=datetime.now(),
                            message="Internet connectivity is healthy",
                        )
                    )
                else:
                    results.append(
                        HealthCheckResult(
                            service_name="internet_connectivity",
                            status=HealthStatus.DEGRADED,
                            response_time_ms=response_time,
                            timestamp=datetime.now(),
                            message="Internet connectivity issues detected",
                            error=f"HTTP {response.status_code}",
                        )
                    )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            results.append(
                HealthCheckResult(
                    service_name="internet_connectivity",
                    status=HealthStatus.UNHEALTHY,
                    response_time_ms=response_time,
                    timestamp=datetime.now(),
                    message="Internet connectivity check failed",
                    error=str(e),
                )
            )

        # Check OpenAI API if enabled
        if self.external_services.get("openai", {}).get("enabled", False):
            start_time = time.time()
            try:
                # Simple ping to OpenAI API
                async with httpx.AsyncClient(timeout=10.0) as client:
                    headers = {"User-Agent": "ZETA-AI-Health-Check"}
                    response = await client.get("https://api.openai.com/v1/models", headers=headers)
                    response_time = (time.time() - start_time) * 1000

                    if response.status_code in [
                        200,
                        401,
                    ]:  # 401 is expected without API key
                        results.append(
                            HealthCheckResult(
                                service_name="openai_api",
                                status=HealthStatus.HEALTHY,
                                response_time_ms=response_time,
                                timestamp=datetime.now(),
                                message="OpenAI API is reachable",
                            )
                        )
                    else:
                        results.append(
                            HealthCheckResult(
                                service_name="openai_api",
                                status=HealthStatus.DEGRADED,
                                response_time_ms=response_time,
                                timestamp=datetime.now(),
                                message="OpenAI API issues detected",
                                error=f"HTTP {response.status_code}",
                            )
                        )

            except Exception as e:
                response_time = (time.time() - start_time) * 1000
                results.append(
                    HealthCheckResult(
                        service_name="openai_api",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=response_time,
                        timestamp=datetime.now(),
                        message="OpenAI API check failed",
                        error=str(e),
                    )
                )

        return results

    async def run_all_checks(self) -> SystemHealthReport:
        """Run all health checks and generate report.

        Returns:
            Complete system health report
        """
        logger.info("Starting comprehensive health check...")
        start_time = time.time()

        all_results = []

        try:
            # Run all checks concurrently
            tasks = [
                self.check_api_endpoints(),
                self.check_database(),
                self.check_cache(),
                self.check_system_resources(),
                self.check_external_services(),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Flatten results
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Health check failed: {result}")
                    all_results.append(
                        HealthCheckResult(
                            service_name="unknown",
                            status=HealthStatus.UNHEALTHY,
                            response_time_ms=0.0,
                            timestamp=datetime.now(),
                            message="Health check failed with exception",
                            error=str(result),
                        )
                    )
                elif isinstance(result, list):
                    all_results.extend(result)
                else:
                    all_results.append(result)

            # Determine overall status
            statuses = [check.status for check in all_results]

            if all(status == HealthStatus.HEALTHY for status in statuses):
                overall_status = HealthStatus.HEALTHY
            elif any(status == HealthStatus.UNHEALTHY for status in statuses):
                overall_status = HealthStatus.UNHEALTHY
            elif any(status == HealthStatus.DEGRADED for status in statuses):
                overall_status = HealthStatus.DEGRADED
            else:
                overall_status = HealthStatus.UNKNOWN

            # Generate summary
            total_time = (time.time() - start_time) * 1000
            summary = {
                "total_checks": len(all_results),
                "healthy_checks": sum(1 for check in all_results if check.status == HealthStatus.HEALTHY),
                "degraded_checks": sum(1 for check in all_results if check.status == HealthStatus.DEGRADED),
                "unhealthy_checks": sum(1 for check in all_results if check.status == HealthStatus.UNHEALTHY),
                "total_time_ms": total_time,
                "average_response_time_ms": sum(check.response_time_ms for check in all_results) / len(all_results)
                if all_results
                else 0,
            }

            report = SystemHealthReport(
                overall_status=overall_status,
                timestamp=datetime.now(),
                checks=all_results,
                summary=summary,
            )

            logger.info(f"Health check completed: {overall_status.value} ({total_time:.2f}ms)")
            return report

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return SystemHealthReport(
                overall_status=HealthStatus.UNHEALTHY,
                timestamp=datetime.now(),
                checks=[
                    HealthCheckResult(
                        service_name="health_monitor",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=0.0,
                        timestamp=datetime.now(),
                        message="Health monitoring system failed",
                        error=str(e),
                    )
                ],
                summary={"error": str(e)},
            )

    async def save_report(self, report: SystemHealthReport, file_path: str | None = None) -> None:
        """Save health report to file.

        Args:
            report: Health report to save
            file_path: Optional custom file path
        """
        try:
            if file_path is None:
                # Default path with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                reports_dir = Path("storage/monitoring/health")
                reports_dir.mkdir(parents=True, exist_ok=True)
                file_path = reports_dir / f"health_report_{timestamp}.json"

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, indent=2)

            logger.info(f"Health report saved: {file_path}")

        except Exception as e:
            logger.error(f"Failed to save health report: {e}")


async def main():
    """Main function for running health checks."""
    import argparse

    parser = argparse.ArgumentParser(description="ZETA AI Health Monitor")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--output", help="Output file path for report")
    parser.add_argument("--watch", action="store_true", help="Run continuously")
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Check interval in seconds (for watch mode)",
    )

    args = parser.parse_args()

    # Load configuration
    config = {}
    if args.config and Path(args.config).exists():
        try:
            with open(args.config, encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return 1

    # Create health monitor
    monitor = HealthMonitor(config)

    try:
        if args.watch:
            logger.info(f"Starting continuous health monitoring (interval: {args.interval}s)")

            while True:
                report = await monitor.run_all_checks()

                # Save report
                if args.output:
                    await monitor.save_report(report, args.output)
                else:
                    await monitor.save_report(report)

                # Print summary
                print(f"\n--- Health Check Report ({report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}) ---")
                print(f"Overall Status: {report.overall_status.value.upper()}")
                print(f"Total Checks: {report.summary['total_checks']}")
                print(f"Healthy: {report.summary['healthy_checks']}")
                print(f"Degraded: {report.summary['degraded_checks']}")
                print(f"Unhealthy: {report.summary['unhealthy_checks']}")
                print(f"Total Time: {report.summary['total_time_ms']:.2f}ms")

                # Show unhealthy services
                unhealthy = [check for check in report.checks if check.status == HealthStatus.UNHEALTHY]
                if unhealthy:
                    print("\nUnhealthy Services:")
                    for check in unhealthy:
                        print(f"  - {check.service_name}: {check.error or check.message}")

                await asyncio.sleep(args.interval)

        else:
            # Single run
            report = await monitor.run_all_checks()

            # Save report
            if args.output:
                await monitor.save_report(report, args.output)
            else:
                await monitor.save_report(report)

            # Print detailed report
            print(json.dumps(report.to_dict(), indent=2))

            # Exit with appropriate code
            if report.overall_status == HealthStatus.HEALTHY:
                return 0
            elif report.overall_status == HealthStatus.DEGRADED:
                return 1
            else:
                return 2

    except KeyboardInterrupt:
        logger.info("Health monitoring interrupted by user")
        return 0

    except Exception as e:
        logger.error(f"Health monitoring failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
