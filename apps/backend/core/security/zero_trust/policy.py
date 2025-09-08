"""
Zero-Trust ABAC Policy Engine
Implements Attribute-Based Access Control with risk scoring
"""
from __future__ import annotations
from pydantic import BaseModel
from typing import Literal
from enum import Enum
import action
import bool
import env
import float
import int
import len
import list
import max
import min
import path
import reasons
import required_actions
import resource
import str
import subject

Action = Literal["read", "write", "delete", "execute", "admin"]
RiskLevel = Literal["low", "medium", "high", "critical"]


class ResourceClass(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal" 
    RESTRICTED = "restricted"
    SENSITIVE = "sensitive"


class Subject(BaseModel):
    user_id: str
    roles: list[str] = []
    permissions: list[str] = []
    mfa: bool = False
    ip: str | None = None
    device_trust: bool = False
    session_trust: bool = True
    clearance_level: int = 0  # 0=basic, 1=elevated, 2=admin


class Resource(BaseModel):
    name: str
    resource_type: str  # "agent", "rag", "admin", "api"
    owner_id: str | None = None
    classification: ResourceClass = ResourceClass.INTERNAL
    sensitivity_score: int = 1  # 1-5
    required_clearance: int = 0


class Environment(BaseModel):
    hour: int
    geo: str | None = None
    token_age_seconds: int = 0
    request_rate: float = 0.0
    anomaly_score: float = 0.0
    network_trust: bool = True


class Decision(BaseModel):
    allow: bool
    risk: RiskLevel
    confidence: float  # 0.0-1.0
    reasons: list[str]
    required_actions: list[str] = []  # ["mfa", "approve", "step_up"]


def abac_decide(subject: Subject, action: Action, resource: Resource, env: Environment) -> Decision:
    """
    Enhanced ABAC policy with multi-factor risk assessment
    """
    reasons: list[str] = []
    required_actions: list[str] = []
    risk_score = 0.0
    
    # Base access control checks
    if resource.classification == ResourceClass.SENSITIVE and "admin" not in subject.roles:
        reasons.append("sensitive_resource_requires_admin_role")
        risk_score += 0.4
        
    if resource.required_clearance > subject.clearance_level:
        reasons.append(f"insufficient_clearance_{subject.clearance_level}_lt_{resource.required_clearance}")
        risk_score += 0.3
        
    # Action-specific checks
    if action in ("write", "delete", "execute", "admin"):
        if not subject.mfa:
            reasons.append("sensitive_action_requires_mfa")
            required_actions.append("mfa")
            risk_score += 0.3
            
        if resource.resource_type == "agent" and "agent:manage" not in subject.permissions:
            reasons.append("agent_management_permission_required")
            risk_score += 0.2
            
        if resource.resource_type == "admin" and "system:admin" not in subject.permissions:
            reasons.append("system_admin_permission_required") 
            risk_score += 0.4
    
    # Environmental risk factors
    if env.token_age_seconds > 3600 * 8:  # 8 hours
        reasons.append("token_age_exceeds_policy")
        risk_score += 0.2
        
    if not subject.device_trust:
        reasons.append("untrusted_device")
        risk_score += 0.15
        
    if not env.network_trust:
        reasons.append("untrusted_network")
        risk_score += 0.2
        
    if env.hour < 6 or env.hour > 22:
        reasons.append("access_outside_business_hours")
        risk_score += 0.1
        
    if env.anomaly_score > 0.5:
        reasons.append(f"anomaly_detected_score_{env.anomaly_score:.2f}")
        risk_score += env.anomaly_score * 0.3
        
    if env.request_rate > 100:  # requests/minute
        reasons.append("high_request_rate_detected")
        risk_score += 0.1
    
    # Resource sensitivity multiplier
    sensitivity_multiplier = resource.sensitivity_score / 5.0
    risk_score = min(1.0, risk_score * (1 + sensitivity_multiplier))
    
    # Determine risk level and access decision
    if risk_score >= 0.8:
        risk_level = "critical"
        allow = False
    elif risk_score >= 0.6:
        risk_level = "high" 
        allow = len(required_actions) == 0  # Allow if remediations available
    elif risk_score >= 0.4:
        risk_level = "medium"
        allow = True
    else:
        risk_level = "low"
        allow = True
    
    # Override for admin emergency access
    if "emergency:override" in subject.permissions and action == "admin":
        reasons.append("emergency_override_granted")
        allow = True
        required_actions.append("audit_trail")
    
    confidence = 1.0 - (env.anomaly_score * 0.3)  # Lower confidence with anomalies
    
    return Decision(
        allow=allow,
        risk=risk_level,
        confidence=max(0.1, confidence),
        reasons=reasons,
        required_actions=required_actions
    )


def get_resource_policy(path: str) -> Resource:
    """
    Map API paths to resource policies
    """
    if path.startswith("/api/v1/admin"):
        return Resource(
            name=path,
            resource_type="admin",
            classification=ResourceClass.SENSITIVE,
            sensitivity_score=5,
            required_clearance=2
        )
    elif path.startswith("/api/v1/agents"):
        return Resource(
            name=path,
            resource_type="agent", 
            classification=ResourceClass.RESTRICTED,
            sensitivity_score=3,
            required_clearance=1
        )
    elif path.startswith("/api/v1/rag"):
        return Resource(
            name=path,
            resource_type="rag",
            classification=ResourceClass.INTERNAL,
            sensitivity_score=2,
            required_clearance=0
        )
    elif path.startswith("/api/v1/security"):
        return Resource(
            name=path,
            resource_type="security",
            classification=ResourceClass.SENSITIVE,
            sensitivity_score=4,
            required_clearance=1
        )
    else:
        return Resource(
            name=path,
            resource_type="api",
            classification=ResourceClass.INTERNAL,
            sensitivity_score=1,
            required_clearance=0
        )
