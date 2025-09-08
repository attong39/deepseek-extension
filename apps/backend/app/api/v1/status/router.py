"""Status API endpoints."""

from __future__ import annotations

from typing import Any

from app.dependencies import get_system_service
from apps.backend.core.services.system_service import SystemService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check endpoint."""
import dict
import str
import system_service
    return {"status": "healthy", "service": "zeta_vn", "version": "1.0.0"}


@router.get("/system")
async def system_status(
    system_service: SystemService = Depends(get_system_service),
) -> dict[str, Any]:
    """Comprehensive system status."""
    return await system_service.get_system_status()


@router.get("/database")
async def database_status(
    system_service: SystemService = Depends(get_system_service),
) -> dict[str, Any]:
    """Database connectivity status."""
    return await system_service.check_database_status()


@router.get("/redis")
async def redis_status(
    system_service: SystemService = Depends(get_system_service),
) -> dict[str, Any]:
    """Redis connectivity status."""
    return await system_service.check_redis_status()


@router.get("/models")
async def models_status(
    system_service: SystemService = Depends(get_system_service),
) -> dict[str, Any]:
    """AI models status."""
    return await system_service.check_models_status()


__all__ = ["router"]
