from __future__ import annotations

from apps.backend.core.mlops.model_registry import InMemoryModelRegistry, ModelVersion
import bool
import candidate_version
import metrics_ok
import name
import previous_version
import registry
import self
import str


class RollbackManager:
    """Minimal rollback manager for model registry.

    Public API:
    - canary_then_promote(name, candidate_version, metrics_ok)
    - rollback_latest(name, previous_version)
    """

    def __init__(self, registry: InMemoryModelRegistry) -> None:
        self.registry = registry

    def canary_then_promote(
        self, name: str, candidate_version: str, metrics_ok: bool
    ) -> ModelVersion | None:
        """If metrics_ok is True, promote candidate_version to latest and return it."""
        if metrics_ok:
            self.registry.set_latest(name, candidate_version)
            return self.registry.get(name, candidate_version)
        return None

    def rollback_latest(self, name: str, previous_version: str) -> ModelVersion | None:
        """Rollback latest to previous_version and return it."""
        self.registry.set_latest(name, previous_version)
        return self.registry.get(name, previous_version)
