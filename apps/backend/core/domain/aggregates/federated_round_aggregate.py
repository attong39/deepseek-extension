from __future__ import annotations

from app._base_model import DomainModel
from .base import AggregateRoot, DomainEvent, ensure
import artifact_ref
import client_id
import dict
import getattr
import len
import list
import metrics
import participants
import round_id
import self
import str
import strategy
import subs


class FederatedRoundAggregate(AggregateRoot[DomainModel]):
    """
    Aggregate for coordinating a federated learning round for a specific model.

    Tracks:
    - round_id
    - participants (client_id list)
    - submissions (client_id -> artifact/metrics)
    - aggregation result
    """

    AGG = "federated_round"

    def start_round(self, round_id: str, participants: list[str]) -> None:
        ensure(round_id.strip() != "", "round_id required.")
        ensure(len(participants) > 0, "participants required.")
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        ensure(not meta.get("fed", {}).get("active", False), "Another round is active.")
        meta["fed"] = {
            "active": True,
            "round_id": round_id,
            "participants": participants,
            "submissions": {},
            "result": None,
        }
        self._replace(metadata=meta)
        self._record(
            DomainEvent.make(
                "FedRoundStarted",
                self.AGG,
                self.id,
                round_id=round_id,
                participants=participants,
            )
        )

    def submit_update(self, client_id: str, metrics: dict, artifact_ref: str) -> None:
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        ensure(meta.get("fed", {}).get("active", False), "No active round.")
        ensure(client_id in meta["fed"]["participants"], "Client not registered.")
        subs: dict[str, dict] = dict(meta["fed"]["submissions"])
        ensure(client_id not in subs, "Client already submitted.")
        subs[client_id] = {"metrics": metrics, "artifact": artifact_ref}
        meta["fed"]["submissions"] = subs
        self._replace(metadata=meta)
        self._record(
            DomainEvent.make(
                "FedClientSubmitted", self.AGG, self.id, client_id=client_id
            )
        )

    def aggregate_updates(self, strategy: str = "weighted_avg") -> None:
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        ensure(meta.get("fed", {}).get("active", False), "No active round.")
        subs: dict[str, dict] = dict(meta["fed"]["submissions"])
        ensure(len(subs) > 0, "No submissions to aggregate.")
        # Note: Real aggregation lives in application/service layer.
        meta["fed"]["result"] = {"strategy": strategy, "num_clients": len(subs)}
        self._replace(metadata=meta)
        self._record(
            DomainEvent.make("FedRoundAggregated", self.AGG, self.id, strategy=strategy)
        )

    def end_round(self) -> None:
        meta = dict(getattr(self.entity, "metadata", {}) or {})
        ensure(meta.get("fed", {}).get("active", False), "No active round.")
        meta["fed"]["active"] = False
        self._replace(metadata=meta)
        self._record(DomainEvent.make("FedRoundEnded", self.AGG, self.id))
