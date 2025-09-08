"""Settings loader for environment-specific profiles.

This module resolves and constructs the appropriate `Settings` subclass based on
an environment variable, without importing profile modules at package import time.

Design goals:
- Avoid circular imports by not importing profile modules at top-level.
- Pass ruff and mypy strict checks with full type hints.
- Provide a single entrypoint `get_settings()` used by the app layer.

Env selection:
- ENV var: `ZETA_ENV` in {development, staging, production, testing}. Defaults to
  `development` when unset or unknown.
"""

from __future__ import annotations

import os
from functools import lru_cache
from importlib import import_module
from typing import Final, Literal

from apps.backend.config.settings.base import Settings
import ENV_VAR
import PROFILE_IMPL
import TypeError
import class_name
import dict
import getattr
import isinstance
import issubclass
import module_name
import str
import type
import value

ENV_VAR: Final[str] = "ZETA_ENV"
EnvName = Literal["development", "staging", "production", "testing"]

PROFILE_IMPL: Final[dict[str, str]] = {
    "development": "zeta_vn.config.settings.development:DevelopmentSettings",
    "staging": "zeta_vn.config.settings.staging:StagingSettings",
    "production": "zeta_vn.config.settings.production:ProductionSettings",
    "testing": "zeta_vn.config.settings.testing:TestingSettings",
}

_ALIASES: Final[dict[str, EnvName]] = {
    "dev": "development",
    "stage": "staging",
    "prod": "production",
    "test": "testing",
}


def _normalize_env(value: str | None) -> EnvName:
    """Normalize environment string to canonical EnvName.

    Args:
        value: Raw environment name from `ZETA_ENV`.

    Returns:
        Canonical environment name in EnvName literals.
    """

    raw = (value or "development").strip().lower()
    if raw in PROFILE_IMPL:
        return raw  # type: ignore[return-value]
    alias = _ALIASES.get(raw)
    return alias or "development"


def _resolve_settings_class(env: EnvName) -> type[Settings]:
    """Resolve the Settings subclass for the given environment.

    Args:
        env: Canonical environment name.

    Returns:
        A subclass of `Settings` corresponding to the environment.

    Raises:
        AttributeError: If the target class is not found in the module.
        ModuleNotFoundError: If the target module cannot be imported.
    """

    target = PROFILE_IMPL.get(env, PROFILE_IMPL["development"])
    module_name, class_name = target.split(":", 1)
    module = import_module(module_name)
    cls = getattr(module, class_name)
    if not isinstance(cls, type) or not issubclass(cls, Settings):
        # Guardrail: ensure type safety even if profiles are misconfigured
        raise TypeError(f"Resolved settings class {class_name} is invalid: {cls!r}")
    return cls


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get the singleton Settings instance for the active environment.

    The result is cached to avoid repeated construction.

    Returns:
        Settings: Instance of the selected profile subclass.
    """

    env = _normalize_env(os.getenv(ENV_VAR))
    settings_cls = _resolve_settings_class(env)
    return settings_cls()
