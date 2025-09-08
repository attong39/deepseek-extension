"""Permission definitions và permission checks cho hệ thống ZETA.

Module này định nghĩa:
- Danh sách permissions chuẩn của hệ thống
- Mapping permissions theo roles
- Helper functions để kiểm tra quyền
"""

from __future__ import annotations

from typing import Literal
import DEFAULT_ROLE_PERMISSIONS
import PERMISSIONS
import action
import bool
import description
import dict
import domain
import list
import name
import perm
import permission_name
import required_permission
import requires_mfa
import risk
import risk_level
import role_name
import self
import str
import user_permissions

Risk = Literal["low", "medium", "high", "critical"]


class Permission:
    """Định nghĩa một permission với metadata."""

    def __init__(
        self,
        name: str,
        domain: str,
        action: str,
        risk: Risk = "low",
        requires_mfa: bool = False,
        description: str = "",
    ) -> None:
        self.name = name
        self.domain = domain
        self.action = action
        self.risk = risk
        self.requires_mfa = requires_mfa
        self.description = description

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Permission({self.name}, {self.risk})"


# Định nghĩa tất cả permissions của hệ thống
PERMISSIONS: dict[str, Permission] = {
    # Agent management
    "agent:create": Permission(
        "agent:create", "agent", "create", "medium", description="Tạo agent mới"
    ),
    "agent:read": Permission(
        "agent:read", "agent", "read", "low", description="Xem thông tin agent"
    ),
    "agent:update": Permission(
        "agent:update",
        "agent",
        "update",
        "medium",
        description="Cập nhật cấu hình agent",
    ),
    "agent:delete": Permission(
        "agent:delete", "agent", "delete", "high", description="Xóa agent"
    ),
    "agent:run": Permission(
        "agent:run", "agent", "run", "high", description="Chạy agent"
    ),
    "agent:stop": Permission(
        "agent:stop", "agent", "stop", "medium", description="Dừng agent"
    ),
    # Memory management
    "memory:create": Permission(
        "memory:create", "memory", "create", "low", description="Tạo memory mới"
    ),
    "memory:read": Permission(
        "memory:read", "memory", "read", "low", description="Đọc memory"
    ),
    "memory:search": Permission(
        "memory:search", "memory", "search", "low", description="Tìm kiếm trong memory"
    ),
    "memory:update": Permission(
        "memory:update", "memory", "update", "medium", description="Cập nhật memory"
    ),
    "memory:delete": Permission(
        "memory:delete", "memory", "delete", "medium", description="Xóa memory"
    ),
    "memory:purge": Permission(
        "memory:purge", "memory", "purge", "high", description="Xóa toàn bộ memory"
    ),
    # File operations
    "files:upload": Permission(
        "files:upload", "files", "upload", "low", description="Upload file"
    ),
    "files:download": Permission(
        "files:download", "files", "download", "low", description="Download file"
    ),
    "files:read": Permission(
        "files:read", "files", "read", "low", description="Đọc nội dung file"
    ),
    "files:update": Permission(
        "files:update", "files", "update", "medium", description="Chỉnh sửa file"
    ),
    "files:delete": Permission(
        "files:delete", "files", "delete", "high", description="Xóa file"
    ),
    "files:share": Permission(
        "files:share", "files", "share", "medium", description="Chia sẻ file"
    ),
    # Training operations
    "training:start": Permission(
        "training:start", "training", "start", "medium", description="Bắt đầu training"
    ),
    "training:stop": Permission(
        "training:stop", "training", "stop", "low", description="Dừng training"
    ),
    "training:view": Permission(
        "training:view", "training", "view", "low", description="Xem training progress"
    ),
    "training:delete": Permission(
        "training:delete", "training", "delete", "high", description="Xóa training job"
    ),
    # Admin operations
    "admin:user:list": Permission(
        "admin:user:list",
        "admin",
        "user_list",
        "medium",
        description="Xem danh sách người dùng",
    ),
    "admin:user:create": Permission(
        "admin:user:create",
        "admin",
        "user_create",
        "high",
        description="Tạo người dùng mới",
    ),
    "admin:user:update": Permission(
        "admin:user:update",
        "admin",
        "user_update",
        "high",
        description="Cập nhật thông tin người dùng",
    ),
    "admin:user:delete": Permission(
        "admin:user:delete",
        "admin",
        "user_delete",
        "critical",
        True,
        description="Xóa người dùng",
    ),
    "admin:user:invite": Permission(
        "admin:user:invite",
        "admin",
        "user_invite",
        "medium",
        description="Mời người dùng mới",
    ),
    "admin:role:manage": Permission(
        "admin:role:manage",
        "admin",
        "role_manage",
        "high",
        description="Quản lý roles và permissions",
    ),
    # System operations
    "system:audit:read": Permission(
        "system:audit:read",
        "system",
        "audit_read",
        "medium",
        description="Đọc audit logs",
    ),
    "system:config:read": Permission(
        "system:config:read",
        "system",
        "config_read",
        "medium",
        description="Đọc cấu hình hệ thống",
    ),
    "system:config:update": Permission(
        "system:config:update",
        "system",
        "config_update",
        "critical",
        True,
        description="Cập nhật cấu hình hệ thống",
    ),
    "system:backup:create": Permission(
        "system:backup:create",
        "system",
        "backup_create",
        "high",
        description="Tạo backup",
    ),
    "system:backup:restore": Permission(
        "system:backup:restore",
        "system",
        "backup_restore",
        "critical",
        True,
        description="Restore từ backup",
    ),
    # Policy management
    "ops:policy:read": Permission(
        "ops:policy:read",
        "ops",
        "policy_read",
        "medium",
        description="Đọc security policies",
    ),
    "ops:policy:update": Permission(
        "ops:policy:update",
        "ops",
        "policy_update",
        "critical",
        True,
        description="Cập nhật security policies",
    ),
    "ops:security:monitor": Permission(
        "ops:security:monitor",
        "ops",
        "security_monitor",
        "medium",
        description="Giám sát bảo mật",
    ),
    # Chat operations
    "chat:create": Permission(
        "chat:create", "chat", "create", "low", description="Tạo cuộc trò chuyện"
    ),
    "chat:read": Permission(
        "chat:read", "chat", "read", "low", description="Đọc lịch sử chat"
    ),
    "chat:delete": Permission(
        "chat:delete", "chat", "delete", "medium", description="Xóa chat"
    ),
}

