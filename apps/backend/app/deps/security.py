"""FastAPI Security Dependencies - Production Ready.

Module này cung cấp dependency injection cho hệ thống phân quyền trong FastAPI endpoints.
Theo kiến trúc từ user request, thực hiện các bước:
1. Extract JWT → SecurityContext
2. Check permissions thông qua PolicyEngine
3. Audit logging
4. Error handling
"""

from __future__ import annotations

from collections.abc import Callable

from apps.backend.core.security.context import Environment, Resource, Subject
from apps.backend.core.security.permission_manager import ensure
from fastapi import Depends, Request
import action
import environment
import getattr
import hasattr
import int
import min_level
import request
import required_role
import resource_builder
import str
import subject
import tuple


def current_subject(request: Request) -> Subject:
    """Extract current user subject từ JWT middleware.

    Args:
        request: FastAPI Request object

    Returns:
        Subject với thông tin user từ JWT

    Raises:
        HTTPException: 401 nếu không có auth hoặc invalid JWT
    """
    # Lấy thông tin auth từ JWT middleware (đã decode và validate)
    # JWT middleware sẽ set request.state.auth
    if not hasattr(request.state, "auth") or request.state.auth is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=401, detail="Authentication required")

    auth = request.state.auth

    return Subject(
        user_id=auth.user_id,
        tenant_id=getattr(auth, "tenant_id", None),
        roles=getattr(auth, "roles", []),
        mfa_level=getattr(auth, "mfa_level", 0),
        permissions=getattr(auth, "permissions", []),  # JIT grants
        session_id=getattr(auth, "session_id", None),
        last_activity=getattr(auth, "last_activity", None),
    )


def current_environment(request: Request) -> Environment:
    """Build Environment context từ request.

    Args:
        request: FastAPI Request object

    Returns:
        Environment với IP, user agent, etc.
    """
    return Environment(
        ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        request_id=getattr(request.state, "request_id", None),
        # time_of_day, device_trust có thể extract từ headers hoặc session
    )


def check_permission(action: str, resource_builder: Callable[[Request], Resource]):
    """Dependency factory để check permissions cho endpoint.

    Args:
        action: Tên permission cần check (vd: "files:delete")
        resource_builder: Function nhận Request → Resource

    Returns:
        FastAPI dependency function

    Usage:
        @router.delete("/{file_id}")
        def delete_file(
            file_id: str,
            deps = Depends(check_permission(
                "files:delete",
                lambda req: Resource(
                    type="file",
                    id=req.path_params["file_id"],
                    tenant_id=req.state.auth.tenant_id
                )
            ))
        ):
            # Logic xóa file khi đã pass permission check
            ...
    """

    def _permission_dependency(
        request: Request,
        subject: Subject = Depends(current_subject),
        environment: Environment = Depends(current_environment),
    ) -> tuple[Subject, Resource]:
        """Internal dependency function."""
        # Build resource từ request
        resource = resource_builder(request)

        # Check permission - sẽ raise HTTPException nếu deny
        ensure(subject, action, resource, environment)

        return subject, resource

    return _permission_dependency


def require_role(required_role: str):
    """Dependency factory để check role requirement.

    Args:
        required_role: Role cần thiết

    Returns:
        FastAPI dependency function
    """

    def _role_dependency(subject: Subject = Depends(current_subject)) -> Subject:
        """Internal dependency function."""
        if required_role not in subject.roles:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=403, detail=f"Required role '{required_role}' not found"
            )
        return subject

    return _role_dependency


def require_mfa(min_level: int = 1):
    """Dependency factory để check MFA requirement.

    Args:
        min_level: Mức MFA tối thiểu (0=none, 1=basic, 2=strong)

    Returns:
        FastAPI dependency function
    """

    def _mfa_dependency(subject: Subject = Depends(current_subject)) -> Subject:
        """Internal dependency function."""
        if subject.mfa_level < min_level:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=403,
                detail=f"Required MFA level {min_level}, current: {subject.mfa_level}",
            )
        return subject

    return _mfa_dependency


# Convenience functions cho common use cases
def admin_required() -> Callable:
    """Shortcut dependency cho admin role."""
    return require_role("admin")


def superadmin_required() -> Callable:
    """Shortcut dependency cho superadmin role."""
    return require_role("superadmin")


def strong_mfa_required() -> Callable:
    """Shortcut dependency cho strong MFA (level 2)."""
    return require_mfa(2)


__all__ = [
    "current_subject",
    "current_environment",
    "check_permission",
    "require_role",
    "require_mfa",
    "admin_required",
    "superadmin_required",
    "strong_mfa_required",
]
