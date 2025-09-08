"""
Exception telemetry and monitoring utilities.

Integrates with OpenTelemetry for tracing, Prometheus for metrics, and
structlog/standard logging for structured logs. All external deps are optional;
graceful fallbacks are provided when unavailable.
"""

from __future__ import annotations

import inspect
import logging
import time
from typing import TYPE_CHECKING, Any
import Exception
import bool
import callable
import context
import dict
import exc
import getattr
import hasattr
import result
import self
import span
import str
import type

try:  # pragma: no cover - optional dependency
    from opentelemetry import trace as _otel_trace

    def _get_tracer(_name: str):  # type: ignore[return-type]
        return _otel_trace.get_tracer(_name)
except Exception:  # pragma: no cover - fallback

    def _get_tracer(_name: str):  # type: ignore[return-type]
        class _NoopSpan:
            def set_attribute(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
                pass

        class _NoopCM:
            def __enter__(self) -> _NoopSpan:
                return _NoopSpan()

            def __exit__(self, exc_type, exc, tb) -> bool:  # noqa: ANN001
                return False

        class _NoopTracer:
            def start_as_current_span(self, _name: str) -> _NoopCM:
                return _NoopCM()

        return _NoopTracer()


# Typing for optional prometheus types
if TYPE_CHECKING:  # pragma: no cover - typing only
    from prometheus_client import Counter as PromCounter
    from prometheus_client import Histogram as PromHistogram
else:  # Fallback placeholders for runtime
    PromCounter = Any  # type: ignore[assignment]
    PromHistogram = Any  # type: ignore[assignment]

# Initialize optional metrics
exception_counter: PromCounter | None = None
exception_duration: PromHistogram | None = None
try:  # pragma: no cover - exercised in integration
    from prometheus_client import Counter, Histogram

    exception_counter = Counter(
        "zeta_exceptions_total",
        "Total number of exceptions",
        ["error_type", "error_code", "severity"],
    )
    exception_duration = Histogram(
        "zeta_exception_handling_duration_seconds",
        "Time spent handling exceptions",
    )
except Exception:  # pragma: no cover - metrics optional
    pass


# structlog is optional
try:  # pragma: no cover - exercised in integration
    import structlog as _structlog

    STRUCTLOG_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    _structlog = None  # type: ignore[assignment]
    STRUCTLOG_AVAILABLE = False


class ExceptionTelemetry:
    """Telemetry collection for exceptions.

    Captures tracing span, increments Prometheus counters/histograms (if
    available), and emits structured logs. Designed to be safe as a best-effort
    observer: failures in telemetry should not raise.
    """

    def __init__(self) -> None:
        self.tracer = _get_tracer(__name__)
        if STRUCTLOG_AVAILABLE and _structlog is not None:
            self.logger = _structlog.get_logger()
        else:
            self.logger = logging.getLogger(__name__)

    async def track_exception(
        self, exc: Exception, context: dict[str, Any] | None = None
    ) -> None:
        """Track an exception across tracing, metrics, and logs.

        Args:
            exc: The exception instance to record.
            context: Optional contextual data to include in logs.
        """

        start = time.perf_counter()
        try:
            with self.tracer.start_as_current_span("exception_handling") as span:
                # Span attributes
                span.set_attribute("exception.type", type(exc).__name__)
                span.set_attribute("exception.message", str(exc))
                code = getattr(exc, "error_code", None)
                if code is not None:
                    span.set_attribute("exception.code", code)

                # Prometheus metrics (best-effort)
                try:
                    sev_raw = getattr(exc, "severity", "medium")
                    sev = getattr(sev_raw, "value", sev_raw)
                    if exception_counter is not None:
                        exception_counter.labels(
                            error_type=type(exc).__name__,
                            error_code=code or "unknown",
                            severity=str(sev),
                        ).inc()
                except Exception:
                    # Never fail request due to metrics
                    pass

                # Structured logging
                try:
                    payload = {
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                        "error_code": code,
                        "context": context or {},
                    }
                    # Prefer async structlog if available
                    aerror = getattr(self.logger, "aerror", None)
                    if callable(aerror):
                        _ = aerror("exception_occurred", **payload)
                        if inspect.isawaitable(result):
                            await result  # type: ignore[no-any-return]
                    else:
                        # Detect structlog vs std logging by presence of bind
                        if hasattr(self.logger, "bind"):
                            # structlog sync path
                            self.logger.error("exception_occurred", **payload)
                        else:
                            # std logging path
                            self.logger.error("exception_occurred", extra=payload)
                except Exception:
                    # Logging should not raise
                    pass
        finally:
            # Observe duration if metric available
            try:
                if exception_duration is not None:
                    exception_duration.observe(time.perf_counter() - start)
            except Exception:
                pass


__all__ = [
    "ExceptionTelemetry",
    "exception_counter",
    "exception_duration",
]
