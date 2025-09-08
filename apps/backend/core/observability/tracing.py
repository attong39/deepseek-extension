"""Tracing module."""

from __future__ import annotations

from contextlib import nullcontext

try:
    from opentelemetry import trace
except Exception:  # pragma: no cover

    class _DummyTracer:
        def start_as_current_span(self, _name: str):  # type: ignore
            return nullcontext()

    class _Dummy:
        def get_tracer(self, *_args, **_kwargs):  # type: ignore
            return _DummyTracer()

    trace = _Dummy()  # type: ignore

tracer = trace.get_tracer("zeta.core")  # type: ignore
import Exception
import str
