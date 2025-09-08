"""Outbox DLQ init.

Create tables for Outbox pattern với DLQ support và idempotency.

Revision ID: 20250823_outbox_dlq_init
Revises:
Create Date: 2025-08-23

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision = "20250823_outbox_dlq_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create outbox, DLQ và processed_message tables."""

    # Outbox events table
    op.create_table(
        "outbox_events",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("event_id", sa.String(64), nullable=False, unique=True),
        sa.Column("event_type", sa.String(128), nullable=False, index=True),
        sa.Column("schema_version", sa.String(16), nullable=False, default="evt.v1"),
        sa.Column("partition_key", sa.BigInteger, nullable=False, index=True),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column(
            "next_run_at", sa.DateTime(timezone=True), nullable=False, index=True
        ),
        sa.Column("attempts", sa.Integer, nullable=False, default=0),
        sa.Column("backoff_sec", sa.Integer, nullable=False, default=0),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("lock_owner", sa.String(64), nullable=True, index=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.UniqueConstraint("event_id", name="uq_outbox_event_id"),
        comment="Outbox events chờ processing",
    )

    # Composite index cho efficient polling
    op.create_index(
        "ix_outbox_due",
        "outbox_events",
        ["next_run_at", "partition_key"],
        comment="Index cho worker polling với sharding",
    )

    # Index cho lock management
    op.create_index(
        "ix_outbox_locks",
        "outbox_events",
        ["locked_at", "lock_owner"],
        comment="Index cho lock cleanup",
    )

    # Dead Letter Queue table
    op.create_table(
        "outbox_dlq",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("event_id", sa.String(64), nullable=False, index=True),
        sa.Column("event_type", sa.String(128), nullable=False, index=True),
        sa.Column("schema_version", sa.String(16), nullable=False),
        sa.Column("partition_key", sa.BigInteger, nullable=False, index=True),
        sa.Column("payload", sa.JSON, nullable=False),
        sa.Column("error", sa.Text, nullable=False),
        sa.Column("attempts", sa.Integer, nullable=False, default=0),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "archived", sa.Boolean, nullable=False, server_default=sa.text("false")
        ),
        comment="Dead Letter Queue cho events failed",
    )

    # Index cho DLQ management
    op.create_index(
        "ix_dlq_management",
        "outbox_dlq",
        ["created_at", "archived", "event_type"],
        comment="Index cho DLQ queries và cleanup",
    )

    # Processed messages table cho idempotency
    op.create_table(
        "processed_message",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("handler", sa.String(128), nullable=False),
        sa.Column("message_key", sa.String(128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            index=True,
        ),
        sa.UniqueConstraint("handler", "message_key", name="uq_processed_handler_key"),
        comment="Idempotency tracking cho exactly-once processing",
    )

    # Index cho TTL cleanup (optional)
    op.create_index(
        "ix_processed_cleanup",
        "processed_message",
        ["created_at"],
        comment="Index cho cleanup cũ processed records",
    )


def downgrade() -> None:
    """Drop tất cả outbox tables."""
    op.drop_table("processed_message")
    op.drop_table("outbox_dlq")
    op.drop_table("outbox_events")
