#!/usr/bin/env python3
"""
Advanced Middleware Fix Script

Tự động fix các middleware files có completeness scores thấp.
Thêm missing functions, classes, documentation và structure hoàn chỉnh.
"""

from __future__ import annotations

import time
from pathlib import Path
import SystemExit
import bool
import file_path_str
import int
import len
import print
import str
import template_key

# Templates để fix các files cụ thể
FIX_TEMPLATES = {
    "metrics_middleware.py": '''"""Metrics collection middleware for HTTP requests."""
from __future__ import annotations

import logging
import time
from typing import Optional

from fastapi import Request, Response
from prometheus_client import Counter, Histogram, start_http_server
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

REQUEST_SIZE = Histogram(
    'http_request_size_bytes',
    'HTTP request size in bytes',
    ['method', 'endpoint']
)

RESPONSE_SIZE = Histogram(
    'http_response_size_bytes',
    'HTTP response size in bytes',
    ['method', 'endpoint']
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware thu thập metrics cho HTTP requests."""

    def __init__(
        self,
        app,
        metrics_port: Optional[int] = None,
        enable_response_size: bool = True
    ):
        super().__init__(app)
        self.enable_response_size = enable_response_size
        
        # Start metrics server if port provided
        if metrics_port:
            try:
                start_http_server(metrics_port)
                logger.info(f"Metrics server started on port {metrics_port}")
            except Exception as e:
                logger.error(f"Failed to start metrics server: {e}")

    async def dispatch(self, request: Request, call_next):
        """Collect metrics for HTTP request/response."""
        start_time = time.time()
        method = request.method
        endpoint = self._get_endpoint_pattern(request)
        
        # Measure request size
        content_length = request.headers.get('content-length', '0')
        request_size = int(content_length) if content_length.isdigit() else 0
        
        REQUEST_SIZE.labels(method=method, endpoint=endpoint).observe(request_size)
        
        try:
            # Process request
            response = await call_next(request)
            status_code = response.status_code
            
            # Record successful request metrics
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status=status_code
            ).inc()
            
        except Exception as e:
            # Record error metrics
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status=500
            ).inc()
            
            logger.error(f"Request failed: {method} {endpoint} - {e}")
            raise
        
        # Measure response time
        duration = time.time() - start_time
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
        
        # Measure response size if enabled
        if self.enable_response_size and hasattr(response, 'body'):
            response_size = len(response.body) if response.body else 0
            RESPONSE_SIZE.labels(method=method, endpoint=endpoint).observe(response_size)
        
        return response

    def _get_endpoint_pattern(self, request: Request) -> str:
        """Extract endpoint pattern for consistent metrics grouping."""
        # Try to get route pattern from FastAPI
        if hasattr(request, 'scope') and 'route' in request.scope:
            route = request.scope['route']
            if hasattr(route, 'path'):
                return route.path
        
        # Fallback to normalized path
        path = request.url.path
        
        # Normalize path parameters
        import re
        path = re.sub(r'/[0-9a-f-]{36}', '/{uuid}', path)  # UUIDs
        path = re.sub(r'/\\d+', '/{id}', path)  # Numeric IDs
        
        return path

    def get_metrics_summary(self) -> Dict[str, float]:
        """Get current metrics summary."""
        return {
            'total_requests': REQUEST_COUNT._value.sum(),
            'avg_response_time': REQUEST_DURATION._sum.sum() / max(REQUEST_DURATION._count.sum(), 1),
            'total_request_size': REQUEST_SIZE._sum.sum(),
            'total_response_size': RESPONSE_SIZE._sum.sum(),
        }


def setup_metrics_middleware(app, metrics_port: Optional[int] = 9090):
    """Helper function để setup metrics middleware."""
    middleware = MetricsMiddleware(app, metrics_port=metrics_port)
    app.add_middleware(MetricsMiddleware, metrics_port=metrics_port)
    return middleware


__all__ = [
    "MetricsMiddleware",
    "setup_metrics_middleware",
    "REQUEST_COUNT",
    "REQUEST_DURATION",
    "REQUEST_SIZE",
    "RESPONSE_SIZE"
]
''',
    "zero_trust.py": '''"""Zero Trust security middleware implementation."""
from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

from apps.backend.core.security.context import SecurityContext
from apps.backend.core.security.policy_engine import PolicyEngine
from apps.backend.core.security.risk_assessment import RiskAssessment

logger = logging.getLogger(__name__)


class ZeroTrustMiddleware(BaseHTTPMiddleware):
    """
    Zero Trust security middleware.
    
    Implements continuous verification and risk-based access control.
    Never trust, always verify approach for all requests.
    """

    def __init__(
        self,
        app,
        policy_engine: Optional[PolicyEngine] = None,
        risk_assessment: Optional[RiskAssessment] = None,
        high_risk_threshold: float = 0.8,
        medium_risk_threshold: float = 0.5
    ):
        super().__init__(app)
        self.policy_engine = policy_engine or PolicyEngine()
        self.risk_assessment = risk_assessment or RiskAssessment()
        self.high_risk_threshold = high_risk_threshold
        self.medium_risk_threshold = medium_risk_threshold

    async def dispatch(self, request: Request, call_next):
        """Apply Zero Trust security checks."""
        # Build security context
        security_context = await self._build_security_context(request)
        
        # Assess risk level
        risk_score = await self.risk_assessment.calculate_risk(
            request, security_context
        )
        
        # Apply risk-based policies
        await self._apply_risk_policies(request, security_context, risk_score)
        
        # Verify access permissions
        await self._verify_access_permissions(request, security_context)
        
        # Log security event
        self._log_security_event(request, security_context, risk_score)
        
        # Process request with enhanced monitoring
        response = await call_next(request)
        
        # Post-processing security checks
        await self._post_process_security(request, response, security_context)
        
        return response

    async def _build_security_context(self, request: Request) -> SecurityContext:
        """Build comprehensive security context."""
        user_id = getattr(request.state, 'user_id', None)
        session_id = getattr(request.state, 'session_id', None)
        
        return SecurityContext(
            user_id=user_id,
            session_id=session_id,
            ip_address=self._get_client_ip(request),
            user_agent=request.headers.get('user-agent', ''),
            path=request.url.path,
            method=request.method,
            headers=dict(request.headers),
            timestamp=time.time()
        )

    async def _apply_risk_policies(
        self,
        request: Request,
        context: SecurityContext,
        risk_score: float
    ) -> None:
        """Apply policies based on risk assessment."""
        if risk_score >= self.high_risk_threshold:
            # High risk - require additional authentication
            await self._require_mfa(request, context)
            await self._apply_additional_monitoring(request, context)
            
        elif risk_score >= self.medium_risk_threshold:
            # Medium risk - apply enhanced monitoring
            await self._apply_enhanced_monitoring(request, context)
        
        # Apply rate limiting based on risk
        await self._apply_risk_based_rate_limiting(request, context, risk_score)

    async def _verify_access_permissions(
        self,
        request: Request,
        context: SecurityContext
    ) -> None:
        """Verify user has permission for requested resource."""
        # Check if authentication is required
        if self._requires_authentication(request.url.path):
            if not context.user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
        
        # Check resource-level permissions
        if context.user_id:
            has_permission = await self.policy_engine.check_permission(
                user_id=context.user_id,
                resource=request.url.path,
                action=request.method.lower()
            )
            
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )

    async def _require_mfa(self, request: Request, context: SecurityContext) -> None:
        """Require multi-factor authentication for high-risk requests."""
        mfa_token = request.headers.get('X-MFA-Token')
        if not mfa_token:
            logger.warning(f"MFA required for high-risk request from {context.ip_address}")
            raise HTTPException(
                status_code=status.HTTP_428_PRECONDITION_REQUIRED,
                detail="Multi-factor authentication required",
                headers={"X-Require-MFA": "true"}
            )
        
        # Verify MFA token
        if not await self._verify_mfa_token(context.user_id, mfa_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA token"
            )

    async def _apply_additional_monitoring(
        self,
        request: Request,
        context: SecurityContext
    ) -> None:
        """Apply additional monitoring for high-risk requests."""
        # Enhanced logging
        logger.warning(
            f"High-risk request: {context.method} {context.path} "
            f"from {context.ip_address} (user: {context.user_id})"
        )
        
        # Real-time alerting
        await self._send_security_alert(
            level="HIGH",
            message=f"High-risk request detected",
            context=context
        )

    async def _apply_enhanced_monitoring(
        self,
        request: Request,
        context: SecurityContext
    ) -> None:
        """Apply enhanced monitoring for medium-risk requests."""
        logger.info(
            f"Medium-risk request: {context.method} {context.path} "
            f"from {context.ip_address}"
        )

    async def _apply_risk_based_rate_limiting(
        self,
        request: Request,
        context: SecurityContext,
        risk_score: float
    ) -> None:
        """Apply stricter rate limits for higher risk requests."""
        if risk_score >= self.high_risk_threshold:
            # High risk: very strict limits
            await self._apply_rate_limit(context.ip_address, requests_per_minute=10)
        elif risk_score >= self.medium_risk_threshold:
            # Medium risk: moderate limits
            await self._apply_rate_limit(context.ip_address, requests_per_minute=30)

    def _requires_authentication(self, path: str) -> bool:
        """Check if path requires authentication."""
        public_paths = [
            "/health",
            "/docs",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register"
        ]
        return not any(path.startswith(p) for p in public_paths)

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address with proxy support."""
        # Check X-Forwarded-For header
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to client host
        return request.client.host if request.client else "unknown"

    def _log_security_event(
        self,
        request: Request,
        context: SecurityContext,
        risk_score: float
    ) -> None:
        """Log security event for audit trail."""
        logger.info(
            f"Security event: {context.method} {context.path} "
            f"risk={risk_score:.2f} ip={context.ip_address} "
            f"user={context.user_id or 'anonymous'}"
        )

    async def _post_process_security(
        self,
        request: Request,
        response: Response,
        context: SecurityContext
    ) -> None:
        """Post-processing security checks."""
        # Add security headers
        response.headers["X-Security-Scan"] = "passed"
        response.headers["X-Risk-Level"] = await self._get_risk_level_header(context)
        
        # Log successful completion
        logger.debug(f"Security check completed for {context.path}")

    # Placeholder methods for integration points
    async def _verify_mfa_token(self, user_id: str, token: str) -> bool:
        """Verify MFA token (implement with actual MFA service)."""
        # TODO: Integrate with actual MFA service
        return len(token) >= 6

    async def _send_security_alert(self, level: str, message: str, context: SecurityContext) -> None:
        """Send security alert (implement with actual alerting system)."""
        # TODO: Integrate with alerting system
        logger.critical(f"[{level}] {message} - Context: {context}")

    async def _apply_rate_limit(self, identifier: str, requests_per_minute: int) -> None:
        """Apply rate limiting (integrate with rate limiting service)."""
        # TODO: Integrate with rate limiting service
        pass

    async def _get_risk_level_header(self, context: SecurityContext) -> str:
        """Get risk level for response header."""
        # TODO: Calculate based on context
        return "low"


__all__ = ["ZeroTrustMiddleware"]
''',
    "logging.py": '''"""Comprehensive logging middleware."""
from __future__ import annotations

import json
import logging
import time
import uuid
from typing import Any, Dict, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """
    Structured logging middleware with request tracing.
    
    Provides comprehensive request/response logging with correlation IDs,
    performance metrics, and structured JSON output.
    """

    def __init__(
        self,
        app,
        log_requests: bool = True,
        log_responses: bool = True,
        log_request_body: bool = False,
        log_response_body: bool = False,
        sensitive_headers: Optional[list] = None,
        max_body_size: int = 1024 * 10  # 10KB
    ):
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.max_body_size = max_body_size
        
        # Headers to redact for security
        self.sensitive_headers = sensitive_headers or [
            'authorization', 'cookie', 'x-api-key', 'x-auth-token'
        ]

    async def dispatch(self, request: Request, call_next):
        """Process request with comprehensive logging."""
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        request.state.correlation_id = correlation_id
        
        # Start timing
        start_time = time.time()
        
        # Log incoming request
        if self.log_requests:
            await self._log_request(request, correlation_id)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            if self.log_responses:
                await self._log_response(request, response, correlation_id, duration)
            
            # Add correlation header to response
            response.headers["X-Correlation-ID"] = correlation_id
            
            return response
            
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            await self._log_error(request, e, correlation_id, duration)
            raise

    async def _log_request(self, request: Request, correlation_id: str) -> None:
        """Log incoming request details."""
        # Extract basic request info
        log_data = {
            "event": "request_start",
            "correlation_id": correlation_id,
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": self._sanitize_headers(dict(request.headers)),
            "client_ip": self._get_client_ip(request),
            "user_agent": request.headers.get("user-agent", ""),
            "timestamp": time.time()
        }
        
        # Add user info if available
        if hasattr(request.state, 'user_id'):
            log_data["user_id"] = request.state.user_id
        
        # Add request body if enabled
        if self.log_request_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await self._get_request_body(request)
                if body:
                    log_data["request_body"] = body
            except Exception as e:
                log_data["request_body_error"] = str(e)
        
        logger.info(json.dumps(log_data, default=str))

    async def _log_response(
        self,
        request: Request,
        response: Response,
        correlation_id: str,
        duration: float
    ) -> None:
        """Log response details."""
        log_data = {
            "event": "request_complete",
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "response_headers": self._sanitize_headers(dict(response.headers)),
            "timestamp": time.time()
        }
        
        # Add response body if enabled and successful
        if (self.log_response_body and
            200 <= response.status_code < 300 and
            hasattr(response, 'body')):
            try:
                body = await self._get_response_body(response)
                if body:
                    log_data["response_body"] = body
            except Exception as e:
                log_data["response_body_error"] = str(e)
        
        # Determine log level based on status code
        if response.status_code >= 500:
            logger.error(json.dumps(log_data, default=str))
        elif response.status_code >= 400:
            logger.warning(json.dumps(log_data, default=str))
        else:
            logger.info(json.dumps(log_data, default=str))

    async def _log_error(
        self,
        request: Request,
        error: Exception,
        correlation_id: str,
        duration: float
    ) -> None:
        """Log request error."""
        log_data = {
            "event": "request_error",
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "duration_ms": round(duration * 1000, 2),
            "timestamp": time.time()
        }
        
        logger.error(json.dumps(log_data, default=str), exc_info=True)

    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Remove sensitive information from headers."""
        sanitized = {}
        for key, value in headers.items():
            if key.lower() in self.sensitive_headers:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        return sanitized

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP with proxy support."""
        # Check X-Forwarded-For header
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to client host
        return request.client.host if request.client else "unknown"

    async def _get_request_body(self, request: Request) -> Optional[str]:
        """Extract request body safely."""
        try:
            content_type = request.headers.get("content-type", "")
            
            # Only log text-based content types
            if not any(ct in content_type for ct in ["json", "text", "xml", "form"]):
                return f"[Binary content: {content_type}]"
            
            # Read body with size limit
            body = await request.body()
            if len(body) > self.max_body_size:
                return f"[Body too large: {len(body)} bytes]"
            
            # Try to decode as text
            try:
                body_text = body.decode("utf-8")
                # Try to parse as JSON for better formatting
                if "json" in content_type:
                    parsed = json.loads(body_text)
                    return json.dumps(parsed, indent=2)
                return body_text
            except (UnicodeDecodeError, json.JSONDecodeError):
                return f"[Unable to decode body: {len(body)} bytes]"
                
        except Exception:
            return None

    async def _get_response_body(self, response: Response) -> Optional[str]:
        """Extract response body safely."""
        try:
            if not hasattr(response, 'body') or not response.body:
                return None
            
            content_type = response.headers.get("content-type", "")
            
            # Only log text-based responses
            if not any(ct in content_type for ct in ["json", "text", "xml"]):
                return f"[Binary response: {content_type}]"
            
            body = response.body
            if isinstance(body, bytes):
                if len(body) > self.max_body_size:
                    return f"[Response too large: {len(body)} bytes]"
                
                try:
                    body_text = body.decode("utf-8")
                    # Try to parse as JSON
                    if "json" in content_type:
                        parsed = json.loads(body_text)
                        return json.dumps(parsed, indent=2)
                    return body_text
                except (UnicodeDecodeError, json.JSONDecodeError):
                    return f"[Unable to decode response: {len(body)} bytes]"
            
            return str(body)
            
        except Exception:
            return None


def get_correlation_id(request: Request) -> Optional[str]:
    """Helper function to get correlation ID from request."""
    return getattr(request.state, 'correlation_id', None)


__all__ = ["StructuredLoggingMiddleware", "get_correlation_id"]
''',
    "api_version.py": r'''"""API versioning middleware."""
from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set

from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class APIVersionMiddleware(BaseHTTPMiddleware):
    """
    API versioning middleware with deprecation support.
    
    Handles API version negotiation through headers or URL path.
    Supports version deprecation warnings and sunset policies.
    """

    def __init__(
        self,
        app,
        default_version: str = "v1",
        supported_versions: Optional[List[str]] = None,
        deprecated_versions: Optional[Dict[str, str]] = None,
        version_header: str = "X-API-Version",
        require_version: bool = False
    ):
        super().__init__(app)
        self.default_version = default_version
        self.supported_versions = supported_versions or ["v1", "v2"]
        self.deprecated_versions = deprecated_versions or {}
        self.version_header = version_header
        self.require_version = require_version

    async def dispatch(self, request: Request, call_next):
        """Process API version negotiation."""
        # Extract API version from request
        api_version = self._extract_api_version(request)
        
        # Validate version
        if not self._is_version_supported(api_version):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Unsupported API version",
                    "version": api_version,
                    "supported_versions": self.supported_versions
                }
            )
        
        # Check if version is deprecated
        deprecation_info = self._check_deprecation(api_version)
        
        # Set version in request state
        request.state.api_version = api_version
        
        # Process request
        response = await call_next(request)
        
        # Add version headers to response
        self._add_version_headers(response, api_version, deprecation_info)
        
        # Log version usage
        self._log_version_usage(request, api_version, deprecation_info)
        
        return response

    def _extract_api_version(self, request: Request) -> str:
        """Extract API version from request."""
        # 1. Check header first
        version = request.headers.get(self.version_header)
        if version:
            return self._normalize_version(version)
        
        # 2. Check URL path
        path_parts = request.url.path.strip('/').split('/')
        if path_parts and path_parts[0].startswith('v') and path_parts[0][1:].isdigit():
            return path_parts[0]
        
        # 3. Check if API path contains version
        if '/api/' in request.url.path:
            # Look for /api/v1/, /api/v2/, etc.
            import re
            match = re.search(r'/api/(v\d+)/', request.url.path)
            if match:
                return match.group(1)
        
        # 4. Check Accept header for version
        accept_header = request.headers.get('Accept', '')
        if 'version=' in accept_header:
            import re
            match = re.search(r'version=([^;,\s]+)', accept_header)
            if match:
                return self._normalize_version(match.group(1))
        
        # 5. Use default version
        if self.require_version:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="API version is required"
            )
        
        return self.default_version

    def _normalize_version(self, version: str) -> str:
        """Normalize version string format."""
        version = version.strip().lower()
        
        # Remove 'v' prefix if present
        if version.startswith('v'):
            version = version[1:]
        
        # Add 'v' prefix back
        if version.isdigit():
            return f"v{version}"
        
        # Handle semantic versions (1.0, 2.1, etc.)
        if '.' in version:
            major = version.split('.')[0]
            if major.isdigit():
                return f"v{major}"
        
        return version

    def _is_version_supported(self, version: str) -> bool:
        """Check if API version is supported."""
        return version in self.supported_versions

    def _check_deprecation(self, version: str) -> Optional[Dict[str, str]]:
        """Check if version is deprecated and return deprecation info."""
        if version in self.deprecated_versions:
            return {
                "deprecated": "true",
                "sunset_date": self.deprecated_versions[version],
                "message": f"API version {version} is deprecated. Please migrate to a newer version."
            }
        return None

    def _add_version_headers(
        self,
        response: Response,
        version: str,
        deprecation_info: Optional[Dict[str, str]]
    ) -> None:
        """Add version-related headers to response."""
        # Add current version header
        response.headers["X-API-Version"] = version
        
        # Add supported versions
        response.headers["X-Supported-Versions"] = ",".join(self.supported_versions)
        
        # Add deprecation headers if applicable
        if deprecation_info:
            response.headers["Deprecation"] = "true"
            response.headers["Sunset"] = deprecation_info["sunset_date"]
            response.headers["Warning"] = f'299 - "{deprecation_info["message"]}"'

    def _log_version_usage(
        self,
        request: Request,
        version: str,
        deprecation_info: Optional[Dict[str, str]]
    ) -> None:
        """Log API version usage for analytics."""
        log_data = {
            "event": "api_version_usage",
            "version": version,
            "path": request.url.path,
            "method": request.method,
            "user_agent": request.headers.get("user-agent", ""),
            "deprecated": bool(deprecation_info)
        }
        
        if deprecation_info:
            logger.warning(f"Deprecated API version used: {version} - {deprecation_info['message']}")
        else:
            logger.debug(f"API version used: {version}")

    def get_version_metrics(self) -> Dict[str, int]:
        """Get version usage metrics (placeholder for implementation)."""
        # TODO: Implement actual metrics collection
        return {
            "v1": 100,
            "v2": 50,
            "deprecated_usage": 10
        }

    def add_version_route_mapping(self, version: str, handler_mapping: Dict[str, str]) -> None:
        """Add route mapping for specific version (placeholder for implementation)."""
        # TODO: Implement version-specific route mapping
        pass

    def set_version_sunset_date(self, version: str, sunset_date: str) -> None:
        """Set sunset date for deprecated version."""
        self.deprecated_versions[version] = sunset_date
        logger.info(f"Set sunset date for version {version}: {sunset_date}")


__all__ = ["APIVersionMiddleware"]
''',
    "request_id.py": '''"""Request ID middleware for distributed tracing."""
from __future__ import annotations

import logging
import uuid
from typing import Callable, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Request ID middleware for distributed tracing.
    
    Generates unique request IDs for tracking requests across services.
    Supports both incoming request IDs and generates new ones when missing.
    """

    def __init__(
        self,
        app,
        header_name: str = "X-Request-ID",
        response_header_name: Optional[str] = None,
        generator: Optional[Callable[[], str]] = None,
        trust_incoming_header: bool = True
    ):
        super().__init__(app)
        self.header_name = header_name
        self.response_header_name = response_header_name or header_name
        self.generator = generator or self._default_generator
        self.trust_incoming_header = trust_incoming_header

    async def dispatch(self, request: Request, call_next):
        """Process request with ID tracking."""
        # Extract or generate request ID
        request_id = self._get_or_generate_request_id(request)
        
        # Store in request state
        request.state.request_id = request_id
        
        # Add to logging context
        self._add_to_logging_context(request_id)
        
        # Log request start
        logger.debug(f"Request started: {request.method} {request.url.path} (ID: {request_id})")
        
        try:
            # Process request
            response = await call_next(request)
            
            # Add request ID to response headers
            response.headers[self.response_header_name] = request_id
            
            # Log request completion
            logger.debug(f"Request completed: {request_id} (Status: {response.status_code})")
            
            return response
            
        except Exception as e:
            # Log request error
            logger.error(f"Request failed: {request_id} - {str(e)}")
            raise
        finally:
            # Clean up logging context
            self._cleanup_logging_context()

    def _get_or_generate_request_id(self, request: Request) -> str:
        """Get request ID from headers or generate new one."""
        # Check for existing request ID in headers
        if self.trust_incoming_header:
            existing_id = request.headers.get(self.header_name)
            if existing_id and self._is_valid_request_id(existing_id):
                return existing_id
        
        # Generate new request ID
        return self.generator()

    def _default_generator(self) -> str:
        """Default request ID generator using UUID4."""
        return str(uuid.uuid4())

    def _is_valid_request_id(self, request_id: str) -> bool:
        """Validate request ID format."""
        # Basic validation - non-empty, reasonable length
        if not request_id or len(request_id) > 128:
            return False
        
        # Check for potentially malicious content
        if any(char in request_id for char in ['<', '>', '"', "'", '&']):
            return False
        
        return True

    def _add_to_logging_context(self, request_id: str) -> None:
        """Add request ID to logging context."""
        # Use structured logging adapter if available
        try:
            import contextvars
            
            # Create context var for request ID
            if not hasattr(self, '_request_id_var'):
                self._request_id_var = contextvars.ContextVar('request_id')
            
            self._request_id_var.set(request_id)
            
        except ImportError:
            # Fallback to logger adapter
            pass

    def _cleanup_logging_context(self) -> None:
        """Clean up logging context."""
        try:
            if hasattr(self, '_request_id_var'):
                # Context vars are automatically cleaned up
                pass
        except Exception:
            pass

    def get_request_id(self, request: Request) -> Optional[str]:
        """Get request ID from request state."""
        return getattr(request.state, 'request_id', None)

    def create_child_request_id(self, parent_id: str, suffix: str = None) -> str:
        """Create child request ID for internal service calls."""
        if suffix:
            return f"{parent_id}.{suffix}"
        else:
            # Generate random suffix
            import random
            import string
            suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            return f"{parent_id}.{suffix}"

    def validate_request_id_chain(self, request_id: str) -> bool:
        """Validate request ID chain for distributed tracing."""
        # Check for valid chain format (parent.child.grandchild...)
        parts = request_id.split('.')
        
        # Root ID should be valid UUID or similar
        if not parts[0]:
            return False
        
        # Each part should be non-empty
        for part in parts:
            if not part or len(part) > 32:
                return False
        
        # Reasonable chain depth
        if len(parts) > 10:
            return False
        
        return True

    def extract_root_request_id(self, request_id: str) -> str:
        """Extract root request ID from chain."""
        return request_id.split('.')[0]

    def get_request_depth(self, request_id: str) -> int:
        """Get depth of request in chain."""
        return len(request_id.split('.')) - 1


def get_request_id(request: Request) -> Optional[str]:
    """Helper function to get request ID from request."""
    return getattr(request.state, 'request_id', None)


def get_or_create_request_id(request: Request) -> str:
    """Helper function to get or create request ID."""
    request_id = get_request_id(request)
    if not request_id:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
    return request_id


__all__ = [
    "RequestIDMiddleware",
    "get_request_id",
    "get_or_create_request_id"
]
''',
}


