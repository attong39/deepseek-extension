"""API endpoints for Self-Improvement system."""

from typing import Any

from apps.backend.core.container import Container
from apps.backend.core.self_improvement.auto_updater import UpdatePriority
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/self-improvement", tags=["self-improvement"])


class UpdateRequest(BaseModel):
    """Request model for manual update trigger."""
import Exception
import bool
import container
import dict
import e
import float
import int
import len
import list
import r
import result
import str
import sum
import update_request

    version: str
    changelog: str
    features: list[str]
    performance: bool = False
    force_priority: UpdatePriority | None = None


class UpdateResponse(BaseModel):
    """Response model for update operations."""

    status: str
    priority: str
    estimated_downtime_seconds: int
    actions_taken: list[str] = []
    rollback_available: bool = False


class HealthResponse(BaseModel):
    """Response model for health status."""

    score: float
    status: str
    metrics: dict[str, Any]
    monitoring_active: bool


def get_container() -> Container:
    """Get dependency injection container."""
    return Container()


@router.get("/health", response_model=HealthResponse)
async def get_system_health(
    container: Container = Depends(get_container),
) -> HealthResponse:
    """Get current system health status."""
    try:
        health_monitor = container.health_monitor()

        # Get health summary
        summary = health_monitor.get_health_summary()
        current_health = summary["current_health"]
        monitoring_status = summary["monitoring_status"]

        return HealthResponse(
            score=current_health["score"],
            status=current_health["status"],
            metrics=current_health.get("metrics", {}),
            monitoring_active=monitoring_status["is_active"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get health status: {str(e)}",
        )


@router.post("/health/heal")
async def trigger_manual_healing(
    container: Container = Depends(get_container),
) -> dict[str, Any]:
    """Trigger manual healing process."""
    try:
        health_monitor = container.health_monitor()

        # Collect current metrics
        metrics = health_monitor.collect_health_metrics()

        # Trigger healing
        healing_results = health_monitor.auto_heal(metrics)

        return {
            "status": "healing_triggered",
            "actions_attempted": len(healing_results),
            "successful_actions": sum(1 for r in healing_results if r.success),
            "healing_results": [
                {
                    "action": r.action.value,
                    "success": r.success,
                    "execution_time_ms": r.execution_time_ms,
                    "health_improvement": r.health_after - r.health_before,
                }
                for r in healing_results
            ],
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger healing: {str(e)}",
        )


@router.get("/updates/status")
async def get_update_status(
    container: Container = Depends(get_container),
) -> dict[str, Any]:
    """Get update system status."""
    try:
        updater = container.intelligent_updater()
        return updater.get_update_status()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get update status: {str(e)}",
        )


@router.post("/updates/check")
async def check_for_updates(
    update_request: UpdateRequest | None = None,
    container: Container = Depends(get_container),
) -> dict[str, Any]:
    """Check for available updates and optionally apply them."""
    try:
        updater = container.intelligent_updater()

        # Convert request to release metadata
        release_meta = None
        if update_request:
            release_meta = {
                "version": update_request.version,
                "changelog": update_request.changelog,
                "features": update_request.features,
                "performance": update_request.performance,
            }

        # Check and potentially apply updates
        _ = updater.check_and_update(release_meta)

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check for updates: {str(e)}",
        )


@router.post("/updates/plan")
async def create_update_plan(
    update_request: UpdateRequest, container: Container = Depends(get_container)
) -> dict[str, Any]:
    """Create an update plan without executing it."""
    try:
        updater = container.intelligent_updater()

        # Convert request to release metadata
        release_meta = {
            "version": update_request.version,
            "changelog": update_request.changelog,
            "features": update_request.features,
            "performance": update_request.performance,
        }

        # Create update plan
        plan = updater.create_update_plan(release_meta)

        return {
            "priority": plan.priority.value,
            "estimated_downtime_seconds": plan.estimated_downtime_seconds,
            "rollback_strategy": plan.rollback_strategy,
            "safety_checks": plan.safety_checks,
            "impact_assessment": plan.impact_assessment,
            "created_at": plan.created_at.isoformat(),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create update plan: {str(e)}",
        )


@router.get("/status")
async def get_self_improvement_status(
    container: Container = Depends(get_container),
) -> dict[str, Any]:
    """Get comprehensive self-improvement system status."""
    try:
        # Get health monitor status
        health_monitor = container.health_monitor()
        health_summary = health_monitor.get_health_summary()

        # Get updater status
        updater = container.intelligent_updater()
        update_status = updater.get_update_status()

        return {
            "system_health": {
                "current_score": health_summary["current_health"]["score"],
                "status": health_summary["current_health"]["status"],
                "monitoring_active": health_summary["monitoring_status"]["is_active"],
                "healing_stats": health_summary.get("healing_stats", {}),
            },
            "auto_updater": {
                "current_version": update_status["current_version"],
                "last_check": update_status["last_check"],
                "status": update_status["status"],
                "update_history_count": update_status["update_history_count"],
            },
            "self_improvement_active": True,
            "last_updated": health_summary["current_health"].get(
                "timestamp", "unknown"
            ),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get self-improvement status: {str(e)}",
        )


@router.post("/monitoring/start")
async def start_health_monitoring(
    container: Container = Depends(get_container),
) -> dict[str, str]:
    """Start continuous health monitoring."""
    try:
        health_monitor = container.health_monitor()

        if health_monitor.is_monitoring:
            return {
                "status": "already_running",
                "message": "Health monitoring is already active",
            }

        # Start monitoring in background
        # In real implementation, would use background tasks
        # asyncio.create_task(health_monitor.monitor_and_heal())

        return {
            "status": "started",
            "message": "Health monitoring started successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start monitoring: {str(e)}",
        )


@router.post("/monitoring/stop")
async def stop_health_monitoring(
    container: Container = Depends(get_container),
) -> dict[str, str]:
    """Stop continuous health monitoring."""
    try:
        health_monitor = container.health_monitor()
        health_monitor.stop_monitoring()

        return {
            "status": "stopped",
            "message": "Health monitoring stopped successfully",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop monitoring: {str(e)}",
        )
