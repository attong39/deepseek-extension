"""
Security Policy API Router for Zero-Trust and OPA Integration
Provides policy evaluation endpoints with side-by-side ABAC/OPA comparison.
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from prometheus_client import Counter

from ...security.jwt_dependency import Identity, get_identity
from ...security.opa_client import evaluate_zero_trust_policy, get_opa_health
from ...security.jwks_cache import get_jwks_stats
from apps.backend.core.security.zero_trust.policy import Subject, Resource, Environment, Decision, abac_decide
import Exception
import body
import bool
import e
import getattr
import identity
import int
import k
import list
import max
import request
import str
import v


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/security", tags=["security", "policy"])

# Prometheus metrics
policy_evaluations_total = Counter(
    "zeta_policy_evaluations_total",
    "Total policy evaluations",
    ["engine", "allow", "risk"]
)

policy_comparison_total = Counter(
    "zeta_policy_comparison_total",
    "Policy engine comparison results",
    ["abac_allow", "opa_allow", "agreement"]
)


class PolicyEvaluationRequest(BaseModel):
    """Request model for policy evaluation"""
    
    action: str = Field(description="Action being performed", examples=["read", "write", "delete"])
    resource_path: str = Field(description="Resource path being accessed", examples=["/api/v1/agents/teams"])
    classification: str = Field(
        default="internal",
        description="Resource classification level",
        examples=["public", "internal", "confidential", "restricted", "secret"]
    )
    tenant: Optional[str] = Field(default=None, description="Resource tenant (for multi-tenancy)")
    
    # Optional context overrides
    client_ip: Optional[str] = Field(default=None, description="Override client IP")
    force_mfa_check: Optional[bool] = Field(default=None, description="Force MFA requirement check")


class PolicyEvaluationResponse(BaseModel):
    """Response model for policy evaluation"""
    
    # Final decision (AND of both engines)
    allow: bool = Field(description="Final access decision")
    risk: str = Field(description="Risk level (low/medium/high)")
    
    # Individual engine results
    abac_result: Dict[str, Any] = Field(description="ABAC engine result")
    opa_result: Dict[str, Any] = Field(description="OPA engine result")
    
    # Metadata
    evaluation_time_ms: int = Field(description="Total evaluation time in milliseconds")
    engines_agree: bool = Field(description="Whether ABAC and OPA agree")
    primary_engine: str = Field(description="Primary engine used for decision")
    
    # Risk factors and recommendations
    violations: list[str] = Field(default_factory=list, description="Policy violations")
    risk_factors: list[str] = Field(default_factory=list, description="Risk factors identified")
    recommendations: list[str] = Field(default_factory=list, description="Security recommendations")


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    
    status: str = Field(description="Overall health status")
    components: Dict[str, Any] = Field(description="Component health details")
    timestamp: str = Field(description="Health check timestamp")


@router.post("/policy/evaluate", response_model=PolicyEvaluationResponse)
async def evaluate_policy(
    request: Request,
    body: PolicyEvaluationRequest,
    identity: Identity = Depends(get_identity)
) -> PolicyEvaluationResponse:
    """
    Evaluate access policy using both ABAC and OPA engines side-by-side.
    
    This endpoint performs Zero-Trust policy evaluation using both the legacy
    ABAC system and the new OPA system, comparing results for analysis.
    """
    import time
    start_time = time.time()
    
    try:
        # Extract client information
        client_ip = body.client_ip or getattr(request.client, 'host', 'unknown')
        current_hour = datetime.now(timezone.utc).hour
        
        # Prepare common input data
        subject_data = {
            "sub": identity.sub,
            "roles": identity.roles,
            "mfa": identity.mfa,
            "device_trust": identity.device_trust,
            "session_id": identity.session_id,
            "org": identity.org,
            "tenant": identity.org,  # Use org as tenant for now
            "clearance": identity.clearance,
            "token_age_seconds": identity.token_age_seconds()
        }
        
        resource_data = {
            "path": body.resource_path,
            "classification": body.classification,
            "tenant": body.tenant
        }
        
        environment_data = {
            "hour": current_hour,
            "client_ip": client_ip,
            "token_age": identity.token_age_seconds(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # ================================================================
        # ABAC Evaluation (Legacy System)
        # ================================================================
        
        try:
            abac_subject = Subject(
                user_id=identity.sub,
                roles=identity.roles,
                mfa=body.force_mfa_check if body.force_mfa_check is not None else identity.mfa,
                device_trust=identity.device_trust,
                ip=client_ip,
                clearance=identity.clearance,
                org=identity.org
            )
            
            abac_resource = Resource(
                name=body.resource_path,
                classification=body.classification,
                tenant=body.tenant
            )
            
            abac_env = Environment(
                hour=current_hour,
                token_age_seconds=identity.token_age_seconds()
            )
            
            abac_decision = abac_decide(abac_subject, body.action, abac_resource, abac_env)
            
            abac_result = {
                "allow": abac_decision.allow,
                "risk": abac_decision.risk,
                "reason": abac_decision.reason,
                "engine": "abac"
            }
            
            # Record ABAC metrics
            policy_evaluations_total.labels(
                engine="abac",
                allow=str(abac_decision.allow),
                risk=abac_decision.risk
            ).inc()
            
        except Exception as e:
            logger.error(f"ABAC evaluation failed: {e}")
            abac_result = {
                "allow": False,
                "risk": "high",
                "reason": f"ABAC evaluation error: {str(e)}",
                "engine": "abac",
                "error": True
            }
        
        # ================================================================
        # OPA Evaluation (New System)
        # ================================================================
        
        opa_result = await evaluate_zero_trust_policy(
            subject=subject_data,
            action=body.action,
            resource=resource_data,
            environment=environment_data,
            include_diagnostics=False
        )
        
        # Record OPA metrics
        policy_evaluations_total.labels(
            engine="opa",
            allow=str(opa_result["allow"]),
            risk=opa_result["risk"]
        ).inc()
        
        # ================================================================
        # Side-by-side Comparison and Final Decision
        # ================================================================
        
        # Compare decisions
        engines_agree = abac_result["allow"] == opa_result["allow"]
        
        # Record comparison metrics
        policy_comparison_total.labels(
            abac_allow=str(abac_result["allow"]),
            opa_allow=str(opa_result["allow"]),
            agreement=str(engines_agree)
        ).inc()
        
        # Determine final decision (AND logic for now)
        # Both engines must allow for final allow
        final_allow = abac_result["allow"] and opa_result["allow"]
        
        # Risk is the highest of both engines
        risk_levels = {"low": 1, "medium": 2, "high": 3}
        abac_risk_level = risk_levels.get(abac_result["risk"], 2)
        opa_risk_level = risk_levels.get(opa_result["risk"], 2)
        
        final_risk_level = max(abac_risk_level, opa_risk_level)
        final_risk = {v: k for k, v in risk_levels.items()}[final_risk_level]
        
        # Determine primary engine (configurable)
        primary_engine = "opa"  # Transition to OPA as primary
        
        # Collect violations and recommendations
        violations = []
        risk_factors = []
        recommendations = []
        
        if not engines_agree:
            violations.append("policy_engine_disagreement")
            recommendations.append("review_policy_configuration")
        
        if not abac_result["allow"]:
            violations.append(f"abac_denial: {abac_result.get('reason', 'unknown')}")
        
        violations.extend(opa_result.get("violations", []))
        risk_factors.extend(opa_result.get("risk_factors", []))
        recommendations.extend(opa_result.get("recommendations", []))
        
        # Calculate evaluation time
        evaluation_time_ms = int((time.time() - start_time) * 1000)
        
        # Log policy decision for audit
        logger.info(
            f"Policy evaluation: user={identity.sub} action={body.action} "
            f"resource={body.resource_path} abac={abac_result['allow']} "
            f"opa={opa_result['allow']} final={final_allow} risk={final_risk} "
            f"time={evaluation_time_ms}ms"
        )
        
        return PolicyEvaluationResponse(
            allow=final_allow,
            risk=final_risk,
            abac_result=abac_result,
            opa_result=opa_result,
            evaluation_time_ms=evaluation_time_ms,
            engines_agree=engines_agree,
            primary_engine=primary_engine,
            violations=violations,
            risk_factors=risk_factors,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Policy evaluation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Policy evaluation failed: {str(e)}"
        )


@router.get("/health", response_model=HealthCheckResponse)
async def security_health_check() -> HealthCheckResponse:
    """
    Health check for security components (JWKS, OPA, etc.).
    """
    components = {}
    overall_status = "healthy"
    
    # Check JWKS health
    try:
        jwks_stats = get_jwks_stats()
        if jwks_stats.get("status") == "disabled":
            components["jwks"] = {"status": "disabled", "message": "JWKS not configured"}
        elif jwks_stats.get("cache_valid", False):
            components["jwks"] = {"status": "healthy", "stats": jwks_stats}
        else:
            components["jwks"] = {"status": "degraded", "stats": jwks_stats}
            overall_status = "degraded"
    except Exception as e:
        components["jwks"] = {"status": "error", "error": str(e)}
        overall_status = "unhealthy"
    
    # Check OPA health
    try:
        opa_health = await get_opa_health()
        components["opa"] = opa_health
        
        if opa_health["status"] not in ["healthy", "disabled"]:
            overall_status = "degraded"
            
    except Exception as e:
        components["opa"] = {"status": "error", "error": str(e)}
        overall_status = "unhealthy"
    
    return HealthCheckResponse(
        status=overall_status,
        components=components,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.get("/policy/stats")
async def get_policy_stats(
    identity: Identity = Depends(get_identity)
) -> Dict[str, Any]:
    """
    Get policy evaluation statistics (requires admin role).
    """
    if not identity.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    
    # This would typically pull from metrics storage
    # For now, return basic stats
    return {
        "message": "Policy statistics endpoint - implement metrics aggregation",
        "user": identity.sub,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
