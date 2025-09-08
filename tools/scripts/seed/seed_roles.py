"""Seed roles and permissions for ZETA security system.

This script populates the authorization tables with default roles and permissions
according to the production-ready security architecture.
"""

from __future__ import annotations

import uuid

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from apps.backend.config.database import get_database_url
import Exception
import assignment
import dict
import e
import exit
import len
import perm_data
import perm_name
import permission_ids
import print
import role_data
import role_ids
import role_name
import str

# Permission definitions with risk levels
PERMISSIONS_DATA = [
    # Agent permissions
    {"name": "agent:create", "risk_level": "medium", "description": "Create new AI agents"},
    {"name": "agent:read", "risk_level": "low", "description": "View agent information"},
    {"name": "agent:update", "risk_level": "medium", "description": "Modify agent configuration"},
    {"name": "agent:delete", "risk_level": "high", "description": "Delete agents"},
    {"name": "agent:run", "risk_level": "high", "description": "Execute AI agents"},
    # Memory permissions
    {"name": "memory:search", "risk_level": "low", "description": "Search memory database"},
    {"name": "memory:ingest", "risk_level": "medium", "description": "Add data to memory"},
    {"name": "memory:update", "risk_level": "medium", "description": "Modify memory entries"},
    {"name": "memory:delete", "risk_level": "high", "description": "Delete memory entries"},
    {
        "name": "memory:purge",
        "risk_level": "critical",
        "description": "Purge entire memory database",
    },
    # File permissions
    {"name": "files:upload", "risk_level": "low", "description": "Upload files"},
    {"name": "files:download", "risk_level": "low", "description": "Download files"},
    {"name": "files:read", "risk_level": "low", "description": "Read file metadata"},
    {"name": "files:write", "risk_level": "medium", "description": "Modify files"},
    {"name": "files:delete", "risk_level": "high", "description": "Delete files"},
    # Training permissions
    {"name": "training:start", "risk_level": "medium", "description": "Start model training"},
    {"name": "training:stop", "risk_level": "low", "description": "Stop training jobs"},
    {"name": "training:view_status", "risk_level": "low", "description": "View training status"},
    {"name": "training:view_logs", "risk_level": "low", "description": "View training logs"},
    {"name": "training:delete_job", "risk_level": "high", "description": "Delete training jobs"},
    # Admin permissions
    {"name": "admin:user:list", "risk_level": "medium", "description": "List all users"},
    {"name": "admin:user:create", "risk_level": "high", "description": "Create new users"},
    {"name": "admin:user:update", "risk_level": "high", "description": "Modify user accounts"},
    {"name": "admin:user:delete", "risk_level": "critical", "description": "Delete user accounts"},
    {"name": "admin:user:invite", "risk_level": "medium", "description": "Invite new users"},
    {"name": "admin:user:disable", "risk_level": "high", "description": "Disable user accounts"},
    {"name": "admin:roles:manage", "risk_level": "critical", "description": "Manage user roles"},
    # System permissions
    {"name": "system:audit:read", "risk_level": "medium", "description": "Read audit logs"},
    {"name": "system:config:read", "risk_level": "low", "description": "Read system configuration"},
    {
        "name": "system:config:update",
        "risk_level": "critical",
        "description": "Update system configuration",
    },
    {"name": "system:backup:create", "risk_level": "high", "description": "Create system backups"},
    {
        "name": "system:backup:restore",
        "risk_level": "critical",
        "description": "Restore from backups",
    },
    # Operations permissions
    {"name": "ops:policy:read", "risk_level": "medium", "description": "Read security policies"},
    {
        "name": "ops:policy:update",
        "risk_level": "critical",
        "description": "Update security policies",
    },
    {"name": "ops:monitoring:read", "risk_level": "low", "description": "Read monitoring data"},
    {"name": "ops:alerts:manage", "risk_level": "medium", "description": "Manage system alerts"},
    # API permissions
    {"name": "api:read", "risk_level": "low", "description": "Read access to API"},
    {"name": "api:write", "risk_level": "medium", "description": "Write access to API"},
    {"name": "api:admin", "risk_level": "high", "description": "Admin access to API"},
]

# Role definitions with their permissions
ROLES_DATA = {
    "guest": {
        "scope": "system",
        "description": "Guest user with minimal access",
        "permissions": [
            "api:read",
            "system:config:read",
        ],
    },
    "user": {
        "scope": "system",
        "description": "Standard user with basic permissions",
        "permissions": [
            "agent:read",
            "agent:run",
            "memory:search",
            "memory:ingest",
            "files:upload",
            "files:download",
            "files:read",
            "training:start",
            "training:stop",
            "training:view_status",
            "training:view_logs",
            "api:read",
            "api:write",
            "ops:monitoring:read",
        ],
    },
    "power_user": {
        "scope": "system",
        "description": "Power user with elevated permissions",
        "permissions": [
            "agent:create",
            "agent:update",
            "agent:delete",
            "memory:update",
            "memory:delete",
            "files:write",
            "files:delete",
            "training:delete_job",
            "system:backup:create",
        ],
    },
    "admin": {
        "scope": "system",
        "description": "Administrator with user management permissions",
        "permissions": [
            "admin:user:list",
            "admin:user:create",
            "admin:user:update",
            "admin:user:invite",
            "admin:user:disable",
            "system:audit:read",
            "system:config:update",
            "ops:policy:read",
            "ops:alerts:manage",
            "api:admin",
        ],
    },
    "superadmin": {
        "scope": "system",
        "description": "Super administrator with full system access",
        "permissions": [
            "admin:user:delete",
            "admin:roles:manage",
            "memory:purge",
            "system:backup:restore",
            "ops:policy:update",
        ],
    },
}


