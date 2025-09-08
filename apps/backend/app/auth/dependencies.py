"""FastAPI middleware và dependencies cho hệ thống phân quyền ZETA.

Module này cung cấp:
- Middleware để build SecurityContext tự động từ request
- Dependencies để kiểm tra permissions trong endpoints
- Helper functions để tích hợp với FastAPI
"""

from __future__ import annotations

import logging
from typing import Annotated, Any

from apps.backend.core.security.audit import audit_permission_check
from apps.backend.core.security.context import (
import Exception
import action_name
import action_risk
import context
import dict
import e
import permission_name
import permission_names
import request
import resource_id
import resource_type
import str
import token
import user
import user_agent
    Action,
    Environment,
    Resource,
    SecurityContext,
    Subject,
)
from apps.backend.core.security.permission_manager import PermissionManager
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

logger = logging.getLogger(__name__)

# Security scheme cho JWT tokens
security = HTTPBearer()


def get_current_user(
    request: Request, token: str = Depends(security)
) -> dict[str, Any]:
    """Extract user từ JWT token.

    Args:
        request: FastAPI request
        token: JWT token từ Authorization header

    Returns:
        User information dict

    Raises:
        HTTPException: Nếu token không hợp lệ
    """
    # NOTE: Mock implementation - replace với JWT validation thực tế
    # Sẽ integrate với existing auth system sau
    if not token.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Mock user - thay thế bằng JWT validation thực tế
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
    request_id = request.headers.get("x-request-id", "unknown")

    # Build SecurityContext
    subject = Subject(
        user_id=user["user_id"],
        tenant_id=user["tenant_id"],
        roles=user["roles"],
    )

    # Resource sẽ được set cụ thể trong từng endpoint
    resource = Resource(
        type="api",
        id=str(request.url.path),
        sensitivity="low",
    )

    # Action sẽ được set cụ thể trong từng endpoint
    action = Action(
        name=request.method.lower(),
        risk="low",
    )

    environment = Environment(
        ip=client_ip,
        user_agent=user_agent,
        time_of_day=None,  # Will be set by policy engine
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
    resource_type: str = "api",
    resource_id: str | None = None,
    action_name: str | None = None,
    action_risk: str = "low",
) -> Any:
    """Dependency factory để require permission cụ thể.

    Args:
        permission_name: Tên permission cần kiểm tra
        resource_type: Loại resource (default: "api")
        resource_id: ID của resource (default: None)
        action_name: Tên action (default: None, sẽ dùng HTTP method)
        action_risk: Risk level của action (default: "low")

    Returns:
        FastAPI dependency function

    Usage:
        @router.get("/users")
        async def list_users(
            security_ctx: SecurityContext = Depends(require_permission("users.read"))
        ):
            # Endpoint code here
    """

    async def permission_dependency(
        request: Request,
        context: SecurityContext = Depends(get_security_context),
    ) -> SecurityContext:
        """Check permission và return SecurityContext nếu được phép."""
        # Cập nhật context với thông tin cụ thể
        if resource_id:
            context.resource.id = resource_id
        context.resource.type = resource_type

        if action_name:
            context.action.name = action_name
        else:
            context.action.name = request.method.lower()
        context.action.risk = action_risk

        # Kiểm tra permission
        permission_manager = PermissionManager()

        try:
            is_allowed = await permission_manager.check_permission_async(
                context, permission_name
            )

            if not is_allowed:
                # Audit log đã được ghi trong permission_manager
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission_name}",
                )

            return context

        except Exception as e:
            logger.error(f"Permission check failed: {e}")
            # Audit log cho lỗi system
            audit_permission_check(
                context, False, f"System error during permission check: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Permission check failed",
            )

    return permission_dependency


def require_any_permission(*permission_names: str) -> Any:
    """Dependency factory để require ít nhất một trong các permissions.

    Args:
        *permission_names: Danh sách tên permissions

    Returns:
        FastAPI dependency function

    Usage:
        @router.get("/admin")
        async def admin_endpoint(
            ctx: SecurityContext = Depends(require_any_permission("admin.read", "admin.write"))
        ):
            # Endpoint code here
    """

    async def any_permission_dependency(
        request: Request,
        context: SecurityContext = Depends(get_security_context),
    ) -> SecurityContext:
        """Check ít nhất một permission và return SecurityContext nếu được phép."""
        permission_manager = PermissionManager()

        for permission_name in permission_names:
            try:
                is_allowed = await permission_manager.check_permission_async(
                    context, permission_name
                )

                if is_allowed:
                    return context

            except Exception as e:
                logger.error(f"Permission check failed for {permission_name}: {e}")
                continue

        # Không có permission nào được phép
        audit_permission_check(
            context, False, f"None of required permissions granted: {permission_names}"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"At least one of these permissions required: {permission_names}",
        )

    return any_permission_dependency


def require_all_permissions(*permission_names: str) -> Any:
    """Dependency factory để require tất cả permissions.

    Args:
        *permission_names: Danh sách tên permissions

    Returns:
        FastAPI dependency function

    Usage:
        @router.delete("/admin/users/{user_id}")
        async def delete_user(
            ctx: SecurityContext = Depends(require_all_permissions("admin.write", "users.delete"))
        ):
            # Endpoint code here
    """

    async def all_permissions_dependency(
        request: Request,
        context: SecurityContext = Depends(get_security_context),
    ) -> SecurityContext:
        """Check tất cả permissions và return SecurityContext nếu được phép."""
        permission_manager = PermissionManager()

        for permission_name in permission_names:
            try:
                is_allowed = await permission_manager.check_permission_async(
                    context, permission_name
                )

                if not is_allowed:
                    audit_permission_check(
                        context,
                        False,
                        f"Missing required permission: {permission_name}",
                    )

                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Permission denied: {permission_name}",
                    )

            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Permission check failed for {permission_name}: {e}")
                audit_permission_check(
                    context, False, f"System error checking {permission_name}: {str(e)}"
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Permission check failed",
                )

        return context

    return all_permissions_dependency


# Convenience type annotations
SecurityContextDep = Annotated[SecurityContext, Depends(get_security_context)]
CurrentUserDep = Annotated[dict[str, Any], Depends(get_current_user)]
