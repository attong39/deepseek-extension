from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator
from typing import Protocol

from apps.backend.core.domain.entities.document_clean import (
import Exception
import RuntimeError
import ValueError
import bool
import chunking_service
import e
import embedding_service
import float
import int
import len
import list
import locals
import request
import self
import str
import vector_store_service
    Document,
    DocumentStatus,
    create_document,
)
from pydantic import BaseModel

"""
🎯 ZETA_AI Use Cases - RAG One-Click Learning Pipeline
Clean Architecture use case implementation
Features:
- ✅ Orchestrates full RAG pipeline: ingest→extract→chunk→embed→index
- ✅ WebSocket streaming support
- ✅ Type-safe với dependency injection
- ✅ Error handling và retry logic
"""
logger = logging.getLogger(__name__)


class EmbeddingService(Protocol):
    """Protocol for embedding service"""

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for text chunks"""
        ...


class ChunkingService(Protocol):
    """Protocol for text chunking service"""

    def chunk_text(self, text: str, chunk_size: int = 512) -> list[str]:
        """Split text into semantic chunks"""
        ...


class VectorStoreService(Protocol):
    """Protocol for vector database service"""

    async def index_document(self, document: Document) -> bool:
        """Index document in vector database"""
        ...


class RAGRequest(BaseModel):
    """Request for RAG One-Click Learning"""

    title: str
    content: str
    file_type: str = "txt"
    file_size: int = 0
    chunk_size: int = 512
    enable_streaming: bool = True


class RAGProgressUpdate(BaseModel):
    """Progress update for streaming"""

    step: str
    progress: float  # 0.0 to 1.0
    message: str
    document_id: str | None = None


class RAGResult(BaseModel):
    """Final result of RAG processing"""

    document_id: str
    status: DocumentStatus
    chunks_count: int
    embeddings_count: int
    processing_time_ms: int
    error: str | None = None


class OneClickRAGUseCase:
    """
    Use case for One-Click RAG Learning Pipeline
    Orchestrates the complete flow:
    1. Create document entity
    2. Chunk text into semantic pieces
    3. Generate embeddings for chunks
    4. Index in vector database
    5. Stream progress via WebSocket
    """

    def __init__(
        self,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
    ) -> None:
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_store_service = vector_store_service

    async def execute(
        self, request: RAGRequest
    ) -> AsyncGenerator[RAGProgressUpdate | RAGResult, None]:
        """
        Execute One-Click RAG Learning pipeline with streaming progress
        Args:
            request: RAG processing request
        Yields:
            Progress updates during processing
            Final result at the end
        Raises:
            ValueError: Invalid input data
            RuntimeError: Processing failure
        """
        start_time = asyncio.get_event_loop().time()
        try:
            yield RAGProgressUpdate(
                step="create_document",
                progress=0.1,
                message="Creating document entity...",
            )
            document = create_document(
                title=request.title,
                content=request.content,
                file_type=request.file_type,
                file_size=request.file_size or len(request.content.encode()),
            )
            document = document.mark_as_processing()
            yield RAGProgressUpdate(
                step="chunking",
                progress=0.3,
                message="Chunking text into semantic pieces...",
                document_id=document.id,
            )
            chunks = self.chunking_service.chunk_text(
                document.content, chunk_size=request.chunk_size
            )
            if not chunks:
                raise ValueError("No chunks generated from document content")
            yield RAGProgressUpdate(
                step="embedding",
                progress=0.6,
                message=f"Generating embeddings for {len(chunks)} chunks...",
                document_id=document.id,
            )
            embeddings = await self.embedding_service.generate_embeddings(chunks)
            if len(embeddings) != len(chunks):
                raise RuntimeError(
                    f"Embedding count mismatch: {len(embeddings)} != {len(chunks)}"
                )
            document = document.mark_as_processed(chunks=chunks, embeddings=embeddings)
            yield RAGProgressUpdate(
                step="indexing",
                progress=0.9,
                message="Indexing in vector database...",
                document_id=document.id,
            )
            success = await self.vector_store_service.index_document(document)
            if not success:
                raise RuntimeError("Failed to index document in vector database")
            end_time = asyncio.get_event_loop().time()
            processing_time_ms = int((end_time - start_time) * 1000)
            yield RAGResult(
                document_id=document.id,
                status=document.status,
                chunks_count=len(chunks),
                embeddings_count=len(embeddings),
                processing_time_ms=processing_time_ms,
            )
            logger.info(
                f"RAG pipeline completed successfully: {document.id} "
                f"({len(chunks)} chunks, {processing_time_ms}ms)"
            )
        except Exception as e:
            error_msg = str(e)
            logger.error(f"RAG pipeline failed: {error_msg}")
            try:
                if "document" in locals():
                    document = document.mark_as_failed()
            except Exception:
                pass  # Ignore secondary errors
            end_time = asyncio.get_event_loop().time()
            processing_time_ms = int((end_time - start_time) * 1000)
            yield RAGResult(
                document_id=locals().get("document", Document).id
                if "document" in locals()
                else "unknown",
                status=DocumentStatus.FAILED,
                chunks_count=0,
                embeddings_count=0,
                processing_time_ms=processing_time_ms,
                error=error_msg,
            )


__all__ = [
    "ChunkingService",
    "EmbeddingService",
    "OneClickRAGUseCase",
    "RAGProgressUpdate",
    "RAGRequest",
    "RAGResult",
    "VectorStoreService",
]
