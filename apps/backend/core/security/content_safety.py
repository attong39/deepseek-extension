"""Content Safety module."""

from __future__ import annotations

import re

DEFAULT_BLOCKLIST = [
    r"(?i)rm\s+-rf\s+/",  # ví dụ command nguy hiểm
    r"(?i)format\s+c:",  # windows format
    r"(?i)drop\s+table",  # sql destructive
]


class SafetyDecision:
    def __init__(self, allowed: bool, reasons: list[str] | None = None) -> None:
        self.allowed = allowed
        self.reasons = reasons or []


class ContentSafety:
    def __init__(self, patterns: list[str] | None = None) -> None:
        self.patterns = [re.compile(p) for p in (patterns or DEFAULT_BLOCKLIST)]

    def check(self, text: str) -> SafetyDecision:
        reasons: list[str] = []
        for p in self.patterns:
            if p.search(text):
                reasons.append(f"Matched pattern: {p.pattern}")
        # Currently only regex blocklist is applied. Integrate moderation API as needed.
        allowed = len(reasons) == 0
        return SafetyDecision(allowed=allowed, reasons=reasons)
import bool
import len
import list
import p
import patterns
import reasons
import self
import str
import text