def seed_roles_and_permissions() -> None:
    """Seed the database with default roles and permissions."""

    # Create database connection
    database_url = get_database_url()
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)

    db = SessionLocal()
    try:
        print("🌱 Starting to seed roles and permissions...")

        # 1. Seed permissions
        print("📝 Seeding permissions...")
        permission_ids: dict[str, str] = {}

        for perm_data in PERMISSIONS_DATA:
            perm_id = str(uuid.uuid4())
            permission_ids[perm_data["name"]] = perm_id

            db.execute(
                text("""
                INSERT INTO permissions (id, name, risk_level, description)
                VALUES (:id, :name, :risk_level, :description)
                ON CONFLICT (name) DO NOTHING
            """),
                {
                    "id": perm_id,
                    "name": perm_data["name"],
                    "risk_level": perm_data["risk_level"],
                    "description": perm_data["description"],
                },
            )

        print(f"✅ Created {len(PERMISSIONS_DATA)} permissions")

        # 2. Seed roles
        print("👥 Seeding roles...")
        role_ids: dict[str, str] = {}

        for role_name, role_data in ROLES_DATA.items():
            role_id = str(uuid.uuid4())
            role_ids[role_name] = role_id

            db.execute(
                text("""
                INSERT INTO roles (id, name, scope, description)
                VALUES (:id, :name, :scope, :description)
                ON CONFLICT (name) DO NOTHING
            """),
                {
                    "id": role_id,
                    "name": role_name,
                    "scope": role_data["scope"],
                    "description": role_data["description"],
                },
            )

        print(f"✅ Created {len(ROLES_DATA)} roles")

        # 3. Seed role-permission mappings
        print("🔗 Seeding role-permission mappings...")
        mapping_count = 0

        for role_name, role_data in ROLES_DATA.items():
            role_id = role_ids[role_name]

            for perm_name in role_data["permissions"]:
                if perm_name in permission_ids:
                    perm_id = permission_ids[perm_name]

                    db.execute(
                        text("""
                        INSERT INTO role_permissions (role_id, perm_id)
                        VALUES (:role_id, :perm_id)
                        ON CONFLICT (role_id, perm_id) DO NOTHING
                    """),
                        {
                            "role_id": role_id,
                            "perm_id": perm_id,
                        },
                    )
                    mapping_count += 1
                else:
                    print(f"⚠️  Permission '{perm_name}' not found for role '{role_name}'")

        print(f"✅ Created {mapping_count} role-permission mappings")

        # Commit transaction
        db.commit()

        # 4. Verify seeding
        print("🔍 Verifying seeded data...")

        # Count permissions
        perm_count = db.execute(text("SELECT COUNT(*) FROM permissions")).scalar()
        print(f"📊 Total permissions in database: {perm_count}")

        # Count roles
        role_count = db.execute(text("SELECT COUNT(*) FROM roles")).scalar()
        print(f"📊 Total roles in database: {role_count}")

        # Count mappings
        mapping_count = db.execute(text("SELECT COUNT(*) FROM role_permissions")).scalar()
        print(f"📊 Total role-permission mappings: {mapping_count}")

        # Show role permission counts
        print("\n📋 Role permission summary:")
        for role_name in ROLES_DATA:
            count = db.execute(
                text("""
                SELECT COUNT(rp.perm_id)
                FROM roles r
                JOIN role_permissions rp ON r.id = rp.role_id
                WHERE r.name = :role_name
            """),
                {"role_name": role_name},
            ).scalar()
            print(f"   {role_name}: {count} permissions")

        print("\n🎉 Successfully seeded roles and permissions!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise e
    finally:
        db.close()


def create_sample_user_roles() -> None:
    """Create sample user role assignments for testing."""

    database_url = get_database_url()
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)

    db = SessionLocal()
    try:
        print("👤 Creating sample user role assignments...")

        # Sample user-role assignments
        sample_assignments = [
            {"user_id": "user-123", "role_name": "user", "tenant_id": "tenant-1"},
            {"user_id": "admin-456", "role_name": "admin", "tenant_id": "tenant-1"},
            {"user_id": "super-789", "role_name": "superadmin", "tenant_id": None},
        ]

        for assignment in sample_assignments:
            # Get role ID
            role_result = db.execute(
                text("""
                SELECT id FROM roles WHERE name = :role_name
            """),
                {"role_name": assignment["role_name"]},
            ).fetchone()

            if role_result:
                role_id = role_result[0]

                db.execute(
                    text("""
                    INSERT INTO user_roles (user_id, role_id, tenant_id)
                    VALUES (:user_id, :role_id, :tenant_id)
                    ON CONFLICT DO NOTHING
                """),
                    {
                        "user_id": assignment["user_id"],
                        "role_id": role_id,
                        "tenant_id": assignment["tenant_id"],
                    },
                )

        db.commit()
        print("✅ Created sample user role assignments")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating user roles: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    try:
        seed_roles_and_permissions()
        create_sample_user_roles()
        print("\n🚀 Security system seeding completed successfully!")
    except Exception as e:
        print(f"\n💥 Seeding failed: {e}")
        exit(1)
