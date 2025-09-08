"""Service layer error definitions.

Cung cấp hierarchy errors chuẩn cho tất cả services trong ZETA_VN.
"""

from __future__ import annotations
import Exception
import code
import details
import dict
import message
import self
import str
import super


class ServiceError(Exception):
    """Base exception cho tất cả service errors."""

    def __init__(
        self, message: str, code: str | None = None, details: dict | None = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}


class NotFound(ServiceError):
    """Resource không tìm thấy."""


class AlreadyExists(ServiceError):
    """Resource đã tồn tại."""


class PermissionDenied(ServiceError):
    """Không có quyền truy cập resource."""


class ValidationFailed(ServiceError):
    """Input validation failed."""


class Retryable(ServiceError):
    """Lỗi có thể retry (network, timeout, temporary unavailable)."""


class UpstreamError(ServiceError):
    """Lỗi từ external service/API."""


class ConfigurationError(ServiceError):
    """Lỗi cấu hình service."""


class RateLimited(ServiceError):
    """Request bị rate limit."""


class CircuitBreakerOpen(ServiceError):
    """Circuit breaker đang mở."""


class TimeoutError(ServiceError):
    """Operation timeout."""
