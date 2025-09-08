"""Config repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyConfigRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyConfigRepository"]
import self
import session
