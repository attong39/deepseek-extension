from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apps.backend.core.services.moe_router import MoERouter
import context_len
import dict
import float
import int
import max
import min
import model
import provider
import reward
import risk
import self
import str
import task


@dataclass
class SelfLearningService:
    """Online self-learning (nhẹ): thu thập feedback và cập nhật router MoE.

    Sử dụng bandit cực đơn giản (Rolling average + epsilon-greedy stub).
    Không đụng đến fine-tuning model trong path online.
    """

    router: MoERouter
    epsilon: float = 0.05
    alpha: float = 0.2  # EMA smoothing
    _stats: dict[str, dict[str, float]] = field(default_factory=dict)

    def record_feedback(
        self, *, task: str, provider: str, model: str, reward: float
    ) -> None:
        key = f"{task}:{provider}:{model}"
        s = self._stats.setdefault(key, {"mean": 0.5, "n": 0.0})
        # EMA update
        s["mean"] = (1.0 - self.alpha) * s["mean"] + self.alpha * max(
            0.0, min(1.0, reward)
        )
        s["n"] += 1.0

    def suggest(
        self, *, task: str, context_len: int, risk: float = 0.0
    ) -> dict[str, Any]:
        # Call router for a base choice
        base = self.router.choose(
            task=task, context_len=context_len, risk=risk, fast_ok=True
        )
        key = f"{task}:{base['provider']}:{base['model']}"
        s = self._stats.get(key, {"mean": 0.5, "n": 0.0})
        # Epsilon-greedy: thi thoảng thử chiến lược khác (ở đây giữ nguyên đơn giản)
        base["score"] = float(s["mean"])  # attach expected reward for observability
        return base
