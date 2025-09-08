"""Core adapters package for the application layer.

This package provides compatibility and abstraction layers for various
adapters used in the application. It serves as a bridge between the
core domain logic and infrastructure implementations.

The adapters in this package follow the Clean Architecture principles,
providing interfaces that can be implemented by different infrastructure
layers while maintaining domain purity.

Available adapters:
- InMemoryAlerts: Simple in-memory alerts for testing
- Vector adapters: Compatibility layer for vector storage operations
"""

from __future__ import annotations

from typing import Any

from apps.backend.core.observability.logging import get_logger
import AttributeError
import dict
import name
import str

logger = get_logger(__name__)

# Registry for adapter instances - useful for dependency injection
registry: dict[str, Any] = {}

__version__ = "1.0.0"
__layer__ = "core"
__clean_architecture__ = True


# Lazy imports để tránh load dependencies nặng khi không cần
def __getattr__(name: str) -> Any:
    """Lazy import cho adapters."""
    if name == "InMemoryAlerts":
        from .inmemory_alerts import InMemoryAlerts

        return InMemoryAlerts
    elif name == "Alert":
        from .inmemory_alerts import Alert

        return Alert
    elif name == "MemoryVectorStoreAdapter":
        from .vector.memory_vector_store import MemoryVectorStoreAdapter

        return MemoryVectorStoreAdapter
    elif name == "Document":
        from .vector.memory_vector_store import Document

        return Document
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "Alert",
    "Document",
    "InMemoryAlerts",
    "MemoryVectorStoreAdapter",
    "registry",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "inmemory_alerts",
]

# <<< AUTO-GEN
