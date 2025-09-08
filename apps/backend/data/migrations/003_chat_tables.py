"""Migration 003: Create chat tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Constants


USERS_TABLE = "users"


CONVERSATIONS_TABLE = "conversations"


MESSAGES_TABLE = "messages"


MESSAGE_ATTACHMENTS_TABLE = "message_attachments"


def upgrade() -> None:
    """Create chat-related tables."""

    # Create users table

    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("username", sa.String(255), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("preferences", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
        sa.Column("is_verified", sa.Boolean, nullable=False, default=False),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Create conversations table

    op.create_table(
        CONVERSATIONS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey(f"{USERS_TABLE}.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(500), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("status", sa.String(50), nullable=False, default="active"),
        sa.Column("conversation_type", sa.String(100), nullable=False, default="chat"),
        sa.Column("agent_id", sa.String(36), nullable=True),
        sa.Column("context", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("settings", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("tags", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("message_count", sa.Integer, nullable=False, default=0),
        sa.Column("last_message_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("is_archived", sa.Boolean, nullable=False, default=False),
    )

    # Create messages table

    op.create_table(
        MESSAGES_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "conversation_id",
            sa.String(36),
            sa.ForeignKey(f"{CONVERSATIONS_TABLE}.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey(f"{USERS_TABLE}.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("agent_id", sa.String(36), nullable=True),
        sa.Column("role", sa.String(50), nullable=False),  # user, assistant, system
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("content_type", sa.String(100), nullable=False, default="text"),
        sa.Column("message_type", sa.String(100), nullable=False, default="message"),
        sa.Column(
            "parent_message_id",
            sa.String(36),
            sa.ForeignKey(f"{MESSAGES_TABLE}.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("thread_id", sa.String(36), nullable=True),
        sa.Column("sequence_number", sa.Integer, nullable=False),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("context", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("attachments_count", sa.Integer, nullable=False, default=0),
        sa.Column("tokens_used", sa.Integer, nullable=True),
        sa.Column("processing_time_ms", sa.Integer, nullable=True),
        sa.Column("model_used", sa.String(100), nullable=True),
        sa.Column("temperature", sa.Float, nullable=True),
        sa.Column("is_edited", sa.Boolean, nullable=False, default=False),
        sa.Column("edit_count", sa.Integer, nullable=False, default=0),
        sa.Column("edited_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create message_attachments table

    op.create_table(
        MESSAGE_ATTACHMENTS_TABLE,
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "message_id",
            sa.String(36),
            sa.ForeignKey(f"{MESSAGES_TABLE}.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_type", sa.String(100), nullable=False),
        sa.Column("file_size", sa.BigInteger, nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("file_url", sa.String(500), nullable=True),
        sa.Column("mime_type", sa.String(255), nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "processing_status", sa.String(50), nullable=False, default="pending"
        ),
        sa.Column("processing_result", postgresql.JSONB, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create conversation_participants table (for multi-user conversations)

    op.create_table(
        "conversation_participants",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "conversation_id",
            sa.String(36),
            sa.ForeignKey(f"{CONVERSATIONS_TABLE}.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey(f"{USERS_TABLE}.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "role", sa.String(50), nullable=False, default="participant"
        ),  # owner, participant, observer
        sa.Column("permissions", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "joined_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("left_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, default=True),
        sa.Column("last_read_message_id", sa.String(36), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create message_reactions table

    op.create_table(
        "message_reactions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "message_id",
            sa.String(36),
            sa.ForeignKey(f"{MESSAGES_TABLE}.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.String(36),
            sa.ForeignKey(f"{USERS_TABLE}.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "reaction_type", sa.String(50), nullable=False
        ),  # like, dislike, helpful, etc.
        sa.Column("emoji", sa.String(10), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create indexes for users table

    op.create_index("idx_users_username", USERS_TABLE, ["username"])

    op.create_index("idx_users_email", USERS_TABLE, ["email"])

    op.create_index("idx_users_is_active", USERS_TABLE, ["is_active"])

    op.create_index("idx_users_created_at", USERS_TABLE, ["created_at"])

    op.create_index("idx_users_last_login_at", USERS_TABLE, ["last_login_at"])

    # Create indexes for conversations table

    op.create_index("idx_conversations_user_id", CONVERSATIONS_TABLE, ["user_id"])

    op.create_index("idx_conversations_status", CONVERSATIONS_TABLE, ["status"])

    op.create_index(
        "idx_conversations_type", CONVERSATIONS_TABLE, ["conversation_type"]
    )

    op.create_index("idx_conversations_agent_id", CONVERSATIONS_TABLE, ["agent_id"])

    op.create_index("idx_conversations_created_at", CONVERSATIONS_TABLE, ["created_at"])

    op.create_index("idx_conversations_updated_at", CONVERSATIONS_TABLE, ["updated_at"])

    op.create_index(
        "idx_conversations_last_message_at", CONVERSATIONS_TABLE, ["last_message_at"]
    )

    op.create_index(
        "idx_conversations_is_archived", CONVERSATIONS_TABLE, ["is_archived"]
    )

    op.create_index(
        "idx_conversations_user_status", CONVERSATIONS_TABLE, ["user_id", "status"]
    )

    # Create GIN indexes for JSONB columns in conversations

    op.create_index(
        "idx_conversations_context_gin",
        CONVERSATIONS_TABLE,
        ["context"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_conversations_metadata_gin",
        CONVERSATIONS_TABLE,
        ["metadata"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_conversations_tags_gin",
        CONVERSATIONS_TABLE,
        ["tags"],
        postgresql_using="gin",
    )

    # Create indexes for messages table

    op.create_index("idx_messages_conversation_id", MESSAGES_TABLE, ["conversation_id"])

    op.create_index("idx_messages_user_id", MESSAGES_TABLE, ["user_id"])

    op.create_index("idx_messages_agent_id", MESSAGES_TABLE, ["agent_id"])

    op.create_index("idx_messages_role", MESSAGES_TABLE, ["role"])

    op.create_index("idx_messages_message_type", MESSAGES_TABLE, ["message_type"])

    op.create_index(
        "idx_messages_parent_message_id", MESSAGES_TABLE, ["parent_message_id"]
    )

    op.create_index("idx_messages_thread_id", MESSAGES_TABLE, ["thread_id"])

    op.create_index("idx_messages_sequence_number", MESSAGES_TABLE, ["sequence_number"])

    op.create_index("idx_messages_created_at", MESSAGES_TABLE, ["created_at"])

    op.create_index("idx_messages_updated_at", MESSAGES_TABLE, ["updated_at"])

    op.create_index(
        "idx_messages_conv_sequence",
        MESSAGES_TABLE,
        ["conversation_id", "sequence_number"],
    )

    op.create_index("idx_messages_is_edited", MESSAGES_TABLE, ["is_edited"])

    # Create GIN indexes for JSONB columns in messages

    op.create_index(
        "idx_messages_metadata_gin",
        MESSAGES_TABLE,
        ["metadata"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_messages_context_gin", MESSAGES_TABLE, ["context"], postgresql_using="gin"
    )

    # Create full-text search index for message content

    op.create_index(
        "idx_messages_content_fts",
        MESSAGES_TABLE,
        [sa.text("to_tsvector('english', content)")],
        postgresql_using="gin",
    )

    # Create indexes for message_attachments table

    op.create_index(
        "idx_message_attachments_message_id", MESSAGE_ATTACHMENTS_TABLE, ["message_id"]
    )

    op.create_index(
        "idx_message_attachments_file_type", MESSAGE_ATTACHMENTS_TABLE, ["file_type"]
    )

    op.create_index(
        "idx_message_attachments_processing_status",
        MESSAGE_ATTACHMENTS_TABLE,
        ["processing_status"],
    )

    op.create_index(
        "idx_message_attachments_created_at", MESSAGE_ATTACHMENTS_TABLE, ["created_at"]
    )

    # Create indexes for conversation_participants table

    op.create_index(
        "idx_conv_participants_conversation_id",
        "conversation_participants",
        ["conversation_id"],
    )

    op.create_index(
        "idx_conv_participants_user_id", "conversation_participants", ["user_id"]
    )

    op.create_index("idx_conv_participants_role", "conversation_participants", ["role"])

    op.create_index(
        "idx_conv_participants_is_active", "conversation_participants", ["is_active"]
    )

    op.create_index(
        "idx_conv_participants_joined_at", "conversation_participants", ["joined_at"]
    )

    # Create indexes for message_reactions table

    op.create_index(
        "idx_message_reactions_message_id", "message_reactions", ["message_id"]
    )

    op.create_index("idx_message_reactions_user_id", "message_reactions", ["user_id"])

    op.create_index(
        "idx_message_reactions_type", "message_reactions", ["reaction_type"]
    )

    op.create_index(
        "idx_message_reactions_created_at", "message_reactions", ["created_at"]
    )

    # Create unique constraints

    op.create_unique_constraint(
        "uq_conv_participants_conv_user",
        "conversation_participants",
        ["conversation_id", "user_id"],
    )

    op.create_unique_constraint(
        "uq_message_reactions_message_user_type",
        "message_reactions",
        ["message_id", "user_id", "reaction_type"],
    )


def downgrade() -> None:
    """Drop chat-related tables."""

    # Drop indexes first

    op.drop_index("idx_message_reactions_created_at")

    op.drop_index("idx_message_reactions_type")

    op.drop_index("idx_message_reactions_user_id")

    op.drop_index("idx_message_reactions_message_id")

    op.drop_index("idx_conv_participants_joined_at")

    op.drop_index("idx_conv_participants_is_active")

    op.drop_index("idx_conv_participants_role")

    op.drop_index("idx_conv_participants_user_id")

    op.drop_index("idx_conv_participants_conversation_id")

    op.drop_index("idx_message_attachments_created_at")

    op.drop_index("idx_message_attachments_processing_status")

    op.drop_index("idx_message_attachments_file_type")

    op.drop_index("idx_message_attachments_message_id")

    op.drop_index("idx_messages_content_fts")

    op.drop_index("idx_messages_context_gin")

    op.drop_index("idx_messages_metadata_gin")

    op.drop_index("idx_messages_is_edited")

    op.drop_index("idx_messages_conv_sequence")

    op.drop_index("idx_messages_updated_at")

    op.drop_index("idx_messages_created_at")

    op.drop_index("idx_messages_sequence_number")

    op.drop_index("idx_messages_thread_id")

    op.drop_index("idx_messages_parent_message_id")

    op.drop_index("idx_messages_message_type")

    op.drop_index("idx_messages_role")

    op.drop_index("idx_messages_agent_id")

    op.drop_index("idx_messages_user_id")

    op.drop_index("idx_messages_conversation_id")

    op.drop_index("idx_conversations_tags_gin")

    op.drop_index("idx_conversations_metadata_gin")

    op.drop_index("idx_conversations_context_gin")

    op.drop_index("idx_conversations_user_status")

    op.drop_index("idx_conversations_is_archived")

    op.drop_index("idx_conversations_last_message_at")

    op.drop_index("idx_conversations_updated_at")

    op.drop_index("idx_conversations_created_at")

    op.drop_index("idx_conversations_agent_id")

    op.drop_index("idx_conversations_type")

    op.drop_index("idx_conversations_status")

    op.drop_index("idx_conversations_user_id")

    op.drop_index("idx_users_last_login_at")

    op.drop_index("idx_users_created_at")

    op.drop_index("idx_users_is_active")

    op.drop_index("idx_users_email")

    op.drop_index("idx_users_username")

    # Drop tables in reverse order of dependencies

    op.drop_table("message_reactions")

    op.drop_table("conversation_participants")

    op.drop_table(MESSAGE_ATTACHMENTS_TABLE)

    op.drop_table(MESSAGES_TABLE)

    op.drop_table(CONVERSATIONS_TABLE)

    op.drop_table(USERS_TABLE)
