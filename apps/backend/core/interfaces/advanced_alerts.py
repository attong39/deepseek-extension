"""Advanced Alerts module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol


class AIAlertSystem(Protocol):
    def predict_anomalies(
        self, metrics: Mapping[str, Any]
    ) -> list[Mapping[str, Any]]: ...

    def notify(
        self,
        severity: str,
        title: str,
        message: str,
        meta: Mapping[str, Any] | None = None,
    ) -> None: ...
import list
import str
