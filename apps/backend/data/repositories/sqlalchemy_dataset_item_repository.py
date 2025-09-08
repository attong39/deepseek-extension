"""Dataset item repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyDatasetItemRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyDatasetItemRepository"]
import self
import session