# Mapping default permissions cho từng role
DEFAULT_ROLE_PERMISSIONS: dict[str, list[str]] = {
    "guest": [],
    "user": [
        "agent:read",
        "agent:run",
        "memory:create",
        "memory:read",
        "memory:search",
        "files:upload",
        "files:download",
        "files:read",
        "training:start",
        "training:view",
        "chat:create",
        "chat:read",
    ],
    "power_user": [
        "agent:create",
        "agent:read",
        "agent:update",
        "agent:run",
        "agent:stop",
        "memory:create",
        "memory:read",
        "memory:search",
        "memory:update",
        "memory:delete",
        "files:upload",
        "files:download",
        "files:read",
        "files:update",
        "files:delete",
        "files:share",
        "training:start",
        "training:stop",
        "training:view",
        "training:delete",
        "chat:create",
        "chat:read",
        "chat:delete",
    ],
    "admin": [
        # Tất cả quyền của power_user
        "agent:create",
        "agent:read",
        "agent:update",
        "agent:run",
        "agent:stop",
        "memory:create",
        "memory:read",
        "memory:search",
        "memory:update",
        "memory:delete",
        "memory:purge",
        "files:upload",
        "files:download",
        "files:read",
        "files:update",
        "files:delete",
        "files:share",
        "training:start",
        "training:stop",
        "training:view",
        "training:delete",
        "chat:create",
        "chat:read",
        "chat:delete",
        # Quyền admin
        "admin:user:list",
        "admin:user:create",
        "admin:user:update",
        "admin:user:invite",
        "admin:role:manage",
        "system:audit:read",
        "system:config:read",
        "system:backup:create",
        "ops:security:monitor",
    ],
    "superadmin": list(PERMISSIONS.keys()),  # Tất cả permissions
}


# Missing constants cho policy engine
DEFAULT_ROLE_PERMS = DEFAULT_ROLE_PERMISSIONS  # Alias để tương thích


def get_permission_risk(permission_name: str) -> Risk:
    """Lấy risk level của permission.

    Args:
        permission_name: Tên permission

    Returns:
        Risk level của permission
    """
    permission = PERMISSIONS.get(permission_name)
    if permission:
        return permission.risk
    return "low"


def get_permission(name: str) -> Permission | None:
    """Lấy permission object theo tên.

    Args:
        name: Tên permission

    Returns:
        Permission object hoặc None nếu không tìm thấy
    """
    return PERMISSIONS.get(name)


def get_required_permissions(action: str) -> list[str]:
    """Lấy danh sách permissions cần thiết cho một action.

    Args:
        action: Tên action cần kiểm tra

    Returns:
        Danh sách permission names
    """
    # Mapping từ action name sang permission names
    action_permissions = {
        "create_agent": ["agent:create"],
        "run_agent": ["agent:run"],
        "delete_file": ["files:delete"],
        "start_training": ["training:start"],
        "manage_users": ["admin:user:create", "admin:user:update"],
        "update_config": ["system:config:update"],
        # Thêm mapping khác khi cần
    }
    return action_permissions.get(action, [])


def has_permission(user_permissions: list[str], required_permission: str) -> bool:
    """Kiểm tra user có permission cần thiết không.

    Args:
        user_permissions: Danh sách permissions của user
        required_permission: Permission cần kiểm tra

    Returns:
        True nếu có quyền
    """
    return required_permission in user_permissions


def get_role_permissions(role_name: str) -> list[str]:
    """Lấy danh sách permissions của một role.

    Args:
        role_name: Tên role

    Returns:
        Danh sách permission names
    """
    return DEFAULT_ROLE_PERMISSIONS.get(role_name, [])


def get_permissions_by_risk(risk_level: Risk) -> list[str]:
    """Lấy danh sách permissions theo mức độ rủi ro.

    Args:
        risk_level: Mức độ rủi ro cần lọc

    Returns:
        Danh sách permission names
    """
    return [name for name, perm in PERMISSIONS.items() if perm.risk == risk_level]


def get_permissions_requiring_mfa() -> list[str]:
    """Lấy danh sách permissions yêu cầu MFA.

    Returns:
        Danh sách permission names yêu cầu MFA
    """
    return [name for name, perm in PERMISSIONS.items() if perm.requires_mfa]


def validate_permission_name(name: str) -> bool:
    """Kiểm tra tên permission có hợp lệ không.

    Args:
        name: Tên permission cần kiểm tra

    Returns:
        True nếu permission hợp lệ
    """
    return name in PERMISSIONS
