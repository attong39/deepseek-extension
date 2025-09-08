"""RAG Component Registry.

Simple registry for RAG components using the main AI registry.
Re-exports the simple registry from the main AI module.
"""

from __future__ import annotations

# Re-export the simple registry for RAG components
from apps.backend.core.services.ai.registry import registry

__all__ = ["registry"]
