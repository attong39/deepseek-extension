#!/usr/bin/env python3
"""
Enhanced Middleware Completion Script

Tự động thêm code vào các middleware files còn thiếu chức năng.
Tuân thủ patterns security, performance, observability của ZETA_VN.
"""

from __future__ import annotations

from pathlib import Path
import SystemExit
import bool
import file_path_str
import imp
import int
import len
import print
import str
import template_key

# Định nghĩa templates cho các loại middleware
MIDDLEWARE_TEMPLATES = {
    "auth_middleware.py": '''"""Authentication middleware for FastAPI applications."""
from __future__ import annotations

import logging
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware

from apps.backend.core.auth.jwt_handler import JWTHandler
from apps.backend.core.auth.models import User

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware xác thực JWT token cho protected routes."""

    def __init__(self, app, jwt_handler: Optional[JWTHandler] = None):
        super().__init__(app)
        self.jwt_handler = jwt_handler or JWTHandler()
        self.security = HTTPBearer(auto_error=False)

    async def dispatch(self, request: Request, call_next):
        """Process authentication for incoming requests."""
        # Skip auth for public endpoints
        if self._is_public_endpoint(request.url.path):
            return await call_next(request)

        try:
            # Extract token from Authorization header
            token = await self._extract_token(request)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing authentication token"
                )

            # Validate and decode token
            payload = self.jwt_handler.decode_token(token)
            user_id = payload.get("sub")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )

            # Attach user info to request state
            request.state.user_id = user_id
            request.state.token_payload = payload
            
            logger.debug(f"Authenticated user: {user_id}")
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )

        return await call_next(request)

    def _is_public_endpoint(self, path: str) -> bool:
        """Check if endpoint requires authentication."""
        public_paths = [
            "/health",
            "/docs",
            "/openapi.json",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
        ]
        return any(path.startswith(p) for p in public_paths)

    async def _extract_token(self, request: Request) -> Optional[str]:
        """Extract JWT token from request headers."""
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None
        
        if not auth_header.startswith("Bearer "):
            return None
            
        return auth_header[7:]  # Remove "Bearer " prefix


__all__ = ["AuthenticationMiddleware"]
''',
    "compression_middleware.py": '''"""Response compression middleware."""
from __future__ import annotations

import gzip
import logging
from typing import List

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class CompressionMiddleware(BaseHTTPMiddleware):
    """Middleware nén response để giảm bandwidth."""

    def __init__(
        self,
        app,
        minimum_size: int = 1024,
        compress_level: int = 6,
        excluded_types: List[str] = None
    ):
        super().__init__(app)
        self.minimum_size = minimum_size
        self.compress_level = compress_level
        self.excluded_types = excluded_types or [
            "image/",
            "video/",
            "audio/",
            "application/zip",
            "application/gzip"
        ]

    async def dispatch(self, request: Request, call_next):
        """Process request and compress response if applicable."""
        response = await call_next(request)
        
        # Check if client accepts gzip compression
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding.lower():
            return response

        # Check response size and content type
        content = b""
        async for chunk in response.body_iterator:
            content += chunk

        if not self._should_compress(content, response):
            # Return original response
            response.body = content
            return response

        # Compress content
        try:
            compressed_content = gzip.compress(
                content,
                compresslevel=self.compress_level
            )
            
            # Update headers
            response.headers["content-encoding"] = "gzip"
            response.headers["content-length"] = str(len(compressed_content))
            response.body = compressed_content
            
            # Log compression ratio
            original_size = len(content)
            compressed_size = len(compressed_content)
            ratio = (1 - compressed_size / original_size) * 100
            
            logger.debug(
                f"Compressed response: {original_size}B -> {compressed_size}B "
                f"({ratio:.1f}% reduction)"
            )
            
        except Exception as e:
            logger.error(f"Compression failed: {e}")
            response.body = content

        return response

    def _should_compress(self, content: bytes, response: Response) -> bool:
        """Determine if response should be compressed."""
        # Check minimum size
        if len(content) < self.minimum_size:
            return False

        # Check content type
        content_type = response.headers.get("content-type", "")
        for excluded in self.excluded_types:
            if content_type.startswith(excluded):
                return False

        # Check if already compressed
        if response.headers.get("content-encoding"):
            return False

        return True


__all__ = ["CompressionMiddleware"]
''',
    "cors_middleware.py": '''"""CORS middleware for cross-origin requests."""
from __future__ import annotations

import logging
from typing import List, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

logger = logging.getLogger(__name__)


class CORSMiddleware(BaseHTTPMiddleware):
    """Middleware xử lý Cross-Origin Resource Sharing (CORS)."""

    def __init__(
        self,
        app,
        allow_origins: List[str] = None,
        allow_methods: List[str] = None,
        allow_headers: List[str] = None,
        allow_credentials: bool = True,
        max_age: int = 3600
    ):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or [
            "GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"
        ]
        self.allow_headers = allow_headers or [
            "Accept", "Accept-Language", "Content-Language", "Content-Type",
            "Authorization", "X-Requested-With", "X-API-Key"
        ]
        self.allow_credentials = allow_credentials
        self.max_age = max_age

    async def dispatch(self, request: Request, call_next):
        """Process CORS for incoming requests."""
        origin = request.headers.get("origin")
        
        # Handle preflight OPTIONS request
        if request.method == "OPTIONS":
            return self._handle_preflight(request, origin)

        # Process normal request
        response = await call_next(request)
        
        # Add CORS headers to response
        self._add_cors_headers(response, origin)
        
        return response

    def _handle_preflight(self, request: Request, origin: Optional[str]) -> Response:
        """Handle CORS preflight OPTIONS request."""
        response = StarletteResponse()
        
        # Check if origin is allowed
        if not self._is_origin_allowed(origin):
            logger.warning(f"CORS: Origin not allowed: {origin}")
            return response

        # Add CORS headers
        self._add_cors_headers(response, origin, is_preflight=True)
        
        # Add preflight-specific headers
        requested_method = request.headers.get("access-control-request-method")
        if requested_method and requested_method in self.allow_methods:
            response.headers["access-control-allow-methods"] = ", ".join(self.allow_methods)

        requested_headers = request.headers.get("access-control-request-headers")
        if requested_headers:
            response.headers["access-control-allow-headers"] = ", ".join(self.allow_headers)

        response.headers["access-control-max-age"] = str(self.max_age)
        
        logger.debug(f"CORS preflight handled for origin: {origin}")
        return response

    def _add_cors_headers(
        self,
        response: Response,
        origin: Optional[str],
        is_preflight: bool = False
    ) -> None:
        """Add CORS headers to response."""
        if self._is_origin_allowed(origin):
            response.headers["access-control-allow-origin"] = origin or "*"
        
        if self.allow_credentials:
            response.headers["access-control-allow-credentials"] = "true"

        if not is_preflight:
            # Expose headers for actual requests
            response.headers["access-control-expose-headers"] = ", ".join([
                "Content-Length", "Content-Type", "X-Request-ID", "X-API-Version"
            ])

    def _is_origin_allowed(self, origin: Optional[str]) -> bool:
        """Check if origin is in allowed list."""
        if not origin:
            return True
        
        if "*" in self.allow_origins:
            return True
            
        return origin in self.allow_origins


__all__ = ["CORSMiddleware"]
''',
    "performance_middleware.py": r'''"""Performance monitoring middleware."""
from __future__ import annotations

import logging
import time
from typing import Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from apps.backend.core.observability.metrics import performance_metrics

logger = logging.getLogger(__name__)


class PerformanceMiddleware(BaseHTTPMiddleware):
    """Middleware theo dõi performance của requests."""

    def __init__(
        self,
        app,
        slow_request_threshold: float = 1.0,
        enable_detailed_logging: bool = False
    ):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
        self.enable_detailed_logging = enable_detailed_logging

    async def dispatch(self, request: Request, call_next):
        """Monitor request performance."""
        start_time = time.time()
        method = request.method
        path = request.url.path
        
        # Extract route pattern for better grouping
        route_pattern = self._extract_route_pattern(request)
        
        try:
            # Process request
            response = await call_next(request)
            status_code = response.status_code
            
        except Exception as e:
            # Handle errors
            end_time = time.time()
            duration = end_time - start_time
            
            # Record error metrics
            performance_metrics.record_request_duration(
                method=method,
                route=route_pattern,
                status_code=500,
                duration=duration
            )
            
            logger.error(
                f"Request failed: {method} {path} - {duration:.3f}s - {e}"
            )
            raise
        
        # Calculate duration
        end_time = time.time()
        duration = end_time - start_time
        
        # Record metrics
        performance_metrics.record_request_duration(
            method=method,
            route=route_pattern,
            status_code=status_code,
            duration=duration
        )
        
        # Log slow requests
        if duration > self.slow_request_threshold:
            logger.warning(
                f"Slow request: {method} {path} - {duration:.3f}s - {status_code}"
            )
        
        # Detailed logging if enabled
        if self.enable_detailed_logging:
            logger.info(
                f"Request: {method} {path} - {duration:.3f}s - {status_code}"
            )
        
        # Add performance headers
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        response.headers["X-Process-Time"] = str(int(duration * 1000))  # milliseconds
        
        return response

    def _extract_route_pattern(self, request: Request) -> str:
        """Extract route pattern from request for better metrics grouping."""
        # Try to get route from FastAPI
        if hasattr(request, "scope") and "route" in request.scope:
            route = request.scope["route"]
            if hasattr(route, "path"):
                return route.path
        
        # Fallback to path with parameter normalization
        path = request.url.path
        
        # Simple parameter normalization
        # Replace UUIDs and numbers with placeholders
        import re
        path = re.sub(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '/{uuid}', path)
        path = re.sub(r'/\d+', '/{id}', path)
        
        return path


__all__ = ["PerformanceMiddleware"]
''',
    "rate_limiting.py": '''"""Rate limiting middleware."""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Dict, Optional, Tuple

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware giới hạn số lượng requests từ mỗi client."""

    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        burst_size: int = 10,
        enable_per_route_limits: bool = True
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst_size = burst_size
        self.enable_per_route_limits = enable_per_route_limits
        
        # In-memory storage for rate limit data
        # Format: {client_id: (request_times, last_reset)}
        self._client_data: Dict[str, Tuple[list, float]] = {}
        self._cleanup_interval = 300  # 5 minutes
        self._last_cleanup = time.time()
        
        # Per-route limits
        self._route_limits = {
            "/api/v1/auth/login": 5,  # 5 per minute
            "/api/v1/auth/register": 3,  # 3 per minute
            "/api/v1/upload": 10,  # 10 per minute
        }

    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting to incoming requests."""
        # Extract client identifier
        client_id = self._get_client_id(request)
        
        # Determine rate limit for this request
        rate_limit = self._get_rate_limit(request)
        
        # Check rate limit
        if not self._is_request_allowed(client_id, rate_limit):
            # Get remaining time until reset
            reset_time = self._get_reset_time(client_id)
            
            logger.warning(
                f"Rate limit exceeded for client {client_id}: "
                f"{rate_limit} requests/minute"
            )
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": rate_limit,
                    "retry_after": reset_time
                },
                headers={
                    "Retry-After": str(int(reset_time)),
                    "X-RateLimit-Limit": str(rate_limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + reset_time))
                }
            )

        # Record this request
        self._record_request(client_id)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        remaining = self._get_remaining_requests(client_id, rate_limit)
        reset_time = self._get_reset_time(client_id)
        
        response.headers["X-RateLimit-Limit"] = str(rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + reset_time))
        
        # Cleanup old data periodically
        await self._cleanup_if_needed()
        
        return response

    def _get_client_id(self, request: Request) -> str:
        """Extract client identifier from request."""
        # Try to get user ID from authentication
        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"
        
        # Fallback to IP address
        client_ip = request.client.host if request.client else "unknown"
        
        # Consider X-Forwarded-For header
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        
        return f"ip:{client_ip}"

    def _get_rate_limit(self, request: Request) -> int:
        """Get rate limit for specific route."""
        if not self.enable_per_route_limits:
            return self.requests_per_minute
        
        path = request.url.path
        return self._route_limits.get(path, self.requests_per_minute)

    def _is_request_allowed(self, client_id: str, rate_limit: int) -> bool:
        """Check if request is within rate limit."""
        current_time = time.time()
        window_start = current_time - 60  # 1 minute window
        
        if client_id not in self._client_data:
            return True
        
        request_times, _ = self._client_data[client_id]
        
        # Remove old requests outside the window
        recent_requests = [t for t in request_times if t > window_start]
        
        return len(recent_requests) < rate_limit

    def _record_request(self, client_id: str) -> None:
        """Record a new request for client."""
        current_time = time.time()
        
        if client_id not in self._client_data:
            self._client_data[client_id] = ([], current_time)
        
        request_times, _ = self._client_data[client_id]
        request_times.append(current_time)
        
        # Keep only recent requests (last 2 minutes for safety)
        window_start = current_time - 120
        recent_requests = [t for t in request_times if t > window_start]
        
        self._client_data[client_id] = (recent_requests, current_time)

    def _get_remaining_requests(self, client_id: str, rate_limit: int) -> int:
        """Get number of remaining requests for client."""
        if client_id not in self._client_data:
            return rate_limit
        
        current_time = time.time()
        window_start = current_time - 60
        
        request_times, _ = self._client_data[client_id]
        recent_requests = [t for t in request_times if t > window_start]
        
        return max(0, rate_limit - len(recent_requests))

    def _get_reset_time(self, client_id: str) -> float:
        """Get time until rate limit resets."""
        if client_id not in self._client_data:
            return 0
        
        request_times, _ = self._client_data[client_id]
        if not request_times:
            return 0
        
        # Time until oldest request in window expires
        oldest_request = min(request_times)
        reset_time = oldest_request + 60 - time.time()
        
        return max(0, reset_time)

    async def _cleanup_if_needed(self) -> None:
        """Clean up old client data to prevent memory leaks."""
        current_time = time.time()
        
        if current_time - self._last_cleanup < self._cleanup_interval:
            return
        
        # Remove data for clients with no recent activity
        cutoff_time = current_time - 3600  # 1 hour
        
        clients_to_remove = []
        for client_id, (request_times, last_seen) in self._client_data.items():
            if last_seen < cutoff_time:
                clients_to_remove.append(client_id)
        
        for client_id in clients_to_remove:
            del self._client_data[client_id]
        
        self._last_cleanup = current_time
        
        if clients_to_remove:
            logger.debug(f"Cleaned up rate limit data for {len(clients_to_remove)} clients")


__all__ = ["RateLimitMiddleware"]
''',
    "security_consolidated.py": '''"""Consolidated security middleware."""
from __future__ import annotations

import logging
from typing import List, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware thêm các security headers quan trọng."""

    def __init__(
        self,
        app,
        enable_hsts: bool = True,
        enable_csp: bool = True,
        custom_csp: Optional[str] = None
    ):
        super().__init__(app)
        self.enable_hsts = enable_hsts
        self.enable_csp = enable_csp
        self.custom_csp = custom_csp

    async def dispatch(self, request: Request, call_next):
        """Add security headers to response."""
        response = await call_next(request)
        
        # Add security headers
        self._add_security_headers(response, request)
        
        return response

    def _add_security_headers(self, response: Response, request: Request) -> None:
        """Add comprehensive security headers."""
        # X-Content-Type-Options
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # X-Frame-Options
        response.headers["X-Frame-Options"] = "DENY"
        
        # X-XSS-Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), "
            "payment=(), usb=(), magnetometer=(), gyroscope=()"
        )
        
        # HSTS (HTTP Strict Transport Security)
        if self.enable_hsts and request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        # Content Security Policy
        if self.enable_csp:
            csp = self.custom_csp or self._get_default_csp()
            response.headers["Content-Security-Policy"] = csp

    def _get_default_csp(self) -> str:
        """Get default Content Security Policy."""
        return (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    """Middleware sanitize input data."""

    def __init__(self, app, max_content_length: int = 10 * 1024 * 1024):  # 10MB
        super().__init__(app)
        self.max_content_length = max_content_length

    async def dispatch(self, request: Request, call_next):
        """Sanitize and validate input data."""
        # Check content length
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_content_length:
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Request body too large. Maximum size: {self.max_content_length} bytes"
            )

        # Validate content type for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if content_type and not self._is_allowed_content_type(content_type):
                from fastapi import HTTPException, status
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail=f"Unsupported content type: {content_type}"
                )

        # Check for suspicious patterns in path
        if self._has_suspicious_patterns(request.url.path):
            logger.warning(f"Suspicious request path detected: {request.url.path}")
            from fastapi import HTTPException, status
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request path"
            )

        return await call_next(request)

    def _is_allowed_content_type(self, content_type: str) -> bool:
        """Check if content type is allowed."""
        allowed_types = [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "text/plain",
            "application/octet-stream"
        ]
        return any(content_type.startswith(allowed) for allowed in allowed_types)

    def _has_suspicious_patterns(self, path: str) -> bool:
        """Check for suspicious patterns in request path."""
        suspicious_patterns = [
            "../",
            "..\\\\",
            "/etc/",
            "/proc/",
            "/sys/",
            "cmd.exe",
            "powershell",
            "<script",
            "javascript:",
            "data:",
            "vbscript:"
        ]
        path_lower = path.lower()
        return any(pattern in path_lower for pattern in suspicious_patterns)


__all__ = ["SecurityHeadersMiddleware", "InputSanitizationMiddleware"]
''',
}

