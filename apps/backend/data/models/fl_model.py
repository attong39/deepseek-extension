from __future__ import annotations

from typing import ClassVar

from apps.backend.data.models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
import dict
import str


class FLModel(Base):
    """Published global model artifact registry."""

    __tablename__: ClassVar[str] = "fl_models"

    version: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    artifact_uri: Mapped[str] = mapped_column(String(1024), nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    metrics: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    __table_args__ = ({"extend_existing": True},)
