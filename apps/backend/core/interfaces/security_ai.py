"""Security-AI interfaces (UEBA, phishing, liveness, malware).

Defines clean, testable contracts for security analytics components.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
import bytes
import dict
import float
import str


@dataclass(frozen=True)
class ScoreResult:
    """Generic score output.

    Attributes:
        score: Float score in range [0, 1].
        label: Derived label from score or classifier.
        details: Optional detail dictionary for debugging/explanations.
    """

    score: float
    label: str
    details: dict[str, Any] | None = None


class UebaScorer(ABC):
    """Interface for UEBA (User and Entity Behavior Analytics) scorer."""

    @abstractmethod
    async def score_event(self, event: dict[str, Any]) -> ScoreResult:
        """Score a single behavioral event.

        Args:
            event: Arbitrary event dict (request/auth/traffic features).

        Returns:
            ScoreResult with score and label.
        """


class PhishingDetector(ABC):
    """Interface for phishing detection from URL/text."""

    @abstractmethod
    async def analyze(self, url: str, text: str | None = None) -> ScoreResult:
        """Analyze potential phishing indicators.

        Args:
            url: URL to analyze.
            text: Optional related text (email/page content).

        Returns:
            ScoreResult with score and label.
        """


class MediaLiveness(ABC):
    """Interface for media (image/audio) liveness/anti-spoof checks."""

    @abstractmethod
    async def analyze(self, payload: bytes, modality: str = "image") -> ScoreResult:
        """Analyze media payload for liveness.

        Args:
            payload: Raw media bytes.
            modality: "image" or "audio".

        Returns:
            ScoreResult with score and label.
        """


class MalwareScanner(ABC):
    """Interface for malware scanning logic."""

    @abstractmethod
    async def scan(self, payload: bytes, filename: str | None = None) -> ScoreResult:
        """Scan payload for malware indicators.

        Args:
            payload: Raw file bytes.
            filename: Optional file name.

        Returns:
            ScoreResult with score and label.
        """
