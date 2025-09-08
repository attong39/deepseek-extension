"""
Enhanced Vector Store with Hybrid Search Capabilities.

Combines semantic vector search with BM25 lexical search for better retrieval.
"""

from __future__ import annotations

import asyncio
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
import int
import isinstance
import k
import key
import len
import list
import metadata
import metadata_filter
import open
import query
import range
import result
import self
import str
import sum
import super
import text
import tuple
import use_hybrid
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
    text: str
    metadata: dict[str, Any] | None = None
    vector: Vector | None = None


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


class MemoryVectorStoreAdapterEnhanced:
    """
    Enhanced in-memory vector store with hybrid search capabilities.

    Features:
    - Async operations for better performance
    - Hybrid search (BM25 + Vector similarity)
    - Document persistence/restore
    - Metadata filtering
    - Efficient batch operations
    - Deterministic embedding fallback
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

        # Update hybrid search corpus after adding documents
        if self._hybrid_engine and self._docs:
            all_docs = list(self._docs.values())
            self._hybrid_engine.update_corpus(all_docs)

        logger.debug(f"Added {len(added_ids)} documents async")
        return added_ids

    async def search(
        self,
        query: str | Vector,
        k: int = 10,
        metadata_filter: dict[str, Any] | None = None,
        use_hybrid: bool = True,
    ) -> list[SearchResult]:
        """
        Search for similar documents with optional hybrid search.

        Args:
            query: Query text or vector
            k: Number of results to return
            metadata_filter: Optional metadata filtering
            use_hybrid: Whether to use hybrid search (lexical + semantic)

        Returns:
            List of search results sorted by relevance
        """
        # Convert query to vector if needed
        query_text = ""
        if isinstance(query, str):
            query_text = query
            query_vector = await asyncio.to_thread(_hashing_embed, query, self.dim)
        else:
            query_vector = query

        # Get vector similarity results first
        vector_results = await self._vector_search(query_vector, k * 2, metadata_filter)

        # Use hybrid search if enabled and query is text
        if (
            use_hybrid
            and self.enable_hybrid_search
            and self._hybrid_engine
            and query_text.strip()
        ):
            # Hybrid search combines vector + BM25
            return self._hybrid_engine.search(query_text, query_vector, vector_results)
        else:
            # Return pure vector search results
            return vector_results[:k]

    async def _vector_search(
        self,
        query_vector: Vector,
        k: int,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        """Pure vector similarity search."""

        def _compute_similarities():
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

            return scored_docs

        # Offload computation to thread pool
        scored_docs = await asyncio.to_thread(_compute_similarities)

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

    async def get(self, doc_id: str) -> Document | None:
        """Get document by ID."""
        return self._docs.get(doc_id)

    async def delete(self, doc_id: str) -> bool:
        """Delete document by ID."""
        if doc_id in self._docs:
            del self._docs[doc_id]
            # Update hybrid search corpus after deletion
            if self._hybrid_engine and self._docs:
                all_docs = list(self._docs.values())
                self._hybrid_engine.update_corpus(all_docs)
            return True
        return False

    async def get_stats(self) -> dict[str, Any]:
        """Get store statistics."""
        total_docs = len(self._docs)
        has_vectors = sum(1 for doc in self._docs.values() if doc.vector)

        stats = {
            "total_documents": total_docs,
            "documents_with_vectors": has_vectors,
            "dimension": self.dim,
            "hybrid_search_enabled": self.enable_hybrid_search,
            "status": "healthy" if total_docs >= 0 else "degraded",
        }

        # Add hybrid search stats
        if self._hybrid_engine:
            hybrid_stats = self._hybrid_engine.get_stats()
            stats["hybrid_search"] = hybrid_stats

        return stats

    async def save_to_file(self, filepath: str) -> None:
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

        def _write_file():
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

        await asyncio.to_thread(_write_file)
        logger.info(f"Saved {len(self._docs)} documents to {filepath}")

    async def load_from_file(self, filepath: str) -> None:
        """Load store from JSON file."""

        def _read_file():
            with open(filepath, encoding="utf-8") as f:
                return json.load(f)

        data = await asyncio.to_thread(_read_file)

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

        # Update hybrid search corpus after loading
        if self._hybrid_engine and self._docs:
            all_docs = list(self._docs.values())
            self._hybrid_engine.update_corpus(all_docs)

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


# Legacy compatibility wrapper
class MemoryVectorStoreAdapter(MemoryVectorStoreAdapterEnhanced):
    """Legacy adapter for backward compatibility."""

    def add(self, docs: Sequence[Document]) -> list[str]:  # type: ignore
        """Sync version of add for backward compatibility."""
        import asyncio

        return asyncio.run(super().add(docs))

    def search(  # type: ignore
        self,
        query: str | Vector,
        k: int = 10,
        metadata_filter: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        """Sync version of search for backward compatibility."""
        import asyncio

        return asyncio.run(super().search(query, k, metadata_filter, use_hybrid=False))

    def get(self, doc_id: str) -> Document | None:  # type: ignore
        """Sync version of get for backward compatibility."""
        import asyncio

        return asyncio.run(super().get(doc_id))

    def delete(self, doc_id: str) -> bool:  # type: ignore
        """Sync version of delete for backward compatibility."""
        import asyncio

        return asyncio.run(super().delete(doc_id))

    def get_stats(self) -> dict[str, Any]:  # type: ignore
        """Sync version of get_stats for backward compatibility."""
        import asyncio

        return asyncio.run(super().get_stats())

    def save_to_file(self, filepath: str) -> None:  # type: ignore
        """Sync version of save_to_file for backward compatibility."""
        import asyncio

        asyncio.run(super().save_to_file(filepath))

    def load_from_file(self, filepath: str) -> None:  # type: ignore
        """Sync version of load_from_file for backward compatibility."""
        import asyncio

        asyncio.run(super().load_from_file(filepath))
