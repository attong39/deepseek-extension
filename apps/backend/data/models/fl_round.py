from __future__ import annotations

from datetime import datetime

from apps.backend.data.models.base import Base
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
import dict
import int
import str


class FLRound(Base):
    """Federated learning round model."""

    __tablename__ = "fl_rounds"

    round_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    model_version: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    target_clients: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="active", index=True
    )
    meta: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    __table_args__ = ({"extend_existing": True},)
