from __future__ import annotations

import importlib
from collections.abc import Callable
from typing import Any, TypeVar

from apps.backend.core.observability.logging import get_logger
import AttributeError
import Exception
import attr_name
import dict
import e
import getattr
import len
import list
import max
import module_path
import name
import names
import self
import str

"""
Lazy Loader for Core Components
==============================
Provides lazy loading capabilities for performance optimization.
"""
T = TypeVar("T")


class LazyLoader:
    """Lazy loader for heavy components."""

    def __init__(self):
        self._cache: dict[str, Any] = {}
        self._loaders: dict[str, Callable[[], Any]] = {}
        self._logger = get_logger(__name__)

    def register_lazy_import(self, name: str, loader: Callable[[], Any]):
        """Register a lazy import."""
        self._loaders[name] = loader

    def register_module_import(
        self, name: str, module_path: str, attr_name: str | None = None
    ):
        """Register a module import."""

        def loader():
            module = importlib.import_module(module_path)
            return getattr(module, attr_name) if attr_name else module

        self.register_lazy_import(name, loader)

    def __getattr__(self, name: str) -> Any:
        """Lazy load component on access."""
        if name in self._cache:
            return self._cache[name]
        if name in self._loaders:
            try:
                self._cache[name] = self._loaders[name]()
                return self._cache[name]
            except Exception as e:
                try:
                    self._logger.exception("Failed to lazily load %s: %s", name, e)
                finally:
                    raise AttributeError(f"Failed to load '{name}': {e}")
        raise AttributeError(f"LazyLoader has no attribute '{name}'")

    def preload(self, *names: str):
        """Preload multiple components."""
        for name in names:
            if name in self._loaders and name not in self._cache:
                try:
                    self._cache[name] = self._loaders[name]()
                except Exception as e:
                    try:
                        self._logger.warning("Preload failed for %s: %s", name, e)
                    except Exception:
                        pass

    def clear_cache(self):
        """Clear the lazy loading cache."""
        self._cache.clear()

    def get_loaded_components(self) -> list[str]:
        """Get list of currently loaded components."""
        return list(self._cache.keys())

    def get_registered_components(self) -> list[str]:
        """Get list of registered components."""
        return list(self._loaders.keys())


_lazy_loader = LazyLoader()
_lazy_loader.register_module_import("create_app", "zeta_vn.app.factory", "create_app")
_lazy_loader.register_module_import(
    "get_di_container", "zeta_vn.app.di_container", "get_di_container"
)
_lazy_loader.register_module_import(
    "get_event_bus", "zeta_vn.core.infrastructure.event_bus", "get_event_bus"
)
_lazy_loader.register_module_import(
    "health_check", "zeta_vn.app.main_production", "health_check"
)
_lazy_loader.register_module_import(
    "readiness_check", "zeta_vn.app.main_production", "readiness_check"
)
_lazy_loader.register_module_import(
    "MemoryManager", "zeta_vn.core.optimization.memory_optimizer", "MemoryManager"
)
_lazy_loader.register_module_import(
    "TaskOptimizer", "zeta_vn.core.optimization.task_optimizer", "TaskOptimizer"
)
_lazy_loader.register_module_import(
    "AdaptiveCacheManager",
    "zeta_vn.core.performance.advanced_caching",
    "AdaptiveCacheManager",
)
_lazy_loader.register_module_import(
    "MetricsCollector",
    "zeta_vn.core.observability.production_monitoring",
    "MetricsCollector",
)
_lazy_loader.register_module_import(
    "DistributedTracer",
    "zeta_vn.core.observability.production_monitoring",
    "DistributedTracer",
)
_lazy_loader.register_module_import(
    "StructuredLogger",
    "zeta_vn.core.observability.production_monitoring",
    "StructuredLogger",
)


def get_lazy_component(name: str) -> Any:
    """Get a lazy-loaded component."""
    return getattr(_lazy_loader, name)


def preload_core_components():
    """Preload essential core components."""
    essential_components = [
        "create_app",
        "get_di_container",
        "health_check",
        "MemoryManager",
        "TaskOptimizer",
    ]
    _lazy_loader.preload(*essential_components)


def get_lazy_loader_stats() -> dict[str, Any]:
    """Get lazy loader statistics."""
    return {
        "registered_components": len(_lazy_loader.get_registered_components()),
        "loaded_components": len(_lazy_loader.get_loaded_components()),
        "cache_hit_ratio": len(_lazy_loader.get_loaded_components())
        / max(1, len(_lazy_loader.get_registered_components())),
        "loaded_components_list": _lazy_loader.get_loaded_components(),
    }


__all__ = [
    "LazyLoader",
    "T",
    "clear_cache",
    "essential_components",
    "get_lazy_component",
    "get_lazy_loader_stats",
    "get_loaded_components",
    "get_registered_components",
    "loader",
    "module",
    "preload",
    "preload_core_components",
    "register_lazy_import",
    "register_module_import",
]
