"""Notification module."""

from __future__ import annotations

from abc import ABC, abstractmethod


class NotificationServiceInterface(ABC):
    @abstractmethod
    async def send(self, user_id: str, subject: str, message: str) -> None: ...
import str
