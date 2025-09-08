# Security & RBAC for Teacher-Student AI System
from __future__ import annotations

import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import bool
import creds
import e
import list
import roles
import set
import str
import token

# Configuration
ALGO = os.getenv("JWT_ALGO", "HS256")
SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PRODUCTION")
TEAM_ID = os.getenv("TEAM_ID", "zeta_default_team")

bearer = HTTPBearer(auto_error=True)


class TokenClaims(BaseModel):
    """JWT token claims structure"""

    sub: str  # user ID
    team_id: str  # team lock
    roles: list[str] = []  # OWNER|ADMIN|ENGINEER|TRAINER_EXTERNAL|VIEWER
    scopes: list[str] = []  # future: fine-grained permissions


def _decode(token: str) -> TokenClaims:
    """Decode and validate JWT token"""
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return TokenClaims(**data)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )


async def require_auth(
    creds: HTTPAuthorizationCredentials = Depends(bearer),  # noqa: B008
) -> TokenClaims:
    """Base authentication dependency - validates JWT and team membership"""
    claims = _decode(creds.credentials)

    # Team lock - only allow matching team_id
    if claims.team_id != TEAM_ID:
        raise HTTPException(status_code=403, detail="Forbidden: team mismatch")

    return claims


def require_roles(*roles: str):
    """Role-based access control decorator

    Usage:
        @router.get("/admin")
        async def admin_endpoint(claims = Depends(require_roles("ADMIN", "OWNER"))):
            ...
    """

    async def _dep(claims: TokenClaims = Depends(require_auth)):
        if not set(roles).intersection(set(claims.roles)):
            raise HTTPException(
                status_code=403, detail=f"Forbidden: requires one of {roles}"
            )
        return claims

    return _dep


def has_external_role(claims: TokenClaims) -> bool:
    """Check if user has external trainer role (limited permissions)"""
    return "TRAINER_EXTERNAL" in claims.roles


def forbid_external_trainers(
    claims: TokenClaims = Depends(require_auth),
) -> TokenClaims:
    """Dependency to block external trainers from sensitive endpoints"""
    if has_external_role(claims):
        raise HTTPException(
            status_code=403, detail="External trainers cannot access this endpoint"
        )
    return claims


# Role definitions for clarity
class Roles:
    OWNER = "OWNER"  # Full system access
    ADMIN = "ADMIN"  # Administrative privileges
    ENGINEER = "ENGINEER"  # Development & training access
    TRAINER_EXTERNAL = "TRAINER_EXTERNAL"  # Limited to data upload only
    VIEWER = "VIEWER"  # Read-only access to dashboards
