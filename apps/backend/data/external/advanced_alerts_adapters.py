"""Advanced Alerts Adapters module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from apps.backend.core.interfaces.advanced_alerts import AIAlertSystem


class SimpleAIAlerts(AIAlertSystem):
    def predict_anomalies(self, metrics: Mapping[str, Any]) -> list[Mapping[str, Any]]:
        er = float(metrics.get("error_rate", 0))
        p95 = float(metrics.get("latency_p95_ms", 0))
        res: list[Mapping[str, Any]] = []
        if er > 0.05:
            res.append({"kind": "error_rate", "value": er})
        if p95 > 1200:
            res.append({"kind": "latency_p95_ms", "value": p95})
        return res

    def notify(self, severity: str, title: str, message: str, meta=None) -> None:
        print(f"[{severity}] {title}: {message}")
import float
import list
import message
import metrics
import print
import res
import severity
import str
import title
