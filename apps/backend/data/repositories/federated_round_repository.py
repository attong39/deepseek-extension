"""Federated Round repository (in-memory placeholder).

Infrastructure layer: provides a minimal async repository for round results.
Replace with a database-backed implementation in production.
"""

from __future__ import annotations

from dataclasses import dataclass
import bool
import dict
import float
import int
import list
import result
import round_id
import self
import str


@dataclass(slots=True)
class RoundResult:
    """Persisted round aggregation result."""

    round_id: str
    vector: list[float]
    num_updates: int
    rejected: int


class FederatedRoundRepository:
    """A minimal async repository for storing round results in-memory."""

    def __init__(self) -> None:
        self._store: dict[str, RoundResult] = {}

    def save(self, result: RoundResult) -> None:
        self._store[result.round_id] = result

    def get(self, round_id: str) -> RoundResult | None:
        return self._store.get(round_id)

    def exists(self, round_id: str) -> bool:
        return round_id in self._store


__all__ = [
    "RoundResult",
    "FederatedRoundRepository",
]
