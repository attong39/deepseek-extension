"""
Enhanced health endpoints cho ZETA_VN với dependency checking
Tích hợp observability và feature status
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import UTC, datetime
from typing import Any

from app.api.v1.__meta__ import API_VERSION, BUILD_TIME_UTC, SERVICE_NAME
from apps.backend.observability.metrics import get_metrics
from fastapi import APIRouter
from pydantic import BaseModel
import Exception
import all
import bool
import dep
import dict
import e
import enumerate
import error
import float
import i
import is_healthy
import isinstance
import k
import len
import result
import round
import str
import sum
import tuple
import v

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["System Health"])

# Server start time cho uptime calculation
_start_time = time.time()


class HealthCheck(BaseModel):
    """Health check response model"""

    status: str  # ready|degraded|down
    service: str
    version: str
    uptime_seconds: float
    timestamp: str
    dependencies: dict[str, Any]
    latency_ms: float


class LivenessCheck(BaseModel):
    """Liveness check response"""

    status: str
    timestamp: str


class ReadinessCheck(BaseModel):
    """Readiness check response"""

    status: str
    service: str
    build: str
    api: str
    dependencies: dict[str, bool]


async def check_database(timeout: float = 1.0) -> tuple[bool, str | None]:
    """Kiểm tra database connection"""
    try:
        # TODO: Thực hiện check database pool
        # await db_pool.execute("SELECT 1")
        await asyncio.sleep(0.01)  # Simulate DB check
        return True, None
    except Exception as e:
        return False, str(e)


async def check_redis(timeout: float = 0.5) -> tuple[bool, str | None]:
    """Kiểm tra Redis connection"""
    try:
        # TODO: Thực hiện check Redis
        # await redis_client.ping()
        await asyncio.sleep(0.01)  # Simulate Redis check
        return True, None
    except Exception as e:
        return False, str(e)


async def check_model_service(timeout: float = 1.0) -> tuple[bool, str | None]:
    """Kiểm tra AI model service"""
    try:
        # TODO: Thực hiện check model loading/inference
        # await model_service.health_check()
        await asyncio.sleep(0.01)  # Simulate model check
        return True, None
    except Exception as e:
        return False, str(e)


async def check_storage(timeout: float = 0.5) -> tuple[bool, str | None]:
    """Kiểm tra file storage"""
    try:
        # TODO: Kiểm tra S3/local storage
        # await storage_client.list_buckets()
        await asyncio.sleep(0.01)  # Simulate storage check
        return True, None
    except Exception as e:
        return False, str(e)


async def check_vector_db(timeout: float = 1.0) -> tuple[bool, str | None]:
    """Kiểm tra vector database"""
    try:
        # TODO: Kiểm tra Pinecone/Weaviate/Qdrant
        # await vector_db.health_check()
        await asyncio.sleep(0.01)  # Simulate vector DB check
        return True, None
    except Exception as e:
        return False, str(e)


async def run_dependency_checks() -> dict[str, Any]:
    """Chạy tất cả dependency checks song song"""
    start_time = time.perf_counter()

    try:
        # Chạy song song các checks với timeout
        results = await asyncio.gather(
            check_database(),
            check_redis(),
            check_model_service(),
            check_storage(),
            check_vector_db(),
            return_exceptions=True,
        )

        check_latency = (time.perf_counter() - start_time) * 1000

        dependencies = {}
        check_names = ["database", "redis", "model_service", "storage", "vector_db"]

        for i, result in enumerate(results):
            name = check_names[i]
            if isinstance(result, Exception):
                dependencies[name] = {
                    "status": False,
                    "error": str(result),
                    "latency_ms": None,
                }
            elif isinstance(result, tuple) and len(result) == 2:
                is_healthy, error = result
                dependencies[name] = {
                    "status": is_healthy,
                    "error": error,
                    "latency_ms": check_latency / len(check_names),  # Estimate
                }
            else:
                dependencies[name] = {
                    "status": False,
                    "error": "Invalid check result",
                    "latency_ms": None,
                }

        return dependencies

    except Exception as e:
        logger.error(f"Lỗi khi chạy dependency checks: {e}")
        return {
            "error": str(e),
            "latency_ms": (time.perf_counter() - start_time) * 1000,
        }


@router.get("/live", response_model=LivenessCheck)
async def liveness_check() -> LivenessCheck:
    """
    Liveness probe - kiểm tra process còn sống không
    Kubernetes dùng để restart pod nếu cần
    """
    return LivenessCheck(status="ok", timestamp=datetime.now(UTC).isoformat())


@router.get("/ready", response_model=ReadinessCheck)
async def readiness_check() -> ReadinessCheck:
    """
    Readiness probe - kiểm tra service sẵn sàng nhận traffic không
    Kubernetes dùng để quyết định route traffic đến pod
    """
    # Chạy basic dependency checks
    deps = await run_dependency_checks()

    # Xác định readiness dựa trên critical dependencies
    critical_deps = ["database", "model_service"]
    is_ready = all(
        deps.get(dep, {}).get("status", False) for dep in critical_deps if dep in deps
    )

    return ReadinessCheck(
        status="ready" if is_ready else "not_ready",
        service=SERVICE_NAME,
        build=BUILD_TIME_UTC,
        api=API_VERSION,
        dependencies={
            k: v.get("status", False) for k, v in deps.items() if isinstance(v, dict)
        },
    )


@router.get("/startup")
async def startup_check() -> dict[str, Any]:
    """
    Startup probe - kiểm tra service đã khởi động xong chưa
    Kubernetes dùng để biết khi nào bắt đầu liveness/readiness checks
    """
    uptime = time.time() - _start_time

    # Service coi như startup hoàn thành sau 10 giây
    is_started = uptime > 10.0

    return {
        "status": "ready" if is_started else "starting",
        "uptime_seconds": uptime,
        "message": "Service started" if is_started else f"Starting... {uptime:.1f}s",
    }


@router.get("", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """
    Comprehensive health check với dependency details
    Dùng cho monitoring và debugging
    """
    start_time = time.perf_counter()

    # Lấy uptime
    uptime_seconds = time.time() - _start_time

    # Chạy dependency checks
    dependencies = await run_dependency_checks()

    # Xác định overall status
    if "error" in dependencies:
        overall_status = "down"
    else:
        healthy_count = sum(
            1
            for dep in dependencies.values()
            if isinstance(dep, dict) and dep.get("status", False)
        )
        total_count = len([k for k in dependencies if k != "error"])

        if healthy_count == total_count:
            overall_status = "ready"
        elif healthy_count >= total_count * 0.7:  # 70% healthy
            overall_status = "degraded"
        else:
            overall_status = "down"

    # Tính latency
    check_latency = (time.perf_counter() - start_time) * 1000

    # Ghi metrics
    try:
        metrics = get_metrics()
        metrics.record_http_request("/health", "GET", 200, check_latency / 1000)
    except Exception as e:
        logger.warning(f"Không thể ghi health check metrics: {e}")

    return HealthCheck(
        status=overall_status,
        service=SERVICE_NAME,
        version=API_VERSION,
        uptime_seconds=uptime_seconds,
        timestamp=datetime.now(UTC).isoformat(),
        dependencies=dependencies,
        latency_ms=round(check_latency, 2),
    )


@router.get("/ping")
async def ping() -> dict[str, str]:
    """Simple ping endpoint cho basic connectivity check"""
    return {
        "message": "pong",
        "timestamp": datetime.now(UTC).isoformat(),
        "service": SERVICE_NAME,
    }


@router.get("/metrics-summary")
async def metrics_summary() -> dict[str, Any]:
    """
    Metrics summary cho health monitoring
    Chỉ expose metrics cơ bản, không sensitive data
    """
    try:
        metrics = get_metrics()
        simple_metrics = metrics.get_simple_metrics()

        return {
            "uptime_seconds": time.time() - _start_time,
            "metrics_available": True,
            "prometheus_enabled": metrics.use_prometheus,
            "otel_enabled": metrics.use_otel,
            "simple_metrics": {
                "counters_count": len(simple_metrics.get("counters", {})),
                "histograms_count": len(simple_metrics.get("histograms", {})),
                "gauges_count": len(simple_metrics.get("gauges", {})),
            },
        }
    except Exception as e:
        logger.error(f"Lỗi lấy metrics summary: {e}")
        return {
            "uptime_seconds": time.time() - _start_time,
            "metrics_available": False,
            "error": str(e),
        }
