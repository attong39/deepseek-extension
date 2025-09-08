"""Advanced Monitoring module."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.alerts import AlertSystem
from apps.backend.core.interfaces.security import (
    BehaviorAnalyticsEngine,
    SecurityEventFeed,
    ThreatIntelDatabase,
)


@dataclass(slots=True)
class AISecurityMonitor:
    intel: ThreatIntelDatabase
    bae: BehaviorAnalyticsEngine
    feed: SecurityEventFeed
    alerts: AlertSystem

    def assess_threat_level(self, behavior: Mapping[str, Any]) -> float:
        rep = self.intel.reputation(behavior.get("indicator", ""))
        weight = behavior.get("severity", 0.5)
        return min(1.0, rep * 0.6 + weight * 0.4)

    def auto_mitigate(self, behavior: Mapping[str, Any]) -> None:
        # hook: revoke token, kill session, block tool, tighten rate-limits, ...
        self.alerts.warn(
            "Auto-mitigate", f"Mitigated behavior: {behavior.get('id', 'unknown')}"
        )

    def proactive_threat_detection(self, window_sec: int = 300) -> list[dict]:
        events = self.feed.recent(window_sec=window_sec)
        suspects = self.bae.anomalies(events)
        acted: list[dict] = []
        for b in suspects:
            score = self.assess_threat_level(b)
            b["threat_score"] = score
            if score > 0.8:
                self.auto_mitigate(b)
                self.alerts.page_oncall(
                    "security", f"High threat score={score:.2f} on {b.get('indicator')}"
                )
                acted.append(b)
        if not acted:
            self.alerts.info("Security", "No high-risk anomalies detected.")
        return acted
import acted
import b
import behavior
import dict
import float
import int
import list
import min
import self
import str
import window_sec
