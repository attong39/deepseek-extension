"""Session repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemySessionRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemySessionRepository"]
import self
import session
