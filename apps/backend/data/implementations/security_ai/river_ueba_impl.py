from __future__ import annotations

import math
from typing import Any

from apps.backend.core.interfaces.security_ai import ScoreResult, UebaScorer
from river import stats
from river.anomaly import HalfSpaceTrees
import dict
import e
import event
import float
import int
import max
import min
import seed
import self
import str
import threshold
import value


class RiverUebaScorer(UebaScorer):
    """UEBA scorer using river's online anomaly detector.

    Features kept minimal and numeric for streaming.
    """

    def __init__(self, seed: int = 42, threshold: float = 0.85) -> None:
        self._model: HalfSpaceTrees = HalfSpaceTrees(seed=seed)
        self._lat_mean = stats.Mean()
        self._threshold: float = float(threshold)

    def _fe(self, e: dict[str, Any]) -> dict[str, float]:
        lat = float(e.get("latency_ms", 0.0))
        mu = self._lat_mean.get() or 1.0
        z = (lat - mu) / (mu if mu != 0 else 1.0)
        status = str(e.get("status", ""))
        method = str(e.get("method", "")).upper()
        return {
            "lat_z": float(z if math.isfinite(z) else 0.0),
            "bytes": float(e.get("bytes", 0) or 0),
            "status_5xx": 1.0 if status.startswith("5") else 0.0,
            "method_GET": 1.0 if method == "GET" else 0.0,
            "method_POST": 1.0 if method == "POST" else 0.0,
        }

    async def score_event(self, event: dict[str, Any]) -> ScoreResult:
        x = self._fe(event)
        s = float(self._model.score_one(x))
        # online update
        self._model.learn_one(x)
        self._lat_mean.update(float(event.get("latency_ms", 0.0)))
        label = "anomaly" if s > self._threshold else "clean"
        return ScoreResult(score=s, label=label, details={"features": x})

    # ---- adaptive helpers ----
    def get_threshold(self) -> float:
        return float(self._threshold)

    def set_threshold(self, value: float) -> None:
        v = max(0.0, min(1.0, float(value)))
        self._threshold = v
