"""
JWT Dependency with JWKS Integration for Production Authentication
"""
from __future__ import annotations
import logging
from typing import Optional, Annotated
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
import jwt

from .jwks_cache import decode_bearer_rs256
import Exception
import any
import bool
import e
import int
import isinstance
import level
import list
import method
import r
import request
import required_level
import role
import self
import set
import str


logger = logging.getLogger(__name__)


class Identity(BaseModel):
    """Enhanced identity model with enterprise features"""
    
    sub: str = Field(description="Subject identifier")
    roles: list[str] = Field(default_factory=list, description="User roles")
    mfa: bool = Field(default=False, description="Multi-factor authentication verified")
    device_trust: bool = Field(default=False, description="Device trust status")
    session_id: Optional[str] = Field(default=None, description="Session identifier")
    org: Optional[str] = Field(default=None, description="Organization")
    clearance: Optional[str] = Field(default=None, description="Security clearance level")
    
    # Token metadata
    iss: Optional[str] = Field(default=None, description="Token issuer")
    aud: Optional[str] = Field(default=None, description="Token audience")
    exp: Optional[int] = Field(default=None, description="Token expiration")
    iat: Optional[int] = Field(default=None, description="Token issued at")
    
    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return "admin" in self.roles or "administrator" in self.roles
    
    def has_role(self, role: str) -> bool:
        """Check if user has specific role"""
        return role.lower() in [r.lower() for r in self.roles]
    
    def has_clearance(self, required_level: str) -> bool:
        """Check if user has required security clearance"""
        if not self.clearance:
            return False
        
        clearance_levels = {
            "public": 0,
            "internal": 1,
            "confidential": 2,
            "secret": 3,
            "top_secret": 4
        }
        
        user_level = clearance_levels.get(self.clearance.lower(), 0)
        required = clearance_levels.get(required_level.lower(), 1)
        
        return user_level >= required
    
    def is_token_valid(self) -> bool:
        """Check if token is still valid"""
        if not self.exp:
            return True  # No expiration set
        
        current_time = datetime.now(timezone.utc).timestamp()
        return current_time < self.exp
    
    def token_age_seconds(self) -> int:
        """Get token age in seconds"""
        if not self.iat:
            return 0
        
        current_time = datetime.now(timezone.utc).timestamp()
        return int(current_time - self.iat)

def _extract_bearer_token(request: Request) -> str:
    """Extract bearer token from Authorization header"""
    auth_header = request.headers.get("authorization", "")
    
    if not auth_header.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = auth_header.split(" ", 1)[1]
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empty bearer token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return token


async def get_identity(request: Request) -> Identity:
    """
    Extract and validate identity from JWT token using JWKS
    """
    try:
        token = _extract_bearer_token(request)
        claims = await decode_bearer_rs256(token)
        
        # Extract roles from various claim locations
        roles = []
        
        # Standard roles claim
        if "roles" in claims:
            roles.extend(claims["roles"])
        
        # Keycloak realm access
        if "realm_access" in claims and "roles" in claims["realm_access"]:
            roles.extend(claims["realm_access"]["roles"])
        
        # Azure AD roles
        if "app_roles" in claims:
            roles.extend([role["value"] for role in claims["app_roles"]])
        
        # Auth0/Okta custom claims
        if "https://zeta.ai/roles" in claims:
            roles.extend(claims["https://zeta.ai/roles"])
        
        # Extract MFA status
        mfa_verified = False
        amr = claims.get("amr", [])
        if isinstance(amr, list):
            mfa_verified = any(method in amr for method in ["mfa", "otp", "sms", "totp"])
        
        # Create identity
        identity = Identity(
            sub=str(claims.get("sub", "anonymous")),
            roles=list(set(roles)),  # Remove duplicates
            mfa=mfa_verified,
            device_trust=bool(claims.get("device_trust", False)),
            session_id=claims.get("sid") or claims.get("session_id"),
            org=claims.get("org") or claims.get("organization"),
            clearance=claims.get("clearance") or claims.get("security_clearance"),
            iss=claims.get("iss"),
            aud=claims.get("aud"),
            exp=claims.get("exp"),
            iat=claims.get("iat")
        )
        
        # Validate token expiration
        if not identity.is_token_valid():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Store identity in request state for middleware access
        request.state.identity = identity
        
        logger.debug(f"Identity extracted for user: {identity.sub}")
        return identity
        
    except jwt.InvalidTokenError as e:
        logger.warning(f"JWT validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Identity extraction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def get_optional_identity(request: Request) -> Optional[Identity]:
    """
    Extract identity if present, but don't raise exception if missing
    """
    try:
        return await get_identity(request)
    except HTTPException:
        return None


# FastAPI dependency annotations
JWTIdentity = Annotated[Identity, Depends(get_identity)]
OptionalJWTIdentity = Annotated[Optional[Identity], Depends(get_optional_identity)]


async def require_admin(identity: Identity = Depends(get_identity)) -> Identity:
    """Dependency that requires admin role"""
    if not identity.is_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return identity


async def require_mfa(identity: Identity = Depends(get_identity)) -> Identity:
    """Dependency that requires MFA verification"""
    if not identity.mfa:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Multi-factor authentication required"
        )
    return identity


def require_clearance(level: str):
    """Factory for clearance requirement dependency"""
    async def _require_clearance(identity: Identity = Depends(get_identity)) -> Identity:
        if not identity.has_clearance(level):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Security clearance '{level}' required"
            )
        return identity
    return _require_clearance


def require_role(role: str):
    """Factory for role requirement dependency"""
    async def _require_role(identity: Identity = Depends(get_identity)) -> Identity:
        if not identity.has_role(role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' required"
            )
        return identity
    return _require_role