# Mapping files cần enhance với templates
FILES_TO_ENHANCE = {
    "zeta_vn/app/middleware/auth_middleware.py": "auth_middleware.py",
    "zeta_vn/app/middleware/compression_middleware.py": "compression_middleware.py",
    "zeta_vn/app/middleware/cors_middleware.py": "cors_middleware.py",
    "zeta_vn/app/middleware/performance_middleware.py": "performance_middleware.py",
    "zeta_vn/app/middleware/rate_limiting.py": "rate_limiting.py",
    "zeta_vn/app/middleware/security_consolidated.py": "security_consolidated.py",
}


def check_file_needs_enhancement(file_path: Path) -> bool:
    """Kiểm tra file có cần enhance không dựa trên content hiện tại."""
    if not file_path.exists():
        return True

    content = file_path.read_text(encoding="utf-8")

    # File empty hoặc chỉ có import/comment
    if len(content.strip()) < 100:
        return True

    # Kiểm tra có class implementation chưa
    if "class " not in content:
        return True

    # Kiểm tra có method implementation chưa
    if "def " not in content or "pass" in content or "NotImplementedError" in content:
        return True

    return False


def enhance_middleware_file(file_path: Path, template_key: str) -> bool:
    """Enhance một middleware file với template content."""
    if template_key not in MIDDLEWARE_TEMPLATES:
        print(f"❌ No template found for {template_key}")
        return False

    # Backup existing content if file exists and has content
    backup_content = ""
    if file_path.exists():
        existing_content = file_path.read_text(encoding="utf-8")
        if len(existing_content.strip()) > 50:
            backup_content = f"# Original content backed up:\\n'''{existing_content}'''\\n\\n"

    # Write enhanced content
    template_content = MIDDLEWARE_TEMPLATES[template_key]

    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write content
    enhanced_content = backup_content + template_content
    file_path.write_text(enhanced_content, encoding="utf-8")

    print(f"✅ Enhanced {file_path}")
    return True


