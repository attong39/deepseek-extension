"""
OpenTelemetry tracing setup với fail-safe fallback.

Features:
- Automatic tracing setup với optional dependencies
- OTLP HTTP exporter configuration
- Graceful degradation khi missing dependencies
- Runtime toggle support
- Resource attribution và service naming
"""

from __future__ import annotations

import logging

from apps.backend.perf.config import get_runtime, get_settings
import Exception
import ImportError
import app
import app_name
import args
import bool
import exc
import func
import kwargs
import name
import object
import operation_name
import result
import self
import span
import str

logger = logging.getLogger("zeta.perf.tracing")


def setup_tracing(app_name: str = "zeta_api") -> bool:
    """
    Setup OpenTelemetry tracing với fail-safe behavior.

    Args:
        app_name: Service name for tracing

    Returns:
        True if tracing was successfully enabled, False otherwise
    """
    settings = get_settings()
    runtime = get_runtime()

    if not (settings.PERF_TRACING_ENABLED and runtime.tracing_enabled):
        logger.info("Tracing disabled via configuration")
        return False

    try:
        # Optional dependencies - only imported when needed
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.sdk.trace.sampling import TraceIdRatioBasedSampler

        # Create resource với service identification
        resource = Resource.create(
            {
                "service.name": app_name,
                "service.version": "1.0.0",  # Could be read from package metadata
                "deployment.environment": "production",  # Could be from env
            }
        )

        # Setup tracer provider với sampling
        sampler = TraceIdRatioBasedSampler(rate=settings.PERF_SAMPLING)
        provider = TracerProvider(resource=resource, sampler=sampler)
        trace.set_tracer_provider(provider)

        # Setup OTLP exporter
        otlp_endpoint = f"{settings.PERF_OTLP_ENDPOINT}/v1/traces"
        exporter = OTLPSpanExporter(
            endpoint=otlp_endpoint,
            timeout=10,  # 10 second timeout
        )

        # Add batch span processor
        span_processor = BatchSpanProcessor(
            exporter,
            max_queue_size=512,
            export_timeout_millis=30000,
            max_export_batch_size=512,
        )
        provider.add_span_processor(span_processor)

        logger.info(
            "OpenTelemetry tracing enabled: service=%s endpoint=%s sampling=%.2f",
            app_name,
            otlp_endpoint,
            settings.PERF_SAMPLING,
        )
        return True

    except ImportError as exc:
        logger.warning(
            "OpenTelemetry dependencies not available - tracing disabled: %s",
            exc,
        )
        return False
    except Exception as exc:
        logger.error(
            "Failed to setup OpenTelemetry tracing - soft disable: %s",
            exc,
        )
        return False


def get_tracer(name: str = "zeta") -> object:
    """
    Get tracer instance với fail-safe fallback.

    Args:
        name: Tracer name

    Returns:
        OpenTelemetry tracer or no-op tracer
    """
    try:
        from opentelemetry import trace

        return trace.get_tracer(name)
    except ImportError:
        # Return no-op tracer-like object
        class NoOpTracer:
            def start_span(self, _name: str, **_kwargs):
                class NoOpSpan:
                    def __enter__(self):
                        return self

                    def __exit__(self, *args):
                        pass

                    def set_attribute(self, key: str, value) -> None:
                        pass

                    def set_status(self, status) -> None:
                        pass

                return NoOpSpan()

            def start_as_current_span(self, name: str, **kwargs):
                return self.start_span(name, **kwargs)

        return NoOpTracer()


def instrument_fastapi_tracing(app) -> None:
    """
    Instrument FastAPI app với OpenTelemetry tracing.

    Args:
        app: FastAPI application instance
    """
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
        from opentelemetry.instrumentation.requests import RequestsInstrumentor

        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(app)

        # Instrument HTTP clients
        HTTPXClientInstrumentor().instrument()
        RequestsInstrumentor().instrument()

        logger.info("FastAPI instrumentation enabled")

    except ImportError:
        logger.info("OpenTelemetry FastAPI instrumentation not available")
    except Exception as exc:
        logger.warning("Failed to instrument FastAPI: %s", exc)


def trace_operation(operation_name: str):
    """
    Decorator để trace operations manually.

    Args:
        operation_name: Name of the operation being traced
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            with tracer.start_as_current_span(operation_name) as span:
                try:
                    _ = func(*args, **kwargs)
                    span.set_attribute("operation.success", True)
                    return result
                except Exception as exc:
                    span.set_attribute("operation.success", False)
                    span.set_attribute("operation.error", str(exc))
                    raise

        return wrapper

    return decorator
