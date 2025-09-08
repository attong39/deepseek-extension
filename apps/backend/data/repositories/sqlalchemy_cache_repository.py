"""Cache repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyCacheRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyCacheRepository"]
import self
import session
