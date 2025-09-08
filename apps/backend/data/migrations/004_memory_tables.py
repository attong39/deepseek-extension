"""Migration 004: Create memory tables."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade() -> None:
    """Create memory-related tables."""

    # Create memories table

    op.create_table(
        "memories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("memory_type", sa.String(100), nullable=False, default="general"),
        sa.Column("importance_score", sa.Float, nullable=False, default=0.5),
        sa.Column("access_count", sa.Integer, nullable=False, default=0),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("tags", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("embedding_vector", postgresql.ARRAY(sa.Float), nullable=True),
        sa.Column("compression_type", sa.String(50), nullable=True),
        sa.Column("original_length", sa.Integer, nullable=True),
        sa.Column("compressed_length", sa.Integer, nullable=True),
        sa.Column("related_memories", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("context_window", sa.Text, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("last_accessed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_archived", sa.Boolean, nullable=False, default=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Create memory_associations table (for memory relationships)

    op.create_table(
        "memory_associations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "source_memory_id",
            sa.String(36),
            sa.ForeignKey("memories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "target_memory_id",
            sa.String(36),
            sa.ForeignKey("memories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("association_type", sa.String(100), nullable=False),
        sa.Column("strength", sa.Float, nullable=False, default=1.0),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create memory_summaries table (for compressed summaries)

    op.create_table(
        "memory_summaries",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("summary_type", sa.String(100), nullable=False),
        sa.Column(
            "target_type", sa.String(100), nullable=False
        ),  # conversation, topic, daily, etc.
        sa.Column("target_id", sa.String(36), nullable=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("source_memories", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("word_count", sa.Integer, nullable=False, default=0),
        sa.Column("compression_ratio", sa.Float, nullable=True),
        sa.Column("validity_period", sa.Interval, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Create memory_backups table

    op.create_table(
        "memory_backups",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("backup_type", sa.String(50), nullable=False),  # full, incremental
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("memory_count", sa.Integer, nullable=False, default=0),
        sa.Column("backup_path", sa.String(500), nullable=False),
        sa.Column("file_size_bytes", sa.BigInteger, nullable=False, default=0),
        sa.Column("compression_enabled", sa.Boolean, nullable=False, default=False),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column(
            "base_backup_id", sa.String(36), nullable=True
        ),  # for incremental backups
        sa.Column("status", sa.String(50), nullable=False, default="pending"),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(36), nullable=True),
    )

    # Create memory_access_logs table (for tracking access patterns)

    op.create_table(
        "memory_access_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "memory_id",
            sa.String(36),
            sa.ForeignKey("memories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column(
            "access_type", sa.String(50), nullable=False
        ),  # read, write, update, delete
        sa.Column("context", sa.String(500), nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=False, default="{}"),
        sa.Column("session_id", sa.String(100), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column(
            "accessed_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create memory_search_index table (for full-text search optimization)

    op.create_table(
        "memory_search_index",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "memory_id",
            sa.String(36),
            sa.ForeignKey("memories.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("search_vector", postgresql.TSVECTOR, nullable=False),
        sa.Column("keywords", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("entities", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("topics", postgresql.JSONB, nullable=False, default="[]"),
        sa.Column("language", sa.String(10), nullable=False, default="en"),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
    )

    # Create indexes for memories table

    op.create_index("idx_memories_user_id", "memories", ["user_id"])

    op.create_index("idx_memories_memory_type", "memories", ["memory_type"])

    op.create_index("idx_memories_importance_score", "memories", ["importance_score"])

    op.create_index("idx_memories_created_at", "memories", ["created_at"])

    op.create_index("idx_memories_updated_at", "memories", ["updated_at"])

    op.create_index("idx_memories_last_accessed_at", "memories", ["last_accessed_at"])

    op.create_index("idx_memories_expires_at", "memories", ["expires_at"])

    op.create_index("idx_memories_is_archived", "memories", ["is_archived"])

    op.create_index("idx_memories_user_type", "memories", ["user_id", "memory_type"])

    # Create GIN indexes for JSONB columns

    op.create_index(
        "idx_memories_metadata_gin", "memories", ["metadata"], postgresql_using="gin"
    )

    op.create_index(
        "idx_memories_tags_gin", "memories", ["tags"], postgresql_using="gin"
    )

    op.create_index(
        "idx_memories_related_gin",
        "memories",
        ["related_memories"],
        postgresql_using="gin",
    )

    # Create indexes for memory_associations table

    op.create_index(
        "idx_memory_associations_source", "memory_associations", ["source_memory_id"]
    )

    op.create_index(
        "idx_memory_associations_target", "memory_associations", ["target_memory_id"]
    )

    op.create_index(
        "idx_memory_associations_type", "memory_associations", ["association_type"]
    )

    op.create_index(
        "idx_memory_associations_strength", "memory_associations", ["strength"]
    )

    op.create_index(
        "idx_memory_associations_created_at", "memory_associations", ["created_at"]
    )

    # Create indexes for memory_summaries table

    op.create_index("idx_memory_summaries_type", "memory_summaries", ["summary_type"])

    op.create_index(
        "idx_memory_summaries_target", "memory_summaries", ["target_type", "target_id"]
    )

    op.create_index("idx_memory_summaries_user_id", "memory_summaries", ["user_id"])

    op.create_index(
        "idx_memory_summaries_created_at", "memory_summaries", ["created_at"]
    )

    op.create_index(
        "idx_memory_summaries_expires_at", "memory_summaries", ["expires_at"]
    )

    # Create indexes for memory_backups table

    op.create_index("idx_memory_backups_type", "memory_backups", ["backup_type"])

    op.create_index("idx_memory_backups_user_id", "memory_backups", ["user_id"])

    op.create_index("idx_memory_backups_status", "memory_backups", ["status"])

    op.create_index("idx_memory_backups_created_at", "memory_backups", ["created_at"])

    op.create_index(
        "idx_memory_backups_base_backup", "memory_backups", ["base_backup_id"]
    )

    # Create indexes for memory_access_logs table

    op.create_index(
        "idx_memory_access_logs_memory_id", "memory_access_logs", ["memory_id"]
    )

    op.create_index("idx_memory_access_logs_user_id", "memory_access_logs", ["user_id"])

    op.create_index(
        "idx_memory_access_logs_access_type", "memory_access_logs", ["access_type"]
    )

    op.create_index(
        "idx_memory_access_logs_accessed_at", "memory_access_logs", ["accessed_at"]
    )

    op.create_index(
        "idx_memory_access_logs_session_id", "memory_access_logs", ["session_id"]
    )

    # Create indexes for memory_search_index table

    op.create_index(
        "idx_memory_search_index_memory_id", "memory_search_index", ["memory_id"]
    )

    op.create_index(
        "idx_memory_search_vector_gin",
        "memory_search_index",
        ["search_vector"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_memory_search_keywords_gin",
        "memory_search_index",
        ["keywords"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_memory_search_entities_gin",
        "memory_search_index",
        ["entities"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_memory_search_topics_gin",
        "memory_search_index",
        ["topics"],
        postgresql_using="gin",
    )

    op.create_index("idx_memory_search_language", "memory_search_index", ["language"])

    # Create unique constraints

    op.create_unique_constraint(
        "uq_memory_associations_source_target",
        "memory_associations",
        ["source_memory_id", "target_memory_id", "association_type"],
    )


def downgrade() -> None:
    """Drop memory-related tables."""

    # Drop indexes first

    op.drop_index("idx_memory_search_language")

    op.drop_index("idx_memory_search_topics_gin")

    op.drop_index("idx_memory_search_entities_gin")

    op.drop_index("idx_memory_search_keywords_gin")

    op.drop_index("idx_memory_search_vector_gin")

    op.drop_index("idx_memory_search_index_memory_id")

    op.drop_index("idx_memory_access_logs_session_id")

    op.drop_index("idx_memory_access_logs_accessed_at")

    op.drop_index("idx_memory_access_logs_access_type")

    op.drop_index("idx_memory_access_logs_user_id")

    op.drop_index("idx_memory_access_logs_memory_id")

    op.drop_index("idx_memory_backups_base_backup")

    op.drop_index("idx_memory_backups_created_at")

    op.drop_index("idx_memory_backups_status")

    op.drop_index("idx_memory_backups_user_id")

    op.drop_index("idx_memory_backups_type")

    op.drop_index("idx_memory_summaries_expires_at")

    op.drop_index("idx_memory_summaries_created_at")

    op.drop_index("idx_memory_summaries_user_id")

    op.drop_index("idx_memory_summaries_target")

    op.drop_index("idx_memory_summaries_type")

    op.drop_index("idx_memory_associations_created_at")

    op.drop_index("idx_memory_associations_strength")

    op.drop_index("idx_memory_associations_type")

    op.drop_index("idx_memory_associations_target")

    op.drop_index("idx_memory_associations_source")

    op.drop_index("idx_memories_related_gin")

    op.drop_index("idx_memories_tags_gin")

    op.drop_index("idx_memories_metadata_gin")

    op.drop_index("idx_memories_user_type")

    op.drop_index("idx_memories_is_archived")

    op.drop_index("idx_memories_expires_at")

    op.drop_index("idx_memories_last_accessed_at")

    op.drop_index("idx_memories_updated_at")

    op.drop_index("idx_memories_created_at")

    op.drop_index("idx_memories_importance_score")

    op.drop_index("idx_memories_memory_type")

    op.drop_index("idx_memories_user_id")

    # Drop tables in reverse order of dependencies

    op.drop_table("memory_search_index")

    op.drop_table("memory_access_logs")

    op.drop_table("memory_backups")

    op.drop_table("memory_summaries")

    op.drop_table("memory_associations")

    op.drop_table("memories")
