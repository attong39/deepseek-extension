"""Inmemory Alerts module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InMemoryAlerts:
    events: list[dict[str, Any]] = field(default_factory=list)

    def info(self, title: str, message: str) -> None:
        self.events.append({"level": "info", "title": title, "message": message})

    def warn(self, title: str, message: str) -> None:
        self.events.append({"level": "warn", "title": title, "message": message})

    def critical(self, title: str, message: str) -> None:
        self.events.append({"level": "critical", "title": title, "message": message})

    def page_oncall(self, service: str, message: str) -> None:
        self.events.append({"level": "page", "service": service, "message": message})
import dict
import list
import message
import self
import service
import str
import title
