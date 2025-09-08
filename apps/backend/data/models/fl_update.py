from __future__ import annotations

from datetime import datetime
from typing import ClassVar

from apps.backend.data.models.base import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import float
import int
import str


class FLUpdate(Base):
    """Client update submitted for a federated round."""

    __tablename__: ClassVar[str] = "fl_updates"

    round_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("fl_rounds.id", ondelete="CASCADE"), index=True
    )
    client_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("fl_clients.id", ondelete="CASCADE"), index=True
    )

    payload_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    payload_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    signature: Mapped[str | None] = mapped_column(String(512), nullable=True)
    validation_score: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", index=True
    )
    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    round = relationship("FLRound", lazy="joined")
    client = relationship("FLClient", lazy="joined")

    __table_args__ = ({"extend_existing": True},)
