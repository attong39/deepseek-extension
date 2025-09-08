"""Memory vector store adapter compatibility module.

This module provides compatibility re-exports from the data layer vector
store implementations. It allows the core application layer to access
vector storage functionality without direct dependencies on infrastructure.

The re-exported components include:
- Document: Data structure for vectorized documents
- MemoryVectorStoreAdapter: In-memory vector storage implementation
"""

from __future__ import annotations

from apps.backend.data.adapters.vector.memory_vector_store import (
    Document,
    MemoryVectorStoreAdapter,
)

__all__ = [
    "Document",
    "MemoryVectorStoreAdapter",
]
