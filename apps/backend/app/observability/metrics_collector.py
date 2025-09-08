"""Metrics collector service for comprehensive system monitoring.





This service collects, aggregates, and exposes metrics for system performance,


business operations, and AI agent activities.


"""

from __future__ import annotations

import asyncio
import logging
import statistics
import time
from collections import defaultdict, deque
from collections.abc import Callable
from enum import Enum
from typing import Any
import Exception
import ImportError
import ValueError
import bool
import collection_interval
import collector
import collector_func
import description
import dict
import e
import enable_detailed_timing
import entry
import float
import format_type
import history_deque
import hours
import int
import isinstance
import k
import len
import list
import max
import max_histogram_buckets
import metric_name
import metric_type
import min
import name
import rate_deque
import result
import retention_hours
import self
import sorted
import str
import sum
import t
import tags
import timestamp
import tuple
import unit
import v
import value
import window_seconds

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics that can be collected."""

    COUNTER = "counter"  # Monotonically increasing value

    GAUGE = "gauge"  # Current value that can go up or down

    HISTOGRAM = "histogram"  # Distribution of values

    TIMER = "timer"  # Measure duration

    RATE = "rate"  # Events per time period


class MetricUnit(Enum):
    """Units for metrics."""

    COUNT = "count"

    SECONDS = "seconds"

    MILLISECONDS = "milliseconds"

    BYTES = "bytes"

    KILOBYTES = "kilobytes"

    MEGABYTES = "megabytes"

    PERCENT = "percent"

    REQUESTS_PER_SECOND = "requests_per_second"


class MetricsCollector:
    """Service for collecting and managing system metrics."""

    def __init__(
        self,
        collection_interval: int = 60,
        retention_hours: int = 168,  # 7 days
        max_histogram_buckets: int = 100,
        enable_detailed_timing: bool = True,
    ) -> None:
        """Initialize the metrics collector.





        Args:


            collection_interval: How often to collect metrics in seconds.


            retention_hours: How long to retain metrics.


            max_histogram_buckets: Maximum histogram bucket count.


            enable_detailed_timing: Whether to enable detailed timing metrics.


        """

        self.collection_interval = collection_interval

        self.retention_hours = retention_hours

        self.max_histogram_buckets = max_histogram_buckets

        self.enable_detailed_timing = enable_detailed_timing

        # Metric storage

        self._counters: dict[str, float] = defaultdict(float)

        self._gauges: dict[str, float] = defaultdict(float)

        self._histograms: dict[str, list[float]] = defaultdict(list)

        self._timers: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=1000))

        self._rates: dict[str, deque[tuple[float, float]]] = defaultdict(
            lambda: deque(maxlen=1000)
        )

        # Metric metadata

        self._metric_metadata: dict[str, dict[str, Any]] = {}

        # Aggregated metrics history

        self._metric_history: dict[str, deque[dict[str, Any]]] = defaultdict(
            lambda: deque(maxlen=self.retention_hours)
        )

        # Custom metric collectors

        self._custom_collectors: dict[str, Callable[[], dict[str, Any]]] = {}

        # Background tasks

        self._collection_task: asyncio.Task[None] | None = None

        self._cleanup_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start background metric collection tasks."""

        self._collection_task = asyncio.create_task(
            self._collect_metrics_periodically()
        )

        self._cleanup_task = asyncio.create_task(self._cleanup_old_metrics())

        logger.info("Metrics collector background tasks started")

    async def stop(self) -> None:
        """Stop background metric collection tasks."""

        if self._collection_task:
            self._collection_task.cancel()

            try:
                await self._collection_task

            except asyncio.CancelledError:
                logger.debug("Collection task cancelled")

                raise

        if self._cleanup_task:
            self._cleanup_task.cancel()

            try:
                await self._cleanup_task

            except asyncio.CancelledError:
                logger.debug("Cleanup task cancelled")

                raise

        logger.info("Metrics collector background tasks stopped")

    def register_metric(
        self,
        name: str,
        metric_type: MetricType,
        description: str,
        unit: MetricUnit = MetricUnit.COUNT,
        tags: dict[str, str] | None = None,
    ) -> None:
        """Register a new metric.





        Args:


            name: Metric name.


            metric_type: Type of metric.


            description: Metric description.


            unit: Metric unit.


            tags: Optional tags for the metric.


        """

        self._metric_metadata[name] = {
            "type": metric_type.value,
            "description": description,
            "unit": unit.value,
            "tags": tags or {},
            "created_at": time.time(),
        }

        logger.debug(f"Registered metric: {name} ({metric_type.value})")

    def increment_counter(
        self, name: str, value: float = 1.0, tags: dict[str, str] | None = None
    ) -> None:
        """Increment a counter metric.





        Args:


            name: Counter name.


            value: Value to add.


            tags: Optional tags.


        """

        full_name = self._get_tagged_name(name, tags)

        self._counters[full_name] += value

        if name not in self._metric_metadata:
            self.register_metric(
                name, MetricType.COUNTER, f"Auto-registered counter: {name}"
            )

    def set_gauge(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """Set a gauge metric value.





        Args:


            name: Gauge name.


            value: Current value.


            tags: Optional tags.


        """

        full_name = self._get_tagged_name(name, tags)

        self._gauges[full_name] = value

        if name not in self._metric_metadata:
            self.register_metric(
                name, MetricType.GAUGE, f"Auto-registered gauge: {name}"
            )

    def record_histogram(
        self, name: str, value: float, tags: dict[str, str] | None = None
    ) -> None:
        """Record a value in a histogram.





        Args:


            name: Histogram name.


            value: Value to record.


            tags: Optional tags.


        """

        full_name = self._get_tagged_name(name, tags)

        histogram = self._histograms[full_name]

        histogram.append(value)

        # Keep histogram size manageable

        if len(histogram) > self.max_histogram_buckets:
            histogram.pop(0)

        if name not in self._metric_metadata:
            self.register_metric(
                name, MetricType.HISTOGRAM, f"Auto-registered histogram: {name}"
            )

    def time_operation(self, name: str, tags: dict[str, str] | None = None):
        """Context manager for timing operations.





        Args:


            name: Timer name.


            tags: Optional tags.





        Returns:


            Context manager for timing.


        """

        return TimerContext(self, name, tags)

    def record_timing(
        self, name: str, duration: float, tags: dict[str, str] | None = None
    ) -> None:
        """Record a timing measurement.





        Args:


            name: Timer name.


            duration: Duration in seconds.


            tags: Optional tags.


        """

        full_name = self._get_tagged_name(name, tags)

        self._timers[full_name].append(duration)

        if name not in self._metric_metadata:
            self.register_metric(
                name,
                MetricType.TIMER,
                f"Auto-registered timer: {name}",
                MetricUnit.SECONDS,
            )

    def record_rate(
        self, name: str, count: float, tags: dict[str, str] | None = None
    ) -> None:
        """Record a rate metric (events per time period).





        Args:


            name: Rate metric name.


            count: Number of events.


            tags: Optional tags.


        """

        full_name = self._get_tagged_name(name, tags)

        current_time = time.time()

        self._rates[full_name].append((current_time, count))

        if name not in self._metric_metadata:
            self.register_metric(
                name,
                MetricType.RATE,
                f"Auto-registered rate: {name}",
                MetricUnit.REQUESTS_PER_SECOND,
            )

    def get_counter(self, name: str, tags: dict[str, str] | None = None) -> float:
        """Get current counter value.





        Args:


            name: Counter name.


            tags: Optional tags.





        Returns:


            Current counter value.


        """

        full_name = self._get_tagged_name(name, tags)

        return self._counters.get(full_name, 0.0)

    def get_gauge(self, name: str, tags: dict[str, str] | None = None) -> float:
        """Get current gauge value.





        Args:


            name: Gauge name.


            tags: Optional tags.





        Returns:


            Current gauge value.


        """

        full_name = self._get_tagged_name(name, tags)

        return self._gauges.get(full_name, 0.0)

    def get_histogram_stats(
        self, name: str, tags: dict[str, str] | None = None
    ) -> dict[str, float]:
        """Get histogram statistics.





        Args:


            name: Histogram name.


            tags: Optional tags.





        Returns:


            Histogram statistics.


        """

        full_name = self._get_tagged_name(name, tags)

        values = self._histograms.get(full_name, [])

        if not values:
            return {
                "count": 0,
                "min": 0.0,
                "max": 0.0,
                "mean": 0.0,
                "median": 0.0,
                "p95": 0.0,
                "p99": 0.0,
                "stddev": 0.0,
            }

        sorted_values = sorted(values)

        count = len(values)

        return {
            "count": count,
            "min": min(values),
            "max": max(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "p95": sorted_values[int(0.95 * count)] if count > 0 else 0.0,
            "p99": sorted_values[int(0.99 * count)] if count > 0 else 0.0,
            "stddev": statistics.stdev(values) if count > 1 else 0.0,
        }

    def get_timer_stats(
        self, name: str, tags: dict[str, str] | None = None
    ) -> dict[str, float]:
        """Get timer statistics.





        Args:


            name: Timer name.


            tags: Optional tags.





        Returns:


            Timer statistics.


        """

        full_name = self._get_tagged_name(name, tags)

        timings = list(self._timers.get(full_name, []))

        if not timings:
            return {
                "count": 0,
                "min_ms": 0.0,
                "max_ms": 0.0,
                "mean_ms": 0.0,
                "median_ms": 0.0,
                "p95_ms": 0.0,
                "p99_ms": 0.0,
            }

        # Convert to milliseconds

        timings_ms = [t * 1000 for t in timings]

        sorted_timings = sorted(timings_ms)

        count = len(timings_ms)

        return {
            "count": count,
            "min_ms": min(timings_ms),
            "max_ms": max(timings_ms),
            "mean_ms": statistics.mean(timings_ms),
            "median_ms": statistics.median(timings_ms),
            "p95_ms": sorted_timings[int(0.95 * count)] if count > 0 else 0.0,
            "p99_ms": sorted_timings[int(0.99 * count)] if count > 0 else 0.0,
        }

    def get_rate_stats(
        self, name: str, tags: dict[str, str] | None = None, window_seconds: int = 60
    ) -> dict[str, float]:
        """Get rate statistics.





        Args:


            name: Rate metric name.


            tags: Optional tags.


            window_seconds: Time window for rate calculation.





        Returns:


            Rate statistics.


        """

        full_name = self._get_tagged_name(name, tags)

        rate_data = list(self._rates.get(full_name, []))

        if not rate_data:
            return {
                "events_per_second": 0.0,
                "total_events": 0.0,
                "window_seconds": window_seconds,
            }

        current_time = time.time()

        window_start = current_time - window_seconds

        # Filter to window

        recent_data = [
            (timestamp, count)
            for timestamp, count in rate_data
            if timestamp >= window_start
        ]

        if not recent_data:
            return {
                "events_per_second": 0.0,
                "total_events": 0.0,
                "window_seconds": window_seconds,
            }

        total_events = sum(count for _, count in recent_data)

        actual_window = (
            current_time - recent_data[0][0] if recent_data else window_seconds
        )

        actual_window = max(actual_window, 1)  # Avoid division by zero

        return {
            "events_per_second": total_events / actual_window,
            "total_events": total_events,
            "window_seconds": actual_window,
        }

    def get_all_metrics(self) -> dict[str, Any]:
        """Get all current metrics.





        Returns:


            All metrics with their current values.


        """

        _ = {
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "histograms": {},
            "timers": {},
            "rates": {},
            "metadata": self._metric_metadata,
            "timestamp": time.time(),
        }

        # Get histogram stats

        for name in self._histograms:
            result["histograms"][name] = self.get_histogram_stats(name)

        # Get timer stats

        for name in self._timers:
            result["timers"][name] = self.get_timer_stats(name)

        # Get rate stats

        for name in self._rates:
            result["rates"][name] = self.get_rate_stats(name)

        return result

    def register_custom_collector(
        self, name: str, collector_func: Callable[[], dict[str, Any]]
    ) -> None:
        """Register a custom metric collector function.





        Args:


            name: Collector name.


            collector_func: Function that returns metrics.


        """

        self._custom_collectors[name] = collector_func

        logger.debug(f"Registered custom collector: {name}")

    def get_metric_history(self, name: str, hours: int = 24) -> list[dict[str, Any]]:
        """Get historical metric data.





        Args:


            name: Metric name.


            hours: Number of hours of history.





        Returns:


            Historical metric data.


        """

        history = list(self._metric_history.get(name, []))

        # Filter by time window

        cutoff_time = time.time() - (hours * 3600)

        filtered_history = [
            entry for entry in history if entry["timestamp"] >= cutoff_time
        ]

        return filtered_history

    def export_metrics(self, format_type: str = "prometheus") -> str:
        """Export metrics in specified format.





        Args:


            format_type: Export format (prometheus, json).





        Returns:


            Exported metrics string.


        """

        if format_type.lower() == "prometheus":
            return self._export_prometheus_format()

        elif format_type.lower() == "json":
            import json

            return json.dumps(self.get_all_metrics(), indent=2, default=str)

        else:
            raise ValueError(f"Unsupported export format: {format_type}")

    def _get_tagged_name(self, name: str, tags: dict[str, str] | None) -> str:
        """Get metric name with tags included.





        Args:


            name: Base metric name.


            tags: Optional tags.





        Returns:


            Tagged metric name.


        """

        if not tags:
            return name

        tag_string = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))

        return f"{name}{{{tag_string}}}"

    def _export_prometheus_format(self) -> str:
        """Export metrics in Prometheus format."""

        lines = []

        # Counters

        for name, value in self._counters.items():
            clean_name = (
                name.replace("{", "_")
                .replace("}", "_")
                .replace(",", "_")
                .replace("=", "_")
            )

            lines.append(f"# TYPE {clean_name} counter")

            lines.append(f"{clean_name} {value}")

        # Gauges

        for name, value in self._gauges.items():
            clean_name = (
                name.replace("{", "_")
                .replace("}", "_")
                .replace(",", "_")
                .replace("=", "_")
            )

            lines.append(f"# TYPE {clean_name} gauge")

            lines.append(f"{clean_name} {value}")

        # Histograms (simplified)

        for name in self._histograms:
            stats = self.get_histogram_stats(name)

            clean_name = (
                name.replace("{", "_")
                .replace("}", "_")
                .replace(",", "_")
                .replace("=", "_")
            )

            lines.append(f"# TYPE {clean_name} histogram")

            lines.append(f"{clean_name}_count {stats['count']}")

            lines.append(f"{clean_name}_sum {stats['mean'] * stats['count']}")

        return "\n".join(lines)

    async def _collect_metrics_periodically(self) -> None:
        """Background task to collect metrics periodically."""

        while True:
            try:
                self._collect_system_metrics()

                await self._collect_custom_metrics()

                self._aggregate_metrics()

                await asyncio.sleep(self.collection_interval)

            except asyncio.CancelledError:
                logger.debug("Metric collection task cancelled")

                raise

            except Exception as e:
                logger.error(f"Error in metric collection: {e}")

                await asyncio.sleep(30)  # Wait 30 seconds before retry

    def _collect_system_metrics(self) -> None:
        """Collect system-level metrics."""

        try:
            import psutil

            # CPU metrics

            cpu_percent = psutil.cpu_percent()

            self.set_gauge("system.cpu.usage_percent", cpu_percent)

            # Memory metrics

            memory = psutil.virtual_memory()

            self.set_gauge("system.memory.usage_percent", memory.percent)

            self.set_gauge("system.memory.available_bytes", memory.available)

            self.set_gauge("system.memory.used_bytes", memory.used)

            # Disk metrics

            disk = psutil.disk_usage("/")

            self.set_gauge("system.disk.usage_percent", (disk.used / disk.total) * 100)

            self.set_gauge("system.disk.free_bytes", disk.free)

            # Network metrics (if available)

            try:
                net_io = psutil.net_io_counters()

                self.increment_counter("system.network.bytes_sent", net_io.bytes_sent)

                self.increment_counter("system.network.bytes_recv", net_io.bytes_recv)

            except Exception:
                pass  # Network stats may not be available

        except ImportError:
            # psutil not available, skip system metrics

            pass

        except Exception as e:
            logger.debug(f"Error collecting system metrics: {e}")

    async def _collect_custom_metrics(self) -> None:
        """Collect custom metrics from registered collectors."""

        for name, collector_func in self._custom_collectors.items():
            try:
                if asyncio.iscoroutinefunction(collector_func):
                    metrics = await collector_func()

                else:
                    metrics = collector_func()

                # Register collected metrics

                for metric_name, value in metrics.items():
                    if isinstance(value, (int, float)):
                        self.set_gauge(f"custom.{name}.{metric_name}", value)

            except Exception as e:
                logger.error(f"Error collecting custom metrics from {name}: {e}")

    def _aggregate_metrics(self) -> None:
        """Aggregate current metrics into history."""

        current_time = time.time()

        # Create aggregated snapshot

        snapshot = {
            "timestamp": current_time,
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "histogram_stats": {},
            "timer_stats": {},
            "rate_stats": {},
        }

        # Add aggregated stats

        for name in self._histograms:
            snapshot["histogram_stats"][name] = self.get_histogram_stats(name)

        for name in self._timers:
            snapshot["timer_stats"][name] = self.get_timer_stats(name)

        for name in self._rates:
            snapshot["rate_stats"][name] = self.get_rate_stats(name)

        # Store in history for each metric type

        for metric_type in [
            "counters",
            "gauges",
            "histogram_stats",
            "timer_stats",
            "rate_stats",
        ]:
            for metric_name in snapshot[metric_type]:
                self._metric_history[f"{metric_type}.{metric_name}"].append(
                    {
                        "timestamp": current_time,
                        "value": snapshot[metric_type][metric_name],
                    }
                )

    async def _cleanup_old_metrics(self) -> None:
        """Background task to clean up old metric data."""

        while True:
            try:
                current_time = time.time()

                cutoff_time = current_time - (self.retention_hours * 3600)

                # Clean up rate data

                for rate_deque in self._rates.values():
                    while rate_deque and rate_deque[0][0] < cutoff_time:
                        rate_deque.popleft()

                # Clean up metric history

                for history_deque in self._metric_history.values():
                    while history_deque and history_deque[0]["timestamp"] < cutoff_time:
                        history_deque.popleft()

                # Sleep for 1 hour

                await asyncio.sleep(3600)

            except asyncio.CancelledError:
                logger.debug("Cleanup task cancelled")

                raise

            except Exception as e:
                logger.error(f"Error in metric cleanup: {e}")

                await asyncio.sleep(1800)  # Wait 30 minutes before retry


class TimerContext:
    """Context manager for timing operations."""

    def __init__(
        self, collector: MetricsCollector, name: str, tags: dict[str, str] | None = None
    ) -> None:
        """Initialize timer context.





        Args:


            collector: Metrics collector instance.


            name: Timer name.


            tags: Optional tags.


        """

        self.collector = collector

        self.name = name

        self.tags = tags

        self.start_time: float = 0.0

    def __enter__(self) -> TimerContext:
        """Enter timer context."""

        self.start_time = time.time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[misc]
        """Exit timer context and record duration."""

        duration = time.time() - self.start_time

        self.collector.record_timing(self.name, duration, self.tags)
