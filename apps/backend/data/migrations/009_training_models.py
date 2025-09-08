"""Migration 009: Create training jobs and dataset items tables.

This migration introduces the training_jobs and dataset_items tables with
PostgreSQL-optimized JSONB columns and relevant indexes.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# Reusable default JSONB empty literal
JSONB_EMPTY = sa.text("'{}'::jsonb")


def upgrade() -> None:
    """Apply training models schema."""

    op.create_table(
        "training_jobs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("model_name", sa.String(100), nullable=False),
        sa.Column(
            "params", postgresql.JSONB, nullable=False, server_default=JSONB_EMPTY
        ),
        sa.Column(
            "metrics", postgresql.JSONB, nullable=False, server_default=JSONB_EMPTY
        ),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
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
    )

    op.create_index("idx_training_jobs_status", "training_jobs", ["status"])
    op.create_index("idx_training_jobs_name", "training_jobs", ["name"])

    op.create_table(
        "dataset_items",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "training_job_id",
            sa.String(36),
            sa.ForeignKey("training_jobs.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("dataset_name", sa.String(255), nullable=False),
        sa.Column("external_id", sa.String(255), nullable=True),
        sa.Column("content", sa.Text, nullable=True),
        sa.Column(
            "metadata", postgresql.JSONB, nullable=False, server_default=JSONB_EMPTY
        ),
        sa.Column("status", sa.String(50), nullable=False, server_default="ready"),
        sa.Column("order_index", sa.Integer, nullable=True),
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
    )

    op.create_index("idx_dataset_items_status", "dataset_items", ["status"])
    op.create_index("idx_dataset_items_dataset_name", "dataset_items", ["dataset_name"])
    op.create_index("idx_dataset_items_external_id", "dataset_items", ["external_id"])
    op.create_index(
        "idx_dataset_items_training_job_id", "dataset_items", ["training_job_id"]
    )


def downgrade() -> None:
    """Drop training models schema."""

    op.drop_index("idx_dataset_items_training_job_id", table_name="dataset_items")
    op.drop_index("idx_dataset_items_external_id", table_name="dataset_items")
    op.drop_index("idx_dataset_items_dataset_name", table_name="dataset_items")
    op.drop_index("idx_dataset_items_status", table_name="dataset_items")
    op.drop_table("dataset_items")

    op.drop_index("idx_training_jobs_name", table_name="training_jobs")
    op.drop_index("idx_training_jobs_status", table_name="training_jobs")
    op.drop_table("training_jobs")
