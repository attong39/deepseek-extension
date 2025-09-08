from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Annotated, Any

from app.auth.jwt_dependencies import jwt_bearer
from app.startup.authorization import get_permission_manager
from apps.backend.core.security.context import (
import Exception
import dict
import e
import getattr
import hasattr
import permission_name
import request
import required_role
import resource_builder
import str
import tenant_id_param
import tuple
import user
    Action,
    Environment,
    Resource,
    SecurityContext,
    Subject,
)
from apps.backend.core.security.permission_manager import PermissionDeniedError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

"""FastAPI middleware và dependencies cho hệ thống phân quyền ZETA.
Module này cung cấp:
- Middleware để build SecurityContext tự động từ request
- Dependencies để kiểm tra permissions trong endpoints
- Helper functions để tích hợp với FastAPI
- RBAC (Role-Based Access Control) functions
"""
logger = logging.getLogger(__name__)
security = HTTPBearer()


def get_current_user(request: Request) -> dict[str, Any]:
    """Extract user từ JWT token hoặc request state.
    Args:
        request: FastAPI request
    Returns:
        User information dict
    Raises:
        HTTPException: Nếu không có authentication
    """
    if hasattr(request.state, "subject") and request.state.subject:
        subject = request.state.subject
        return {
            "user_id": subject.user_id,
            "tenant_id": subject.tenant_id,
            "roles": subject.roles,
            "email": f"{subject.user_id}@example.com",
        }
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header[7:]  # Remove "Bearer " prefix
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        payload = loop.run_until_complete(jwt_bearer.decode_async(token))
        loop.close()
        return {
            "user_id": payload.get("sub"),
            "tenant_id": payload.get("tenant_id", "default"),
            "roles": payload.get("roles", ["user"]),
            "email": payload.get("email", f"{payload.get('sub')}@example.com"),
        }
    except Exception as e:
        logger.error("JWT validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_security_context(
    request: Request,
    user: dict[str, Any] = Depends(get_current_user),
) -> SecurityContext:
    """Build SecurityContext từ request và user info.
    Args:
        request: FastAPI request object
        user: User information từ get_current_user
    Returns:
        SecurityContext đầy đủ để kiểm tra permissions
    """
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    request_id = request.headers.get(
        "x-request-id", f"req_{datetime.now().timestamp()}"
    )
    subject = Subject(
        user_id=user["user_id"],
        tenant_id=user["tenant_id"],
        roles=user["roles"],
        mfa_level=0,
        permissions=[],
        session_id=f"session_{user['user_id']}",
        last_activity=datetime.now(UTC),
    )
    resource = Resource(
        type="api",
        id=str(request.url.path),
        owner_id=user["user_id"],
        tenant_id=user["tenant_id"],
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )
    action = Action(
        name=request.method.lower(),
        risk="low",
        requires_mfa=False,
        rate_limit_key=f"api:{client_ip}",
    )
    environment = Environment(
        ip=client_ip,
        user_agent=user_agent,
        time_of_day=datetime.now().hour,
        device_trust="high",
        location=None,
        is_vpn=False,
        request_id=request_id,
    )
    return SecurityContext(
        subject=subject,
        resource=resource,
        action=action,
        environment=environment,
    )


def require_permission(
    permission_name: str,
    resource_builder=None,
) -> Any:
    """Dependency factory để require permission cụ thể.
    Args:
        permission_name: Tên permission cần kiểm tra
        resource_builder: Function để build Resource từ request (optional)
    Returns:
        FastAPI dependency function
    Usage:
        @router.get("/files/{file_id}")
        def get_file(
            file_id: str,
            auth_data = Depends(require_permission("files:read", build_file_resource))
        ):
            context, resource = auth_data
    """

    def permission_dependency(
        request: Request,
        context: SecurityContext = Depends(get_security_context),
    ) -> tuple[SecurityContext, Resource]:
        """Check permission và return SecurityContext + Resource nếu được phép."""
        if resource_builder:
            resource = resource_builder(request)
            context = SecurityContext(
                subject=context.subject,
                action=Action(
                    name=permission_name,
                    risk="low",  # Will be looked up in permissions
                    requires_mfa=False,
                    rate_limit_key=f"api:{context.environment.ip}:{permission_name}",
                ),
                resource=resource,
                environment=context.environment,
            )
        else:
            resource = context.resource
        permission_manager = get_permission_manager()
        try:
            permission_manager.ensure_permission(context, permission_name)
            return context, resource
        except PermissionDeniedError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )
        except Exception as e:
            logger.error(f"Permission check failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Permission check failed",
            )

    return permission_dependency


