"""
Federated Learning core interfaces and lightweight data models.

Clean Architecture: This module defines domain-level contracts (Protocols)
that services and repositories should depend on. No infrastructure imports.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import float
import int
import list
import str


@dataclass(slots=True, frozen=True)
class RoundPlan:
    """Plan/configuration for a federated training round.

    Args:
        round_id: Unique identifier for the round.
        clip_norm: L2 clipping threshold C for updates.
        dp_sigma: Gaussian noise multiplier (sigma). Use 0.0 to disable.
        sample_rate: Expected client sampling rate (0-1).
        steps: Local training steps per client.
        min_clients: Minimum number of client updates required to aggregate.
    """

    round_id: str
    clip_norm: float
    dp_sigma: float
    sample_rate: float
    steps: int
    min_clients: int


@dataclass(slots=True, frozen=True)
class ClientUpdate:
    """Client update payload for a round.

    Args:
        client_id: Unique client identifier.
        round_id: Round this update belongs to.
        vector: Flattened parameter delta (same length across clients).
        weight: Optional weight (e.g., samples count) for weighted average.
        signature: Optional detached signature for authenticity.
    """

    client_id: str
    round_id: str
    vector: list[float]
    weight: float = 1.0
    signature: str | None = None


class AggregationStrategy(Protocol):
    """Aggregation strategy contract (e.g., FedAvg, Median, Krum)."""

    async def aggregate(self, updates: list[ClientUpdate]) -> list[float]: ...


class PrivacyGuard(Protocol):
    """Privacy mechanisms applied client-side or server-side before aggregation."""

    def clip(self, vector: list[float], *, clip_norm: float) -> list[float]: ...

    def add_noise(
        self,
        vector: list[float],
        *,
        clip_norm: float,
        sigma: float,
        seed: int | None = None,
    ) -> list[float]: ...


class ClientSelector(Protocol):
    """Client sampling strategy contract."""

    async def select(self, candidates: list[str], k: int) -> list[str]: ...


__all__ = [
    "RoundPlan",
    "ClientUpdate",
    "AggregationStrategy",
    "PrivacyGuard",
    "ClientSelector",
]
