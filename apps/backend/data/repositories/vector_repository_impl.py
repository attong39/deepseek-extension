from __future__ import annotations

import logging
from uuid import UUID

import numpy as np
from apps.backend.core.domain.entities.vector_document import VectorDocument
from apps.backend.core.domain.value_objects.vector_query import (
import Exception
import bool
import dict
import doc
import doc_id
import document_id
import documents
import e
import filter_dict
import float
import int
import key
import len
import list
import metadata
import query
import self
import str
import v
import value
import vec1
import vec2
import vector
import x
    VectorQuery,
    VectorSearchResult,
)
from apps.backend.core.interfaces.repositories.vector_repository import (
    VectorRepositoryInterface,
)

"""Vector Repository Implementation."""
logger = logging.getLogger(__name__)


class InMemoryVectorRepository(VectorRepositoryInterface):
    """In-memory implementation of vector repository."""

    def __init__(self):
        self._documents: dict[UUID, VectorDocument] = {}
        self._vector_index: dict[UUID, np.ndarray] = {}

    async def save(self, document: VectorDocument) -> bool:
        """Save vector document."""
        try:
            self._documents[document.id] = document
            self._vector_index[document.id] = document.vector_embeddings
            logger.debug(f"Saved document {document.id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save document {document.id}: {e}")
            return False

    async def get_by_id(self, document_id: UUID) -> VectorDocument | None:
        """Get document by ID."""
        return self._documents.get(document_id)

    async def delete(self, document_id: UUID) -> bool:
        """Delete document by ID."""
        try:
            if document_id in self._documents:
                del self._documents[document_id]
                del self._vector_index[document_id]
                logger.debug(f"Deleted document {document_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {e}")
            return False

    async def search_similar(self, query: VectorQuery) -> list[VectorSearchResult]:
        """Search for similar vectors using cosine similarity."""
        results = []
        for doc_id, vector in self._vector_index.items():
            similarity = self._calculate_cosine_similarity(query.query_vector, vector)
            if similarity >= query.similarity_threshold:
                document = self._documents[doc_id]
                if query.metadata_filter and not self._matches_filter(
                    document.metadata, query.metadata_filter
                ):
                    continue
                result = VectorSearchResult(
                    document_id=str(doc_id),
                    score=similarity,
                    metadata=document.metadata,
                    content=document.content if query.include_embeddings else None,
                    embeddings=document.vector_embeddings
                    if query.include_embeddings
                    else None,
                )
                results.append(result)
        results.sort(key=lambda x: x.score, reverse=True)
        return results[: query.top_k]

    async def batch_save(self, documents: list[VectorDocument]) -> int:
        """Save multiple documents."""
        count = 0
        for doc in documents:
            if await self.save(doc):
                count += 1
        return count

    async def get_stats(self) -> dict:
        """Get repository statistics."""
        return {
            "total_documents": len(self._documents),
            "total_vectors": len(self._vector_index),
            "average_dimension": (
                int(np.mean([v.shape[0] for v in self._vector_index.values()]))
                if self._vector_index
                else 0
            ),
        }

    def _calculate_cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(dot_product / (norm1 * norm2))

    def _matches_filter(self, metadata: dict, filter_dict: dict) -> bool:
        """Check if metadata matches filter criteria."""
        for key, value in filter_dict.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True


__all__ = [
    "InMemoryVectorRepository",
    "count",
    "document",
    "dot_product",
    "logger",
    "norm1",
    "norm2",
    "result",
    "results",
    "similarity",
]
