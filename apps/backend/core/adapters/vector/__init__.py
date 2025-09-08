"""Vector adapters compatibility layer.

This module provides compatibility exports for vector storage operations,
bridging the core application layer with data layer implementations.

It re-exports key components from the data layer vector adapters to maintain
clean separation of concerns while providing convenient access for application
logic that needs vector operations.
"""

from __future__ import annotations

__all__ = [
    "Document",
    "MemoryVectorStoreAdapter",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "memory_vector_store",
]

# <<< AUTO-GEN
