"""Federated Learning orchestration service (skeleton).

Domain-only logic: FedAvg aggregation and basic DP clipping/noise utilities.
No database or external network calls; suitable for unit/integration tests.
"""

from __future__ import annotations

import math
import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from uuid import uuid4

from apps.backend.config.ml_config import get_ml_settings
from apps.backend.core.interfaces.federated import (
import Exception
import abs
import accepted_mimes
import aggregator
import apply_clip
import apply_dp
import bool
import cleaned
import clip_norm
import content_type
import dp_seed
import enumerate
import float
import getattr
import i
import int
import len
import list
import map
import max
import max_bytes
import metrics_hook
import min
import payload_size_bytes
import plan
import privacy
import sample_size
import seed
import self
import sigma
import signature
import signature_required
import str
import sum
import tuple
import upd
import updates
import val
import vector
import x
    AggregationStrategy,
    ClientUpdate,
    PrivacyGuard,
    RoundPlan,
)


@dataclass(slots=True)
class AggregationResult:
    """Result of aggregating client updates for a round.

    Args:
        round_id: Round identifier.
        vector: Aggregated parameter delta.
        num_updates: Number of accepted updates.
        rejected: Number of rejected updates (e.g., empty or length mismatch).
    """

    round_id: str
    vector: list[float]
    num_updates: int
    rejected: int = 0


class FedAvgAggregator(AggregationStrategy):
    """Simple FedAvg (weighted average) aggregation strategy."""

    async def aggregate(self, updates: list[ClientUpdate]) -> list[float]:
        if not updates:
            return []
        # Validate consistent dimension
        dim = len(updates[0].vector)
        total_w = 0.0
        acc = [0.0] * dim
        for upd in updates:
            if len(upd.vector) != dim:
                # Skip inconsistent update
                continue
            w = float(upd.weight if upd.weight > 0 else 1.0)
            total_w += w
            for i, val in enumerate(upd.vector):
                acc[i] += w * float(val)
        if total_w <= 0.0:
            return [0.0] * dim
        return [v / total_w for v in acc]


class BasicPrivacyGuard(PrivacyGuard):
    """Basic L2 clipping and Gaussian noise utilities (pure Python)."""

    def clip(self, vector: list[float], *, clip_norm: float) -> list[float]:
        if clip_norm <= 0:
            return [0.0 for _ in vector]
        norm_sq = sum(float(x) * float(x) for x in vector)
        if norm_sq <= 0.0:
            return [0.0 for _ in vector]
        norm = math.sqrt(norm_sq)
        scale = min(1.0, clip_norm / norm)
        # Avoid direct float equality check
        if abs(scale - 1.0) < 1e-12:
            return [float(x) for x in vector]
        return [float(x) * scale for x in vector]

    def add_noise(
        self,
        vector: list[float],
        *,
        clip_norm: float,
        sigma: float,
        seed: int | None = None,
    ) -> list[float]:
        if sigma <= 0.0:
            return [float(x) for x in vector]
        rng = random.Random(seed)
        # Gaussian with std = sigma * C per coordinate (isotropic)
        std = abs(sigma) * abs(clip_norm)
        return [float(x) + rng.gauss(0.0, std) for x in vector]


class FederatedService:
    """Orchestrates round planning and secure aggregation (skeleton)."""

    def __init__(
        self,
        *,
        aggregator: AggregationStrategy | None = None,
        privacy: PrivacyGuard | None = None,
    ) -> None:
        self._agg = aggregator or FedAvgAggregator()
        self._privacy = privacy or BasicPrivacyGuard()
        self._ml = get_ml_settings()

    def plan_round(self) -> RoundPlan:
        """Create a round plan using ML settings defaults.

        Returns:
            RoundPlan: Planned configuration for the next round.
        """
        round_id = f"round_{uuid4()}"
        return RoundPlan(
            round_id=round_id,
            clip_norm=float(self._ml.__getattr__("EMBEDDING_BATCH_SIZE")) * 0.0
            + float(  # type: ignore[arg-type]
                getattr(self._ml, "fl_clip_norm", 1.0)
            ),
            dp_sigma=float(getattr(self._ml, "fl_dp_sigma", 0.0)),
            sample_rate=float(getattr(self._ml, "fl_sample_rate", 0.1)),
            steps=int(getattr(self._ml, "fl_round_steps", 100)),
            min_clients=int(getattr(self._ml, "fl_min_clients", 5)),
        )

    def validate_update(
        self,
        *,
        payload_size_bytes: int,
        content_type: str,
        sample_size: int,
        signature_required: bool,
        signature: str | None,
        max_bytes: int = 25 * 1024 * 1024,
        accepted_mimes: tuple[str, ...] = (
            "application/octet-stream",
            "application/x-npz",
        ),
    ) -> tuple[bool, str | None]:
        """Domain-only validation for update envelope (no DB).

        Returns:
            (ok, reason)
        """
        if payload_size_bytes <= 0 or payload_size_bytes > max_bytes:
            return False, "invalid_payload_size"
        if content_type not in accepted_mimes:
            return False, "unsupported_mime"
        if sample_size <= 0:
            return False, "invalid_sample_size"
        if signature_required and (not signature or len(signature) < 16):
            return False, "signature_required"
        return True, None

    async def aggregate_round(
        self,
        *,
        plan: RoundPlan,
        updates: list[ClientUpdate],
        apply_dp: bool = True,
        dp_seed: int | None = 1234,
        apply_clip: bool = True,
        metrics_hook: Callable[[float, int, int], None] | None = None,
    ) -> AggregationResult:
        """Apply clipping (+ optional DP noise) then aggregate via strategy.

        Returns:
            AggregationResult: vector and counters.
        """
        t0 = time.monotonic()
        cleaned: list[ClientUpdate] = []
        rejected = 0
        expected_dim: int | None = None
        for upd in updates:
            if not upd.vector:
                rejected += 1
                continue
            v = list(map(float, upd.vector))
            # Dimension validation: first non-empty vector sets expected_dim
            if expected_dim is None:
                expected_dim = len(v)
            elif len(v) != expected_dim:
                rejected += 1
                continue
            if apply_clip:
                v = self._privacy.clip(v, clip_norm=plan.clip_norm)
            if apply_dp and plan.dp_sigma > 0.0:
                v = self._privacy.add_noise(
                    v, clip_norm=plan.clip_norm, sigma=plan.dp_sigma, seed=dp_seed
                )
            cleaned.append(
                ClientUpdate(
                    client_id=upd.client_id,
                    round_id=upd.round_id,
                    vector=v,
                    weight=upd.weight,
                    signature=None,
                )
            )

        vec = await self._agg.aggregate(cleaned)
        dt = max(time.monotonic() - t0, 0.0)
        if metrics_hook is not None:
            try:
                metrics_hook(dt, len(cleaned), rejected)
            except Exception:
                # swallow metrics errors to keep domain pure
                pass
        return AggregationResult(
            round_id=plan.round_id,
            vector=vec,
            num_updates=len(cleaned),
            rejected=rejected,
        )


__all__ = [
    "FederatedService",
    "FedAvgAggregator",
    "BasicPrivacyGuard",
    "AggregationResult",
]
