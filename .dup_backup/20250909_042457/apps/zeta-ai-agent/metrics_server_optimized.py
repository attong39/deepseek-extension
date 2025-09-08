# 🚀 Optimized Metrics Server Implementation

import asyncio
import sqlite3
import time
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime
from threading import RLock

import psutil
import structlog
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config.settings import get_environment_settings
import Exception
import all
import bool
import call_next
import check_func
import conn
import count
import dict
import e
import exc
import feedback
import float
import int
import len
import list
import m
import maxsize
import metric
import name
import older_than
import request
import self
import str
import sum

# Initialize settings
settings = get_environment_settings()

# Initialize logger
logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter("zeta_requests_total", "Total requests", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("zeta_request_duration_seconds", "Request duration", ["endpoint"])
MEMORY_USAGE = Gauge("zeta_memory_usage_bytes", "Memory usage in bytes")
CPU_USAGE = Gauge("zeta_cpu_usage_percent", "CPU usage percentage")
ACTIVE_CONNECTIONS = Gauge("zeta_active_connections", "Active connections")
ERROR_COUNT = Counter("zeta_errors_total", "Total errors", ["error_type"])

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


class CircularMetricsBuffer:
    """Memory-efficient circular buffer for metrics"""

    def __init__(self, maxsize: int = 50000):
        self.buffer = deque(maxlen=maxsize)
        self.lock = RLock()

    def add_metric(self, metric: dict) -> None:
        with self.lock:
            metric["timestamp"] = time.time()
            self.buffer.append(metric)

    def get_recent_metrics(self, count: int = 100) -> list[dict]:
        with self.lock:
            return list(self.buffer)[-count:]

    def clear_old_metrics(self, older_than: float) -> int:
        """Clear metrics older than specified timestamp"""
        with self.lock:
            current_time = time.time()
            removed_count = 0
            while self.buffer and self.buffer[0]["timestamp"] < current_time - older_than:
                self.buffer.popleft()
                removed_count += 1
            return removed_count

    def get_stats(self) -> dict:
        with self.lock:
            if not self.buffer:
                return {"count": 0, "memory_usage_mb": 0}

            return {
                "count": len(self.buffer),
                "oldest_timestamp": self.buffer[0]["timestamp"] if self.buffer else None,
                "newest_timestamp": self.buffer[-1]["timestamp"] if self.buffer else None,
                "memory_usage_mb": len(str(self.buffer)) / (1024 * 1024),
            }


class SystemMetricsCollector:
    """Collect system metrics periodically"""

    def __init__(self):
        self.process = psutil.Process()
        self.is_running = False

    async def start_collection(self):
        """Start metrics collection"""
        self.is_running = True
        while self.is_running:
            try:
                # Memory metrics
                memory_info = self.process.memory_info()
                MEMORY_USAGE.set(memory_info.rss)

                # CPU metrics
                cpu_percent = self.process.cpu_percent()
                CPU_USAGE.set(cpu_percent)

                # Log system status
                if cpu_percent > settings.monitoring.cpu_threshold:
                    logger.warning(f"High CPU usage: {cpu_percent}%")

                memory_percent = psutil.virtual_memory().percent
                if memory_percent > settings.monitoring.memory_threshold:
                    logger.warning(f"High memory usage: {memory_percent}%")

                await asyncio.sleep(settings.metrics.collection_interval)

            except Exception as e:
                logger.error(f"Failed to collect system metrics: {e}")
                ERROR_COUNT.labels(error_type="system_metrics").inc()
                await asyncio.sleep(60)  # Retry after 1 minute

    def stop_collection(self):
        """Stop metrics collection"""
        self.is_running = False


class HealthCheckRegistry:
    """Registry for health checks"""

    def __init__(self):
        self.checks = {}

    def register(self, name: str, check_func):
        self.checks[name] = check_func

    async def run_all_checks(self) -> dict[str, bool]:
        results = {}
        for name, check_func in self.checks.items():
            try:
                if asyncio.iscoroutinefunction(check_func):
                    results[name] = await check_func()
                else:
                    results[name] = check_func()
            except Exception as e:
                logger.error(f"Health check {name} failed: {e}")
                results[name] = False
        return results


# Global instances
metrics_buffer = CircularMetricsBuffer(maxsize=settings.metrics.buffer_size)
metrics_collector = SystemMetricsCollector()
health_registry = HealthCheckRegistry()


# Pydantic models
class FeedbackRequest(BaseModel):
    model_name: str = Field(..., max_length=50, description="AI model name")
    prompt: str = Field(..., max_length=settings.security.max_prompt_length, description="User prompt")
    response: str = Field(..., max_length=settings.security.max_response_length, description="AI response")
    rating: int = Field(..., ge=1, le=10, description="Rating from 1-10")
    latency: float = Field(..., gt=0, le=300, description="Response latency in seconds")
    vietnamese_quality: int = Field(..., ge=1, le=10, description="Vietnamese quality rating")
    session_id: str = Field(..., max_length=50, description="Session identifier")


# Health check functions
async def check_database() -> bool:
    """Check database connectivity"""
    try:
        with sqlite3.connect(settings.database.url.replace("sqlite:///", ""), timeout=5) as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False


def check_memory() -> bool:
    """Check memory usage"""
    memory_percent = psutil.virtual_memory().percent
    return memory_percent < settings.monitoring.memory_threshold


def check_disk_space() -> bool:
    """Check disk space"""
    disk_usage = psutil.disk_usage("/").percent
    return disk_usage < settings.monitoring.disk_threshold


def check_buffer_health() -> bool:
    """Check metrics buffer health"""
    stats = metrics_buffer.get_stats()
    max_size_mb = settings.cache.max_memory_mb
    return stats.get("memory_usage_mb", 0) < max_size_mb


# Register health checks
health_registry.register("database", check_database)
health_registry.register("memory", check_memory)
health_registry.register("disk", check_disk_space)
health_registry.register("buffer", check_buffer_health)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Zeta AI Agent metrics server", version=settings.version, environment=settings.environment)

    # Start metrics collection
    metrics_task = asyncio.create_task(metrics_collector.start_collection())

    # Cleanup old metrics periodically
    async def cleanup_old_metrics():
        while True:
            try:
                retention_seconds = settings.metrics.retention_days * 24 * 3600
                removed = metrics_buffer.clear_old_metrics(retention_seconds)
                if removed > 0:
                    logger.info(f"Cleaned up {removed} old metrics")
                await asyncio.sleep(3600)  # Run every hour
            except Exception as e:
                logger.error(f"Failed to cleanup metrics: {e}")
                await asyncio.sleep(3600)

    cleanup_task = asyncio.create_task(cleanup_old_metrics())

    yield

    # Shutdown
    logger.info("Shutting down metrics server")
    metrics_collector.stop_collection()
    metrics_task.cancel()
    cleanup_task.cancel()

    try:
        await metrics_task
        await cleanup_task
    except asyncio.CancelledError:
        pass


# Initialize FastAPI app
app = FastAPI(
    title="Zeta AI Agent Metrics Server",
    description="Optimized metrics collection and monitoring",
    version=settings.version,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allowed_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allowed_methods,
    allow_headers=settings.cors.allowed_headers,
    max_age=settings.cors.max_age,
)


# Rate limiting error handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(status_code=429, content={"detail": f"Rate limit exceeded: {exc.detail}"})
    return response


# Middleware for request metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Record metrics
    duration = time.time() - start_time
    REQUEST_DURATION.labels(endpoint=request.url.path).observe(duration)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=response.status_code).inc()

    return response


