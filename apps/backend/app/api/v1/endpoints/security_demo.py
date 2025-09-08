"""Security Demo Endpoints - Production Ready Examples.

Module này cung cấp ví dụ sử dụng hệ thống phân quyền trong FastAPI endpoints.
Minh họa các pattern phổ biến của RBAC/ABAC/Policy-based authorization.
"""

from __future__ import annotations

from typing import Any

from app.deps.security import (
import action
import admin_subject
import agent_id
import deps
import dict
import file_id
import int
import list
import req
import resource
import resource_type
import str
import subject
import user_id
    admin_required,
    check_permission,
    current_subject,
    require_mfa,
    strong_mfa_required,
)
from apps.backend.core.security.context import Resource, Subject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/security-demo", tags=["Security Demo"])


class FileResponse(BaseModel):
    """Response model cho file operations."""

    id: str
    name: str
    type: str
    owner_id: str
    tenant_id: str
    sensitivity: str


class UserResponse(BaseModel):
    """Response model cho user info."""

    user_id: str
    roles: list[str]
    tenant_id: str | None
    mfa_level: int


@router.get("/whoami")
def get_current_user_info(
    subject: Subject = Depends(current_subject),
) -> UserResponse:
    """Get thông tin user hiện tại từ JWT.

    Endpoint này không cần permission check đặc biệt,
    chỉ cần authentication (JWT valid).
    """
    return UserResponse(
        user_id=subject.user_id,
        roles=subject.roles,
        tenant_id=subject.tenant_id,
        mfa_level=subject.mfa_level,
    )


@router.get("/files/{file_id}")
def read_file(
    file_id: str,
    deps=Depends(
        check_permission(
            "files:read",
            lambda req: Resource(
                type="file",
                id=req.path_params["file_id"],
                # Tenant sẽ được extract từ JWT trong thực tế
                tenant_id=req.state.auth.tenant_id if req.state.auth else None,
                sensitivity="internal",  # Sẽ query từ DB trong thực tế
            ),
        )
    ),
) -> FileResponse:
    """Read file với permission check.

    Permission: files:read
    ABAC: kiểm tra tenant_id matching
    """
    subject, resource = deps

    # Simulate file data
    return FileResponse(
        id=file_id,
        name=f"file_{file_id}.txt",
        type="file",
        owner_id="user123",
        tenant_id=resource.tenant_id or "default",
        sensitivity=resource.sensitivity,
    )


@router.delete("/files/{file_id}")
def delete_file(
    file_id: str,
    deps=Depends(
        check_permission(
            "files:delete",
            lambda req: Resource(
                type="file",
                id=req.path_params["file_id"],
                tenant_id=req.state.auth.tenant_id if req.state.auth else None,
                owner_id="user123",  # Sẽ query từ DB
                sensitivity="restricted",  # High-risk file
            ),
        )
    ),
) -> dict[str, str]:
    """Delete file với high-risk permission check.

    Permission: files:delete (high risk)
    ABAC: kiểm tra ownership + tenant
    Safety: blocked nếu sensitivity=restricted và không có JIT grant
    """
    subject, resource = deps

    # Logic xóa file ở đây
    return {
        "message": f"File {file_id} deleted successfully",
        "deleted_by": subject.user_id,
    }


@router.post("/admin/users/{user_id}/disable")
def disable_user(
    user_id: str,
    admin_subject: Subject = Depends(admin_required()),
) -> dict[str, str]:
    """Disable user - chỉ admin mới được phép.

    Role-based: admin role required
    """
    # Logic disable user
    return {
        "message": f"User {user_id} disabled",
        "disabled_by": admin_subject.user_id,
    }


@router.post("/system/backup")
def create_system_backup(
    subject: Subject = Depends(strong_mfa_required()),
    deps=Depends(
        check_permission(
            "system:backup:create",
            lambda req: Resource(
                type="system",
                id="backup",
                sensitivity="secret",
            ),
        )
    ),
) -> dict[str, str]:
    """Create system backup - cần strong MFA + high permission.

    Permission: system:backup:create (high risk)
    MFA: level 2 required
    """
    subject, resource = deps

    return {
        "message": "System backup created",
        "backup_id": "backup_123",
        "created_by": subject.user_id,
    }


@router.get("/sensitive-data")
def read_sensitive_data(
    subject: Subject = Depends(require_mfa(min_level=1)),
    deps=Depends(
        check_permission(
            "system:audit:read",
            lambda req: Resource(
                type="audit_logs",
                sensitivity="restricted",
            ),
        )
    ),
) -> dict[str, Any]:
    """Read sensitive audit data.

    Permission: system:audit:read
    MFA: basic MFA required
    ABAC: sensitivity=restricted
    """
    subject, resource = deps

    return {
        "data": [
            {"event": "login", "user": "user1", "time": "2025-01-01T00:00:00Z"},
            {"event": "file_delete", "user": "user2", "time": "2025-01-01T01:00:00Z"},
        ],
        "accessed_by": subject.user_id,
        "access_time": "2025-01-01T12:00:00Z",
    }


@router.post("/agents/{agent_id}/run")
def run_agent(
    agent_id: str,
    deps=Depends(
        check_permission(
            "agent:run",
            lambda req: Resource(
                type="agent",
                id=req.path_params["agent_id"],
                tenant_id=req.state.auth.tenant_id if req.state.auth else None,
                sensitivity="internal",
            ),
        )
    ),
) -> dict[str, str]:
    """Run AI agent với permission check.

    Permission: agent:run (high risk)
    Có thể yêu cầu JIT grant tùy thuộc vào risk level
    """
    subject, resource = deps

    return {
        "message": f"Agent {agent_id} started",
        "status": "running",
        "started_by": subject.user_id,
    }


@router.get("/permissions/check")
def check_user_permissions(
    action: str,
    resource_type: str,
    subject: Subject = Depends(current_subject),
) -> dict[str, Any]:
    """Utility endpoint để check permissions của user hiện tại.

    Useful cho frontend để ẩn/hiện buttons, menus based on permissions.
    """
    from apps.backend.core.security.permission_manager import can_user_perform

    allowed = can_user_perform(
        user_id=subject.user_id,
        roles=subject.roles,
        action=action,
        resource_type=resource_type,
        tenant_id=subject.tenant_id,
    )

    return {
        "user_id": subject.user_id,
        "action": action,
        "resource_type": resource_type,
        "allowed": allowed,
        "roles": subject.roles,
        "mfa_level": subject.mfa_level,
    }


# Error handlers
@router.get("/test-errors/forbidden")
def test_forbidden_error():
    """Test endpoint để trigger 403 Forbidden."""
    raise HTTPException(status_code=403, detail="Access denied for testing")


@router.get("/test-errors/unauthorized")
def test_unauthorized_error():
    """Test endpoint để trigger 401 Unauthorized."""
    raise HTTPException(status_code=401, detail="Authentication required for testing")


__all__ = ["router"]
