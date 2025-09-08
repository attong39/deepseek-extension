"""Plan repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyPlanRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyPlanRepository"]
import self
import session
