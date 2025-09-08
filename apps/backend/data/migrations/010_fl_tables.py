"""Migration 010: Federated Learning tables (clients, rounds, updates, models)."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

JSONB_EMPTY = sa.text("'{}'::jsonb")


def upgrade() -> None:
    op.create_table(
        "fl_clients",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("client_id", sa.String(255), nullable=False, unique=True),
        sa.Column("reg_token_hash", sa.String(255), nullable=False),
        sa.Column(
            "capabilities", postgresql.JSONB, nullable=False, server_default=JSONB_EMPTY
        ),
        sa.Column("status", sa.String(32), nullable=False, server_default="registered"),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
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
    op.create_index("ix_fl_clients_client_id", "fl_clients", ["client_id"], unique=True)
    op.create_index("ix_fl_clients_status", "fl_clients", ["status"])

    op.create_table(
        "fl_rounds",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("round_name", sa.String(255), nullable=False),
        sa.Column("model_version", sa.String(64), nullable=False),
        sa.Column("target_clients", sa.Integer, nullable=False, server_default="10"),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("meta", postgresql.JSONB, nullable=False, server_default=JSONB_EMPTY),
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
    op.create_index("ix_fl_rounds_model_version", "fl_rounds", ["model_version"])
    op.create_index("ix_fl_rounds_status", "fl_rounds", ["status"])

    op.create_table(
        "fl_updates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "round_id",
            sa.String(36),
            sa.ForeignKey("fl_rounds.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "client_id",
            sa.String(36),
            sa.ForeignKey("fl_clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("payload_uri", sa.String(1024), nullable=False),
        sa.Column("payload_sha256", sa.String(64), nullable=False),
        sa.Column("sample_size", sa.Integer, nullable=False, server_default="1"),
        sa.Column("signature", sa.String(512), nullable=True),
        sa.Column("validation_score", sa.Float, nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
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
    op.create_index("ix_fl_updates_round_id", "fl_updates", ["round_id"])
    op.create_index("ix_fl_updates_client_id", "fl_updates", ["client_id"])
    op.create_index("ix_fl_updates_payload_sha256", "fl_updates", ["payload_sha256"])

    op.create_table(
        "fl_models",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("version", sa.String(64), nullable=False, unique=True),
        sa.Column("artifact_uri", sa.String(1024), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column(
            "metrics", postgresql.JSONB, nullable=False, server_default=JSONB_EMPTY
        ),
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
    op.create_index("ix_fl_models_version", "fl_models", ["version"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_fl_models_version", table_name="fl_models")
    op.drop_table("fl_models")

    op.drop_index("ix_fl_updates_payload_sha256", table_name="fl_updates")
    op.drop_index("ix_fl_updates_client_id", table_name="fl_updates")
    op.drop_index("ix_fl_updates_round_id", table_name="fl_updates")
    op.drop_table("fl_updates")

    op.drop_index("ix_fl_rounds_status", table_name="fl_rounds")
    op.drop_index("ix_fl_rounds_model_version", table_name="fl_rounds")
    op.drop_table("fl_rounds")

    op.drop_index("ix_fl_clients_status", table_name="fl_clients")
    op.drop_index("ix_fl_clients_client_id", table_name="fl_clients")
    op.drop_table("fl_clients")
