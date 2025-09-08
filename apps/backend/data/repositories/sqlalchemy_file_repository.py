"""File repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyFileRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyFileRepository"]
import self
import session