def build_file_resource(request: Request) -> Resource:
    """Build file resource từ request path parameters."""
    file_id = request.path_params.get("file_id", "unknown")
    subject = getattr(request.state, "subject", None)
    return Resource(
        type="file",
        id=file_id,
        owner_id=getattr(subject, "user_id", None),
        tenant_id=getattr(subject, "tenant_id", None),
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )


def build_agent_resource(request: Request) -> Resource:
    """Build agent resource từ request path parameters."""
    agent_id = request.path_params.get("agent_id", "unknown")
    subject = getattr(request.state, "subject", None)
    return Resource(
        type="agent",
        id=agent_id,
        owner_id=getattr(subject, "user_id", None),
        tenant_id=getattr(subject, "tenant_id", None),
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )


def build_memory_resource(request: Request) -> Resource:
    """Build memory resource từ request path parameters."""
    memory_id = request.path_params.get("memory_id", "unknown")
    subject = getattr(request.state, "subject", None)
    return Resource(
        type="memory",
        id=memory_id,
        owner_id=getattr(subject, "user_id", None),
        tenant_id=getattr(subject, "tenant_id", None),
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )


SecurityContextDep = Annotated[SecurityContext, Depends(get_security_context)]
CurrentUserDep = Annotated[dict[str, Any], Depends(get_current_user)]


def require_admin(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
    """Dependency để require admin role.
    Args:
        user: User information từ get_current_user
    Returns:
        User dict nếu có admin role
    Raises:
        HTTPException: Nếu không có admin role
    """
    if "admin" not in user.get("roles", []):
        logger.warning(
            "Access denied - admin role required", user_id=user.get("user_id")
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return user


def require_role(required_role: str):
    """Factory function để tạo dependency require specific role.
    Args:
        required_role: Role name cần thiết
    Returns:
        FastAPI dependency function
    """

    def role_dependency(
        user: dict[str, Any] = Depends(get_current_user),
    ) -> dict[str, Any]:
        """Check user có required role.
        Args:
            user: User information
        Returns:
            User dict nếu có role
        Raises:
            HTTPException: Nếu không có role
        """
        if required_role not in user.get("roles", []):
            logger.warning(
                "Access denied - role required",
                user_id=user.get("user_id"),
                required_role=required_role,
                user_roles=user.get("roles", []),
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required",
            )
        return user

    return role_dependency


def require_tenant_access(tenant_id_param: str = None):
    """Factory function để tạo dependency kiểm tra tenant access.
    Args:
        tenant_id_param: Tên parameter chứa tenant_id (optional)
    Returns:
        FastAPI dependency function
    """

    def tenant_dependency(
        request: Request, user: dict[str, Any] = Depends(get_current_user)
    ) -> dict[str, Any]:
        """Check user có quyền truy cập tenant.
        Args:
            request: FastAPI request
            user: User information
        Returns:
            User dict nếu có quyền
        Raises:
            HTTPException: Nếu không có quyền
        """
        user_tenant = user.get("tenant_id")
        required_tenant = None
        if tenant_id_param:
            required_tenant = request.path_params.get(tenant_id_param)
        else:
            required_tenant = getattr(
                request.state, "tenant_id", None
            ) or request.headers.get("x-tenant-id")
        if required_tenant and user_tenant != required_tenant:
            if "multi_tenant" not in user.get("roles", []):
                logger.warning(
                    "Access denied - tenant mismatch",
                    user_id=user.get("user_id"),
                    user_tenant=user_tenant,
                    required_tenant=required_tenant,
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied for this tenant",
                )
        return user

    return tenant_dependency


AdminDep = Annotated[dict[str, Any], Depends(require_admin)]
UserDep = Annotated[dict[str, Any], Depends(require_role("user"))]
__all__ = [
    "AdminDep",
    "CurrentUserDep",
    "SecurityContextDep",
    "UserDep",
    "get_current_user",
    "get_security_context",
    "logger",
    "require_admin",
    "require_permission",
    "require_role",
    "require_tenant_access",
    "security",
]
