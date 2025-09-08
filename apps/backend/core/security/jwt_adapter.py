"""
JWT/OIDC Authentication Adapter
Integrates with Zero-Trust middleware for claims-based authentication
"""
from __future__ import annotations
from typing import Dict, List, Optional
from datetime import datetime, timezone
import jwt
from pydantic import BaseModel
from apps.backend.core.security.zero_trust.policy import Subject
import Exception
import algorithms
import any
import audience
import bool
import client_ip
import device_id
import e
import headers
import int
import issuer
import jwt_secret
import list
import max
import mfa_verified
import p
import r
import role
import self
import set
import str
import ttl_hours
import user_id


class JWTClaims(BaseModel):
    sub: str  # subject (user_id)
    iss: str  # issuer
    aud: str  # audience
    exp: int  # expiration
    iat: int  # issued at
    nbf: int  # not before
    jti: str  # JWT ID
    
    # Custom claims
    roles: List[str] = []
    permissions: List[str] = []
    clearance_level: int = 0
    mfa_verified: bool = False
    device_id: str = ""
    session_id: str = ""
    
    # Risk context
    ip_whitelist: List[str] = []
    trusted_devices: List[str] = []


class OIDCUserInfo(BaseModel):
    sub: str
    name: str
    given_name: str = ""
    family_name: str = ""
    email: str = ""
    email_verified: bool = False
    groups: List[str] = []
    department: str = ""
    clearance: str = "basic"


class AuthenticationResult(BaseModel):
    success: bool
    subject: Optional[Subject] = None
    error: Optional[str] = None
    token_age_seconds: int = 0
    requires_mfa: bool = False
    risk_factors: List[str] = []


