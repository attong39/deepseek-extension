"""Migration 007: Create additional performance indexes."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Constants for repeated where clauses
ARCHIVED_FALSE = "archived = false"
STATUS_ACTIVE = "status = 'active'"
RUNNING_STATUSES = "status IN ('running', 'pending')"
FAILED_STATUS = "status = 'failed'"
HIGH_IMPORTANCE = "importance_score >= 0.8 AND archived = false"
RECENT_EVENTS = "timestamp >= NOW() - INTERVAL '30 days'"
CRITICAL_SEVERITY = "severity IN ('error', 'critical')"
HIGH_THREAT = "threat_level IN ('high', 'critical')"
COMPLETED_EXECUTIONS = "completed_at IS NOT NULL AND started_at IS NOT NULL"


def upgrade() -> None:
    """Create additional performance indexes and constraints."""

    # ==========================================
    # COMPOSITE INDEXES FOR COMMON QUERIES
    # ==========================================

    # Agent performance indexes

    op.create_index(
        "idx_agents_status_last_active", "agents", ["status", "last_active_at"]
    )

    op.create_index(
        "idx_agents_type_capabilities",
        "agents",
        ["agent_type"],
        postgresql_where=sa.text("capabilities IS NOT NULL"),
    )

    # Memory performance indexes

    op.create_index(
        "idx_memories_agent_type_importance",
        "memories",
        ["agent_id", "memory_type", "importance_score"],
    )

    op.create_index(
        "idx_memories_created_importance",
        "memories",
        ["created_at", "importance_score"],
        postgresql_where=sa.text(ARCHIVED_FALSE),
    )

    # Agent executions performance indexes

    op.create_index(
        "idx_agent_executions_agent_status_created",
        "agent_executions",
        ["agent_id", "status", "created_at"],
    )

    op.create_index(
        "idx_agent_executions_task_status", "agent_executions", ["task_id", "status"]
    )

    # Chat performance indexes

    op.create_index(
        "idx_conversations_user_updated", "conversations", ["user_id", "updated_at"]
    )

    op.create_index(
        "idx_messages_conversation_created",
        "messages",
        ["conversation_id", "created_at"],
    )

    op.create_index(
        "idx_messages_sender_type_created", "messages", ["sender_type", "created_at"]
    )

    # Analytics performance indexes

    op.create_index(
        "idx_analytics_events_type_timestamp",
        "analytics_events",
        ["event_type", "timestamp"],
    )

    op.create_index(
        "idx_user_sessions_user_created", "user_sessions", ["user_id", "created_at"]
    )

    op.create_index(
        "idx_performance_metrics_source_timestamp",
        "performance_metrics",
        ["source", "timestamp"],
    )

    # Audit performance indexes

    op.create_index(
        "idx_audit_logs_user_action_timestamp",
        "audit_logs",
        ["user_id", "action", "timestamp"],
    )

    op.create_index(
        "idx_security_events_threat_occurred",
        "security_events",
        ["threat_level", "occurred_at"],
    )

    # ==========================================
    # PARTIAL INDEXES FOR FILTERED QUERIES
    # ==========================================

    # Active agents only

    op.create_index(
        "idx_agents_active_created",
        "agents",
        ["created_at"],
        postgresql_where=sa.text(STATUS_ACTIVE),
    )

    # Non-archived memories only

    op.create_index(
        "idx_memories_active_agent_type",
        "memories",
        ["agent_id", "memory_type"],
        postgresql_where=sa.text(ARCHIVED_FALSE),
    )

    # Running executions only

    op.create_index(
        "idx_agent_executions_running",
        "agent_executions",
        ["agent_id", "created_at"],
        postgresql_where=sa.text(RUNNING_STATUSES),
    )

    # Failed executions for debugging

    op.create_index(
        "idx_agent_executions_failed",
        "agent_executions",
        ["agent_id", "created_at", "error_message"],
        postgresql_where=sa.text(FAILED_STATUS),
    )

    # Active conversations only

    op.create_index(
        "idx_conversations_active_user",
        "conversations",
        ["user_id", "updated_at"],
        postgresql_where=sa.text(STATUS_ACTIVE),
    )

    # Unread messages

    op.create_index(
        "idx_messages_unread",
        "messages",
        ["conversation_id", "created_at"],
        postgresql_where=sa.text("read_at IS NULL"),
    )

    # High importance memories

    op.create_index(
        "idx_memories_high_importance",
        "memories",
        ["agent_id", "created_at"],
        postgresql_where=sa.text(HIGH_IMPORTANCE),
    )

    # Recent analytics events

    op.create_index(
        "idx_analytics_events_recent",
        "analytics_events",
        ["event_type", "timestamp"],
        postgresql_where=sa.text(RECENT_EVENTS),
    )

    # High severity system events

    op.create_index(
        "idx_system_events_critical",
        "system_events",
        ["occurred_at", "resolved"],
        postgresql_where=sa.text(CRITICAL_SEVERITY),
    )

    # High threat security events

    op.create_index(
        "idx_security_events_high_threat",
        "security_events",
        ["occurred_at", "investigated"],
        postgresql_where=sa.text(HIGH_THREAT),
    )

    # ==========================================
    # COVERING INDEXES FOR READ-HEAVY QUERIES
    # ==========================================

    # Agent list with basic info

    op.create_index(
        "idx_agents_list_covering",
        "agents",
        ["status", "created_at"],
        postgresql_include=["id", "name", "agent_type", "description"],
    )

    # Memory search covering

    op.create_index(
        "idx_memories_search_covering",
        "memories",
        ["agent_id", "memory_type"],
        postgresql_include=["id", "content", "importance_score", "created_at"],
        postgresql_where=sa.text(ARCHIVED_FALSE),
    )

    # Conversation list covering

    op.create_index(
        "idx_conversations_list_covering",
        "conversations",
        ["user_id", "updated_at"],
        postgresql_include=["id", "title", "status", "message_count"],
    )

    # Message list covering

    op.create_index(
        "idx_messages_list_covering",
        "messages",
        ["conversation_id", "created_at"],
        postgresql_include=["id", "content", "sender_type", "read_at"],
    )

    # ==========================================
    # EXPRESSION INDEXES FOR COMPUTED QUERIES
    # ==========================================

    # Lowercase search indexes for case-insensitive queries

    op.create_index("idx_agents_name_lower", "agents", [sa.func.lower(sa.text("name"))])

    op.create_index(
        "idx_conversations_title_lower",
        "conversations",
        [sa.func.lower(sa.text("title"))],
    )

    # Date part indexes for time-based grouping

    op.create_index(
        "idx_analytics_events_date",
        "analytics_events",
        [sa.func.date(sa.text("timestamp"))],
    )

    op.create_index(
        "idx_agent_executions_date",
        "agent_executions",
        [sa.func.date(sa.text("created_at"))],
    )

    # Duration calculation indexes

    op.create_index(
        "idx_agent_executions_duration",
        "agent_executions",
        [sa.text("EXTRACT(EPOCH FROM (completed_at - started_at))")],
        postgresql_where=sa.text(COMPLETED_EXECUTIONS),
    )

    # ==========================================
    # HASH INDEXES FOR EQUALITY LOOKUPS
    # ==========================================

    # Hash indexes for exact matches on UUIDs and strings

    op.create_index("idx_agents_id_hash", "agents", ["id"], postgresql_using="hash")

    op.create_index(
        "idx_memories_agent_id_hash", "memories", ["agent_id"], postgresql_using="hash"
    )

    op.create_index(
        "idx_conversations_id_hash", "conversations", ["id"], postgresql_using="hash"
    )

    op.create_index(
        "idx_messages_conversation_id_hash",
        "messages",
        ["conversation_id"],
        postgresql_using="hash",
    )

    # ==========================================
    # FULL-TEXT SEARCH INDEXES
    # ==========================================

    # Add tsvector columns for full-text search

    op.add_column("agents", sa.Column("search_vector", postgresql.TSVECTOR))

    op.add_column("memories", sa.Column("search_vector", postgresql.TSVECTOR))

    op.add_column("conversations", sa.Column("search_vector", postgresql.TSVECTOR))

    op.add_column("messages", sa.Column("search_vector", postgresql.TSVECTOR))

    # Create GIN indexes for full-text search

    op.create_index(
        "idx_agents_search_vector", "agents", ["search_vector"], postgresql_using="gin"
    )

    op.create_index(
        "idx_memories_search_vector",
        "memories",
        ["search_vector"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_conversations_search_vector",
        "conversations",
        ["search_vector"],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_messages_search_vector",
        "messages",
        ["search_vector"],
        postgresql_using="gin",
    )

    # Create triggers to automatically update search vectors

    op.execute("""
        CREATE OR REPLACE FUNCTION update_agent_search_vector() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
                                setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B') ||
                                setweight(to_tsvector('english', COALESCE(NEW.agent_type, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER agents_search_vector_update
            BEFORE INSERT OR UPDATE ON agents
            FOR EACH ROW EXECUTE FUNCTION update_agent_search_vector();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_memory_search_vector() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'A') ||
                                setweight(to_tsvector('english', COALESCE(NEW.summary, '')), 'B') ||
                                setweight(to_tsvector('english', COALESCE(NEW.memory_type, '')), 'C');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER memories_search_vector_update
            BEFORE INSERT OR UPDATE ON memories
            FOR EACH ROW EXECUTE FUNCTION update_memory_search_vector();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_conversation_search_vector() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
                                setweight(to_tsvector('english', COALESCE(NEW.summary, '')), 'B');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER conversations_search_vector_update
            BEFORE INSERT OR UPDATE ON conversations
            FOR EACH ROW EXECUTE FUNCTION update_conversation_search_vector();
    """)

    op.execute("""
        CREATE OR REPLACE FUNCTION update_message_search_vector() RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'A');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER messages_search_vector_update
            BEFORE INSERT OR UPDATE ON messages
            FOR EACH ROW EXECUTE FUNCTION update_message_search_vector();
    """)

    # ==========================================
    # ADDITIONAL CONSTRAINTS
    # ==========================================

    # Add check constraints

    op.create_check_constraint(
        "check_memory_importance_range",
        "memories",
        "importance_score >= 0.0 AND importance_score <= 1.0",
    )

    op.create_check_constraint(
        "check_agent_execution_duration",
        "agent_executions",
        "completed_at IS NULL OR completed_at >= started_at",
    )

    op.create_check_constraint(
        "check_security_events_confidence",
        "security_events",
        "confidence_score IS NULL OR (confidence_score >= 0.0 AND confidence_score <= 1.0)",
    )

    # Add exclusion constraints to prevent overlapping sessions

    op.execute("""
        CREATE EXTENSION IF NOT EXISTS btree_gist;

        ALTER TABLE user_sessions
        ADD CONSTRAINT exclude_overlapping_sessions
        EXCLUDE USING gist (
            user_id WITH =,
            tsrange(created_at, ended_at) WITH &&
        ) WHERE (ended_at IS NOT NULL);
    """)


def downgrade() -> None:
    """Drop additional performance indexes and constraints."""

    # Drop exclusion constraint

    op.drop_constraint("exclude_overlapping_sessions", "user_sessions")

    # Drop check constraints

    op.drop_constraint("check_security_events_confidence", "security_events")

    op.drop_constraint("check_agent_execution_duration", "agent_executions")

    op.drop_constraint("check_memory_importance_range", "memories")

    # Drop triggers and functions

    op.execute("DROP TRIGGER IF EXISTS messages_search_vector_update ON messages;")

    op.execute(
        "DROP TRIGGER IF EXISTS conversations_search_vector_update ON conversations;"
    )

    op.execute("DROP TRIGGER IF EXISTS memories_search_vector_update ON memories;")

    op.execute("DROP TRIGGER IF EXISTS agents_search_vector_update ON agents;")

    op.execute("DROP FUNCTION IF EXISTS update_message_search_vector();")

    op.execute("DROP FUNCTION IF EXISTS update_conversation_search_vector();")

    op.execute("DROP FUNCTION IF EXISTS update_memory_search_vector();")

    op.execute("DROP FUNCTION IF EXISTS update_agent_search_vector();")

    # Drop full-text search indexes

    op.drop_index("idx_messages_search_vector")

    op.drop_index("idx_conversations_search_vector")

    op.drop_index("idx_memories_search_vector")

    op.drop_index("idx_agents_search_vector")

    # Drop tsvector columns

    op.drop_column("messages", "search_vector")

    op.drop_column("conversations", "search_vector")

    op.drop_column("memories", "search_vector")

    op.drop_column("agents", "search_vector")

    # Drop hash indexes

    op.drop_index("idx_messages_conversation_id_hash")

    op.drop_index("idx_conversations_id_hash")

    op.drop_index("idx_memories_agent_id_hash")

    op.drop_index("idx_agents_id_hash")

    # Drop expression indexes

    op.drop_index("idx_agent_executions_duration")

    op.drop_index("idx_agent_executions_date")

    op.drop_index("idx_analytics_events_date")

    op.drop_index("idx_conversations_title_lower")

    op.drop_index("idx_agents_name_lower")

    # Drop covering indexes

    op.drop_index("idx_messages_list_covering")

    op.drop_index("idx_conversations_list_covering")

    op.drop_index("idx_memories_search_covering")

    op.drop_index("idx_agents_list_covering")

    # Drop partial indexes

    op.drop_index("idx_security_events_high_threat")

    op.drop_index("idx_system_events_critical")

    op.drop_index("idx_analytics_events_recent")

    op.drop_index("idx_memories_high_importance")

    op.drop_index("idx_messages_unread")

    op.drop_index("idx_conversations_active_user")

    op.drop_index("idx_agent_executions_failed")

    op.drop_index("idx_agent_executions_running")

    op.drop_index("idx_memories_active_agent_type")

    op.drop_index("idx_agents_active_created")

    # Drop performance indexes

    op.drop_index("idx_security_events_threat_occurred")

    op.drop_index("idx_audit_logs_user_action_timestamp")

    op.drop_index("idx_performance_metrics_source_timestamp")

    op.drop_index("idx_user_sessions_user_created")

    op.drop_index("idx_analytics_events_type_timestamp")

    op.drop_index("idx_messages_sender_type_created")

    op.drop_index("idx_messages_conversation_created")

    op.drop_index("idx_conversations_user_updated")

    op.drop_index("idx_agent_executions_task_status")

    op.drop_index("idx_agent_executions_agent_status_created")

    op.drop_index("idx_memories_created_importance")

    op.drop_index("idx_memories_agent_type_importance")

    op.drop_index("idx_agents_type_capabilities")

    op.drop_index("idx_agents_status_last_active")
