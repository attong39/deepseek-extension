"""Minimal blob repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyBlobRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyBlobRepository"]
import self
import session
