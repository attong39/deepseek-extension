"""
Performance Monitoring API Endpoints

Provides REST endpoints for accessing real-time performance metrics,
system health status, and performance analytics.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.middleware.performance import get_performance_middleware
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
import Exception
import dict
import e
import endpoint
import float
import int
import list
import max
import str
import window_minutes

router = APIRouter(
    prefix="/performance",
    tags=["performance"],
)

# Constants
MIDDLEWARE_NOT_AVAILABLE = "Performance monitoring middleware not available"


class PerformanceStatsResponse(BaseModel):
    """Performance statistics response model."""

    total_requests: int = Field(..., description="Total number of requests processed")
    successful_requests: int = Field(..., description="Number of successful requests")
    failed_requests: int = Field(..., description="Number of failed requests")
    average_response_time: float = Field(
        ..., description="Average response time in milliseconds"
    )
    p95_response_time: float = Field(
        ..., description="95th percentile response time in milliseconds"
    )
    p99_response_time: float = Field(
        ..., description="99th percentile response time in milliseconds"
    )
    requests_per_second: float = Field(..., description="Current requests per second")
    error_rate: float = Field(..., description="Error rate percentage")
    average_memory_mb: float = Field(..., description="Average memory usage in MB")
    average_cpu_percent: float = Field(..., description="Average CPU usage percentage")
    peak_memory_mb: float = Field(..., description="Peak memory usage in MB")
    peak_cpu_percent: float = Field(..., description="Peak CPU usage percentage")
    active_connections: int = Field(..., description="Current active connections")
    cache_hit_rate: float = Field(..., description="Cache hit rate percentage")
    database_query_time: float = Field(
        ..., description="Average database query time in milliseconds"
    )


class EndpointStatsResponse(BaseModel):
    """Endpoint-specific performance statistics."""

    count: int = Field(..., description="Number of requests to this endpoint")
    avg_ms: float = Field(..., description="Average response time in milliseconds")
    min_ms: float = Field(..., description="Minimum response time in milliseconds")
    max_ms: float = Field(..., description="Maximum response time in milliseconds")
    p50_ms: float = Field(
        ..., description="50th percentile response time in milliseconds"
    )
    p95_ms: float = Field(
        ..., description="95th percentile response time in milliseconds"
    )
    p99_ms: float = Field(
        ..., description="99th percentile response time in milliseconds"
    )


class SystemMetricsResponse(BaseModel):
    """System performance metrics response."""

    process: dict[str, Any] = Field(..., description="Process-specific metrics")
    system: dict[str, Any] = Field(..., description="System-wide metrics")
    application: dict[str, Any] = Field(..., description="Application-specific metrics")


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Overall system health status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    uptime_seconds: float = Field(..., description="Application uptime in seconds")
    performance_score: float = Field(..., description="Performance score (0-100)")
    alerts: list[str] = Field(..., description="Active performance alerts")
    recommendations: list[str] = Field(
        ..., description="Performance improvement recommendations"
    )


@router.get("/stats", response_model=PerformanceStatsResponse)
async def get_performance_stats(
    window_minutes: int = Query(
        5, ge=1, le=60, description="Time window for statistics in minutes"
    ),
) -> PerformanceStatsResponse:
    """
    Get aggregated performance statistics for the specified time window.

    Args:
        window_minutes: Time window for statistics calculation (1-60 minutes)

    Returns:
        Aggregated performance statistics

    Raises:
        HTTPException: If performance monitoring is not available
    """
    middleware = get_performance_middleware()
    if not middleware:
        raise HTTPException(status_code=503, detail=MIDDLEWARE_NOT_AVAILABLE)

    try:
        stats = middleware.get_performance_stats(window_minutes=window_minutes)
        return PerformanceStatsResponse(**stats.__dict__)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve performance statistics: {e!s}"
        ) from e


@router.get("/endpoints", response_model=dict[str, EndpointStatsResponse])
async def get_endpoint_stats() -> dict[str, EndpointStatsResponse]:
    """
    Get performance statistics for individual API endpoints.

    Returns:
        Dictionary mapping endpoint paths to their performance statistics

    Raises:
        HTTPException: If performance monitoring is not available
    """
    middleware = get_performance_middleware()
    if not middleware:
        raise HTTPException(status_code=503, detail=MIDDLEWARE_NOT_AVAILABLE)

    try:
        endpoint_stats = middleware.get_endpoint_stats()
        return {
            endpoint: EndpointStatsResponse(
                count=int(stats["count"]),
                avg_ms=stats["avg_ms"],
                min_ms=stats["min_ms"],
                max_ms=stats["max_ms"],
                p50_ms=stats["p50_ms"],
                p95_ms=stats["p95_ms"],
                p99_ms=stats["p99_ms"],
            )
            for endpoint, stats in endpoint_stats.items()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve endpoint statistics: {e!s}"
        ) from e


@router.get("/system", response_model=SystemMetricsResponse)
async def get_system_metrics() -> SystemMetricsResponse:
    """
    Get current system performance metrics.

    Returns:
        Current system performance metrics including process, system, and application data

    Raises:
        HTTPException: If performance monitoring is not available
    """
    middleware = get_performance_middleware()
    if not middleware:
        raise HTTPException(status_code=503, detail=MIDDLEWARE_NOT_AVAILABLE)

    try:
        metrics = middleware.get_system_metrics()
        if not metrics:
            raise HTTPException(
                status_code=500, detail="Failed to collect system metrics"
            )

        return SystemMetricsResponse(**metrics)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve system metrics: {e!s}"
        ) from e


@router.get("/health", response_model=HealthCheckResponse)
async def get_health_check() -> HealthCheckResponse:
    """
    Get comprehensive health check including performance analysis.

    Returns:
        Health check status with performance analysis and recommendations

    Raises:
        HTTPException: If performance monitoring is not available
    """
    middleware = get_performance_middleware()
    if not middleware:
        raise HTTPException(status_code=503, detail=MIDDLEWARE_NOT_AVAILABLE)

    try:
        # Get current stats and system metrics
        stats = middleware.get_performance_stats(window_minutes=5)
        system_metrics = middleware.get_system_metrics()

        # Calculate performance score (0-100)
        performance_score = _calculate_performance_score(stats, system_metrics)

        # Determine overall status
        if performance_score >= 80:
            status = "healthy"
        elif performance_score >= 60:
            status = "degraded"
        else:
            status = "unhealthy"

        # Generate alerts and recommendations
        alerts = _generate_alerts(stats, system_metrics)
        recommendations = _generate_recommendations(stats, system_metrics)

        return HealthCheckResponse(
            status=status,
            timestamp=datetime.now(),
            uptime_seconds=system_metrics.get("application", {}).get(
                "uptime_seconds", 0
            ),
            performance_score=performance_score,
            alerts=alerts,
            recommendations=recommendations,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to perform health check: {e!s}"
        ) from e


@router.post("/reset")
async def reset_performance_metrics() -> dict[str, str]:
    """
    Reset all performance metrics and counters.

    Returns:
        Confirmation message

    Raises:
        HTTPException: If performance monitoring is not available
    """
    middleware = get_performance_middleware()
    if not middleware:
        raise HTTPException(status_code=503, detail=MIDDLEWARE_NOT_AVAILABLE)

    try:
        middleware.reset_metrics()
        return {"message": "Performance metrics reset successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to reset performance metrics: {e!s}"
        ) from e


def _calculate_performance_score(stats: Any, system_metrics: dict[str, Any]) -> float:
    """Calculate overall performance score (0-100)."""
    score = 100.0

    # Response time impact (max -30 points)
    if stats.average_response_time > 1000:  # > 1s
        score -= 30
    elif stats.average_response_time > 500:  # > 500ms
        score -= 15
    elif stats.average_response_time > 200:  # > 200ms
        score -= 5

    # Error rate impact (max -25 points)
    if stats.error_rate > 10:  # > 10%
        score -= 25
    elif stats.error_rate > 5:  # > 5%
        score -= 15
    elif stats.error_rate > 1:  # > 1%
        score -= 5

    # Memory usage impact (max -20 points)
    memory_percent = system_metrics.get("process", {}).get("memory_percent", 0)
    if memory_percent > 80:
        score -= 20
    elif memory_percent > 60:
        score -= 10
    elif memory_percent > 40:
        score -= 5

    # CPU usage impact (max -15 points)
    cpu_percent = system_metrics.get("process", {}).get("cpu_percent", 0)
    if cpu_percent > 80:
        score -= 15
    elif cpu_percent > 60:
        score -= 10
    elif cpu_percent > 40:
        score -= 5

    # Throughput impact (max -10 points)
    if stats.requests_per_second < 1:
        score -= 10
    elif stats.requests_per_second < 5:
        score -= 5

    return max(0.0, score)


def _generate_alerts(stats: Any, system_metrics: dict[str, Any]) -> list[str]:
    """Generate performance alerts based on current metrics."""
    alerts = []

    # Response time alerts
    if stats.average_response_time > 1000:
        alerts.append(
            f"High average response time: {stats.average_response_time:.1f}ms"
        )

    if stats.p99_response_time > 3000:
        alerts.append(f"Very high P99 response time: {stats.p99_response_time:.1f}ms")

    # Error rate alerts
    if stats.error_rate > 5:
        alerts.append(f"High error rate: {stats.error_rate:.1f}%")

    # Memory alerts
    memory_percent = system_metrics.get("process", {}).get("memory_percent", 0)
    if memory_percent > 80:
        alerts.append(f"High memory usage: {memory_percent:.1f}%")

    # CPU alerts
    cpu_percent = system_metrics.get("process", {}).get("cpu_percent", 0)
    if cpu_percent > 80:
        alerts.append(f"High CPU usage: {cpu_percent:.1f}%")

    # System memory alerts
    system_memory_percent = system_metrics.get("system", {}).get("memory_percent", 0)
    if system_memory_percent > 90:
        alerts.append(f"Critical system memory usage: {system_memory_percent:.1f}%")

    return alerts


def _generate_recommendations(stats: Any, system_metrics: dict[str, Any]) -> list[str]:
    """Generate performance improvement recommendations."""
    recommendations = []

    # Response time recommendations
    if stats.average_response_time > 500:
        recommendations.append(
            "Consider implementing response caching for frequently accessed data"
        )
        recommendations.append("Review database queries for optimization opportunities")

    # Error rate recommendations
    if stats.error_rate > 1:
        recommendations.append(
            "Review error logs to identify and fix common failure patterns"
        )
        recommendations.append("Implement circuit breakers for external service calls")

    # Memory recommendations
    memory_percent = system_metrics.get("process", {}).get("memory_percent", 0)
    if memory_percent > 60:
        recommendations.append(
            "Monitor for memory leaks and optimize object lifecycle management"
        )
        recommendations.append("Consider implementing memory-efficient data structures")

    # Throughput recommendations
    if stats.requests_per_second < 10:
        recommendations.append(
            "Consider implementing connection pooling and async processing"
        )
        recommendations.append("Review request handling pipeline for bottlenecks")

    # General recommendations
    if stats.total_requests > 1000:
        recommendations.append("Consider implementing rate limiting to prevent abuse")
        recommendations.append("Set up automated performance monitoring and alerting")

    return recommendations
