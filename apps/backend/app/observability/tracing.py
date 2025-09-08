"""Tracing and OpenTelemetry integration - Unified Observability."""

import logging
from collections.abc import Callable
from typing import Any

# Optional OpenTelemetry imports


try:
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.sdk.resources import SERVICE_NAME, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    OTEL_AVAILABLE = True


except ImportError:
    OTEL_AVAILABLE = False


logger = logging.getLogger(__name__)


class TracingConfig:
    """Configuration for distributed tracing."""
import Exception
import ImportError
import app
import args
import attributes
import bool
import e
import enabled
import engine
import func
import jaeger_endpoint
import kwargs
import name
import self
import service_name
import str

    def __init__(
        self,
        service_name: str = "zeta-ai-server",
        jaeger_endpoint: str | None = None,
        enabled: bool = False,
    ):
        """


        Initialize tracing configuration.





        Args:


            service_name: Name of the service for tracing


            jaeger_endpoint: Jaeger collector endpoint


            enabled: Whether tracing is enabled


        """

        self.service_name = service_name

        self.jaeger_endpoint = jaeger_endpoint

        self.enabled = enabled and OTEL_AVAILABLE

        # tracer will be an OpenTelemetry Tracer or None
        self.tracer: Any | None = None

        if self.enabled:
            self._setup_tracing()

    def _setup_tracing(self) -> None:
        """Setup OpenTelemetry tracing."""

        try:
            # Create resource

            resource = Resource(attributes={SERVICE_NAME: self.service_name})

            # Create tracer provider

            provider = TracerProvider(resource=resource)

            trace.set_tracer_provider(provider)

            # Setup Jaeger exporter if endpoint provided

            if self.jaeger_endpoint:
                jaeger_exporter = JaegerExporter(
                    agent_host_name="localhost",
                    agent_port=14268,
                )

                span_processor = BatchSpanProcessor(jaeger_exporter)

                provider.add_span_processor(span_processor)

            # Get tracer

            self.tracer = trace.get_tracer(__name__)

            logger.info(f"OpenTelemetry tracing enabled for {self.service_name}")

        except Exception as e:
            logger.warning(f"Failed to setup tracing: {e}")

            self.enabled = False

    def instrument_fastapi(self, app: Any) -> None:
        """Instrument FastAPI application with tracing."""

        if not self.enabled:
            return

        try:
            FastAPIInstrumentor.instrument_app(app)

            logger.info("FastAPI instrumentation enabled")

        except Exception as e:
            logger.warning(f"Failed to instrument FastAPI: {e}")

    def instrument_requests(self) -> None:
        """Instrument HTTP requests with tracing."""

        if not self.enabled:
            return

        try:
            RequestsInstrumentor().instrument()

            logger.info("Requests instrumentation enabled")

        except Exception as e:
            logger.warning(f"Failed to instrument requests: {e}")

    def instrument_sqlalchemy(self, engine: Any) -> None:
        """Instrument SQLAlchemy with tracing."""

        if not self.enabled:
            return

        try:
            SQLAlchemyInstrumentor().instrument(engine=engine)

            logger.info("SQLAlchemy instrumentation enabled")

        except Exception as e:
            logger.warning(f"Failed to instrument SQLAlchemy: {e}")

    def create_span(self, name: str, **kwargs: Any) -> Any:
        """


        Create a new span for tracing.





        Args:


            name: Span name


            **kwargs: Additional span attributes





        Returns:


            Span context manager or no-op


        """

        if not self.enabled or not self.tracer:
            # Return no-op context manager if tracing disabled

            from contextlib import nullcontext

            return nullcontext()

        return self.tracer.start_as_current_span(name, attributes=kwargs)


# Global tracing configuration


tracing_config = TracingConfig()


def setup_tracing(
    service_name: str = "zeta-ai-server",
    jaeger_endpoint: str | None = None,
    enabled: bool = False,
) -> TracingConfig:
    """


    Setup distributed tracing for the application.





    Args:


        service_name: Name of the service


        jaeger_endpoint: Jaeger collector endpoint


        enabled: Whether to enable tracing





    Returns:


        TracingConfig: Configured tracing instance


    """

    global tracing_config

    tracing_config = TracingConfig(service_name, jaeger_endpoint, enabled)

    return tracing_config


def get_tracer() -> Any | None:
    """Get current tracer instance."""

    return tracing_config.tracer if tracing_config.enabled else None


def trace_span(
    name: str, **attributes: Any
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator for tracing function calls."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracing_config.create_span(name, **attributes):
                return func(*args, **kwargs)

        return wrapper

    return decorator
