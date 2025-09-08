"""Outbox hardening with DLQ, idempotency, and sharding.

Revision ID: outbox_hardening_v1
Revises: 011_release_table
Create Date: 2025-08-23 12:40:00.000000

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision = "outbox_hardening_v1"
down_revision = "011_release_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade to production-ready outbox pattern."""

    # Enhanced outbox messages table
    op.create_table(
        "outbox_messages",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("event_type", sa.String(256), nullable=False),
        sa.Column("schema_version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("payload", sa.Text, nullable=False),
        sa.Column(
            "partition_key", sa.String(128), nullable=True
        ),  # tenant_id for sharding
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("locked_by", sa.String(128), nullable=True),  # worker_id for claiming
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "next_attempt_at", sa.DateTime(timezone=True), nullable=True
        ),  # exponential backoff
        sa.Column("attempt", sa.Integer, nullable=False, server_default="0"),
        sa.Column("last_error", sa.Text, nullable=True),
        sa.Column("dispatched_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Performance indexes
    op.create_index(
        "ix_outbox_pending",
        "outbox_messages",
        ["dispatched_at", "next_attempt_at", "partition_key"],
        postgresql_where=sa.text("dispatched_at IS NULL"),
    )
    op.create_index("ix_outbox_created", "outbox_messages", ["created_at"])
    op.create_index("ix_outbox_partition", "outbox_messages", ["partition_key"])

    # Dead letter queue for failed events
    op.create_table(
        "dead_letter_messages",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("event_type", sa.String(256), nullable=False),
        sa.Column("schema_version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("payload", sa.Text, nullable=False),
        sa.Column(
            "failed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("attempt", sa.Integer, nullable=False),
        sa.Column("last_error", sa.Text, nullable=True),
        sa.Column("partition_key", sa.String(128), nullable=True),
    )
    op.create_index("ix_dlq_failed_at", "dead_letter_messages", ["failed_at"])
    op.create_index("ix_dlq_event_type", "dead_letter_messages", ["event_type"])

    # Idempotency tracking table
    op.create_table(
        "processed_events",
        sa.Column("event_id", sa.String(64), nullable=False),
        sa.Column("handler", sa.String(128), nullable=False),
        sa.Column(
            "processed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("partition_key", sa.String(128), nullable=True),
        sa.PrimaryKeyConstraint("event_id", "handler"),
    )
    op.create_index("ix_processed_events_time", "processed_events", ["processed_at"])

    # Event metrics table for monitoring
    op.create_table(
        "event_metrics",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("metric_name", sa.String(128), nullable=False),
        sa.Column("metric_value", sa.Float, nullable=False),
        sa.Column("labels", sa.JSON, nullable=True),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(
        "ix_metrics_name_time", "event_metrics", ["metric_name", "timestamp"]
    )


def downgrade() -> None:
    """Downgrade outbox hardening."""
    op.drop_table("event_metrics")
    op.drop_table("processed_events")
    op.drop_table("dead_letter_messages")
    op.drop_table("outbox_messages")
