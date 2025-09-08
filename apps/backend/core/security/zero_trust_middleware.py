"""
Zero-Trust Security Middleware for ZETA_VN
Implements comprehensive security controls for production deployment
"""

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any

import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
import Exception
import any
import app
import bool
import call_next
import dict
import e
import float
import getattr
import header
import int
import jwt_secret
import kwargs
import list
import path
import pattern
import request
import requests_per_window
import self
import str
import super
import window_seconds

logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityConfig:
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    max_request_size: int = 10 * 1024 * 1024  # 10MB
    allowed_origins: list[str] = None
    require_https: bool = True


@dataclass
class SecurityContext:
    user_id: str | None = None
    session_id: str | None = None
    device_fingerprint: str | None = None
    ip_address: str | None = None
    threat_level: ThreatLevel = ThreatLevel.LOW
    permissions: list[str] = None
    last_activity: float | None = None


class RateLimiter:
    """Token bucket rate limiter"""

    def __init__(self, requests_per_window: int, window_seconds: int):
        self.requests_per_window = requests_per_window
        self.window_seconds = window_seconds
        self.clients: dict[str, dict[str, Any]] = {}

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed under rate limit"""
        current_time = time.time()

        if client_id not in self.clients:
            self.clients[client_id] = {"requests": 1, "window_start": current_time}
            return True

        client_data = self.clients[client_id]

        # Reset window if expired
        if current_time - client_data["window_start"] >= self.window_seconds:
            client_data["requests"] = 1
            client_data["window_start"] = current_time
            return True

        # Check if under limit
        if client_data["requests"] < self.requests_per_window:
            client_data["requests"] += 1
            return True

        return False


class SecurityValidator:
    """Security validation and threat assessment"""

    def __init__(self, config: SecurityConfig):
        self.config = config
        self.rate_limiter = RateLimiter(
            config.rate_limit_requests, config.rate_limit_window
        )
        self.failed_attempts: dict[str, int] = {}

    def validate_jwt_token(self, token: str) -> dict[str, Any] | None:
        """Validate JWT token and return claims"""
        try:
            payload = jwt.decode(
                token, self.config.jwt_secret, algorithms=[self.config.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {e}")
            return None

    def assess_threat_level(
        self, request: Request, context: SecurityContext
    ) -> ThreatLevel:
        """Assess threat level for request"""
        risk_factors = 0

        # Check for suspicious IP patterns
        if self._is_suspicious_ip(context.ip_address):
            risk_factors += 2

        # Check failed authentication attempts
        if context.ip_address in self.failed_attempts:
            failed_count = self.failed_attempts[context.ip_address]
            if failed_count > 5:
                risk_factors += 3
            elif failed_count > 2:
                risk_factors += 1

        # Check request patterns
        if self._is_suspicious_request(request):
            risk_factors += 1

        # Determine threat level
        if risk_factors >= 4:
            return ThreatLevel.CRITICAL
        elif risk_factors >= 3:
            return ThreatLevel.HIGH
        elif risk_factors >= 2:
            return ThreatLevel.MEDIUM
        else:
            return ThreatLevel.LOW

    def _is_suspicious_ip(self, ip_address: str | None) -> bool:
        """Check if IP address is suspicious"""
        if not ip_address:
            return True

        # Add your IP reputation checks here
        # For now, just check for common attack patterns
        suspicious_patterns = [
            "127.0.0.1",  # Remove this in production
            "0.0.0.0",
        ]

        return any(pattern in ip_address for pattern in suspicious_patterns)

    def _is_suspicious_request(self, request: Request) -> bool:
        """Check for suspicious request patterns"""
        # Check for common attack patterns in URL
        suspicious_patterns = [
            "script",
            "alert",
            "union",
            "select",
            "../",
            "etc/passwd",
        ]

        url = str(request.url).lower()
        return any(pattern in url for pattern in suspicious_patterns)

    def record_failed_attempt(self, ip_address: str):
        """Record failed authentication attempt"""
        if ip_address in self.failed_attempts:
            self.failed_attempts[ip_address] += 1
        else:
            self.failed_attempts[ip_address] = 1

    def record_successful_auth(self, ip_address: str):
        """Record successful authentication (reset failed attempts)"""
        self.failed_attempts.pop(ip_address, None)


class ZeroTrustMiddleware(BaseHTTPMiddleware):
    """Zero-Trust security middleware"""

    def __init__(self, app, config: SecurityConfig):
        super().__init__(app)
        self.config = config
        self.validator = SecurityValidator(config)
        self.security = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next):
        """Process request through security pipeline"""

        # Skip security for health checks and static assets
        if self._should_skip_security(request):
            return await call_next(request)

        # Extract security context
        context = await self._extract_security_context(request)

        # Rate limiting
        client_id = context.ip_address or "unknown"
        if not self.validator.rate_limiter.is_allowed(client_id):
            logger.warning(f"Rate limit exceeded for {client_id}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )

        # Threat assessment
        threat_level = self.validator.assess_threat_level(request, context)
        context.threat_level = threat_level

        # Block high-risk requests
        if threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            logger.warning(
                f"Blocking {threat_level.value} threat from {context.ip_address}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Request blocked by security policy",
            )

        # Request size validation
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.config.max_request_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Request too large",
            )

        # Add security context to request state
        request.state.security_context = context

        # Process request
        try:
            response = await call_next(request)

            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

            return response

        except Exception as e:
            logger.error(f"Request processing error: {e}")
            raise

    def _should_skip_security(self, request: Request) -> bool:
        """Check if security should be skipped for this request"""
        skip_paths = ["/health", "/metrics", "/docs", "/openapi.json", "/favicon.ico"]

        return any(request.url.path.startswith(path) for path in skip_paths)

    async def _extract_security_context(self, request: Request) -> SecurityContext:
        """Extract security context from request"""
        # Get client IP
        ip_address = self._get_client_ip(request)

        # Extract JWT token
        user_id = None
        session_id = None
        permissions = []

        authorization = request.headers.get("authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            payload = self.validator.validate_jwt_token(token)
            if payload:
                user_id = payload.get("sub")
                session_id = payload.get("session_id")
                permissions = payload.get("permissions", [])

        # Generate device fingerprint
        device_fingerprint = self._generate_device_fingerprint(request)

        return SecurityContext(
            user_id=user_id,
            session_id=session_id,
            device_fingerprint=device_fingerprint,
            ip_address=ip_address,
            permissions=permissions,
            last_activity=time.time(),
        )

    def _get_client_ip(self, request: Request) -> str:
        """Get real client IP address"""
        # Check for forwarded IP headers (in order of preference)
        forwarded_headers = [
            "X-Forwarded-For",
            "X-Real-IP",
            "CF-Connecting-IP",
            "X-Client-IP",
        ]

        for header in forwarded_headers:
            if header in request.headers:
                ip = request.headers[header].split(",")[0].strip()
                if ip:
                    return ip

        # Fall back to direct connection IP
        return getattr(request.client, "host", "unknown")

    def _generate_device_fingerprint(self, request: Request) -> str:
        """Generate device fingerprint from request headers"""
        fingerprint_data = {
            "user_agent": request.headers.get("user-agent", ""),
            "accept_language": request.headers.get("accept-language", ""),
            "accept_encoding": request.headers.get("accept-encoding", ""),
        }

        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.md5(fingerprint_str.encode()).hexdigest()


def create_security_middleware(app, jwt_secret: str, **kwargs) -> ZeroTrustMiddleware:
    """Factory function to create security middleware"""
    config = SecurityConfig(jwt_secret=jwt_secret, **kwargs)
    return ZeroTrustMiddleware(app, config)
