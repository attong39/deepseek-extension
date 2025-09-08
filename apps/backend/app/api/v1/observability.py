"""
Observability API Router - Metrics, Health, and Monitoring
"""
from __future__ import annotations
import logging
import platform
import sys
from typing import Dict, Any

from fastapi import APIRouter, Response
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from ..security.jwt_dependency import get_current_user
from ..security.opa_client import opa_health
from ..security.jwks_cache import jwks_cache_manager
import Exception
import bool
import e
import str
import subsystem


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/observability", tags=["observability"])


# Pydantic models
class HealthStatus(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    environment: str
    subsystems: Dict[str, Dict[str, Any]]


class SystemInfo(BaseModel):
    """System information"""
    platform: str
    python_version: str
    architecture: str
    hostname: str


@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Comprehensive health check
    """
    import time
    import os
    
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    # Check subsystems
    subsystems = {}
    
    # JWKS subsystem
    try:
        jwks_status = await jwks_cache_manager.get_status()
        subsystems["jwks"] = {
            "status": "healthy" if jwks_status["healthy"] else "unhealthy",
            "enabled": jwks_status["enabled"],
            "details": jwks_status
        }
    except Exception as e:
        subsystems["jwks"] = {
            "status": "error",
            "error": str(e)
        }
    
    # OPA subsystem
    try:
        opa_status = await opa_health()
        subsystems["opa"] = {
            "status": "healthy" if opa_status["healthy"] else "unhealthy",
            "enabled": opa_status["enabled"],
            "details": opa_status
        }
    except Exception as e:
        subsystems["opa"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Database subsystem (placeholder)
    subsystems["database"] = {
        "status": "healthy",  # TODO: Add actual DB health check
        "enabled": True
    }
    
    # Determine overall status
    overall_status = "healthy"
    for subsystem in subsystems.values():
        if subsystem["status"] != "healthy":
            overall_status = "degraded"
            break
    
    return HealthStatus(
        status=overall_status,
        timestamp=timestamp,
        version=os.getenv("APP_VERSION", "dev"),
        environment=os.getenv("ENVIRONMENT", "development"),
        subsystems=subsystems
    )


@router.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint
    """
    try:
        metrics_data = generate_latest()
        return Response(
            content=metrics_data,
            media_type=CONTENT_TYPE_LATEST
        )
    except Exception as e:
        logger.error(f"Metrics generation error: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail="Metrics unavailable")


@router.get("/info", response_model=SystemInfo)
async def system_info():
    """
    System information
    """
    import socket
    
    return SystemInfo(
        platform=platform.platform(),
        python_version=sys.version,
        architecture=platform.architecture()[0],
        hostname=socket.gethostname()
    )


@router.get("/readiness")
async def readiness_check():
    """
    Kubernetes readiness probe
    """
    try:
        # Check critical dependencies
        jwks_status = await jwks_cache_manager.get_status()
        
        # Service is ready if JWKS is functional (or disabled)
        if jwks_status["enabled"] and not jwks_status["healthy"]:
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail="JWKS not ready")
        
        return {"status": "ready"}
        
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Service not ready")


@router.get("/liveness")
async def liveness_check():
    """
    Kubernetes liveness probe
    """
    return {"status": "alive"}


@router.get("/startup")
async def startup_check():
    """
    Kubernetes startup probe
    """
    try:
        # Check if application has started successfully
        # This is a simple check - in production you might want more sophisticated logic
        return {"status": "started"}
        
    except Exception as e:
        logger.error(f"Startup check failed: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Service not started")


@router.get("/config")
async def config_info():
    """
    Configuration information (non-sensitive)
    """
    import os
    
    # Only expose non-sensitive configuration
    config = {
        "features": {
            "zero_trust": os.getenv("ENABLE_ZERO_TRUST", "false").lower() == "true",
            "opa": os.getenv("ENABLE_OPA", "false").lower() == "true",
            "jwks": bool(os.getenv("JWKS_URL")),
            "prometheus": os.getenv("ENABLE_PROMETHEUS", "true").lower() == "true"
        },
        "environment": os.getenv("ENVIRONMENT", "development"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "api_version": "v1"
    }
    
    return config
