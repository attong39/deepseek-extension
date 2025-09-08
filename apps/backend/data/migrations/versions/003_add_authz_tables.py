"""Add authorization tables for RBAC/ABAC security system.

Revision ID: 003_add_authz_tables
Revises: 002_previous_migration
Create Date: 2025-08-24 12:00:00.000000

This migration creates the core authorization tables for the production-ready
security system including roles, permissions, role_permissions, user_roles,
and jit_grants tables.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "003_add_authz_tables"
down_revision = "002_previous_migration"  # Replace with actual previous revision
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create authorization tables."""

    # Bảng roles - định nghĩa các vai trò hệ thống
    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
        sa.Column(
            "scope", sa.String(length=50), nullable=True
        ),  # 'system', 'tenant', 'project'
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), onupdate=sa.func.now()),
    )

    # Index cho roles
    op.create_index("idx_roles_name", "roles", ["name"])
    op.create_index("idx_roles_scope", "roles", ["scope"])

    # Bảng permissions - định nghĩa các quyền hạn
    op.create_table(
        "permissions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column(
            "risk_level", sa.String(length=10), nullable=False, default="low"
        ),  # 'low', 'medium', 'high', 'critical'
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # Index cho permissions
    op.create_index("idx_permissions_name", "permissions", ["name"])
    op.create_index("idx_permissions_risk", "permissions", ["risk_level"])

    # Bảng role_permissions - mapping role với permissions
    op.create_table(
        "role_permissions",
        sa.Column(
            "role_id",
            sa.String(length=36),
            sa.ForeignKey("roles.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "perm_id",
            sa.String(length=36),
            sa.ForeignKey("permissions.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # Bảng user_roles - gán roles cho users với context
    op.create_table(
        "user_roles",
        sa.Column(
            "user_id", sa.String(length=36), nullable=False
        ),  # Reference to users table
        sa.Column(
            "role_id",
            sa.String(length=36),
            sa.ForeignKey("roles.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "tenant_id", sa.String(length=36), nullable=True
        ),  # Optional: tenant-specific roles
        sa.Column(
            "project_id", sa.String(length=36), nullable=True
        ),  # Optional: project-specific roles
        sa.Column(
            "workspace_id", sa.String(length=36), nullable=True
        ),  # Optional: workspace-specific roles
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column(
            "expires_at", sa.DateTime(), nullable=True
        ),  # Optional: temporary roles
    )

    # Primary key và indexes cho user_roles
    op.create_primary_key(
        "pk_user_roles",
        "user_roles",
        ["user_id", "role_id", "tenant_id", "project_id", "workspace_id"],
    )
    op.create_index("idx_user_roles_user", "user_roles", ["user_id"])
    op.create_index("idx_user_roles_tenant", "user_roles", ["tenant_id"])
    op.create_index("idx_user_roles_expires", "user_roles", ["expires_at"])

    # Bảng jit_grants - Just-In-Time grants cho hành động nhạy cảm
    op.create_table(
        "jit_grants",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "user_id", sa.String(length=36), nullable=False
        ),  # Reference to users table
        sa.Column(
            "perm_name", sa.String(length=100), nullable=False
        ),  # Permission name
        sa.Column(
            "resource_ref", sa.String(length=100), nullable=True
        ),  # Optional: specific resource
        sa.Column("reason", sa.Text(), nullable=True),  # Reason for grant
        sa.Column("mfa_required", sa.Boolean(), default=False),
        sa.Column(
            "approved_by", sa.String(length=36), nullable=True
        ),  # Approver user_id
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("used_at", sa.DateTime(), nullable=True),  # When grant was used
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )

    # Indexes cho jit_grants
    op.create_index("idx_jit_grants_user", "jit_grants", ["user_id"])
    op.create_index("idx_jit_grants_perm", "jit_grants", ["perm_name"])
    op.create_index("idx_jit_grants_expires", "jit_grants", ["expires_at"])
    op.create_index("idx_jit_grants_resource", "jit_grants", ["resource_ref"])

    # Bảng audit_logs - audit logging cho security events
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), nullable=True),
        sa.Column("tenant_id", sa.String(length=36), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=False),
        sa.Column("resource_id", sa.String(length=100), nullable=True),
        sa.Column(
            "decision", sa.String(length=10), nullable=False
        ),  # 'allow' or 'deny'
        sa.Column("reason", sa.String(length=100), nullable=False),
        sa.Column("risk_level", sa.String(length=10), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=True),  # IPv6 support
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("request_id", sa.String(length=36), nullable=True),
        sa.Column("additional_context", sa.JSON(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now()),
    )

    # Indexes cho audit_logs (optimized for queries)
    op.create_index("idx_audit_logs_user", "audit_logs", ["user_id"])
    op.create_index("idx_audit_logs_action", "audit_logs", ["action"])
    op.create_index("idx_audit_logs_decision", "audit_logs", ["decision"])
    op.create_index("idx_audit_logs_timestamp", "audit_logs", ["timestamp"])
    op.create_index("idx_audit_logs_risk", "audit_logs", ["risk_level"])


def downgrade() -> None:
    """Drop authorization tables."""
    op.drop_table("audit_logs")
    op.drop_table("jit_grants")
    op.drop_table("user_roles")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_table("roles")
