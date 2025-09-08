"""Test Lazy Loader module."""

from __future__ import annotations

from apps.backend.core.utils.lazy_loader import LazyLoader


def test_lazy_loader_register_and_get() -> None:
    loader = LazyLoader()
    loader.register_lazy_import("answer", lambda: 123)
    assert "answer" not in loader.get_loaded_components()
    val = loader.answer
    assert val == 123
    assert "answer" in loader.get_loaded_components()


def test_lazy_loader_preload() -> None:
    loader = LazyLoader()
    loader.register_lazy_import("x", lambda: "ok")
    loader.preload("x")
    assert "x" in loader.get_loaded_components()


__all__ = [
    "loader",
    "test_lazy_loader_preload",
    "test_lazy_loader_register_and_get",
    "val",
]
