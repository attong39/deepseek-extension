"""Seed dữ liệu mặc định cho hệ thống phân quyền.

Script này tạo các roles và permissions cơ bản để hệ thống có thể hoạt động ngay.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING
import Exception
import dict
import e
import len
import list
import next
import perm_data
import perm_name
import print
import result
import role_info
import role_name
import str

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from apps.backend.data.database import get_db


def create_default_permissions(db: Session) -> dict[str, str]:
    """Tạo permissions mặc định cho hệ thống.

    Returns:
        Mapping từ permission name sang permission ID
    """
    permissions_data = [
        # Agent management
        {
            "name": "agent:create",
            "domain": "agent",
            "action": "create",
            "risk_level": "medium",
        },
        {
            "name": "agent:read",
            "domain": "agent",
            "action": "read",
            "risk_level": "low",
        },
        {
            "name": "agent:update",
            "domain": "agent",
            "action": "update",
            "risk_level": "medium",
        },
        {
            "name": "agent:delete",
            "domain": "agent",
            "action": "delete",
            "risk_level": "high",
        },
        {"name": "agent:run", "domain": "agent", "action": "run", "risk_level": "high"},
        {
            "name": "agent:stop",
            "domain": "agent",
            "action": "stop",
            "risk_level": "medium",
        },
        # Memory management
        {
            "name": "memory:create",
            "domain": "memory",
            "action": "create",
            "risk_level": "low",
        },
        {
            "name": "memory:read",
            "domain": "memory",
            "action": "read",
            "risk_level": "low",
        },
        {
            "name": "memory:search",
            "domain": "memory",
            "action": "search",
            "risk_level": "low",
        },
        {
            "name": "memory:update",
            "domain": "memory",
            "action": "update",
            "risk_level": "medium",
        },
        {
            "name": "memory:delete",
            "domain": "memory",
            "action": "delete",
            "risk_level": "medium",
        },
        {
            "name": "memory:purge",
            "domain": "memory",
            "action": "purge",
            "risk_level": "high",
        },
        # File operations
        {
            "name": "files:upload",
            "domain": "files",
            "action": "upload",
            "risk_level": "low",
        },
        {
            "name": "files:download",
            "domain": "files",
            "action": "download",
            "risk_level": "low",
        },
        {
            "name": "files:read",
            "domain": "files",
            "action": "read",
            "risk_level": "low",
        },
        {
            "name": "files:update",
            "domain": "files",
            "action": "update",
            "risk_level": "medium",
        },
        {
            "name": "files:delete",
            "domain": "files",
            "action": "delete",
            "risk_level": "high",
        },
        {
            "name": "files:share",
            "domain": "files",
            "action": "share",
            "risk_level": "medium",
        },
        # Training operations
        {
            "name": "training:start",
            "domain": "training",
            "action": "start",
            "risk_level": "medium",
        },
        {
            "name": "training:stop",
            "domain": "training",
            "action": "stop",
            "risk_level": "low",
        },
        {
            "name": "training:view",
            "domain": "training",
            "action": "view",
            "risk_level": "low",
        },
        {
            "name": "training:delete",
            "domain": "training",
            "action": "delete",
            "risk_level": "high",
        },
        # Admin operations
        {
            "name": "admin:user:list",
            "domain": "admin",
            "action": "user_list",
            "risk_level": "medium",
        },
        {
            "name": "admin:user:create",
            "domain": "admin",
            "action": "user_create",
            "risk_level": "high",
        },
        {
            "name": "admin:user:update",
            "domain": "admin",
            "action": "user_update",
            "risk_level": "high",
        },
        {
            "name": "admin:user:delete",
            "domain": "admin",
            "action": "user_delete",
            "risk_level": "critical",
        },
        {
            "name": "admin:user:invite",
            "domain": "admin",
            "action": "user_invite",
            "risk_level": "medium",
        },
        {
            "name": "admin:role:manage",
            "domain": "admin",
            "action": "role_manage",
            "risk_level": "high",
        },
        # System operations
        {
            "name": "system:audit:read",
            "domain": "system",
            "action": "audit_read",
            "risk_level": "medium",
        },
        {
            "name": "system:config:read",
            "domain": "system",
            "action": "config_read",
            "risk_level": "medium",
        },
        {
            "name": "system:config:update",
            "domain": "system",
            "action": "config_update",
            "risk_level": "critical",
        },
        {
            "name": "system:backup:create",
            "domain": "system",
            "action": "backup_create",
            "risk_level": "high",
        },
        {
            "name": "system:backup:restore",
            "domain": "system",
            "action": "backup_restore",
            "risk_level": "critical",
        },
        # Policy management
        {
            "name": "ops:policy:read",
            "domain": "ops",
            "action": "policy_read",
            "risk_level": "medium",
        },
        {
            "name": "ops:policy:update",
            "domain": "ops",
            "action": "policy_update",
            "risk_level": "critical",
        },
        {
            "name": "ops:security:monitor",
            "domain": "ops",
            "action": "security_monitor",
            "risk_level": "medium",
        },
        # Chat operations
        {
            "name": "chat:create",
            "domain": "chat",
            "action": "create",
            "risk_level": "low",
        },
        {"name": "chat:read", "domain": "chat", "action": "read", "risk_level": "low"},
        {
            "name": "chat:delete",
            "domain": "chat",
            "action": "delete",
            "risk_level": "medium",
        },
    ]

    permission_map = {}

    for perm_data in permissions_data:
        perm_id = str(uuid.uuid4())

        # Set MFA requirement for critical and some high-risk actions
        requires_mfa = perm_data["risk_level"] == "critical" or (
            perm_data["risk_level"] == "high"
            and perm_data["domain"] in {"system", "ops", "admin"}
        )

        db.execute(
            """INSERT INTO permissions
               (id, name, domain, action, risk_level, requires_mfa, description, is_active, created_at)
               VALUES (:id, :name, :domain, :action, :risk_level, :requires_mfa, :description, :is_active, :created_at)""",
            {
                "id": perm_id,
                "name": perm_data["name"],
                "domain": perm_data["domain"],
                "action": perm_data["action"],
                "risk_level": perm_data["risk_level"],
                "requires_mfa": requires_mfa,
                "description": f"Permission to {perm_data['action']} {perm_data['domain']} resources",
                "is_active": True,
                "created_at": datetime.now(UTC),
            },
        )

        permission_map[perm_data["name"]] = perm_id

    return permission_map


def create_default_roles(db: Session, permission_map: dict[str, str]) -> dict[str, str]:
    """Tạo roles mặc định và gán permissions.

    Args:
        permission_map: Mapping từ permission name sang ID

    Returns:
        Mapping từ role name sang role ID
    """

    # Định nghĩa roles và permissions của chúng
    roles_data = {
        "guest": {
            "description": "Khách vãng lai - chỉ xem thông tin cơ bản",
            "permissions": [],
        },
        "user": {
            "description": "Người dùng thông thường - có thể sử dụng các tính năng cơ bản",
            "permissions": [
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
        },
        "power_user": {
            "description": "Người dùng nâng cao - có thể thực hiện các thao tác phức tạp",
            "permissions": [
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
        },
        "admin": {
            "description": "Quản trị viên - quản lý người dùng và hệ thống",
            "permissions": [
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
        },
        "superadmin": {
            "description": "Siêu quản trị - toàn quyền hệ thống",
            "permissions": list(permission_map.keys()),  # Tất cả permissions
        },
    }

    role_map = {}

    for role_name, role_info in roles_data.items():
        role_id = str(uuid.uuid4())

        # Tạo role
        db.execute(
            """INSERT INTO roles
               (id, name, scope, description, is_active, created_at, created_by)
               VALUES (:id, :name, :scope, :description, :is_active, :created_at, :created_by)""",
            {
                "id": role_id,
                "name": role_name,
                "scope": "system",
                "description": role_info["description"],
                "is_active": True,
                "created_at": datetime.now(UTC),
                "created_by": "system",
            },
        )

        # Gán permissions cho role
        for perm_name in role_info["permissions"]:
            if perm_name in permission_map:
                db.execute(
                    """INSERT INTO role_permissions
                       (role_id, permission_id, granted_at, granted_by)
                       VALUES (:role_id, :permission_id, :granted_at, :granted_by)""",
                    {
                        "role_id": role_id,
                        "permission_id": permission_map[perm_name],
                        "granted_at": datetime.now(UTC),
                        "granted_by": "system",
                    },
                )

        role_map[role_name] = role_id

    return role_map


def seed_authorization_data() -> None:
    """Seed dữ liệu authorization vào database."""

    db = next(get_db())
    try:
        # Kiểm tra xem đã có dữ liệu chưa
        _ = db.execute("SELECT COUNT(*) as count FROM roles").fetchone()
        if result and result.count > 0:
            print("Authorization data already exists, skipping seed")
            return

        print("Seeding authorization data...")

        # Tạo permissions
        permission_map = create_default_permissions(db)
        print(f"Created {len(permission_map)} permissions")

        # Tạo roles
        role_map = create_default_roles(db, permission_map)
        print(f"Created {len(role_map)} roles")

        db.commit()
        print("Authorization data seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding authorization data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_authorization_data()
