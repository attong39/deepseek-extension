"""Add authorization tables for RBAC/ABAC system.

Migration này tạo các bảng cần thiết cho hệ thống phân quyền nâng cấp:
- roles: định nghĩa các vai trò hệ thống
- permissions: định nghĩa các quyền hạn cụ thể
- role_permissions: mapping giữa vai trò và quyền
- user_roles: gán vai trò cho người dùng theo context
- jit_grants: cấp quyền tạm thời cho hành động nhạy cảm

Revision ID: 012_authz_tables
Revises: 011_release_table
Create Date: 2025-08-24
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op


def upgrade() -> None:
    """Create authorization tables."""

    # Bảng roles - định nghĩa các vai trò
    op.create_table(
        "roles",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
        sa.Column("scope", sa.String(50), nullable=False, server_default="system"),
        sa.Column("description", sa.Text),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(36)),
    )

    # Index cho performance
    op.create_index("idx_roles_name", "roles", ["name"])
    op.create_index("idx_roles_scope", "roles", ["scope"])
    op.create_unique_constraint("uq_roles_name_scope", "roles", ["name", "scope"])

    # Bảng permissions - định nghĩa quyền hạn
    op.create_table(
        "permissions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column(
            "domain", sa.String(50), nullable=False
        ),  # files, agent, memory, etc.
        sa.Column(
            "action", sa.String(50), nullable=False
        ),  # create, read, update, delete
        sa.Column("risk_level", sa.String(10), nullable=False, server_default="low"),
        sa.Column("requires_mfa", sa.Boolean, server_default=sa.text("false")),
        sa.Column("description", sa.Text),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    # Index cho performance
    op.create_index("idx_permissions_name", "permissions", ["name"])
    op.create_index("idx_permissions_domain", "permissions", ["domain"])
    op.create_index("idx_permissions_risk", "permissions", ["risk_level"])

    # Bảng role_permissions - mapping vai trò và quyền
    op.create_table(
        "role_permissions",
        sa.Column(
            "role_id", sa.String(36), sa.ForeignKey("roles.id"), primary_key=True
        ),
        sa.Column(
            "permission_id",
            sa.String(36),
            sa.ForeignKey("permissions.id"),
            primary_key=True,
        ),
        sa.Column(
            "granted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("granted_by", sa.String(36)),
    )

    # Composite index cho role_permissions
    op.create_index(
        "idx_role_permissions_composite",
        "role_permissions",
        ["role_id", "permission_id"],
    )

    # Bảng user_roles - gán vai trò cho user theo context
    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("role_id", sa.String(36), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("tenant_id", sa.String(36)),  # Cho multi-tenant
        sa.Column("project_id", sa.String(36)),  # Cho project-specific roles
        sa.Column("workspace_id", sa.String(36)),  # Cho workspace-specific roles
        sa.Column("scope_data", sa.JSON),  # Metadata bổ sung cho scope
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column(
            "granted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True)),  # Để có thể hết hạn
        sa.Column("granted_by", sa.String(36)),
        sa.PrimaryKeyConstraint(
            "user_id",
            "role_id",
            "tenant_id",
            "project_id",
            "workspace_id",
            name="pk_user_roles",
        ),
    )

    # Index cho performance
    op.create_index("idx_user_roles_user", "user_roles", ["user_id"])
    op.create_index("idx_user_roles_tenant", "user_roles", ["tenant_id"])
    op.create_index("idx_user_roles_active", "user_roles", ["is_active"])
    # Composite index cho lookup queries
    op.create_index(
        "idx_user_roles_lookup",
        "user_roles",
        ["user_id", "tenant_id", "project_id", "workspace_id"],
    )

    # Bảng jit_grants - Just-In-Time grants cho hành động nhạy cảm
    op.create_table(
        "jit_grants",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("permission_name", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(50)),
        sa.Column("resource_id", sa.String(36)),
        sa.Column("reason", sa.Text, nullable=False),
        sa.Column("mfa_required", sa.Boolean, default=False),
        sa.Column("mfa_verified", sa.Boolean, default=False),
        sa.Column("approval_required", sa.Boolean, default=False),
        sa.Column("approved_by", sa.String(36)),
        sa.Column("approved_at", sa.DateTime),
        sa.Column("expires_at", sa.DateTime, nullable=False),
        sa.Column("used_at", sa.DateTime),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("metadata", sa.JSON),
    )

    # Index cho performance
    op.create_index("idx_jit_grants_user", "jit_grants", ["user_id"])
    op.create_index("idx_jit_grants_permission", "jit_grants", ["permission_name"])
    op.create_index("idx_jit_grants_expires", "jit_grants", ["expires_at"])
    op.create_index("idx_jit_grants_active", "jit_grants", ["is_active"])
    # Composite index cho JIT lookup với TTL
    op.create_index(
        "idx_jit_grants_lookup",
        "jit_grants",
        ["user_id", "permission_name", "resource_id", "expires_at"],
    )
    # Constraint để đảm bảo expires_at > created_at
    op.create_check_constraint(
        "ck_jit_expires_future", "jit_grants", "expires_at > created_at"
    )

    # Bảng audit_events - ghi lại mọi quyết định phân quyền
    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36)),
        sa.Column("tenant_id", sa.String(36)),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(50)),
        sa.Column("resource_id", sa.String(36)),
        sa.Column("decision", sa.String(20), nullable=False),  # allow, deny
        sa.Column(
            "reason", sa.String(100)
        ),  # rbac_allow, abac_deny, jit_required, etc.
        sa.Column("risk_level", sa.String(10)),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.Text),
        sa.Column("session_id", sa.String(36)),
        sa.Column("request_id", sa.String(36)),
        sa.Column("context_data", sa.JSON),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    # Index cho audit queries
    op.create_index("idx_audit_user", "audit_events", ["user_id"])
    op.create_index("idx_audit_action", "audit_events", ["action"])
    op.create_index("idx_audit_decision", "audit_events", ["decision"])
    op.create_index("idx_audit_created", "audit_events", ["created_at"])
    op.create_index("idx_audit_request", "audit_events", ["request_id"])


def downgrade() -> None:
    """Drop authorization tables."""

    # Drop in reverse order
    op.drop_table("audit_events")
    op.drop_table("jit_grants")
    op.drop_table("user_roles")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
