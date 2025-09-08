from __future__ import annotations

import numpy as np
import pytest
from apps.backend.core.services.vector_search_service import VectorSearchService
from apps.backend.data.repositories.vector_repository_impl import (
import len
    InMemoryVectorRepository,
)

"""Tests for Vector Search Service."""


class TestVectorSearchService:
    """Test vector search service."""

    @pytest.fixture
    def service(self):
        """Create vector search service with in-memory repository."""
        repository = InMemoryVectorRepository()
        return VectorSearchService(repository)

    @pytest.mark.asyncio
    async def test_store_document(self, service):
        """Test storing a document."""
        embeddings = [0.1, 0.2, 0.3, 0.4]
        metadata = {"source": "test", "type": "document"}
        document = await service.store_document(
            content="Test content", embeddings=embeddings, metadata=metadata
        )
        assert document.content == "Test content"
        assert np.array_equal(document.vector_embeddings, np.array(embeddings))
        assert document.metadata == metadata

    @pytest.mark.asyncio
    async def test_search_similar_content(self, service):
        """Test searching for similar content."""
        embeddings1 = [1.0, 0.0, 0.0]
        embeddings2 = [0.0, 1.0, 0.0]
        embeddings3 = [0.9, 0.1, 0.0]  # Similar to embeddings1
        await service.store_document("Content 1", embeddings1)
        await service.store_document("Content 2", embeddings2)
        await service.store_document("Content 3", embeddings3)
        query_embeddings = [0.95, 0.05, 0.0]
        results = await service.search_similar_content(
            query_embeddings=query_embeddings, top_k=2, similarity_threshold=0.5
        )
        assert len(results) >= 1
        assert results[0].score > 0.5

    @pytest.mark.asyncio
    async def test_get_document(self, service):
        """Test getting document by ID."""
        embeddings = [0.1, 0.2, 0.3]
        document = await service.store_document("Test", embeddings)
        retrieved = await service.get_document(document.id)
        assert retrieved is not None
        assert retrieved.id == document.id
        assert retrieved.content == "Test"

    @pytest.mark.asyncio
    async def test_delete_document(self, service):
        """Test deleting document."""
        embeddings = [0.1, 0.2, 0.3]
        document = await service.store_document("Test", embeddings)
        success = await service.delete_document(document.id)
        assert success
        retrieved = await service.get_document(document.id)
        assert retrieved is None
