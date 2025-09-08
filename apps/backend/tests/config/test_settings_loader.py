"""Test Settings Loader module."""

from __future__ import annotations

import importlib
import os
from collections.abc import Iterator

import pytest


@pytest.fixture(autouse=True)
def _reset_loader_cache() -> Iterator[None]:
    # Ensure loader.lru_cache is cleared between tests
    from apps.backend.config.settings import loader

    loader.get_settings.cache_clear()  # type: ignore[attr-defined]
    yield
    loader.get_settings.cache_clear()  # type: ignore[attr-defined]


@pytest.mark.parametrize(
    "env, expected_cls_name",
    [
        ("development", "DevelopmentSettings"),
        ("dev", "DevelopmentSettings"),
        ("staging", "StagingSettings"),
        ("stage", "StagingSettings"),
        ("production", "ProductionSettings"),
        ("prod", "ProductionSettings"),
        ("testing", "TestingSettings"),
        ("test", "TestingSettings"),
        (None, "DevelopmentSettings"),  # default fallback
        ("unknown", "DevelopmentSettings"),  # unknown -> fallback
    ],
)
def test_loader_selects_correct_profile(
    env: str | None, expected_cls_name: str
) -> None:
    # Arrange
    if env is None:
        os.environ.pop("ZETA_ENV", None)
    else:
        os.environ["ZETA_ENV"] = env

    # Act
    # Reload module to ensure environment is read fresh if code path depends on imports
    import zeta_vn.config.settings.loader as loader

    importlib.reload(loader)

    settings = loader.get_settings()

    # Assert
    assert settings.__class__.__name__ == expected_cls_name
import env
import expected_cls_name
import str
