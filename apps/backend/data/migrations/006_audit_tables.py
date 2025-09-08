"""Migration 006: Create audit tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Constants


AUDIT_LOGS_TABLE = "audit_logs"


SYSTEM_EVENTS_TABLE = "system_events"


SECURITY_EVENTS_TABLE = "security_events"


def upgrade() -> None:
    """Create audit and security-related tables."""

    # Create audit_logs table

    op.create_table(
        AUDIT_LOGS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("session_id", sa.String(100), nullable=True),
        sa.Column("action", sa.String(255), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(36), nullable=True),
        sa.Column("resource_name", sa.String(255), nullable=True),
        sa.Column(
            "operation", sa.String(50), nullable=False
        ),  # CREATE, READ, UPDATE, DELETE
        sa.Column("status", sa.String(50), nullable=False),  # SUCCESS, FAILURE, PARTIAL
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("request_id", sa.String(100), nullable=True),
        sa.Column("api_endpoint", sa.String(255), nullable=True),
        sa.Column("http_method", sa.String(10), nullable=True),
        sa.Column("request_payload", postgresql.JSONB, nullable=True),
        sa.Column("response_payload", postgresql.JSONB, nullable=True),
        sa.Column("before_state", postgresql.JSONB, nullable=True),
        sa.Column("after_state", postgresql.JSONB, nullable=True),
        sa.Column("changes", postgresql.JSONB, nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("tags", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column(
            "risk_level", sa.String(50), nullable=False, default="low"
        ),  # low, medium, high, critical
        sa.Column("compliance_flags", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("duration_ms", sa.Integer, nullable=True),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column(
            "timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create system_events table

    op.create_table(
        SYSTEM_EVENTS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("event_name", sa.String(255), nullable=False),
        sa.Column("event_category", sa.String(100), nullable=False),
        sa.Column(
            "severity", sa.String(50), nullable=False, default="info"
        ),  # debug, info, warning, error, critical
        sa.Column(
            "source", sa.String(100), nullable=False
        ),  # api, worker, agent, system
        sa.Column("component", sa.String(100), nullable=True),
        sa.Column("service", sa.String(100), nullable=True),
        sa.Column("host", sa.String(255), nullable=True),
        sa.Column("environment", sa.String(50), nullable=True),
        sa.Column("version", sa.String(50), nullable=True),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("details", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("context", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metrics", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("tags", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("correlation_id", sa.String(100), nullable=True),
        sa.Column("trace_id", sa.String(100), nullable=True),
        sa.Column("span_id", sa.String(100), nullable=True),
        sa.Column(
            "parent_event_id",
            sa.String(36),
            sa.ForeignKey(f"{SYSTEM_EVENTS_TABLE}.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("resolved", sa.Boolean, nullable=False, default=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_by", sa.String(36), nullable=True),
        sa.Column("resolution_notes", sa.Text, nullable=True),
        sa.Column(
            "occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create security_events table

    op.create_table(
        SECURITY_EVENTS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "event_type", sa.String(100), nullable=False
        ),  # auth_failure, suspicious_activity, etc.
        sa.Column(
            "threat_level", sa.String(50), nullable=False, default="low"
        ),  # low, medium, high, critical
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("session_id", sa.String(100), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("location_country", sa.String(2), nullable=True),
        sa.Column("location_city", sa.String(100), nullable=True),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("details", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("indicators", postgresql.JSONB, nullable=False, default="[]"),  # IOCs
        sa.Column("mitigation_actions", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("affected_resources", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("attack_vector", sa.String(100), nullable=True),
        sa.Column("attack_stage", sa.String(100), nullable=True),
        sa.Column("confidence_score", sa.Float, nullable=True),  # 0.0 to 1.0
        sa.Column("false_positive", sa.Boolean, nullable=False, default=False),
        sa.Column("investigated", sa.Boolean, nullable=False, default=False),
        sa.Column("investigated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("investigated_by", sa.String(36), nullable=True),
        sa.Column("investigation_notes", sa.Text, nullable=True),
        sa.Column("blocked", sa.Boolean, nullable=False, default=False),
        sa.Column("blocked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("blocked_by", sa.String(36), nullable=True),
        sa.Column("blocking_reason", sa.Text, nullable=True),
        sa.Column("related_event_ids", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("alert_sent", sa.Boolean, nullable=False, default=False),
        sa.Column("alert_sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create compliance_logs table

    op.create_table(
        "compliance_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "compliance_framework", sa.String(100), nullable=False
        ),  # GDPR, CCPA, SOX, etc.
        sa.Column("requirement_id", sa.String(100), nullable=False),
        sa.Column("requirement_description", sa.Text, nullable=False),
        sa.Column(
            "audit_log_id",
            sa.String(36),
            sa.ForeignKey(f"{AUDIT_LOGS_TABLE}.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("data_subject_id", sa.String(36), nullable=True),
        sa.Column("action_type", sa.String(100), nullable=False),
        sa.Column("data_categories", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("lawful_basis", sa.String(100), nullable=True),
        sa.Column("consent_id", sa.String(36), nullable=True),
        sa.Column("retention_period", sa.Interval, nullable=True),
        sa.Column("deletion_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "compliance_status", sa.String(50), nullable=False, default="compliant"
        ),
        sa.Column("violations", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column(
            "remediation_actions", postgresql.JSONB, nullable=False, default="[]"
        ),
        sa.Column("evidence", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create data_retention_logs table

    op.create_table(
        "data_retention_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(36), nullable=False),
        sa.Column("retention_policy_id", sa.String(36), nullable=True),
        sa.Column("retention_period", sa.Interval, nullable=False),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expiry_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "status", sa.String(50), nullable=False, default="active"
        ),  # active, expired, deleted, archived
        sa.Column("deletion_reason", sa.String(255), nullable=True),
        sa.Column("deleted_by", sa.String(36), nullable=True),
        sa.Column("backup_location", sa.String(500), nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create access_control_logs table

    op.create_table(
        "access_control_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("session_id", sa.String(100), nullable=True),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(36), nullable=True),
        sa.Column("permission", sa.String(100), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("access_granted", sa.Boolean, nullable=False),
        sa.Column("deny_reason", sa.String(255), nullable=True),
        sa.Column("policy_id", sa.String(36), nullable=True),
        sa.Column("role", sa.String(100), nullable=True),
        sa.Column("context", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column(
            "timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create indexes for audit_logs table

    op.create_index("idx_audit_logs_user_id", AUDIT_LOGS_TABLE, ["user_id"])

    op.create_index("idx_audit_logs_session_id", AUDIT_LOGS_TABLE, ["session_id"])

    op.create_index("idx_audit_logs_action", AUDIT_LOGS_TABLE, ["action"])

    op.create_index("idx_audit_logs_resource_type", AUDIT_LOGS_TABLE, ["resource_type"])

    op.create_index("idx_audit_logs_resource_id", AUDIT_LOGS_TABLE, ["resource_id"])

    op.create_index("idx_audit_logs_operation", AUDIT_LOGS_TABLE, ["operation"])

    op.create_index("idx_audit_logs_status", AUDIT_LOGS_TABLE, ["status"])

    op.create_index("idx_audit_logs_risk_level", AUDIT_LOGS_TABLE, ["risk_level"])

    op.create_index("idx_audit_logs_timestamp", AUDIT_LOGS_TABLE, ["timestamp"])

    op.create_index("idx_audit_logs_created_at", AUDIT_LOGS_TABLE, ["created_at"])

    op.create_index(
        "idx_audit_logs_user_timestamp", AUDIT_LOGS_TABLE, ["user_id", "timestamp"]
    )

    op.create_index(
        "idx_audit_logs_resource_timestamp",
        AUDIT_LOGS_TABLE,
        ["resource_type", "resource_id", "timestamp"],
    )

    # Create GIN indexes for JSONB columns in audit_logs

    op.create_index(
        "idx_audit_logs_metadata_gin",
        AUDIT_LOGS_TABLE,
        ["metadata"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_audit_logs_tags_gin", AUDIT_LOGS_TABLE, ["tags"], postgresql_using="gin"
    )

    op.create_index(
        "idx_audit_logs_compliance_gin",
        AUDIT_LOGS_TABLE,
        ["compliance_flags"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_audit_logs_changes_gin",
        AUDIT_LOGS_TABLE,
        ["changes"],
        postgresql_using="gin",
    )

    # Create indexes for system_events table

    op.create_index("idx_system_events_event_type", SYSTEM_EVENTS_TABLE, ["event_type"])

    op.create_index("idx_system_events_event_name", SYSTEM_EVENTS_TABLE, ["event_name"])

    op.create_index(
        "idx_system_events_category", SYSTEM_EVENTS_TABLE, ["event_category"]
    )

    op.create_index("idx_system_events_severity", SYSTEM_EVENTS_TABLE, ["severity"])

    op.create_index("idx_system_events_source", SYSTEM_EVENTS_TABLE, ["source"])

    op.create_index("idx_system_events_component", SYSTEM_EVENTS_TABLE, ["component"])

    op.create_index(
        "idx_system_events_environment", SYSTEM_EVENTS_TABLE, ["environment"]
    )

    op.create_index(
        "idx_system_events_correlation_id", SYSTEM_EVENTS_TABLE, ["correlation_id"]
    )

    op.create_index("idx_system_events_trace_id", SYSTEM_EVENTS_TABLE, ["trace_id"])

    op.create_index(
        "idx_system_events_parent_event", SYSTEM_EVENTS_TABLE, ["parent_event_id"]
    )

    op.create_index("idx_system_events_resolved", SYSTEM_EVENTS_TABLE, ["resolved"])

    op.create_index(
        "idx_system_events_occurred_at", SYSTEM_EVENTS_TABLE, ["occurred_at"]
    )

    op.create_index("idx_system_events_created_at", SYSTEM_EVENTS_TABLE, ["created_at"])

    # Create GIN indexes for JSONB columns in system_events

    op.create_index(
        "idx_system_events_details_gin",
        SYSTEM_EVENTS_TABLE,
        ["details"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_system_events_context_gin",
        SYSTEM_EVENTS_TABLE,
        ["context"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_system_events_tags_gin",
        SYSTEM_EVENTS_TABLE,
        ["tags"],
        postgresql_using="gin",
    )

    # Create indexes for security_events table

    op.create_index(
        "idx_security_events_event_type", SECURITY_EVENTS_TABLE, ["event_type"]
    )

    op.create_index(
        "idx_security_events_threat_level", SECURITY_EVENTS_TABLE, ["threat_level"]
    )

    op.create_index("idx_security_events_user_id", SECURITY_EVENTS_TABLE, ["user_id"])

    op.create_index(
        "idx_security_events_ip_address", SECURITY_EVENTS_TABLE, ["ip_address"]
    )

    op.create_index(
        "idx_security_events_attack_vector", SECURITY_EVENTS_TABLE, ["attack_vector"]
    )

    op.create_index(
        "idx_security_events_false_positive", SECURITY_EVENTS_TABLE, ["false_positive"]
    )

    op.create_index(
        "idx_security_events_investigated", SECURITY_EVENTS_TABLE, ["investigated"]
    )

    op.create_index("idx_security_events_blocked", SECURITY_EVENTS_TABLE, ["blocked"])

    op.create_index(
        "idx_security_events_occurred_at", SECURITY_EVENTS_TABLE, ["occurred_at"]
    )

    op.create_index(
        "idx_security_events_created_at", SECURITY_EVENTS_TABLE, ["created_at"]
    )

    # Create indexes for compliance_logs table

    op.create_index(
        "idx_compliance_logs_framework", "compliance_logs", ["compliance_framework"]
    )

    op.create_index(
        "idx_compliance_logs_requirement", "compliance_logs", ["requirement_id"]
    )

    op.create_index(
        "idx_compliance_logs_audit_log", "compliance_logs", ["audit_log_id"]
    )

    op.create_index("idx_compliance_logs_user_id", "compliance_logs", ["user_id"])

    op.create_index(
        "idx_compliance_logs_data_subject", "compliance_logs", ["data_subject_id"]
    )

    op.create_index(
        "idx_compliance_logs_status", "compliance_logs", ["compliance_status"]
    )

    op.create_index("idx_compliance_logs_created_at", "compliance_logs", ["created_at"])

    # Create indexes for data_retention_logs table

    op.create_index(
        "idx_data_retention_resource",
        "data_retention_logs",
        ["resource_type", "resource_id"],
    )

    op.create_index("idx_data_retention_status", "data_retention_logs", ["status"])

    op.create_index(
        "idx_data_retention_expiry_date", "data_retention_logs", ["expiry_date"]
    )

    op.create_index(
        "idx_data_retention_created_at", "data_retention_logs", ["created_at"]
    )

    # Create indexes for access_control_logs table

    op.create_index("idx_access_control_user_id", "access_control_logs", ["user_id"])

    op.create_index(
        "idx_access_control_resource",
        "access_control_logs",
        ["resource_type", "resource_id"],
    )

    op.create_index(
        "idx_access_control_permission", "access_control_logs", ["permission"]
    )

    op.create_index(
        "idx_access_control_granted", "access_control_logs", ["access_granted"]
    )

    op.create_index(
        "idx_access_control_timestamp", "access_control_logs", ["timestamp"]
    )

    op.create_index(
        "idx_access_control_created_at", "access_control_logs", ["created_at"]
    )


def downgrade() -> None:
    """Drop audit and security-related tables."""

    # Drop indexes first

    op.drop_index("idx_access_control_created_at")

    op.drop_index("idx_access_control_timestamp")

    op.drop_index("idx_access_control_granted")

    op.drop_index("idx_access_control_permission")

    op.drop_index("idx_access_control_resource")

    op.drop_index("idx_access_control_user_id")

    op.drop_index("idx_data_retention_created_at")

    op.drop_index("idx_data_retention_expiry_date")

    op.drop_index("idx_data_retention_status")

    op.drop_index("idx_data_retention_resource")

    op.drop_index("idx_compliance_logs_created_at")

    op.drop_index("idx_compliance_logs_status")

    op.drop_index("idx_compliance_logs_data_subject")

    op.drop_index("idx_compliance_logs_user_id")

    op.drop_index("idx_compliance_logs_audit_log")

    op.drop_index("idx_compliance_logs_requirement")

    op.drop_index("idx_compliance_logs_framework")

    op.drop_index("idx_security_events_created_at")

    op.drop_index("idx_security_events_occurred_at")

    op.drop_index("idx_security_events_blocked")

    op.drop_index("idx_security_events_investigated")

    op.drop_index("idx_security_events_false_positive")

    op.drop_index("idx_security_events_attack_vector")

    op.drop_index("idx_security_events_ip_address")

    op.drop_index("idx_security_events_user_id")

    op.drop_index("idx_security_events_threat_level")

    op.drop_index("idx_security_events_event_type")

    op.drop_index("idx_system_events_tags_gin")

    op.drop_index("idx_system_events_context_gin")

    op.drop_index("idx_system_events_details_gin")

    op.drop_index("idx_system_events_created_at")

    op.drop_index("idx_system_events_occurred_at")

    op.drop_index("idx_system_events_resolved")

    op.drop_index("idx_system_events_parent_event")

    op.drop_index("idx_system_events_trace_id")

    op.drop_index("idx_system_events_correlation_id")

    op.drop_index("idx_system_events_environment")

    op.drop_index("idx_system_events_component")

    op.drop_index("idx_system_events_source")

    op.drop_index("idx_system_events_severity")

    op.drop_index("idx_system_events_category")

    op.drop_index("idx_system_events_event_name")

    op.drop_index("idx_system_events_event_type")

    op.drop_index("idx_audit_logs_changes_gin")

    op.drop_index("idx_audit_logs_compliance_gin")

    op.drop_index("idx_audit_logs_tags_gin")

    op.drop_index("idx_audit_logs_metadata_gin")

    op.drop_index("idx_audit_logs_resource_timestamp")

    op.drop_index("idx_audit_logs_user_timestamp")

    op.drop_index("idx_audit_logs_created_at")

    op.drop_index("idx_audit_logs_timestamp")

    op.drop_index("idx_audit_logs_risk_level")

    op.drop_index("idx_audit_logs_status")

    op.drop_index("idx_audit_logs_operation")

    op.drop_index("idx_audit_logs_resource_id")

    op.drop_index("idx_audit_logs_resource_type")

    op.drop_index("idx_audit_logs_action")

    op.drop_index("idx_audit_logs_session_id")

    op.drop_index("idx_audit_logs_user_id")

    # Drop tables in reverse order of dependencies

    op.drop_table("access_control_logs")

    op.drop_table("data_retention_logs")

    op.drop_table("compliance_logs")

    op.drop_table(SECURITY_EVENTS_TABLE)

    op.drop_table(SYSTEM_EVENTS_TABLE)

    op.drop_table(AUDIT_LOGS_TABLE)
