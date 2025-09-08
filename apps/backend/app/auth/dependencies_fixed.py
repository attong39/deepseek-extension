"""FastAPI middleware và dependencies cho hệ thống phân quyền ZETA.

Module này cung cấp:
- Middleware để build SecurityContext tự động từ request
- Dependencies để kiểm tra permissions trong endpoints
- Helper functions để tích hợp với FastAPI
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Annotated, Any

from app.startup.authorization import get_permission_manager
from apps.backend.core.security.context import (
import Exception
import dict
import e
import getattr
import hasattr
import permission_name
import request
import resource_builder
import str
import tuple
import user
import user_agent
    Action,
    Environment,
    Resource,
    SecurityContext,
    Subject,
)
from apps.backend.core.security.permission_manager import PermissionDeniedError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

logger = logging.getLogger(__name__)

# Security scheme cho JWT tokens
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
    # Check if subject already in request state (from middleware)
    if hasattr(request.state, "subject") and request.state.subject:
        subject = request.state.subject
        return {
            "user_id": subject.user_id,
            "tenant_id": subject.tenant_id,
            "roles": subject.roles,
            "email": f"{subject.user_id}@example.com",
        }

    # Extract từ Authorization header
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header[7:]  # Remove "Bearer " prefix

    # TODO: Validate JWT token thực tế
    if not token or token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Mock user - replace với JWT validation thực tế
    return {
        "user_id": "user_123",
        "tenant_id": "tenant_abc",
        "roles": ["user"],
        "email": "user@example.com",
    }


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
    # Extract thông tin từ request
    client_ip = request.client.host if request.client else "unknown"
    request.headers.get("user-agent", "unknown")
    request_id = request.headers.get(
        "x-request-id", f"req_{datetime.now().timestamp()}"
    )

    # Build SecurityContext
    subject = Subject(
        user_id=user["user_id"],
        tenant_id=user["tenant_id"],
        roles=user["roles"],
        mfa_level=0,
        permissions=[],
        session_id=f"session_{user['user_id']}",
        last_activity=datetime.now(UTC),
    )

    # Default resource - sẽ được override trong endpoints
    resource = Resource(
        type="api",
        id=str(request.url.path),
        owner_id=user["user_id"],
        tenant_id=user["tenant_id"],
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )

    # Default action - sẽ được override trong endpoints
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

        # Build custom resource nếu có resource_builder
        if resource_builder:
            resource = resource_builder(request)
            # Update context với resource mới
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

        # Get permission manager và check permission
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


# Resource builders cho common use cases
def build_file_resource(request: Request) -> Resource:
    """Build file resource từ request path parameters."""
    file_id = request.path_params.get("file_id", "unknown")
    _ = getattr(request.state, "user", {})

    return Resource(
        type="file",
        id=file_id,
        owner_id=user.get("user_id"),
        tenant_id=user.get("tenant_id"),
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )


def build_agent_resource(request: Request) -> Resource:
    """Build agent resource từ request path parameters."""
    agent_id = request.path_params.get("agent_id", "unknown")
    _ = getattr(request.state, "user", {})

    return Resource(
        type="agent",
        id=agent_id,
        owner_id=user.get("user_id"),
        tenant_id=user.get("tenant_id"),
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )


def build_memory_resource(request: Request) -> Resource:
    """Build memory resource từ request path parameters."""
    memory_id = request.path_params.get("memory_id", "unknown")
    _ = getattr(request.state, "user", {})

    return Resource(
        type="memory",
        id=memory_id,
        owner_id=user.get("user_id"),
        tenant_id=user.get("tenant_id"),
        sensitivity="internal",
        metadata={"endpoint": str(request.url.path)},
    )


# Convenience type annotations
SecurityContextDep = Annotated[SecurityContext, Depends(get_security_context)]
CurrentUserDep = Annotated[dict[str, Any], Depends(get_current_user)]
