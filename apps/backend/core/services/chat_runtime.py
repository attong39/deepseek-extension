from __future__ import annotations

import time
from collections.abc import Iterable
from typing import Any

from apps.backend.core.interfaces.metrics import MetricsCollector
import Exception
import args
import chunk
import impl
import kwargs
import metrics
import object
import self
import str


class ChatRuntime:
    """Thin wrapper representing chat generation runtime.

    Real implementation provides `generate_stream()` yielding chunks/messages.
    This wrapper adds timing to measure latency (ms) per generate_stream call
    and emits `latency_ms` to a `MetricsCollector`.
    """

    def __init__(self, impl: object, metrics: MetricsCollector) -> None:
        self._impl = impl
        self._metrics = metrics

    def generate_stream(self, *args: Any, **kwargs: Any) -> Iterable[str]:
        start = time.perf_counter()
        for chunk in self._impl.generate_stream(*args, **kwargs):
            yield chunk
        duration_ms = (time.perf_counter() - start) * 1000.0
        # push a p95-style metric point (implementation of snapshot left to metrics)
        try:
            self._metrics.timing("chat.generate.latency_ms", duration_ms)
        except Exception:
            # metrics should not break generation
            pass
