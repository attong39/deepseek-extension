"""Security repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemySecurityRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemySecurityRepository"]
import self
import session
