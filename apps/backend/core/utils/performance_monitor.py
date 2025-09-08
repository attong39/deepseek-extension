from __future__ import annotations

import asyncio
import time
from collections import defaultdict
from collections.abc import Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from apps.backend.core.observability.logging import get_logger
from apps.backend.core.utils.error_handler import handle_core_errors
import Exception
import args
import bool
import component
import dict
import error
import float
import func
import int
import kwargs
import len
import list
import max
import metric
import metric_name
import min
import self
import str
import threshold
import value

"""
Performance Monitor for Core Components
=======================================
Monitors and optimizes performance across the core layer.
"""
logger = get_logger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics for a component."""

    total_calls: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0
    min_time: float = float("inf")
    max_time: float = 0.0
    error_count: int = 0
    last_call_time: float = 0.0
    memory_usage: int = 0
    cpu_usage: float = 0.0

    def update(self, execution_time: float, error: bool = False):
        """Update metrics with new execution data."""
        self.total_calls += 1
        self.total_time += execution_time
        self.avg_time = self.total_time / self.total_calls
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        self.last_call_time = time.time()
        if error:
            self.error_count += 1

    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "total_calls": self.total_calls,
            "total_time": self.total_time,
            "avg_time": self.avg_time,
            "min_time": self.min_time if self.min_time != float("inf") else 0.0,
            "max_time": self.max_time,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(1, self.total_calls),
            "last_call_time": self.last_call_time,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
        }


class PerformanceMonitor:
    """Performance monitor for core components."""

    def __init__(self):
        self._metrics: dict[str, PerformanceMetrics] = defaultdict(PerformanceMetrics)
        self._thresholds: dict[str, dict[str, float]] = {}
        self._alerts: list[dict[str, Any]] = []
        self._monitoring_enabled = True

    def set_threshold(self, component: str, metric: str, threshold: float):
        """Set performance threshold for a component."""
        if component not in self._thresholds:
            self._thresholds[component] = {}
        self._thresholds[component][metric] = threshold

    def get_metrics(self, component: str) -> PerformanceMetrics | None:
        """Get metrics for a component."""
        return self._metrics.get(component)

    def get_all_metrics(self) -> dict[str, dict[str, Any]]:
        """Get all performance metrics."""
        return {
            component: metrics.to_dict() for component, metrics in self._metrics.items()
        }

    def get_alerts(self) -> list[dict[str, Any]]:
        """Get performance alerts."""
        return self._alerts.copy()

    def clear_alerts(self):
        """Clear all alerts."""
        self._alerts.clear()

    def enable_monitoring(self):
        """Enable performance monitoring."""
        self._monitoring_enabled = True

    def disable_monitoring(self):
        """Disable performance monitoring."""
        self._monitoring_enabled = False

    @asynccontextmanager
    async def monitor_async(self, component: str):
        """Async context manager for monitoring component performance."""
        if not self._monitoring_enabled:
            yield
            return
        start_time = time.time()
        error_occurred = False
        try:
            yield
        except Exception:
            error_occurred = True
            raise
        finally:
            execution_time = time.time() - start_time
            self._update_metrics(component, execution_time, error_occurred)
            self._check_thresholds(component)

    def monitor_sync(self, component: str):
        """Sync context manager for monitoring component performance."""
        if not self._monitoring_enabled:
            return lambda func: func

        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                start_time = time.time()
                error_occurred = False
                try:
                    return func(*args, **kwargs)
                except Exception:
                    error_occurred = True
                    raise
                finally:
                    execution_time = time.time() - start_time
                    self._update_metrics(component, execution_time, error_occurred)
                    self._check_thresholds(component)

            return wrapper

        return decorator

    def _update_metrics(self, component: str, execution_time: float, error: bool):
        """Update metrics for a component."""
        self._metrics[component].update(execution_time, error)

    def _check_thresholds(self, component: str):
        """Check if metrics exceed thresholds."""
        if component not in self._thresholds:
            return
        metrics = self._metrics[component]
        thresholds = self._thresholds[component]
        for metric_name, threshold in thresholds.items():
            if metric_name == "avg_time" and metrics.avg_time > threshold:
                self._add_alert(component, "avg_time", metrics.avg_time, threshold)
            elif metric_name == "max_time" and metrics.max_time > threshold:
                self._add_alert(component, "max_time", metrics.max_time, threshold)
            elif (
                metric_name == "error_rate"
                and (metrics.error_count / max(1, metrics.total_calls)) > threshold
            ):
                error_rate = metrics.error_count / max(1, metrics.total_calls)
                self._add_alert(component, "error_rate", error_rate, threshold)

    def _add_alert(
        self, component: str, metric: str, value: float, threshold: float
    ) -> None:
        """Add a performance alert."""
        alert = {
            "component": component,
            "metric": metric,
            "value": value,
            "threshold": threshold,
            "timestamp": time.time(),
            "message": f"{component} {metric} ({value:.2f}) exceeds threshold ({threshold:.2f})",
        }
        self._alerts.append(alert)
        try:
            logger.warning(
                "Performance alert: %s %s %.3f > %.3f",
                component,
                metric,
                value,
                threshold,
            )
        except Exception:
            pass

    def get_performance_report(self) -> dict[str, Any]:
        """Generate comprehensive performance report."""
        return {
            "metrics": self.get_all_metrics(),
            "alerts": self.get_alerts(),
            "summary": {
                "total_components": len(self._metrics),
                "total_alerts": len(self._alerts),
                "monitoring_enabled": self._monitoring_enabled,
            },
        }


_performance_monitor = PerformanceMonitor()
_performance_monitor.set_threshold("database_query", "avg_time", 0.1)
_performance_monitor.set_threshold("api_call", "avg_time", 0.5)
_performance_monitor.set_threshold("file_operation", "avg_time", 0.05)
_performance_monitor.set_threshold("cache_operation", "avg_time", 0.01)


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    return _performance_monitor


@handle_core_errors
def monitor_component(component: str):
    """Decorator to monitor component performance."""

    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            async def async_wrapper(*args, **kwargs):
                async with _performance_monitor.monitor_async(component):
                    return await func(*args, **kwargs)

            return async_wrapper
        else:
            return _performance_monitor.monitor_sync(component)(func)

    return decorator


def get_performance_stats() -> dict[str, Any]:
    """Get current performance statistics."""
    return _performance_monitor.get_performance_report()


__all__ = [
    "PerformanceMetrics",
    "PerformanceMonitor",
    "alert",
    "clear_alerts",
    "decorator",
    "disable_monitoring",
    "enable_monitoring",
    "error_occurred",
    "error_rate",
    "execution_time",
    "get_alerts",
    "get_all_metrics",
    "get_metrics",
    "get_performance_monitor",
    "get_performance_report",
    "get_performance_stats",
    "logger",
    "metrics",
    "monitor_component",
    "monitor_sync",
    "set_threshold",
    "start_time",
    "thresholds",
    "to_dict",
    "update",
    "wrapper",
]