def enhance_security_init():
    """Enhance security/__init__.py file."""
    security_init = Path("zeta_vn/app/middleware/security/__init__.py")

    enhanced_content = '''"""Security middleware components.

Comprehensive security middleware suite for ZETA_VN application.
Includes authentication, authorization, headers, and input validation.
"""
from __future__ import annotations

from .auth_middleware import AuthenticationMiddleware
from .security_headers import SecurityHeadersMiddleware
from .input_validation import InputValidationMiddleware
from .zero_trust import ZeroTrustMiddleware

__all__ = [
    "AuthenticationMiddleware",
    "SecurityHeadersMiddleware",
    "InputValidationMiddleware",
    "ZeroTrustMiddleware",
]
'''

    security_init.parent.mkdir(parents=True, exist_ok=True)
    security_init.write_text(enhanced_content, encoding="utf-8")
    print(f"✅ Enhanced {security_init}")


def main() -> int:
    """Main enhancement function."""
    print("🔧 MIDDLEWARE ENHANCEMENT SCRIPT")
    print("=" * 50)

    enhanced_count = 0

    # Enhance main middleware files
    for file_path_str, template_key in FILES_TO_ENHANCE.items():
        file_path = Path(file_path_str)

        if check_file_needs_enhancement(file_path):
            if enhance_middleware_file(file_path, template_key):
                enhanced_count += 1
        else:
            print(f"✓ {file_path} already has good implementation")

    # Enhance security __init__.py
    enhance_security_init()
    enhanced_count += 1

    # Update main middleware __init__.py
    main_init = Path("zeta_vn/app/middleware/__init__.py")
    if main_init.exists():
        # Read existing content
        existing = main_init.read_text(encoding="utf-8")

        # Add imports if not present
        imports_to_add = [
            "from .auth_middleware import AuthenticationMiddleware",
            "from .compression_middleware import CompressionMiddleware",
            "from .cors_middleware import CORSMiddleware",
            "from .performance_middleware import PerformanceMiddleware",
            "from .rate_limiting import RateLimitMiddleware",
            "from .security_consolidated import SecurityHeadersMiddleware, InputSanitizationMiddleware",
        ]

        # Update __all__ if exists
        updated_content = existing
        for imp in imports_to_add:
            if imp not in updated_content:
                updated_content = imp + "\\n" + updated_content

        main_init.write_text(updated_content, encoding="utf-8")
        print(f"✅ Updated {main_init}")
        enhanced_count += 1

    print("\n📊 ENHANCEMENT COMPLETE")
    print(f"   Enhanced files: {enhanced_count}")
    print("   ✅ Ready for completeness re-analysis")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
