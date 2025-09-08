from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from apps.backend.core.interfaces.security_ai import (
import dict
import event
import self
import str
import text
import url
    MalwareScanner,
    MediaLiveness,
    PhishingDetector,
    ScoreResult,
    UebaScorer,
)


@dataclass
class SecurityAiService:
    """Facade/service to aggregate Security-AI detectors and policies."""

    ueba: UebaScorer
    phishing: PhishingDetector
    liveness: MediaLiveness | None = None
    malware: MalwareScanner | None = None

    async def score_event(self, event: dict[str, Any]) -> ScoreResult:
        return await self.ueba.score_event(event)

    async def analyze_url(self, url: str, text: str | None = None) -> ScoreResult:
        return await self.phishing.analyze(url, text)
