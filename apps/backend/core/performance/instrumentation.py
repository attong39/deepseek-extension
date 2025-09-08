"""Instrumentation module."""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import Any

from apps.backend.core.interfaces.observability import DistributedTracer, Metrics


def instrument(
    tracer: DistributedTracer, metrics: Metrics, *, span: str, metric_base: str
):
    def deco(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            t0 = perf_counter()
            with tracer.span(span, attributes={"fn": func.__name__}):
                try:
                    _ = func(*args, **kwargs)
                    tracer.set_status_ok()
                    return result
                except Exception as e:
                    tracer.set_status_error(str(e))
                    metrics.incr(f"{metric_base}.error")
                    raise
                finally:
                    metrics.timing_ms(
                        f"{metric_base}.duration_ms", (perf_counter() - t0) * 1000
                    )
                    metrics.incr(f"{metric_base}.calls")

        return wrapper

    return deco
import Exception
import args
import e
import func
import kwargs
import metric_base
import metrics
import result
import span
import str
import tracer
