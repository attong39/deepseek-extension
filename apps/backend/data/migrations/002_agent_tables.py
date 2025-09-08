"""Migration 002: Create agent tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade() -> None:
    """Create agent-related tables."""

    # Create agents table

    op.create_table(
        "agents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="inactive"),
        sa.Column("version", sa.String(50), nullable=False, default="1.0.0"),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("configuration", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("capabilities", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("last_deployed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deployment_config", postgresql.JSONB, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
    )

    # Create agent_instances table

    op.create_table(
        "agent_instances",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("instance_id", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="pending"),
        sa.Column("host", sa.String(255), nullable=True),
        sa.Column("port", sa.Integer, nullable=True),
        sa.Column("resources", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metrics", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("health_check_url", sa.String(500), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("stopped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("restart_count", sa.Integer, nullable=False, default=0),
    )

    # Create agent_deployments table

    op.create_table(
        "agent_deployments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("version", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, default="pending"),
        sa.Column("deployment_type", sa.String(50), nullable=False, default="docker"),
        sa.Column("environment", sa.String(50), nullable=False, default="development"),
        sa.Column("configuration", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "resources_requested", postgresql.JSONB, nullable=False, default="{}"
        ),
        sa.Column("resources_allocated", postgresql.JSONB, nullable=True),
        sa.Column("deployment_logs", sa.Text, nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("deployed_by", sa.String(36), nullable=True),
        sa.Column("rollback_deployment_id", sa.String(36), nullable=True),
    )

    # Create agent_capabilities table

    op.create_table(
        "agent_capabilities",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("capability_name", sa.String(255), nullable=False),
        sa.Column("capability_type", sa.String(100), nullable=False),
        sa.Column("parameters", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("is_enabled", sa.Boolean, nullable=False, default=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create agent_metrics table

    op.create_table(
        "agent_metrics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "instance_id",
            sa.String(36),
            sa.ForeignKey("agent_instances.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("metric_name", sa.String(255), nullable=False),
        sa.Column("metric_value", sa.Float, nullable=False),
        sa.Column("metric_unit", sa.String(50), nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create indexes

    op.create_index("idx_agents_type", "agents", ["type"])

    op.create_index("idx_agents_status", "agents", ["status"])

    op.create_index("idx_agents_created_at", "agents", ["created_at"])

    op.create_index("idx_agents_updated_at", "agents", ["updated_at"])

    op.create_index("idx_agent_instances_agent_id", "agent_instances", ["agent_id"])

    op.create_index("idx_agent_instances_status", "agent_instances", ["status"])

    op.create_index("idx_agent_instances_created_at", "agent_instances", ["created_at"])

    op.create_index("idx_agent_deployments_agent_id", "agent_deployments", ["agent_id"])

    op.create_index("idx_agent_deployments_status", "agent_deployments", ["status"])

    op.create_index(
        "idx_agent_deployments_environment", "agent_deployments", ["environment"]
    )

    op.create_index(
        "idx_agent_deployments_created_at", "agent_deployments", ["created_at"]
    )

    op.create_index(
        "idx_agent_capabilities_agent_id", "agent_capabilities", ["agent_id"]
    )

    op.create_index(
        "idx_agent_capabilities_name", "agent_capabilities", ["capability_name"]
    )

    op.create_index(
        "idx_agent_capabilities_type", "agent_capabilities", ["capability_type"]
    )

    op.create_index("idx_agent_metrics_agent_id", "agent_metrics", ["agent_id"])

    op.create_index("idx_agent_metrics_instance_id", "agent_metrics", ["instance_id"])

    op.create_index("idx_agent_metrics_name", "agent_metrics", ["metric_name"])

    op.create_index("idx_agent_metrics_recorded_at", "agent_metrics", ["recorded_at"])

    # Create unique constraints

    op.create_unique_constraint(
        "uq_agent_instances_instance_id", "agent_instances", ["instance_id"]
    )

    op.create_unique_constraint(
        "uq_agent_capabilities_agent_capability",
        "agent_capabilities",
        ["agent_id", "capability_name"],
    )


def downgrade() -> None:
    """Drop agent-related tables."""

    # Drop indexes first

    op.drop_index("idx_agent_metrics_recorded_at")

    op.drop_index("idx_agent_metrics_name")

    op.drop_index("idx_agent_metrics_instance_id")

    op.drop_index("idx_agent_metrics_agent_id")

    op.drop_index("idx_agent_capabilities_type")

    op.drop_index("idx_agent_capabilities_name")

    op.drop_index("idx_agent_capabilities_agent_id")

    op.drop_index("idx_agent_deployments_created_at")

    op.drop_index("idx_agent_deployments_environment")

    op.drop_index("idx_agent_deployments_status")

    op.drop_index("idx_agent_deployments_agent_id")

    op.drop_index("idx_agent_instances_created_at")

    op.drop_index("idx_agent_instances_status")

    op.drop_index("idx_agent_instances_agent_id")

    op.drop_index("idx_agents_updated_at")

    op.drop_index("idx_agents_created_at")

    op.drop_index("idx_agents_status")

    op.drop_index("idx_agents_type")

    # Drop tables in reverse order of dependencies

    op.drop_table("agent_metrics")

    op.drop_table("agent_capabilities")

    op.drop_table("agent_deployments")

    op.drop_table("agent_instances")

    op.drop_table("agents")
