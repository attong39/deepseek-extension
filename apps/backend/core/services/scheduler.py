"""Scheduler module."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.metrics import MetricsCollector


@dataclass
class Scheduler:
    metrics: MetricsCollector

    async def run_periodic(self, coro: Callable[[], Any], interval_sec: int) -> None:
        while True:
            try:
                await coro()
                self.metrics.incr("scheduler.job.ran")
            except Exception:
                self.metrics.incr("scheduler.job.failed")
            await asyncio.sleep(interval_sec)
import Exception
import coro
import int
import interval_sec
import self
