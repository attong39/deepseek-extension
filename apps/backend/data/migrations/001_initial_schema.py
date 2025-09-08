"""Initial database schema migration.





This migration creates the base structure for the ZETA AI system.


"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op


def upgrade() -> None:
    """Create initial database schema."""

    # Create agents table

    op.create_table(
        "agents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("agent_type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, default="active"),
        sa.Column("configuration", sa.JSON),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.Column("created_by", sa.String(255)),
        sa.Column("version", sa.String(20), default="1.0.0"),
    )

    # Create chats table

    op.create_table(
        "chats",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("agent_id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36)),
        sa.Column("title", sa.String(255)),
        sa.Column("status", sa.String(20), nullable=False, default="active"),
        sa.Column("metadata", sa.JSON),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
    )

    # Create messages table

    op.create_table(
        "messages",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("chat_id", sa.String(36), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("timestamp", sa.DateTime, nullable=False),
        sa.Column("metadata", sa.JSON),
        sa.Column("processing_time", sa.Float),
        sa.ForeignKeyConstraint(["chat_id"], ["chats.id"]),
    )

    # Create memories table

    op.create_table(
        "memories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("agent_id", sa.String(36), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("memory_type", sa.String(50), nullable=False),
        sa.Column("importance_score", sa.Float, default=0.5),
        sa.Column("embedding", sa.JSON),
        sa.Column("metadata", sa.JSON),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("accessed_at", sa.DateTime),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
    )


def downgrade() -> None:
    """Drop initial database schema."""

    op.drop_table("memories")

    op.drop_table("messages")

    op.drop_table("chats")

    op.drop_table("agents")
