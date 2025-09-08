from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from apps.backend.config.ml_config import get_ml_settings
import allowed
import bool
import context_len
import dict
import fast_ok
import float
import int
import risk
import set
import str
import strat
import task

Strategy = Literal["balanced", "latency", "cost", "quality", "conservative"]


@dataclass
class MoERouter:
    """Router chọn expert (provider/model) theo chiến lược MoE.

    Chỉ chọn provider theo heuristic nhẹ, không ràng buộc SDK.
    """

    def choose(
        self,
        *,
        task: str,
        context_len: int,
        risk: float = 0.0,
        fast_ok: bool = True,
    ) -> dict[str, Any]:
        s = get_ml_settings()
        allowed: set[str] = {"balanced", "latency", "cost", "quality", "conservative"}
        _st = s.moe_default if s.moe_default in allowed else "balanced"
        strat: Strategy = _st  # type: ignore[assignment]

        # Simple heuristics
        long_ctx = context_len > s.max_context_tokens
        high_risk = risk >= 0.7 or s.shielding_level == "strict"

        if (
            strat in {"latency", "conservative"}
            or fast_ok
            or task in {"summary", "classify"}
        ):
            provider = "local"  # giả định local/onnx nhanh
            model = "onnx-small"
        else:
            provider = s.default_model_provider
            model = s.long_context_model if long_ctx else s.default_chat_model

        # Điều chỉnh theo cost
        if strat == "cost":
            provider, model = ("local", "onnx-small")

        # Điều chỉnh theo quality
        if strat == "quality":
            provider = "anthropic"
            model = "claude-3-opus"

        # Khi high_risk: ép provider an toàn hoặc bật policy model
        if high_risk:
            provider = "google"
            model = "gemini-1.5-pro"

        return {
            "provider": provider,
            "model": model,
            "strategy": strat,
            "long_ctx": long_ctx,
        }
