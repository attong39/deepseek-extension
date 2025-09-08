"""
Security API Router - Zero-Trust Policy & JWKS Management
"""
from __future__ import annotations
import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from .jwt_dependency import get_current_user
from .opa_client import opa_decide, opa_health
from .jwks_cache import jwks_cache_manager
import Exception
import bool
import current_user
import e
import int
import key
import len
import list
import policy_input
import str


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/security", tags=["security"])


# Pydantic models
class PolicyInput(BaseModel):
    """Policy evaluation input"""
    subject: Dict[str, Any]
    resource: Dict[str, Any]
    action: str
    context: Dict[str, Any] = {}


class PolicyDecision(BaseModel):
    """Policy evaluation result"""
    allow: bool
    risk: str
    reasons: list[str]


class JWKSStatus(BaseModel):
    """JWKS cache status"""
    enabled: bool
    healthy: bool
    last_updated: str | None
    keys_count: int
    url: str | None


class OPAStatus(BaseModel):
    """OPA service status"""
    enabled: bool
    healthy: bool
    url: str | None


class SecurityStatus(BaseModel):
    """Overall security status"""
    jwks: JWKSStatus
    opa: OPAStatus


@router.post("/policy/evaluate", response_model=PolicyDecision)
async def evaluate_policy(
    policy_input: PolicyInput,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Evaluate Zero-Trust policy using OPA
    """
    try:
        # Add current user context to policy input
        payload = {
            "subject": current_user,
            "resource": policy_input.resource,
            "action": policy_input.action,
            "context": {
                **policy_input.context,
                "evaluator_user": current_user.get("sub", "unknown")
            }
        }
        
        decision = await opa_decide(payload)
        
        logger.info(
            f"Policy evaluation: user={current_user.get('sub')}, "
            f"action={policy_input.action}, "
            f"resource={policy_input.resource.get('type', 'unknown')}, "
            f"allow={decision['allow']}, risk={decision['risk']}"
        )
        
        return PolicyDecision(**decision)
        
    except Exception as e:
        logger.error(f"Policy evaluation error: {e}")
        
        # Fail-safe: deny access on error
        return PolicyDecision(
            allow=False,
            risk="high",
            reasons=["evaluation_error", str(e)]
        )


@router.get("/status", response_model=SecurityStatus)
async def security_status():
    """
    Get security subsystem status
    """
    try:
        # Get JWKS status
        jwks_status = await jwks_cache_manager.get_status()
        
        # Get OPA status
        opa_status = await opa_health()
        
        return SecurityStatus(
            jwks=JWKSStatus(
                enabled=jwks_status["enabled"],
                healthy=jwks_status["healthy"],
                last_updated=jwks_status.get("last_updated"),
                keys_count=jwks_status.get("keys_count", 0),
                url=jwks_status.get("url")
            ),
            opa=OPAStatus(
                enabled=opa_status["enabled"],
                healthy=opa_status["healthy"],
                url=opa_status.get("url")
            )
        )
        
    except Exception as e:
        logger.error(f"Security status error: {e}")
        raise


@router.post("/jwks/refresh")
async def refresh_jwks(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Force refresh JWKS cache (admin only)
    """
    # Check admin role
    user_roles = current_user.get("roles", [])
    if "admin" not in user_roles:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin role required")
    
    try:
        await jwks_cache_manager.force_refresh()
        
        logger.info(f"JWKS cache refreshed by admin: {current_user.get('sub')}")
        
        return {"message": "JWKS cache refreshed successfully"}
        
    except Exception as e:
        logger.error(f"JWKS refresh error: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Refresh failed: {e}")


@router.get("/jwks/keys")
async def get_jwks_keys(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get JWKS public keys (admin only)
    """
    # Check admin role
    user_roles = current_user.get("roles", [])
    if "admin" not in user_roles:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Admin role required")
    
    try:
        keys = await jwks_cache_manager.get_keys()
        
        # Return key metadata only (not full key material)
        key_info = []
        for key in keys:
            key_info.append({
                "kid": key.get("kid"),
                "kty": key.get("kty"),
                "alg": key.get("alg"),
                "use": key.get("use"),
                "last_seen": key.get("_cached_at")  # Internal metadata
            })
        
        return {
            "keys": key_info,
            "count": len(keys)
        }
        
    except Exception as e:
        logger.error(f"JWKS keys error: {e}")
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Keys retrieval failed: {e}")


@router.get("/health")
async def security_health():
    """
    Simple health check for security subsystem
    """
    return {
        "status": "healthy",
        "subsystems": ["jwks", "opa", "jwt"]
    }
