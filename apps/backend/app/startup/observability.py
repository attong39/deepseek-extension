"""
Observability startup module
Khởi tạo metrics, tracing, và health checks cho FastAPI app
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import Exception
import ImportError
import bool
import dict
import e
import enable_metrics
import enable_tracing
import print
import str

if TYPE_CHECKING:
    from fastapi import FastAPI  # noqa: PLC0415

# Import observability modules (với fallback nếu thiếu dependencies)
try:
    from apps.backend.observability.metrics import (  # noqa: PLC0415
        ZetaMetrics,
        init_metrics,
    )

    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    ZetaMetrics = None

try:
    from apps.backend.observability.otel_init import (
        setup_otel_for_fastapi,  # noqa: PLC0415
    )

    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

from app.middleware.metrics_middleware import MetricsMiddleware


def setup_observability(
    app: FastAPI, enable_metrics: bool = True, enable_tracing: bool = True
) -> None:
    """
    Thiết lập observability cho FastAPI app

    Args:
        app: FastAPI application instance
        enable_metrics: Bật metrics collection (Prometheus)
        enable_tracing: Bật distributed tracing (OpenTelemetry)
    """

    # 1. Khởi tạo metrics nếu có thể
    metrics_collector: ZetaMetrics | None = None
    if enable_metrics and METRICS_AVAILABLE:
        try:
            metrics_collector = init_metrics(
                use_prometheus=True, use_otel=enable_tracing
            )
            app.state.metrics = metrics_collector
            print("✅ Metrics initialized successfully")
        except Exception as e:
            print(f"⚠️  Failed to initialize metrics: {e}")

    # 2. Thêm metrics middleware
    if metrics_collector:
        app.add_middleware(MetricsMiddleware, metrics_collector=metrics_collector)
        print("✅ Metrics middleware added")

    # 3. Khởi tạo OpenTelemetry tracing nếu có thể
    if enable_tracing and OTEL_AVAILABLE:
        try:
            setup_otel_for_fastapi(app)
            print("✅ OpenTelemetry tracing initialized")
        except Exception as e:
            print(f"⚠️  Failed to initialize tracing: {e}")

    # 4. Thêm metrics endpoint cho Prometheus scraping
    if metrics_collector:
        _add_metrics_endpoint(app)

    # 5. Enhance health endpoint
    _enhance_health_endpoints(app)


def _add_metrics_endpoint(app: FastAPI) -> None:
    """Thêm /metrics endpoint cho Prometheus"""

    @app.get("/metrics", include_in_schema=False)
    async def metrics_endpoint():
        """Prometheus metrics endpoint"""
        try:
            from fastapi import Response  # noqa: PLC0415
            from prometheus_client import (
                CONTENT_TYPE_LATEST,  # noqa: PLC0415
                REGISTRY,
                generate_latest,
            )

            # Generate Prometheus metrics
            metrics_data = generate_latest(REGISTRY)
            return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)

        except ImportError:
            # Fallback nếu không có prometheus_client
            from fastapi.responses import JSONResponse  # noqa: PLC0415

            return JSONResponse({"error": "Prometheus metrics not available"})
        except Exception as e:
            from fastapi.responses import JSONResponse  # noqa: PLC0415

            return JSONResponse(
                {"error": f"Failed to get metrics: {e}"}, status_code=503
            )


def _enhance_health_endpoints(app: FastAPI) -> None:
    """Thêm các enhanced health endpoints"""

    @app.get("/api/v1/health/live", tags=["health"])
    async def liveness_probe():
        """Liveness probe - app đang chạy"""
        return {"status": "alive", "timestamp": "2025-08-24T12:00:00Z"}

    @app.get("/api/v1/health/ready", tags=["health"])
    async def readiness_probe():
        """Readiness probe - app sẵn sàng nhận traffic"""
        try:
            from app.api.v1._common.health import (
                enhanced_health_check,  # noqa: PLC0415
            )

            return await enhanced_health_check()
        except ImportError:
            # Fallback đơn giản
            return {"status": "ready", "checks": {"basic": True}}
        except Exception as e:
            return {"status": "not_ready", "error": str(e)}

    @app.get("/api/v1/health/startup", tags=["health"])
    async def startup_probe():
        """Startup probe - app đã khởi động xong"""
        return {
            "status": "started",
            "observability": {"metrics": METRICS_AVAILABLE, "tracing": OTEL_AVAILABLE},
        }


def get_observability_info() -> dict:
    """Lấy thông tin về trạng thái observability"""
    return {
        "metrics_available": METRICS_AVAILABLE,
        "tracing_available": OTEL_AVAILABLE,
        "features": {"prometheus": METRICS_AVAILABLE, "opentelemetry": OTEL_AVAILABLE},
    }
