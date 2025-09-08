from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
import bool
import extras
import float
import list
import max
import pat
import self
import str
import t
import text
import threshold

_DEFAULT_DENY = [
    r"(?i)ignore\s+previous\s+instructions",
    r"(?i)you\s+are\s+now\s+.*system",
    r"(?i)exfiltrate|leak|steal\s+keys",
    r"(?i)write\s+malware|drop\s+tables",
]


@dataclass
class PromptInjectionGuard:
    """Guard rule-based đơn giản và matching tương tự cho prompt injection."""

    deny_patterns: list[re.Pattern[str]] | None = None

    def __post_init__(self) -> None:
        if self.deny_patterns is None:
            self.deny_patterns = [re.compile(pat) for pat in _DEFAULT_DENY]

    def score(self, text: str, extras: Iterable[str] | None = None) -> float:
        risk = 0.0
        candidates = [text]
        if extras:
            candidates.extend(extras)
        patterns = self.deny_patterns or []
        for t in candidates:
            for pat in patterns:
                if pat.search(t):
                    risk = max(risk, 0.8)
        return float(risk)

    def is_malicious(self, text: str, threshold: float = 0.8) -> bool:
        return self.score(text) >= threshold
