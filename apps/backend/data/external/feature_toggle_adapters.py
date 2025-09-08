"""Feature Toggle Adapters module."""

from __future__ import annotations

from collections.abc import Mapping

from apps.backend.core.interfaces.feature_toggles import FeatureToggleProvider


class InMemoryFeatureToggleProvider(FeatureToggleProvider):
    def __init__(self) -> None:
        self.toggles: dict[str, bool] = {}

    def is_enabled(
        self,
        feature_name: str,
        user_id: str | None = None,
        attrs: Mapping[str, str] | None = None,
    ) -> bool:
        return self.toggles.get(feature_name, False)
import bool
import dict
import feature_name
import self
import str
