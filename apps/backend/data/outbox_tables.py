"""Outbox pattern database tables (SQLAlchemy 2.x async)."""

from __future__ import annotations

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
    text,
)

metadata = MetaData(schema=None)  # Đặt schema nếu dùng multi-schema

outbox_events = Table(
    "outbox_events",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("event_id", String(64), nullable=False, unique=True),
    Column("event_type", String(128), nullable=False, index=True),
    Column("schema_version", String(16), nullable=False),
    Column("partition_key", BigInteger, nullable=False, index=True),
    Column("payload", JSON, nullable=False),
    Column("next_run_at", DateTime(timezone=True), nullable=False, index=True),
    Column("attempts", Integer, nullable=False, server_default=text("0")),
    Column("backoff_sec", Integer, nullable=False, server_default=text("0")),
    Column("locked_at", DateTime(timezone=True), nullable=True, index=True),
    Column("lock_owner", String(64), nullable=True, index=True),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
)

# Composite index cho performance tối ưu
Index("ix_outbox_due", outbox_events.c.next_run_at, outbox_events.c.partition_key)
Index(
    "ix_outbox_partition_status",
    outbox_events.c.partition_key,
    outbox_events.c.locked_at,
)

outbox_dlq = Table(
    "outbox_dlq",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("event_id", String(64), nullable=False, index=True),
    Column("event_type", String(128), nullable=False, index=True),
    Column("schema_version", String(16), nullable=False),
    Column("partition_key", BigInteger, nullable=False, index=True),
    Column("payload", JSON, nullable=False),
    Column("error", Text, nullable=False),
    Column("attempts", Integer, nullable=False, server_default=text("0")),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column("archived", Boolean, nullable=False, server_default=text("false")),
)

processed_message = Table(
    "processed_message",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("handler", String(128), nullable=False),
    Column("message_key", String(128), nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), index=True
    ),
)

# Unique constraint cho idempotency
Index(
    "uq_processed_handler_key",
    processed_message.c.handler,
    processed_message.c.message_key,
    unique=True,
)
