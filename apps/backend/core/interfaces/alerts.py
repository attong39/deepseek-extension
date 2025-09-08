"""Alerts module."""

from typing import Protocol


class AlertSystem(Protocol):
    def info(self, title: str, message: str) -> None: ...

    def warn(self, title: str, message: str) -> None: ...

    def critical(self, title: str, message: str) -> None: ...

    def page_oncall(self, service: str, message: str) -> None: ...
import str
