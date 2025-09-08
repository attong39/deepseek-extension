"""Add outbox tables migration.

Revision ID: 001_outbox_tables
Create Date: 2025-08-23
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "001_outbox_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create outbox pattern tables."""

    # outbox_events table
    op.create_table(
        "outbox_events",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.String(64), nullable=False),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("schema_version", sa.String(16), nullable=False),
        sa.Column("partition_key", sa.BigInteger(), nullable=False),
        sa.Column("payload", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "attempts", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column(
            "backoff_sec", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("lock_owner", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id"),
    )

    # Indexes cho performance
    op.create_index("ix_outbox_events_event_type", "outbox_events", ["event_type"])
    op.create_index(
        "ix_outbox_events_partition_key", "outbox_events", ["partition_key"]
    )
    op.create_index("ix_outbox_events_next_run_at", "outbox_events", ["next_run_at"])
    op.create_index("ix_outbox_events_locked_at", "outbox_events", ["locked_at"])
    op.create_index("ix_outbox_events_lock_owner", "outbox_events", ["lock_owner"])

    # Composite indexes cho worker queries
    op.create_index("ix_outbox_due", "outbox_events", ["next_run_at", "partition_key"])
    op.create_index(
        "ix_outbox_partition_status", "outbox_events", ["partition_key", "locked_at"]
    )

    # outbox_dlq table
    op.create_table(
        "outbox_dlq",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("event_id", sa.String(64), nullable=False),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("schema_version", sa.String(16), nullable=False),
        sa.Column("partition_key", sa.BigInteger(), nullable=False),
        sa.Column("payload", postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column("error", sa.Text(), nullable=False),
        sa.Column(
            "attempts", sa.Integer(), server_default=sa.text("0"), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "archived", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # DLQ indexes
    op.create_index("ix_outbox_dlq_event_id", "outbox_dlq", ["event_id"])
    op.create_index("ix_outbox_dlq_event_type", "outbox_dlq", ["event_type"])
    op.create_index("ix_outbox_dlq_partition_key", "outbox_dlq", ["partition_key"])

    # processed_message table cho idempotency
    op.create_table(
        "processed_message",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("handler", sa.String(128), nullable=False),
        sa.Column("message_key", sa.String(128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Unique constraint cho idempotency
    op.create_index(
        "ix_processed_message_created_at", "processed_message", ["created_at"]
    )
    op.create_index(
        "uq_processed_handler_key",
        "processed_message",
        ["handler", "message_key"],
        unique=True,
    )


def downgrade() -> None:
    """Drop outbox tables."""
    op.drop_table("processed_message")
    op.drop_table("outbox_dlq")
    op.drop_table("outbox_events")
