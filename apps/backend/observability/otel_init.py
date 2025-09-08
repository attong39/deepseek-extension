"""
OpenTelemetry initialization cho ZETA_VN
Tích hợp traces, metrics, logs theo chuẩn production-ready
"""

from __future__ import annotations

import logging
import os
import Exception
import ImportError
import app
import bool
import e
import enable_db_instrumentation
import enable_logging_instrumentation
import environment
import float
import int
import kwargs
import name
import otlp_endpoint
import prometheus_port
import sample_rate
import self
import service_name
import service_version
import str
import tuple

logger = logging.getLogger(__name__)

# Optional imports cho OpenTelemetry
try:
    from opentelemetry import metrics, trace  # noqa: PLC0415
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter,  # noqa: PLC0415
    )
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,  # noqa: PLC0415
    )
    from opentelemetry.exporter.prometheus import (
        PrometheusMetricReader,  # noqa: PLC0415
    )
    from opentelemetry.instrumentation.fastapi import (
        FastAPIInstrumentor,  # noqa: PLC0415
    )
    from opentelemetry.instrumentation.httpx import (
        HTTPXClientInstrumentor,  # noqa: PLC0415
    )
    from opentelemetry.instrumentation.logging import (
        LoggingInstrumentor,  # noqa: PLC0415
    )
    from opentelemetry.instrumentation.requests import (
        RequestsInstrumentor,  # noqa: PLC0415
    )
    from opentelemetry.instrumentation.sqlalchemy import (
        SQLAlchemyInstrumentor,  # noqa: PLC0415
    )
    from opentelemetry.sdk.metrics import MeterProvider  # noqa: PLC0415
    from opentelemetry.sdk.metrics.export import (
        PeriodicExportingMetricReader,  # noqa: PLC0415
    )
    from opentelemetry.sdk.resources import (
        SERVICE_NAME,  # noqa: PLC0415
        SERVICE_VERSION,
        Resource,
    )
    from opentelemetry.sdk.trace import TracerProvider  # noqa: PLC0415
    from opentelemetry.sdk.trace.export import BatchSpanProcessor  # noqa: PLC0415
    from prometheus_client import start_http_server  # noqa: PLC0415

    OTEL_AVAILABLE = True

except ImportError as e:
    OTEL_AVAILABLE = False
    logger.warning(f"OpenTelemetry không khả dụng: {e}")


class ZetaOTelConfig:
    """Cấu hình OpenTelemetry cho ZETA_VN"""

    def __init__(
        self,
        service_name: str = "zeta-ai-server",
        service_version: str = "1.0.0",
        environment: str = "development",
        otlp_endpoint: str | None = None,
        prometheus_port: int = 8001,
        enable_logging_instrumentation: bool = True,
        enable_db_instrumentation: bool = True,
        sample_rate: float = 0.1,
    ):
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        self.otlp_endpoint = otlp_endpoint or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        self.prometheus_port = prometheus_port
        self.enable_logging_instrumentation = enable_logging_instrumentation
        self.enable_db_instrumentation = enable_db_instrumentation
        self.sample_rate = sample_rate


def setup_otel_tracing(config: ZetaOTelConfig) -> TracerProvider | None:
    """Thiết lập tracing với OpenTelemetry"""
    if not OTEL_AVAILABLE:
        logger.warning("OpenTelemetry không khả dụng - bỏ qua tracing setup")
        return None

    try:
        # Tạo resource
        resource = Resource.create(
            {
                SERVICE_NAME: config.service_name,
                SERVICE_VERSION: config.service_version,
                "environment": config.environment,
                "service.instance.id": os.getenv("HOSTNAME", "unknown"),
            }
        )

        # Tạo TracerProvider
        provider = TracerProvider(resource=resource)

        # Thêm OTLP exporter nếu có endpoint
        if config.otlp_endpoint:
            otlp_exporter = OTLPSpanExporter(endpoint=config.otlp_endpoint)
            span_processor = BatchSpanProcessor(otlp_exporter)
            provider.add_span_processor(span_processor)
            logger.info(f"OTLP trace exporter setup: {config.otlp_endpoint}")

        # Set global provider
        trace.set_tracer_provider(provider)

        logger.info(f"Tracing setup hoàn thành cho service: {config.service_name}")
        return provider

    except Exception as e:
        logger.error(f"Lỗi setup tracing: {e}")
        return None


