"""Ví dụ API router sử dụng hệ thống phân quyền ZETA.

Router này demo cách tích hợp permission checks vào FastAPI endpoints.
"""

from __future__ import annotations

from typing import Any

from app.auth.dependencies import (
import current_user
import dict
import len
import list
import operation_data
import profile_data
import security_ctx
import str
import user_data
import user_id
import user_ids
    CurrentUserDep,
    SecurityContextDep,
    require_all_permissions,
    require_any_permission,
    require_permission,
)
from apps.backend.core.security.context import SecurityContext
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/")
async def list_users(
    security_ctx: SecurityContext = Depends(require_permission("users.read")),
) -> dict[str, Any]:
    """List tất cả users - cần permission users.read."""
    return {
        "users": [
            {"id": "1", "name": "User 1"},
            {"id": "2", "name": "User 2"},
        ],
        "checked_permission": "users.read",
        "user_id": security_ctx.subject.user_id,
    }


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    security_ctx: SecurityContext = Depends(
        require_permission("users.read", resource_type="user", action_name="read")
    ),
) -> dict[str, Any]:
    """Get user cụ thể - cần permission users.read trên resource type 'user'."""
    # Cập nhật resource_id với user_id thực tế
    security_ctx.resource.id = user_id

    return {
        "user": {"id": user_id, "name": f"User {user_id}"},
        "checked_permission": "users.read",
        "resource_id": user_id,
        "checker_user_id": security_ctx.subject.user_id,
    }


@router.post("/")
async def create_user(
    user_data: dict[str, Any],
    security_ctx: SecurityContext = Depends(
        require_permission(
            "users.create",
            resource_type="user",
            action_name="create",
            action_risk="medium",
        )
    ),
) -> dict[str, Any]:
    """Tạo user mới - cần permission users.create với risk medium."""
    return {
        "message": "User created successfully",
        "user_data": user_data,
        "checked_permission": "users.create",
        "action_risk": "medium",
        "creator_user_id": security_ctx.subject.user_id,
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    security_ctx: SecurityContext = Depends(
        require_permission(
            "users.delete",
            resource_type="user",
            action_name="delete",
            action_risk="high",
        )
    ),
) -> dict[str, Any]:
    """Xóa user - cần permission users.delete với risk high."""
    # Cập nhật resource_id với user_id thực tế
    security_ctx.resource.id = user_id

    return {
        "message": f"User {user_id} deleted successfully",
        "checked_permission": "users.delete",
        "action_risk": "high",
        "resource_id": user_id,
        "deleter_user_id": security_ctx.subject.user_id,
    }


@router.get("/admin/dashboard")
async def admin_dashboard(
    security_ctx: SecurityContext = Depends(
        require_any_permission("admin.read", "users.admin")
    ),
) -> dict[str, Any]:
    """Admin dashboard - cần ít nhất một trong các admin permissions."""
    return {
        "dashboard_data": {"total_users": 100, "active_users": 80},
        "required_permissions": ["admin.read", "users.admin"],
        "admin_user_id": security_ctx.subject.user_id,
    }


@router.post("/admin/bulk-delete")
async def bulk_delete_users(
    user_ids: list[str],
    security_ctx: SecurityContext = Depends(
        require_all_permissions("admin.write", "users.delete", "bulk.operations")
    ),
) -> dict[str, Any]:
    """Bulk delete users - cần tất cả admin permissions."""
    return {
        "message": f"Deleted {len(user_ids)} users",
        "user_ids": user_ids,
        "required_permissions": ["admin.write", "users.delete", "bulk.operations"],
        "admin_user_id": security_ctx.subject.user_id,
    }


@router.get("/profile")
async def get_own_profile(
    current_user: CurrentUserDep,
    security_ctx: SecurityContextDep,
) -> dict[str, Any]:
    """Get profile của chính user hiện tại - chỉ cần authenticated."""
    return {
        "profile": current_user,
        "security_context": {
            "user_id": security_ctx.subject.user_id,
            "tenant_id": security_ctx.subject.tenant_id,
            "roles": security_ctx.subject.roles,
            "ip": security_ctx.environment.ip,
        },
    }


@router.put("/profile")
async def update_own_profile(
    profile_data: dict[str, Any],
    security_ctx: SecurityContext = Depends(
        require_permission(
            "profile.update", resource_type="profile", action_name="update"
        )
    ),
) -> dict[str, Any]:
    """Update profile của chính user hiện tại."""
    # Resource ID là chính user_id của người request
    security_ctx.resource.id = security_ctx.subject.user_id

    return {
        "message": "Profile updated successfully",
        "profile_data": profile_data,
        "checked_permission": "profile.update",
        "user_id": security_ctx.subject.user_id,
    }


# Endpoint demo lỗi permission
@router.get("/forbidden-endpoint")
async def forbidden_endpoint(
    security_ctx: SecurityContext = Depends(
        require_permission("super.admin.nuclear.codes")
    ),
) -> dict[str, Any]:
    """Endpoint này sẽ luôn bị forbidden vì permission không tồn tại."""
    return {"message": "You should never see this"}


# Endpoint demo multiple checks
@router.post("/complex-operation")
async def complex_operation(
    operation_data: dict[str, Any],
    security_ctx: SecurityContext = Depends(
        require_all_permissions(
            "complex.operations.execute", "data.modify", "audit.log"
        )
    ),
) -> dict[str, Any]:
    """Demo operation phức tạp cần nhiều permissions."""

    # Có thể thực hiện additional permission checks trong endpoint
    if operation_data.get("is_critical", False):
        # Dynamic permission check cho critical operations
        from apps.backend.core.security.permission_manager import PermissionManager

        permission_manager = PermissionManager()
        critical_allowed = await permission_manager.check_permission_async(
            security_ctx, "critical.operations.approve"
        )

        if not critical_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Critical operations require additional approval",
            )

    return {
        "message": "Complex operation completed",
        "operation_data": operation_data,
        "required_permissions": [
            "complex.operations.execute",
            "data.modify",
            "audit.log",
        ],
        "additional_checks": operation_data.get("is_critical", False),
        "executor_user_id": security_ctx.subject.user_id,
    }
