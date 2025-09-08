"""Migration 008: Targeted performance indexes for agents and messages.

- agents(status, created_at)
- messages(conversation_id, created_at DESC)

Note: The originally requested index for chat_messages(session_id, created_at DESC)
has been adapted to messages(conversation_id, created_at DESC) because the current
schema does not include a session_id on messages. Conversations are the owning
scope for messages in this schema.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op


def upgrade() -> None:  # noqa: D401
    """Create targeted composite indexes for common query patterns."""

    # Composite on agents to accelerate status + time listings
    op.create_index(
        "idx_agents_status_created",
        "agents",
        ["status", "created_at"],
    )

    # Optimize fetching latest messages per conversation
    # DESC ordering on created_at improves ORDER BY created_at DESC queries
    op.create_index(
        "idx_messages_conversation_created_desc",
        "messages",
        ["conversation_id", sa.text("created_at DESC")],
    )


def downgrade() -> None:  # noqa: D401
    """Drop targeted composite indexes."""

    op.drop_index("idx_messages_conversation_created_desc")
    op.drop_index("idx_agents_status_created")
