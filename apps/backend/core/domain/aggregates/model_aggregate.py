from __future__ import annotations

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.aggregates.base import AggregateRoot, DomainEvent, ensure
import dict
import float
import getattr
import list
import metrics
import name
import reason
import registry_uri
import self
import stage
import str
import to_version
import version


class ModelAggregate(AggregateRoot[DomainModel]):
    """
    Aggregate for ML Model lifecycle: register → promote → deprecate → rollback.

    status ∈ {"draft","staging","production","deprecated"}
    """

    AGG = "model"

    def register(
        self, name: str, version: str, registry_uri: str, meta: dict | None = None
    ) -> None:
        ensure(name.strip() != "", "name required.")
        ensure(version.strip() != "", "version required.")
        self._replace(
            name=name, version=version, registry_uri=registry_uri, metadata=meta or {}
        )
        self._record(
            DomainEvent.make(
                "ModelRegistered", self.AGG, self.id, name=name, version=version
            )
        )

    def promote(self, stage: str = "production") -> None:
        ensure(stage in {"staging", "production"}, "Invalid stage.")
        self._replace(status=stage)
        self._record(DomainEvent.make("ModelPromoted", self.AGG, self.id, stage=stage))

    def deprecate(self, reason: str | None = None) -> None:
        self._replace(status="deprecated")
        self._record(
            DomainEvent.make("ModelDeprecated", self.AGG, self.id, reason=reason or "")
        )

    def rollback(self, to_version: str) -> None:
        ensure(to_version.strip() != "", "to_version required.")
        self._replace(version=to_version, status="staging")
        self._record(
            DomainEvent.make(
                "ModelRolledBack", self.AGG, self.id, to_version=to_version
            )
        )

    def update_metrics(self, metrics: dict[str, float]) -> None:
        current_meta = getattr(self.entity, "metadata", {}) or {}
        meta = {**current_meta}
        hist = meta.get("metrics_history", [])
        hist.append({"metrics": metrics})
        meta["metrics_history"] = hist
        self._replace(metadata=meta)
        self._record(
            DomainEvent.make(
                "ModelMetricsUpdated", self.AGG, self.id, keys=list(metrics.keys())
            )
        )