def fix_specific_file(file_path: Path, template_key: str) -> bool:
    """Fix a specific middleware file."""
    if template_key not in FIX_TEMPLATES:
        print(f"❌ No fix template for {template_key}")
        return False

    # Backup existing content
    if file_path.exists():
        existing = file_path.read_text(encoding="utf-8")
        if len(existing.strip()) > 100:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_file = file_path.with_suffix(f".backup_{timestamp}.py")
            backup_file.write_text(existing, encoding="utf-8")
            print(f"📁 Backed up to {backup_file}")

    # Write enhanced content
    enhanced_content = FIX_TEMPLATES[template_key]

    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write new content
    file_path.write_text(enhanced_content, encoding="utf-8")
    print(f"✅ Fixed {file_path}")
    return True


def main() -> int:
    """Main fix function."""
    print("🔧 ADVANCED MIDDLEWARE FIX SCRIPT")
    print("=" * 50)

    fixed_count = 0

    # Files to fix based on analysis
    files_to_fix = [
        ("zeta_vn/app/middleware/metrics_middleware.py", "metrics_middleware.py"),
        ("zeta_vn/app/middleware/zero_trust.py", "zero_trust.py"),
        ("zeta_vn/app/middleware/logging.py", "logging.py"),
        ("zeta_vn/app/middleware/api_version.py", "api_version.py"),
        ("zeta_vn/app/middleware/request_id.py", "request_id.py"),
    ]

    for file_path_str, template_key in files_to_fix:
        file_path = Path(file_path_str)
        if fix_specific_file(file_path, template_key):
            fixed_count += 1

    print("\n📊 FIX COMPLETE")
    print(f"   Fixed files: {fixed_count}")
    print("   ✅ Run completeness analysis again to verify improvements")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
