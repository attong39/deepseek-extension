from __future__ import annotations

import math
from collections import Counter
from typing import Any

import tldextract
from apps.backend.core.interfaces.security_ai import PhishingDetector, ScoreResult
import cnt
import dict
import feats
import float
import len
import max
import min
import p
import s
import self
import str
import sum
import threshold
import url
import value


def _shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    c = Counter(s)
    n = len(s)
    return float(-sum((cnt / n) * math.log2(cnt / n) for cnt in c.values()))


class HeuristicPhishingDetector(PhishingDetector):
    """Lightweight URL phishing detector based on heuristics.

    Not a replacement for full ML; intended as a fast baseline.
    """

    def __init__(self, threshold: float = 0.7) -> None:
        self._threshold = float(threshold)

    async def analyze(self, url: str, text: str | None = None) -> ScoreResult:
        ext = tldextract.extract(url)
        host = ".".join([p for p in [ext.subdomain, ext.domain, ext.suffix] if p])
        feats: dict[str, Any] = {
            "len": len(url),
            "entropy": _shannon_entropy(url),
            "subdomains": len([p for p in (ext.subdomain or "").split(".") if p]),
            "has_ip": host.replace(".", "").isdigit(),
            "has_login": ("login" in url.lower()),
            "has_verify": ("verify" in url.lower()),
        }
        score = min(
            1.0,
            (feats["entropy"] / 5.0)
            + (1.0 if feats["subdomains"] > 2 else 0.0) * 0.2
            + (1.0 if feats["len"] > 100 else 0.0) * 0.2
            + (1.0 if feats["has_ip"] else 0.0) * 0.3
            + (1.0 if (feats["has_login"] or feats["has_verify"]) else 0.0) * 0.1,
        )
        label = "phishing" if score >= self._threshold else "clean"
        return ScoreResult(score=float(score), label=label, details={"features": feats})

    # ---- adaptive helpers ----
    def get_threshold(self) -> float:
        return float(self._threshold)

    def set_threshold(self, value: float) -> None:
        v = max(0.0, min(1.0, float(value)))
        self._threshold = v
