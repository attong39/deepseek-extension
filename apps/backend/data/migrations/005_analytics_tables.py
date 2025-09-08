"""Migration 005: Create analytics tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Constants


ANALYTICS_EVENTS_TABLE = "analytics_events"


USER_SESSIONS_TABLE = "user_sessions"


PERFORMANCE_METRICS_TABLE = "performance_metrics"


def upgrade() -> None:
    """Create analytics-related tables."""

    # Create analytics_events table

    op.create_table(
        ANALYTICS_EVENTS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("session_id", sa.String(100), nullable=True),
        sa.Column("event_type", sa.String(100), nullable=False),
        sa.Column("event_name", sa.String(255), nullable=False),
        sa.Column("event_category", sa.String(100), nullable=True),
        sa.Column("properties", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("context", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("referrer", sa.String(500), nullable=True),
        sa.Column("page_url", sa.String(500), nullable=True),
        sa.Column(
            "timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create user_sessions table

    op.create_table(
        USER_SESSIONS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("session_id", sa.String(100), nullable=False, unique=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("device_type", sa.String(50), nullable=True),
        sa.Column("browser", sa.String(100), nullable=True),
        sa.Column("os", sa.String(100), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("country", sa.String(2), nullable=True),  # ISO country code
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("timezone", sa.String(50), nullable=True),
        sa.Column("language", sa.String(10), nullable=True),
        sa.Column("properties", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "started_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_seconds", sa.Integer, nullable=True),
        sa.Column("page_views", sa.Integer, nullable=False, default=0),
        sa.Column("events_count", sa.Integer, nullable=False, default=0),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
        sa.Column(
            "last_activity_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create performance_metrics table

    op.create_table(
        PERFORMANCE_METRICS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("metric_name", sa.String(255), nullable=False),
        sa.Column(
            "metric_type", sa.String(100), nullable=False
        ),  # counter, gauge, histogram, etc.
        sa.Column("metric_value", sa.Float, nullable=False),
        sa.Column("metric_unit", sa.String(50), nullable=True),
        sa.Column("tags", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("source", sa.String(100), nullable=True),  # api, worker, agent, etc.
        sa.Column("environment", sa.String(50), nullable=True),  # prod, dev, test
        sa.Column("host", sa.String(255), nullable=True),
        sa.Column("service", sa.String(100), nullable=True),
        sa.Column(
            "recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create conversation_analytics table

    op.create_table(
        "conversation_analytics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("conversation_id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("message_count", sa.Integer, nullable=False, default=0),
        sa.Column("total_tokens_used", sa.Integer, nullable=False, default=0),
        sa.Column("avg_response_time_ms", sa.Float, nullable=True),
        sa.Column("user_satisfaction_score", sa.Float, nullable=True),
        sa.Column("conversation_duration_seconds", sa.Integer, nullable=True),
        sa.Column("topics", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("sentiment_scores", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("complexity_score", sa.Float, nullable=True),
        sa.Column("resolution_status", sa.String(50), nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "calculated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create agent_analytics table

    op.create_table(
        "agent_analytics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("agent_id", sa.String(36), nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("total_requests", sa.Integer, nullable=False, default=0),
        sa.Column("successful_requests", sa.Integer, nullable=False, default=0),
        sa.Column("failed_requests", sa.Integer, nullable=False, default=0),
        sa.Column("avg_response_time_ms", sa.Float, nullable=True),
        sa.Column("total_tokens_used", sa.Integer, nullable=False, default=0),
        sa.Column("total_cost", sa.Numeric(10, 4), nullable=False, default=0),
        sa.Column("uptime_percentage", sa.Float, nullable=True),
        sa.Column("error_rate_percentage", sa.Float, nullable=True),
        sa.Column("user_satisfaction_avg", sa.Float, nullable=True),
        sa.Column("peak_concurrent_users", sa.Integer, nullable=False, default=0),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "calculated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create usage_analytics table

    op.create_table(
        "usage_analytics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column(
            "metric_type", sa.String(100), nullable=False
        ),  # daily_active_users, messages_sent, etc.
        sa.Column("metric_value", sa.Float, nullable=False),
        sa.Column("dimensions", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("breakdown", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "calculated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create error_analytics table

    op.create_table(
        "error_analytics",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("error_type", sa.String(100), nullable=False),
        sa.Column("error_code", sa.String(50), nullable=True),
        sa.Column("error_message", sa.Text, nullable=False),
        sa.Column("stack_trace", sa.Text, nullable=True),
        sa.Column("context", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("session_id", sa.String(100), nullable=True),
        sa.Column("request_id", sa.String(100), nullable=True),
        sa.Column("endpoint", sa.String(255), nullable=True),
        sa.Column("method", sa.String(10), nullable=True),
        sa.Column("status_code", sa.Integer, nullable=True),
        sa.Column("environment", sa.String(50), nullable=True),
        sa.Column("service", sa.String(100), nullable=True),
        sa.Column("severity", sa.String(50), nullable=False, default="error"),
        sa.Column("resolved", sa.Boolean, nullable=False, default=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create indexes for analytics_events table

    op.create_index("idx_analytics_events_user_id", ANALYTICS_EVENTS_TABLE, ["user_id"])

    op.create_index(
        "idx_analytics_events_session_id", ANALYTICS_EVENTS_TABLE, ["session_id"]
    )

    op.create_index(
        "idx_analytics_events_event_type", ANALYTICS_EVENTS_TABLE, ["event_type"]
    )

    op.create_index(
        "idx_analytics_events_event_name", ANALYTICS_EVENTS_TABLE, ["event_name"]
    )

    op.create_index(
        "idx_analytics_events_category", ANALYTICS_EVENTS_TABLE, ["event_category"]
    )

    op.create_index(
        "idx_analytics_events_timestamp", ANALYTICS_EVENTS_TABLE, ["timestamp"]
    )

    op.create_index(
        "idx_analytics_events_created_at", ANALYTICS_EVENTS_TABLE, ["created_at"]
    )

    op.create_index(
        "idx_analytics_events_user_timestamp",
        ANALYTICS_EVENTS_TABLE,
        ["user_id", "timestamp"],
    )

    # Create GIN indexes for JSONB columns in analytics_events

    op.create_index(
        "idx_analytics_events_properties_gin",
        ANALYTICS_EVENTS_TABLE,
        ["properties"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_analytics_events_metadata_gin",
        ANALYTICS_EVENTS_TABLE,
        ["metadata"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_analytics_events_context_gin",
        ANALYTICS_EVENTS_TABLE,
        ["context"],
        postgresql_using="gin",
    )

    # Create indexes for user_sessions table

    op.create_index("idx_user_sessions_session_id", USER_SESSIONS_TABLE, ["session_id"])

    op.create_index("idx_user_sessions_user_id", USER_SESSIONS_TABLE, ["user_id"])

    op.create_index(
        "idx_user_sessions_device_type", USER_SESSIONS_TABLE, ["device_type"]
    )

    op.create_index("idx_user_sessions_started_at", USER_SESSIONS_TABLE, ["started_at"])

    op.create_index("idx_user_sessions_ended_at", USER_SESSIONS_TABLE, ["ended_at"])

    op.create_index("idx_user_sessions_is_active", USER_SESSIONS_TABLE, ["is_active"])

    op.create_index(
        "idx_user_sessions_last_activity", USER_SESSIONS_TABLE, ["last_activity_at"]
    )

    op.create_index("idx_user_sessions_country", USER_SESSIONS_TABLE, ["country"])

    # Create indexes for performance_metrics table

    op.create_index(
        "idx_performance_metrics_name", PERFORMANCE_METRICS_TABLE, ["metric_name"]
    )

    op.create_index(
        "idx_performance_metrics_type", PERFORMANCE_METRICS_TABLE, ["metric_type"]
    )

    op.create_index(
        "idx_performance_metrics_source", PERFORMANCE_METRICS_TABLE, ["source"]
    )

    op.create_index(
        "idx_performance_metrics_environment",
        PERFORMANCE_METRICS_TABLE,
        ["environment"],
    )

    op.create_index(
        "idx_performance_metrics_recorded_at",
        PERFORMANCE_METRICS_TABLE,
        ["recorded_at"],
    )

    op.create_index(
        "idx_performance_metrics_created_at", PERFORMANCE_METRICS_TABLE, ["created_at"]
    )

    op.create_index(
        "idx_performance_metrics_name_recorded",
        PERFORMANCE_METRICS_TABLE,
        ["metric_name", "recorded_at"],
    )

    # Create GIN indexes for JSONB columns in performance_metrics

    op.create_index(
        "idx_performance_metrics_tags_gin",
        PERFORMANCE_METRICS_TABLE,
        ["tags"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_performance_metrics_metadata_gin",
        PERFORMANCE_METRICS_TABLE,
        ["metadata"],
        postgresql_using="gin",
    )

    # Create indexes for conversation_analytics table

    op.create_index(
        "idx_conversation_analytics_conv_id",
        "conversation_analytics",
        ["conversation_id"],
    )

    op.create_index(
        "idx_conversation_analytics_user_id", "conversation_analytics", ["user_id"]
    )

    op.create_index(
        "idx_conversation_analytics_calculated_at",
        "conversation_analytics",
        ["calculated_at"],
    )

    op.create_index(
        "idx_conversation_analytics_satisfaction",
        "conversation_analytics",
        ["user_satisfaction_score"],
    )

    op.create_index(
        "idx_conversation_analytics_resolution",
        "conversation_analytics",
        ["resolution_status"],
    )

    # Create indexes for agent_analytics table

    op.create_index("idx_agent_analytics_agent_id", "agent_analytics", ["agent_id"])

    op.create_index("idx_agent_analytics_date", "agent_analytics", ["date"])

    op.create_index(
        "idx_agent_analytics_agent_date", "agent_analytics", ["agent_id", "date"]
    )

    op.create_index(
        "idx_agent_analytics_calculated_at", "agent_analytics", ["calculated_at"]
    )

    # Create indexes for usage_analytics table

    op.create_index("idx_usage_analytics_date", "usage_analytics", ["date"])

    op.create_index(
        "idx_usage_analytics_metric_type", "usage_analytics", ["metric_type"]
    )

    op.create_index(
        "idx_usage_analytics_date_type", "usage_analytics", ["date", "metric_type"]
    )

    op.create_index(
        "idx_usage_analytics_calculated_at", "usage_analytics", ["calculated_at"]
    )

    # Create indexes for error_analytics table

    op.create_index("idx_error_analytics_error_type", "error_analytics", ["error_type"])

    op.create_index("idx_error_analytics_error_code", "error_analytics", ["error_code"])

    op.create_index("idx_error_analytics_user_id", "error_analytics", ["user_id"])

    op.create_index("idx_error_analytics_session_id", "error_analytics", ["session_id"])

    op.create_index("idx_error_analytics_endpoint", "error_analytics", ["endpoint"])

    op.create_index("idx_error_analytics_severity", "error_analytics", ["severity"])

    op.create_index("idx_error_analytics_resolved", "error_analytics", ["resolved"])

    op.create_index(
        "idx_error_analytics_occurred_at", "error_analytics", ["occurred_at"]
    )

    op.create_index(
        "idx_error_analytics_environment", "error_analytics", ["environment"]
    )

    # Create unique constraints

    op.create_unique_constraint(
        "uq_agent_analytics_agent_date", "agent_analytics", ["agent_id", "date"]
    )

    op.create_unique_constraint(
        "uq_usage_analytics_date_type", "usage_analytics", ["date", "metric_type"]
    )


def downgrade() -> None:
    """Drop analytics-related tables."""

    # Drop indexes first

    op.drop_index("idx_error_analytics_environment")

    op.drop_index("idx_error_analytics_occurred_at")

    op.drop_index("idx_error_analytics_resolved")

    op.drop_index("idx_error_analytics_severity")

    op.drop_index("idx_error_analytics_endpoint")

    op.drop_index("idx_error_analytics_session_id")

    op.drop_index("idx_error_analytics_user_id")

    op.drop_index("idx_error_analytics_error_code")

    op.drop_index("idx_error_analytics_error_type")

    op.drop_index("idx_usage_analytics_calculated_at")

    op.drop_index("idx_usage_analytics_date_type")

    op.drop_index("idx_usage_analytics_metric_type")

    op.drop_index("idx_usage_analytics_date")

    op.drop_index("idx_agent_analytics_calculated_at")

    op.drop_index("idx_agent_analytics_agent_date")

    op.drop_index("idx_agent_analytics_date")

    op.drop_index("idx_agent_analytics_agent_id")

    op.drop_index("idx_conversation_analytics_resolution")

    op.drop_index("idx_conversation_analytics_satisfaction")

    op.drop_index("idx_conversation_analytics_calculated_at")

    op.drop_index("idx_conversation_analytics_user_id")

    op.drop_index("idx_conversation_analytics_conv_id")

    op.drop_index("idx_performance_metrics_metadata_gin")

    op.drop_index("idx_performance_metrics_tags_gin")

    op.drop_index("idx_performance_metrics_name_recorded")

    op.drop_index("idx_performance_metrics_created_at")

    op.drop_index("idx_performance_metrics_recorded_at")

    op.drop_index("idx_performance_metrics_environment")

    op.drop_index("idx_performance_metrics_source")

    op.drop_index("idx_performance_metrics_type")

    op.drop_index("idx_performance_metrics_name")

    op.drop_index("idx_user_sessions_country")

    op.drop_index("idx_user_sessions_last_activity")

    op.drop_index("idx_user_sessions_is_active")

    op.drop_index("idx_user_sessions_ended_at")

    op.drop_index("idx_user_sessions_started_at")

    op.drop_index("idx_user_sessions_device_type")

    op.drop_index("idx_user_sessions_user_id")

    op.drop_index("idx_user_sessions_session_id")

    op.drop_index("idx_analytics_events_context_gin")

    op.drop_index("idx_analytics_events_metadata_gin")

    op.drop_index("idx_analytics_events_properties_gin")

    op.drop_index("idx_analytics_events_user_timestamp")

    op.drop_index("idx_analytics_events_created_at")

    op.drop_index("idx_analytics_events_timestamp")

    op.drop_index("idx_analytics_events_category")

    op.drop_index("idx_analytics_events_event_name")

    op.drop_index("idx_analytics_events_event_type")

    op.drop_index("idx_analytics_events_session_id")

    op.drop_index("idx_analytics_events_user_id")

    # Drop tables in reverse order of dependencies

    op.drop_table("error_analytics")

    op.drop_table("usage_analytics")

    op.drop_table("agent_analytics")

    op.drop_table("conversation_analytics")

    op.drop_table(PERFORMANCE_METRICS_TABLE)

    op.drop_table(USER_SESSIONS_TABLE)

    op.drop_table(ANALYTICS_EVENTS_TABLE)
