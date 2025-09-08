"""Seed dữ liệu chuẩn hóa cho hệ thống phân quyền ZETA.

Chuẩn hóa theo gợi ý: đồng bộ với permissions.py, đủ permission set,
sử dụng ORM thay vì raw SQL.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.backend.data.database import SessionLocal
from apps.backend.data.models.authz_models import Permission, Role, RolePermission
import Exception
import description
import dict
import e
import len
import name
import p
import perm
import perm_data
import perm_name
import print
import r
import risk_level
import role_data
import role_name
import scope
import str

# Permissions data - đồng bộ với core.security.permissions
PERMISSIONS_DATA = [
    # Agent operations
    {"name": "agent:create", "risk_level": "medium"},
    {"name": "agent:read", "risk_level": "low"},
    {"name": "agent:update", "risk_level": "medium"},
    {"name": "agent:delete", "risk_level": "high"},
    {"name": "agent:run", "risk_level": "high"},
    {"name": "agent:stop", "risk_level": "medium"},
    # Memory operations
    {"name": "memory:create", "risk_level": "low"},
    {"name": "memory:read", "risk_level": "low"},
    {"name": "memory:search", "risk_level": "low"},
    {"name": "memory:update", "risk_level": "medium"},
    {"name": "memory:delete", "risk_level": "medium"},
    {"name": "memory:purge", "risk_level": "high"},
    # File operations
    {"name": "files:upload", "risk_level": "low"},
    {"name": "files:download", "risk_level": "low"},
    {"name": "files:read", "risk_level": "low"},
    {"name": "files:update", "risk_level": "medium"},
    {"name": "files:delete", "risk_level": "high"},
    {"name": "files:share", "risk_level": "medium"},
    # Training operations
    {"name": "training:start", "risk_level": "medium"},
    {"name": "training:stop", "risk_level": "low"},
    {"name": "training:view", "risk_level": "low"},
    {"name": "training:delete", "risk_level": "high"},
    # Admin operations
    {"name": "admin:user:list", "risk_level": "medium"},
    {"name": "admin:user:create", "risk_level": "high"},
    {"name": "admin:user:update", "risk_level": "high"},
    {"name": "admin:user:delete", "risk_level": "critical"},
    {"name": "admin:user:invite", "risk_level": "medium"},
    {"name": "admin:role:manage", "risk_level": "high"},
    # System operations
    {"name": "system:audit:read", "risk_level": "medium"},
    {"name": "system:config:read", "risk_level": "medium"},
    {"name": "system:config:update", "risk_level": "critical"},
    {"name": "system:backup:create", "risk_level": "high"},
    {"name": "system:backup:restore", "risk_level": "critical"},
    # Policy management
    {"name": "ops:policy:read", "risk_level": "medium"},
    {"name": "ops:policy:update", "risk_level": "critical"},
    {"name": "ops:security:monitor", "risk_level": "medium"},
    # Chat operations
    {"name": "chat:create", "risk_level": "low"},
    {"name": "chat:read", "risk_level": "low"},
    {"name": "chat:delete", "risk_level": "medium"},
]

# Role definitions với permission mappings
ROLES_DATA = {
    "guest": {"description": "Guest user với quyền hạn tối thiểu", "permissions": []},
    "user": {
        "description": "Regular user role",
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
        "description": "Power user với quyền nâng cao",
        "permissions": [
            # Inherit user permissions
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
            # Additional permissions
            "agent:create",
            "agent:update",
            "agent:stop",
            "memory:update",
            "memory:delete",
            "files:update",
            "files:delete",
            "files:share",
            "training:stop",
            "training:delete",
            "chat:delete",
        ],
    },
    "admin": {
        "description": "Administrator role",
        "permissions": [
            # Inherit power_user permissions
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
            # Additional admin permissions
            "agent:delete",
            "admin:user:list",
            "admin:user:create",
            "admin:user:update",
            "admin:user:invite",
            "admin:role:manage",
            "system:audit:read",
            "system:config:read",
            "system:backup:create",
            "ops:policy:read",
            "ops:security:monitor",
        ],
    },
    "superadmin": {
        "description": "Super administrator với full permissions",
        "permissions": [
            # All permissions
            perm["name"]
            for perm in PERMISSIONS_DATA
        ],
    },
}


def get_or_create_permission(db: Session, name: str, risk_level: str) -> Permission:
    """Lấy hoặc tạo permission."""
    permission = db.scalar(select(Permission).where(Permission.name == name))
    if permission:
        return permission

    permission = Permission(id=str(uuid.uuid4()), name=name, risk_level=risk_level)
    db.add(permission)
    return permission


def get_or_create_role(db: Session, name: str, description: str = "", scope: str = "system") -> Role:
    """Lấy hoặc tạo role."""
    role = db.scalar(select(Role).where(Role.name == name, Role.scope == scope))
    if role:
        return role

    role = Role(id=str(uuid.uuid4()), name=name, scope=scope, description=description)
    db.add(role)
    return role


def seed_permissions(db: Session) -> dict[str, Permission]:
    """Seed tất cả permissions."""
    name_to_permission = {}

    for perm_data in PERMISSIONS_DATA:
        permission = get_or_create_permission(db, perm_data["name"], perm_data["risk_level"])
        name_to_permission[perm_data["name"]] = permission

    db.flush()  # Ensure IDs are available
    return name_to_permission


def seed_roles_and_mappings(db: Session, permissions: dict[str, Permission]) -> None:
    """Seed roles và role-permission mappings."""

    for role_name, role_data in ROLES_DATA.items():
        role = get_or_create_role(db, role_name, role_data["description"])
        db.flush()  # Ensure role ID is available

        # Create role-permission mappings
        for perm_name in role_data["permissions"]:
            permission = permissions.get(perm_name)
            if not permission:
                continue

            # Check if mapping already exists
            existing = db.scalar(
                select(RolePermission).where(RolePermission.role_id == role.id, RolePermission.perm_id == permission.id)
            )

            if not existing:
                role_permission = RolePermission(role_id=role.id, perm_id=permission.id)
                db.add(role_permission)


def seed_authz_data() -> None:
    """Main function để seed toàn bộ authorization data."""
    db = SessionLocal()

    try:
        print("🌱 Seeding permissions...")
        permissions = seed_permissions(db)
        print(f"✅ Created/verified {len(permissions)} permissions")

        print("🌱 Seeding roles and mappings...")
        seed_roles_and_mappings(db, permissions)
        print(f"✅ Created/verified {len(ROLES_DATA)} roles")

        db.commit()
        print("✅ Authorization data seeded successfully!")

    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def verify_seed_data() -> None:
    """Verify seed data đã được tạo đúng."""
    db = SessionLocal()

    try:
        # Count permissions
        perm_count = db.scalar(select(Permission).count())
        print(f"📊 Permissions in DB: {perm_count}")

        # Count roles
        role_count = db.scalar(select(Role).count())
        print(f"📊 Roles in DB: {role_count}")

        # Count role-permission mappings
        mapping_count = db.scalar(select(RolePermission).count())
        print(f"📊 Role-Permission mappings: {mapping_count}")

        # Sample some data
        sample_permissions = db.scalars(select(Permission).limit(5)).all()
        print(f"📋 Sample permissions: {[p.name for p in sample_permissions]}")

        sample_roles = db.scalars(select(Role).limit(5)).all()
        print(f"📋 Sample roles: {[r.name for r in sample_roles]}")

    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Starting authorization data seeding...")
    seed_authz_data()
    print("\n📊 Verifying seeded data...")
    verify_seed_data()
    print("\n🎉 Seeding completed successfully!")
