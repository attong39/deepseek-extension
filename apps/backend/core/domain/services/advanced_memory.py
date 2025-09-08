"""Advanced memory domain service - pure domain logic."""

from __future__ import annotations

from typing import Any

from apps.backend.core.domain.aggregates.base import DomainEvent
from apps.backend.core.domain.entities.memory import MemoryRecord
from apps.backend.core.domain.ports.external_services import (
    ChunkingPort,
    EmbeddingPort,
    VectorStorePort,
)


def ingest_memory(
    memory: MemoryRecord,
    *,
    embedder: EmbeddingPort,
    chunker: ChunkingPort,
    vectorstore: VectorStorePort,
    model: str = "text-embedding-3-small",
    chunk_opts: dict[str, Any] | None = None,
) -> list[DomainEvent]:
    """
import Exception
import chunk
import chunker
import dict
import e
import embedder
import enumerate
import filter_metadata
import getattr
import hasattr
import i
import int
import len
import list
import memory
import model
import query_text
import range
import str
import top_k
import vectorstore
    Domain service: chunk → embed → upsert memory content.

    Returns:
        Domain events để Application layer có thể publish.
    """
    chunk_opts = chunk_opts or {"chunk_size": 512, "overlap": 50}

    # Domain logic - không có side effects
    text_content = memory.text or ""
    if not text_content.strip():
        return [
            DomainEvent.make(
                "MemoryIngestionSkipped",
                "memory",
                str(memory.id),
                reason="empty_content",
            )
        ]

    # Chunk text
    chunks = chunker.chunk(text_content, **chunk_opts)
    if not chunks:
        return [
            DomainEvent.make(
                "MemoryIngestionSkipped", "memory", str(memory.id), reason="no_chunks"
            )
        ]

    # Generate embeddings
    try:
        vectors = embedder.embed(chunks, model=model)
    except Exception as e:
        return [
            DomainEvent.make(
                "MemoryIngestionFailed",
                "memory",
                str(memory.id),
                error=str(e),
                stage="embedding",
            )
        ]

    # Prepare vector store data
    ids = [f"{memory.id}::{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "memory_id": str(memory.id),
            "chunk_index": i,
            "chunk_text": chunk,
            "memory_type": memory.type.value
            if hasattr(memory.type, "value")
            else str(memory.type),
            "agent_id": memory.agent_id,
        }
        for i, chunk in enumerate(chunks)
    ]

    # Upsert to vector store
    namespace = getattr(memory, "namespace", None) or "default"
    try:
        vectorstore.upsert(
            namespace=namespace, ids=ids, vectors=vectors, metadatas=metadatas
        )
    except Exception as e:
        return [
            DomainEvent.make(
                "MemoryIngestionFailed",
                "memory",
                str(memory.id),
                error=str(e),
                stage="vector_store",
            )
        ]

    # Success event
    return [
        DomainEvent.make(
            "MemoryIngested",
            "memory",
            str(memory.id),
            chunks_count=len(chunks),
            model=model,
            namespace=namespace,
        )
    ]


def search_memories(
    query_text: str,
    *,
    embedder: EmbeddingPort,
    vectorstore: VectorStorePort,
    namespace: str = "default",
    model: str = "text-embedding-3-small",
    top_k: int = 10,
    filter_metadata: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Domain service: embed query → search similar memories.

    Returns:
        List of search results với metadata.
    """
    # Embed query
    try:
        query_vectors = embedder.embed([query_text], model=model)
        query_vector = query_vectors[0]
    except Exception:
        return []

    # Search vector store
    try:
        results = vectorstore.query(
            namespace=namespace,
            vector=query_vector,
            top_k=top_k,
            filter_metadata=filter_metadata,
        )
        return results
    except Exception:
        return []
