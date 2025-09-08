"""Feedback repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyFeedbackRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyFeedbackRepository"]
import self
import session
