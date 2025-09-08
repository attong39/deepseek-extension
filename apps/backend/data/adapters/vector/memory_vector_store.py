"""
Enhanced In-Memory Vector Store theo ROADMAP specification.

Provides Document storage, cosine similarity search, và persistence.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
import ImportError
import a
import b
import bool
import dict
import dim
import doc_data
import doc_id
import docs
import enable_hybrid_search
import f
import filepath
import filter_criteria
import float
import i
import id
import int
import isinstance
import k
import key
import len
import list
import metadata
import metadata_filter
import open
import property
import query
import range
import result
import self
import str
import sum
import text
import tuple
import value
import vec1
import vec2
import x
import zip

logger = logging.getLogger(__name__)

Vector = list[float]


class BaseAdapter(ABC):
    """Base adapter interface."""

    @abstractmethod
    async def process(self, data: Any) -> Any:
        """Process data."""


@dataclass
class Document:
    """Document với vector embedding và metadata."""

    id: str
    text: str = ""  # Default empty for backward compatibility
    metadata: dict[str, Any] | None = None
    vector: Vector | None = None

    # Backward compatibility properties
    @property
    def content(self) -> str:
        """Alias for text (backward compatibility)."""
        return self.text

    @content.setter
    def content(self, value: str) -> None:
        """Setter for content (backward compatibility)."""
        self.text = value

    @property
    def embedding(self) -> Vector | None:
        """Alias for vector (backward compatibility)."""
        return self.vector

    @embedding.setter
    def embedding(self, value: Vector | None) -> None:
        """Setter for embedding (backward compatibility)."""
        self.vector = value

    def __init__(
        self,
        id: str,
        text: str = "",
        content: str | None = None,  # Backward compatibility
        metadata: dict[str, Any] | None = None,
        vector: Vector | None = None,
        embedding: Vector | None = None,  # Backward compatibility
    ):
        """Initialize with backward compatibility support."""
        self.id = id
        self.text = content if content is not None else text
        self.metadata = metadata
        self.vector = embedding if embedding is not None else vector


@dataclass
class SearchResult:
    """Search result với score và metadata."""

    id: str
    similarity: float
    content: str
    metadata: dict[str, Any] | None = None


def _hashing_embed(text: str, dim: int = 384) -> Vector:
    """
    Deterministic embedding using hash-based approach (fallback cho development).

    Not suitable for production - use proper embedding models.
    """
    # SHA-256 hash của text
    hash_bytes = hashlib.sha256(text.encode("utf-8")).digest()

    # Convert bytes to normalized vector
    vector = []
    for i in range(dim):
        byte_idx = i % len(hash_bytes)
        # Normalize to [-1, 1] range
        vector.append((hash_bytes[byte_idx] / 255.0) * 2.0 - 1.0)

    # Normalize vector
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude > 1e-8:
        vector = [x / magnitude for x in vector]

    return vector


class MemoryVectorStoreAdapter:
    """
    Enhanced in-memory vector store theo ROADMAP specification.

    Features:
    - Cosine similarity search với MMR re-ranking
    - Document persistence/restore
    - Metadata filtering
    - Efficient batch operations
    - Deterministic embedding fallback

    Note: For development/testing - use dedicated vector DB for production.
    """

    def __init__(self, dim: int = 384, enable_hybrid_search: bool = True) -> None:
        """Initialize store với specified dimension."""
        self.dim = dim
        self.enable_hybrid_search = enable_hybrid_search
        self._docs: dict[str, Document] = {}

        # Initialize hybrid search if enabled
        self._hybrid_engine = None
        if enable_hybrid_search:
            try:
                from apps.backend.data.adapters.vector.hybrid_search import (
                    HybridSearchConfig,
                    HybridSearchEngine,
                )

                self._hybrid_engine = HybridSearchEngine(HybridSearchConfig())
            except ImportError:
                logger.warning(
                    "Hybrid search not available, falling back to vector-only search"
                )
                self.enable_hybrid_search = False

        logger.info(
            "Initialized MemoryVectorStoreAdapter with dim=%d, hybrid=%s",
            dim,
            enable_hybrid_search,
        )

    async def add(self, docs: Sequence[Document]) -> list[str]:
        """
        Add documents to store với automatic embedding (async).

        Args:
            docs: Documents to add (auto-embed if no vector)

        Returns:
            List of document IDs added
        """
        import asyncio

        added_ids = []

        # Process documents in parallel for better performance
        async def process_doc(doc: Document) -> tuple[str, Document]:
            # Auto-embed if no vector provided (offload to thread pool)
            if doc.vector is None:
                vector = await asyncio.to_thread(_hashing_embed, doc.text, self.dim)
            else:
                vector = doc.vector

            # Create stored document
            stored_doc = Document(
                id=doc.id, text=doc.text, metadata=doc.metadata, vector=vector
            )
            return doc.id, stored_doc

        # Process all docs concurrently
        tasks = [process_doc(doc) for doc in docs]
        results = await asyncio.gather(*tasks)

        # Store all results
        for doc_id, stored_doc in results:
            self._docs[doc_id] = stored_doc
            added_ids.append(doc_id)

        logger.debug(f"Added {len(added_ids)} documents async")
        return added_ids

    def search(
        self,
        query: str | Vector,
        k: int = 10,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        """
        Search for similar documents.

        Args:
            query: Query text or vector
            k: Number of results to return
            metadata_filter: Optional metadata filtering

        Returns:
            List of search results sorted by relevance
        """
        # Convert query to vector if needed
        if isinstance(query, str):
            query_vector = _hashing_embed(query, self.dim)
        else:
            query_vector = query

        # Score all documents
        scored_docs = []
        for doc in self._docs.values():
            # Apply metadata filter if specified
            if metadata_filter and not self._matches_metadata_filter(
                doc.metadata, metadata_filter
            ):
                continue

            # Calculate similarity
            similarity = self._cosine_similarity(query_vector, doc.vector or [])

            scored_docs.append((similarity, doc))

        # Sort by similarity and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)

        results = []
        for similarity, doc in scored_docs[:k]:
            _ = SearchResult(
                id=doc.id,
                similarity=similarity,
                content=doc.text,
                metadata=doc.metadata,
            )
            results.append(result)

        return results

    async def batch_add(self, docs: Sequence[Document]) -> list[str]:
        """Batch add documents (alias for add method)."""
        return await self.add(docs)

    def get(self, doc_id: str) -> Document | None:  # type: ignore
        """Get document by ID (sync version for compatibility)."""
        return self._docs.get(doc_id)

    def delete(self, doc_id: str) -> bool:
        """Delete document by ID."""
        if doc_id in self._docs:
            del self._docs[doc_id]
            return True
        return False

    def get_stats(self) -> dict[str, Any]:
        """Get store statistics."""
        total_docs = len(self._docs)
        has_vectors = sum(1 for doc in self._docs.values() if doc.vector)

        return {
            "total_documents": total_docs,
            "documents_with_vectors": has_vectors,
            "dimension": self.dim,
            "status": "healthy" if total_docs >= 0 else "degraded",
        }

    def save_to_file(self, filepath: str) -> None:
        """Save store to JSON file."""
        data = {
            "dimension": self.dim,
            "documents": [
                {
                    "id": doc.id,
                    "text": doc.text,
                    "metadata": doc.metadata,
                    "vector": doc.vector,
                }
                for doc in self._docs.values()
            ],
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved {len(self._docs)} documents to {filepath}")

    def load_from_file(self, filepath: str) -> None:
        """Load store from JSON file."""
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        self.dim = data.get("dimension", self.dim)
        self._docs = {}

        for doc_data in data.get("documents", []):
            doc = Document(
                id=doc_data["id"],
                text=doc_data["text"],
                metadata=doc_data.get("metadata"),
                vector=doc_data.get("vector"),
            )
            self._docs[doc.id] = doc

        logger.info(f"Loaded {len(self._docs)} documents from {filepath}")

    def _cosine_similarity(self, vec1: Vector, vec2: Vector) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2, strict=False))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))

        if magnitude1 < 1e-8 or magnitude2 < 1e-8:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    def _matches_metadata_filter(
        self, metadata: dict[str, Any] | None, filter_criteria: dict[str, Any]
    ) -> bool:
        """Check if document metadata matches filter criteria."""
        if not metadata:
            return not filter_criteria

        for key, value in filter_criteria.items():
            if key not in metadata or metadata[key] != value:
                return False

        return True
