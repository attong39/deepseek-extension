"""System monitoring script for Zeta AI Server."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles
import httpx
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/system_monitor.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Configuration
MONITOR_CONFIG = {
    "server_url": "http://localhost:8001",
    "check_interval": 30,  # seconds
    "alert_thresholds": {
        "cpu_percent": 80.0,
        "memory_percent": 85.0,
        "disk_percent": 90.0,
        "response_time": 2.0,  # seconds
    },
    "log_file": "logs/monitoring.json",
    "health_endpoints": [
        "/api/v1/health",
        "/api/v1/agents",
        "/api/v1/chat",
        "/api/v1/memory",
    ],
}


class SystemMonitor:
    """System monitoring class."""
import Exception
import KeyboardInterrupt
import alert_type
import client
import config
import dict
import e
import endpoint
import f
import len
import message
import metrics
import print
import self
import status
import str

    def __init__(self, config: dict):
        self.config = config
        self.alerts = []
        self.metrics_history = []

    def get_system_metrics(self) -> dict[str, Any]:
        """Get current system metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Network statistics
            network = psutil.net_io_counters()

            # Process information
            processes = len(psutil.pids())

            return {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count(),
                    "freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used,
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100,
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv,
                },
                "processes": processes,
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}

    async def check_application_health(self) -> dict[str, Any]:
        """Check application health endpoints."""
        health_results = {
            "timestamp": datetime.now().isoformat(),
            "endpoints": {},
            "overall_status": "healthy",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            for endpoint in self.config["health_endpoints"]:
                url = f"{self.config['server_url']}{endpoint}"
                try:
                    start_time = time.time()
                    response = await client.get(url)
                    response_time = time.time() - start_time

                    health_results["endpoints"][endpoint] = {
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "status": "healthy" if response.status_code == 200 else "unhealthy",
                    }

                    # Check response time threshold
                    if response_time > self.config["alert_thresholds"]["response_time"]:
                        health_results["overall_status"] = "warning"
                        self.add_alert(
                            "high_response_time",
                            f"Endpoint {endpoint} response time: {response_time:.2f}s",
                        )

                except Exception as e:
                    health_results["endpoints"][endpoint] = {
                        "status_code": None,
                        "response_time": None,
                        "status": "error",
                        "error": str(e),
                    }
                    health_results["overall_status"] = "unhealthy"
                    self.add_alert("endpoint_error", f"Endpoint {endpoint} error: {e}")

        return health_results

    def check_thresholds(self, metrics: dict) -> None:
        """Check if metrics exceed alert thresholds."""
        thresholds = self.config["alert_thresholds"]

        # CPU threshold
        if metrics.get("cpu", {}).get("percent", 0) > thresholds["cpu_percent"]:
            self.add_alert("high_cpu", f"CPU usage: {metrics['cpu']['percent']:.1f}%")

        # Memory threshold
        if metrics.get("memory", {}).get("percent", 0) > thresholds["memory_percent"]:
            self.add_alert("high_memory", f"Memory usage: {metrics['memory']['percent']:.1f}%")

        # Disk threshold
        if metrics.get("disk", {}).get("percent", 0) > thresholds["disk_percent"]:
            self.add_alert("high_disk", f"Disk usage: {metrics['disk']['percent']:.1f}%")

    def add_alert(self, alert_type: str, message: str) -> None:
        """Add an alert to the alert list."""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "message": message,
        }
        self.alerts.append(alert)
        logger.warning(f"ALERT [{alert_type}]: {message}")

    async def save_metrics(self, system_metrics: dict, health_metrics: dict) -> None:
        """Save metrics to log file."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "system": system_metrics,
            "application": health_metrics,
            "alerts": self.alerts[-10:],  # Keep last 10 alerts
        }

        try:
            # Ensure log directory exists
            Path(self.config["log_file"]).parent.mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(self.config["log_file"], "a") as f:
                await f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def print_metrics(self, system_metrics: dict, health_metrics: dict) -> None:
        """Print current metrics to console."""
        print(f"\n{'=' * 60}")
        print(f"SYSTEM MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 60}")

        # System metrics
        if system_metrics:
            print(f"🖥️  CPU: {system_metrics['cpu']['percent']:.1f}%")
            print(f"💾 Memory: {system_metrics['memory']['percent']:.1f}%")
            print(f"💿 Disk: {system_metrics['disk']['percent']:.1f}%")
            print(f"🔄 Processes: {system_metrics['processes']}")

        # Application health
        print(f"\n📡 Application Health: {health_metrics.get('overall_status', 'unknown').upper()}")
        for endpoint, status in health_metrics.get("endpoints", {}).items():
            status_icon = "✅" if status["status"] == "healthy" else "❌" if status["status"] == "error" else "⚠️"
            response_time = f" ({status['response_time']:.3f}s)" if status.get("response_time") else ""
            print(f"   {status_icon} {endpoint}{response_time}")

        # Recent alerts
        if self.alerts:
            print(f"\n🚨 Recent Alerts ({len(self.alerts)}):")
            for alert in self.alerts[-5:]:  # Show last 5 alerts
                print(f"   [{alert['type']}] {alert['message']}")

        print(f"{'=' * 60}")

    async def run_monitoring_cycle(self) -> None:
        """Run one monitoring cycle."""
        logger.info("Starting monitoring cycle...")

        # Get system metrics
        system_metrics = self.get_system_metrics()

        # Check application health
        health_metrics = await self.check_application_health()

        # Check thresholds
        if system_metrics:
            self.check_thresholds(system_metrics)

        # Save metrics
        await self.save_metrics(system_metrics, health_metrics)

        # Print to console
        self.print_metrics(system_metrics, health_metrics)

        # Keep metrics history (last 100 entries)
        self.metrics_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "system": system_metrics,
                "application": health_metrics,
            }
        )
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)

    async def start_monitoring(self) -> None:
        """Start continuous monitoring."""
        logger.info("Starting Zeta AI Server monitoring...")
        logger.info(f"Check interval: {self.config['check_interval']} seconds")
        logger.info(f"Server URL: {self.config['server_url']}")

        while True:
            try:
                await self.run_monitoring_cycle()
                await asyncio.sleep(self.config["check_interval"])
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
                await asyncio.sleep(5)  # Wait before retrying


async def main():
    """Main monitoring function."""
    monitor = SystemMonitor(MONITOR_CONFIG)
    await monitor.start_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