def setup_otel_metrics(config: ZetaOTelConfig) -> MeterProvider | None:
    """Thiết lập metrics với OpenTelemetry"""
    if not OTEL_AVAILABLE:
        logger.warning("OpenTelemetry không khả dụng - bỏ qua metrics setup")
        return None

    try:
        # Tạo resource
        resource = Resource.create(
            {
                SERVICE_NAME: config.service_name,
                SERVICE_VERSION: config.service_version,
                "environment": config.environment,
            }
        )

        readers = []

        # Prometheus reader cho scraping
        prometheus_reader = PrometheusMetricReader()
        readers.append(prometheus_reader)

        # Start Prometheus HTTP server
        try:
            start_http_server(config.prometheus_port)
            logger.info(
                f"Prometheus metrics server khởi động trên port {config.prometheus_port}"
            )
        except Exception as e:
            logger.warning(f"Không thể khởi động Prometheus server: {e}")

        # OTLP metrics exporter nếu có endpoint
        if config.otlp_endpoint:
            otlp_exporter = OTLPMetricExporter(endpoint=config.otlp_endpoint)
            otlp_reader = PeriodicExportingMetricReader(
                otlp_exporter, export_interval_millis=30000
            )
            readers.append(otlp_reader)
            logger.info(f"OTLP metrics exporter setup: {config.otlp_endpoint}")

        # Tạo MeterProvider
        provider = MeterProvider(resource=resource, metric_readers=readers)
        metrics.set_meter_provider(provider)

        logger.info("Metrics setup hoàn thành")
        return provider

    except Exception as e:
        logger.error(f"Lỗi setup metrics: {e}")
        return None


def setup_auto_instrumentation(config: ZetaOTelConfig, app=None):
    """Thiết lập auto-instrumentation"""
    if not OTEL_AVAILABLE:
        return

    try:
        # FastAPI instrumentation
        if app:
            FastAPIInstrumentor.instrument_app(app)
            logger.info("FastAPI auto-instrumentation setup")

        # HTTP client instrumentation
        HTTPXClientInstrumentor().instrument()
        RequestsInstrumentor().instrument()
        logger.info("HTTP client auto-instrumentation setup")

        # Database instrumentation
        if config.enable_db_instrumentation:
            SQLAlchemyInstrumentor().instrument()
            logger.info("SQLAlchemy auto-instrumentation setup")

        # Logging instrumentation
        if config.enable_logging_instrumentation:
            LoggingInstrumentor().instrument(set_logging_format=True)
            logger.info("Logging auto-instrumentation setup")

    except Exception as e:
        logger.error(f"Lỗi setup auto-instrumentation: {e}")


def initialize_observability(
    app=None,
    service_name: str = "zeta-ai-server",
    environment: str = "development",
    **kwargs,
) -> tuple[TracerProvider | None, MeterProvider | None]:
    """
    Initialize toàn bộ observability stack

    Args:
        app: FastAPI app instance (optional)
        service_name: Tên service
        environment: Môi trường (development/production)
        **kwargs: Các config khác

    Returns:
        Tuple (TracerProvider, MeterProvider)
    """
    config = ZetaOTelConfig(
        service_name=service_name, environment=environment, **kwargs
    )

    logger.info(
        f"Khởi động observability cho {service_name} trong môi trường {environment}"
    )

    # Setup tracing
    tracer_provider = setup_otel_tracing(config)

    # Setup metrics
    meter_provider = setup_otel_metrics(config)

    # Setup auto-instrumentation
    setup_auto_instrumentation(config, app)

    logger.info("Observability initialization hoàn thành")
    return tracer_provider, meter_provider


# Global instances
_tracer_provider: TracerProvider | None = None
_meter_provider: MeterProvider | None = None


def get_tracer(name: str = "zeta-ai"):
    """Lấy tracer instance"""
    if OTEL_AVAILABLE and trace.get_tracer_provider():
        return trace.get_tracer(name)
    return None


def get_meter(name: str = "zeta-ai"):
    """Lấy meter instance"""
    if OTEL_AVAILABLE and metrics.get_meter_provider():
        return metrics.get_meter(name)
    return None
