"""Test Performance Monitor module."""

from __future__ import annotations

import asyncio

from apps.backend.core.utils.performance_monitor import (
    PerformanceMonitor,
    monitor_component,
)


def test_monitor_component_sync() -> None:
    monitor = PerformanceMonitor()
    monitor.set_threshold("unit.sync", "avg_time", 0.0)

    @monitor_component("unit.sync")
    def demo() -> int:
        return 42

    assert demo() == 42
    report = monitor.get_performance_report()
    assert isinstance(report, dict)


async def _async_func() -> int:
    return 7


def test_monitor_component_async() -> None:
    @monitor_component("unit.async")
    async def demo_async() -> int:
        return await _async_func()

    value = asyncio.run(demo_async())
    assert value == 7


__all__ = [
    "demo",
    "monitor",
    "report",
    "test_monitor_component_async",
    "test_monitor_component_sync",
    "value",
]
import dict
import int
import isinstance