@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "version": settings.version,
    }


@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with all components"""
    results = await health_registry.run_all_checks()
    overall_status = "healthy" if all(results.values()) else "unhealthy"

    buffer_stats = metrics_buffer.get_stats()

    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment,
        "version": settings.version,
        "checks": results,
        "metrics": {
            "buffer_size": buffer_stats["count"],
            "buffer_memory_mb": buffer_stats.get("memory_usage_mb", 0),
            "memory_usage_percent": psutil.virtual_memory().percent,
            "cpu_usage_percent": psutil.cpu_percent(),
            "disk_usage_percent": psutil.disk_usage("/").percent,
        },
    }


@app.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes"""
    # Check critical components
    try:
        db_ok = await check_database()
        memory_ok = check_memory()

        if db_ok and memory_ok:
            return {"status": "ready"}
        else:
            raise HTTPException(status_code=503, detail="Service not ready")
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        raise HTTPException(status_code=503, detail="Service not ready")


@app.post("/feedback")
@limiter.limit(f"{settings.security.rate_limit_requests}/minute")
async def submit_feedback(request: Request, feedback: FeedbackRequest):
    """Submit feedback with rate limiting and validation"""
    try:
        # Add to metrics buffer
        feedback_data = feedback.model_dump()
        metrics_buffer.add_metric(feedback_data)

        # Store in database (simplified for demo)
        db_path = settings.database.url.replace("sqlite:///", "")
        with sqlite3.connect(db_path, timeout=settings.database.timeout) as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO feedback 
                (model_name, prompt, response, rating, latency, vietnamese_quality, session_id, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    feedback.model_name,
                    feedback.prompt[:1000],  # Truncate for storage
                    feedback.response[:2000],  # Truncate for storage
                    feedback.rating,
                    feedback.latency,
                    feedback.vietnamese_quality,
                    feedback.session_id,
                    time.time(),
                ),
            )
            conn.commit()

        logger.info(
            "Feedback submitted successfully",
            model=feedback.model_name,
            rating=feedback.rating,
            session=feedback.session_id,
        )

        return {"status": "success", "message": "Feedback recorded"}

    except Exception as e:
        logger.error(f"Failed to submit feedback: {e}")
        ERROR_COUNT.labels(error_type="feedback_submission").inc()
        raise HTTPException(status_code=500, detail="Failed to record feedback")


@app.get("/metrics")
async def get_prometheus_metrics():
    """Get Prometheus metrics"""
    if not settings.metrics.export_enabled:
        raise HTTPException(status_code=404, detail="Metrics export disabled")

    return generate_latest()


@app.get("/stats")
async def get_stats():
    """Get aggregated statistics"""
    try:
        recent_metrics = metrics_buffer.get_recent_metrics(1000)

        if not recent_metrics:
            return {"message": "No metrics available"}

        # Calculate statistics
        ratings = [m["rating"] for m in recent_metrics if "rating" in m]
        latencies = [m["latency"] for m in recent_metrics if "latency" in m]

        stats = {
            "total_feedback": len(recent_metrics),
            "avg_rating": sum(ratings) / len(ratings) if ratings else 0,
            "avg_latency": sum(latencies) / len(latencies) if latencies else 0,
            "buffer_stats": metrics_buffer.get_stats(),
            "system_stats": {
                "memory_percent": psutil.virtual_memory().percent,
                "cpu_percent": psutil.cpu_percent(),
                "disk_percent": psutil.disk_usage("/").percent,
            },
        }

        return stats

    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        ERROR_COUNT.labels(error_type="stats_retrieval").inc()
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "metrics_server_optimized:app",
        host=settings.server.host,
        port=settings.server.port,
        workers=settings.server.workers,
        reload=settings.server.reload,
        log_level=settings.server.log_level.lower(),
    )
