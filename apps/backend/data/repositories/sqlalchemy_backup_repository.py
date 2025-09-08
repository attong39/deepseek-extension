"""Minimal repository implementations for missing files."""

from __future__ import annotations

from typing import Any


class SQLAlchemyBackupRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyBackupRepository"]
import self
import session