class JWTAuthAdapter:
    """
    JWT/OIDC authentication adapter for Zero-Trust integration
    """
    
    def __init__(
        self,
        jwt_secret: str,
        issuer: str = "zeta-api", 
        audience: str = "zeta-clients",
        algorithms: List[str] = None
    ):
        self.jwt_secret = jwt_secret
        self.issuer = issuer
        self.audience = audience
        self.algorithms = algorithms or ["HS256"]
        
        # Role to permission mapping
        self.role_permissions = {
            "user": ["api:read", "profile:read"],
            "analyst": ["api:read", "api:write", "rag:query", "profile:read"],
            "agent_operator": ["api:read", "api:write", "agent:view", "agent:run"],
            "agent_admin": ["api:read", "api:write", "agent:*", "team:*"],
            "security_analyst": ["api:read", "security:read", "audit:read"],
            "admin": ["*"],
            "emergency": ["emergency:override", "*"]
        }
        
        # Clearance level mapping
        self.clearance_levels = {
            "basic": 0,
            "elevated": 1,
            "admin": 2,
            "emergency": 3
        }
    
    def validate_token(self, token: str, client_ip: str = None) -> AuthenticationResult:
        """
        Validate JWT token and extract claims for Zero-Trust evaluation
        """
        try:
            # Decode and validate JWT
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=self.algorithms,
                audience=self.audience,
                issuer=self.issuer
            )
            
            claims = JWTClaims(**payload)
            now = datetime.now(timezone.utc)
            issued_at = datetime.fromtimestamp(claims.iat, tz=timezone.utc)
            token_age = int((now - issued_at).total_seconds())
            
            # Check token freshness
            if token_age > 24 * 3600:  # 24 hours
                return AuthenticationResult(
                    success=False,
                    error="token_expired",
                    token_age_seconds=token_age
                )
            
            # Build permissions from roles
            permissions = set()
            for role in claims.roles:
                role_perms = self.role_permissions.get(role, [])
                permissions.update(role_perms)
            
            # Add explicit permissions
            permissions.update(claims.permissions)
            
            # Check device trust
            device_trust = (
                claims.device_id in claims.trusted_devices if claims.trusted_devices
                else bool(claims.device_id)  # Has device ID = some trust
            )
            
            # Check IP whitelist
            ip_trusted = (
                client_ip in claims.ip_whitelist if claims.ip_whitelist and client_ip
                else True  # No whitelist = allow all
            )
            
            # Risk factors
            risk_factors = []
            if token_age > 8 * 3600:  # 8 hours
                risk_factors.append("stale_token")
            if not claims.mfa_verified:
                risk_factors.append("no_mfa")
            if not device_trust:
                risk_factors.append("untrusted_device")
            if not ip_trusted:
                risk_factors.append("ip_not_whitelisted")
            
            # Determine if MFA is required
            requires_mfa = (
                not claims.mfa_verified and 
                any(p.startswith(("admin:", "security:", "agent:")) for p in permissions)
            )
            
            # Get clearance level
            clearance_level = claims.clearance_level
            if clearance_level == 0:  # Fallback to role-based clearance
                max_role_clearance = 0
                for role in claims.roles:
                    if role in ["admin", "emergency"]:
                        max_role_clearance = max(max_role_clearance, 2)
                    elif role in ["agent_admin", "security_analyst"]:
                        max_role_clearance = max(max_role_clearance, 1)
                clearance_level = max_role_clearance
            
            # Create Subject for Zero-Trust evaluation
            subject = Subject(
                user_id=claims.sub,
                roles=claims.roles,
                permissions=list(permissions),
                mfa=claims.mfa_verified,
                ip=client_ip,
                device_trust=device_trust,
                session_trust=ip_trusted,
                clearance_level=clearance_level
            )
            
            return AuthenticationResult(
                success=True,
                subject=subject,
                token_age_seconds=token_age,
                requires_mfa=requires_mfa,
                risk_factors=risk_factors
            )
            
        except jwt.ExpiredSignatureError:
            return AuthenticationResult(
                success=False,
                error="token_expired"
            )
        except jwt.InvalidTokenError as e:
            return AuthenticationResult(
                success=False,
                error=f"invalid_token: {str(e)}"
            )
        except Exception as e:
            return AuthenticationResult(
                success=False,
                error=f"auth_error: {str(e)}"
            )
    
    def create_token(
        self,
        user_id: str,
        roles: List[str],
        permissions: List[str] = None,
        mfa_verified: bool = False,
        device_id: str = "",
        ttl_hours: int = 8
    ) -> str:
        """
        Create JWT token with Zero-Trust claims
        """
        now = datetime.now(timezone.utc)
        claims = {
            "sub": user_id,
            "iss": self.issuer,
            "aud": self.audience,
            "exp": int((now.timestamp() + ttl_hours * 3600)),
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
            "jti": f"{user_id}:{int(now.timestamp())}",
            "roles": roles,
            "permissions": permissions or [],
            "mfa_verified": mfa_verified,
            "device_id": device_id,
            "clearance_level": self._get_clearance_from_roles(roles)
        }
        
        return jwt.encode(claims, self.jwt_secret, algorithm="HS256")
    
    def _get_clearance_from_roles(self, roles: List[str]) -> int:
        """Determine clearance level from roles"""
        max_clearance = 0
        for role in roles:
            if role in ["admin", "emergency"]:
                max_clearance = max(max_clearance, 2)
            elif role in ["agent_admin", "security_analyst"]:
                max_clearance = max(max_clearance, 1)
        return max_clearance
    
    def extract_subject_from_headers(self, headers: Dict[str, str], client_ip: str = None) -> Optional[Subject]:
        """
        Extract Subject from HTTP headers (fallback for demo/testing)
        """
        if "authorization" in headers:
            auth_header = headers["authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header[7:]
                result = self.validate_token(token, client_ip)
                return result.subject if result.success else None
        
        # Fallback to custom headers (for testing)
        if "x-user-id" in headers:
            roles = [r.strip() for r in headers.get("x-roles", "").split(",") if r.strip()]
            permissions = [p.strip() for p in headers.get("x-permissions", "").split(",") if p.strip()]
            
            # Auto-expand role permissions
            all_permissions = set(permissions)
            for role in roles:
                role_perms = self.role_permissions.get(role, [])
                all_permissions.update(role_perms)
            
            return Subject(
                user_id=headers["x-user-id"],
                roles=roles,
                permissions=list(all_permissions),
                mfa=headers.get("x-mfa", "false").lower() == "true",
                ip=client_ip,
                device_trust=headers.get("x-device-trust", "false").lower() == "true",
                session_trust=True,
                clearance_level=int(headers.get("x-clearance-level", "0"))
            )
        
        return None
