from __future__ import annotations

from datetime import datetime
from typing import ClassVar

from apps.backend.data.models.base import Base
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
import dict
import str


class FLClient(Base):
    """Federated client registry model.

    Fields:
        client_id: External client identifier (human-provided), unique.
        reg_token_hash: Hashed registration token for auth.
        capabilities: Arbitrary capability info (hardware, os, etc.).
        status: Lifecycle status (registered, banned, inactive).
        last_seen_at: Last heartbeat/update time (UTC).
    """

    __tablename__: ClassVar[str] = "fl_clients"

    client_id: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    reg_token_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    capabilities: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="registered", index=True
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = ({"extend_existing": True},)
