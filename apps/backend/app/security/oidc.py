"""OIDC integration for Keycloak authentication.

Provides JWT verification with JWKS discovery and WebAuthn MFA support.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from fastapi import HTTPException, Request
from jose import JWTError, jwt
from pydantic import BaseModel, Field
import Exception
import RuntimeError
import audience
import client
import dict
import e
import int
import issuer
import k
import list
import request
import self
import str

logger = logging.getLogger(__name__)


class OIDCConfig(BaseModel):
    """OIDC configuration."""

    issuer: str = Field(..., description="OIDC issuer URL")
    audience: str = Field(..., description="Expected audience")
    algorithms: list[str] = Field(
        default=["RS256"], description="Allowed JWT algorithms"
    )


class AuthContext(BaseModel):
    """Authentication context from verified JWT."""

    user_id: str
    tenant_id: str | None = None
    roles: list[str] = Field(default_factory=list)
    mfa_level: int = Field(default=0, description="0=none, 1=webauthn, 2=hardware")
    permissions: list[str] = Field(default_factory=list)
    session_id: str | None = None


class OIDCAuthenticator:
    """OIDC JWT authenticator with JWKS discovery."""

    def __init__(self, config: OIDCConfig):
        self.config = config
        self._jwks: dict[str, Any] | None = None
        self._discovery: dict[str, Any] | None = None

    async def _load_discovery(self) -> dict[str, Any]:
        """Load OIDC discovery document."""
        if self._discovery is None:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.config.issuer}/.well-known/openid-configuration"
                )
                response.raise_for_status()
                self._discovery = response.json()
        assert self._discovery is not None
        return self._discovery

    async def _load_jwks(self) -> dict[str, Any]:
        """Load JWKS from discovery."""
        if self._jwks is None:
            discovery = await self._load_discovery()
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(discovery["jwks_uri"])
                response.raise_for_status()
                self._jwks = response.json()
        assert self._jwks is not None
        return self._jwks

    async def verify_token(self, token: str) -> AuthContext:
        """Verify JWT token and return auth context."""
        try:
            # Get unverified header for key ID
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")

            if not kid:
                raise HTTPException(401, "Missing key ID in token")

            # Load JWKS and find matching key
            jwks = await self._load_jwks()
            key = None
            for k in jwks.get("keys", []):
                if k.get("kid") == kid:
                    key = k
                    break

            if not key:
                raise HTTPException(401, "Key not found in JWKS")

            # Verify token signature (simplified - production should use full JWKS)
            claims = jwt.decode(
                token,
                key,
                algorithms=self.config.algorithms,
                audience=self.config.audience,
                issuer=self.config.issuer,
            )

            # Extract auth context
            mfa_level = 0
            amr = claims.get("amr", [])
            if "webauthn" in amr:
                mfa_level = 1
            elif "hwcrypto" in amr:
                mfa_level = 2

            return AuthContext(
                user_id=claims["sub"],
                tenant_id=claims.get("tenant"),
                roles=claims.get("realm_access", {}).get("roles", []),
                mfa_level=mfa_level,
                permissions=claims.get("permissions", []),
                session_id=claims.get("sid"),
            )

        except JWTError as e:
            logger.warning("JWT verification failed: %s", e)
            raise HTTPException(401, f"Invalid token: {e}")
        except Exception as e:
            logger.error("Token verification error: %s", e)
            raise HTTPException(401, "Token verification failed")


# Module-level authenticator instance (singleton pattern)
_authenticator: OIDCAuthenticator | None = None


def init_oidc(issuer: str, audience: str = "zeta-ai") -> OIDCAuthenticator:
    """Initialize OIDC authenticator."""
    global _authenticator  # noqa: PLW0603 - singleton pattern for FastAPI app
    config = OIDCConfig(issuer=issuer, audience=audience)
    _authenticator = OIDCAuthenticator(config)
    logger.info("OIDC initialized: issuer=%s audience=%s", issuer, audience)
    return _authenticator


async def verify_request(request: Request) -> AuthContext:
    """FastAPI dependency to verify OIDC token from request."""
    if _authenticator is None:
        raise RuntimeError("OIDC not initialized - call init_oidc() first")

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid Authorization header")

    token = auth_header.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(401, "Empty token")

    auth_context = await _authenticator.verify_token(token)

    # Store in request state for access by other components
    request.state.auth = auth_context

    return auth_context
