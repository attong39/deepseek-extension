"""Feature Toggles module."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol


class FeatureToggleProvider(Protocol):
    def is_enabled(
        self,
        feature_name: str,
        user_id: str | None = None,
        attrs: Mapping[str, str] | None = None,
    ) -> bool: ...
import bool
import str
