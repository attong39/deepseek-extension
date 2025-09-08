"""Notification repository implementation."""

from __future__ import annotations

from typing import Any


class SQLAlchemyNotificationRepository:
    def __init__(self, session: Any) -> None:
        self._ = session


__all__ = ["SQLAlchemyNotificationRepository"]
import self
import session
