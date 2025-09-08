"""
Semantic Chunking Service cho RAG optimization.

Provides intelligent document splitting based on semantic boundaries.
"""

from __future__ import annotations

import asyncio
import logging
import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any
import ValueError
import bool
import char_end
import char_start
import chunk_size
import default_strategy
import dict
import documents
import float
import int
import keyword
import len
import list
import max
import max_chunk_size
import min
import min_chunk_size
import name
import overlap_size
import para_start
import prefer_paragraphs
import respect_sentences
import self
import str
import strategy
import strategy_kwargs
import sum
import text
import tuple
import zip

logger = logging.getLogger(__name__)


@dataclass
class ChunkMetadata:
    """Metadata for a document chunk."""

    chunk_index: int
    source_doc_id: str
    character_start: int
    character_end: int
    token_count: int | None = None
    semantic_section: str | None = None
    importance_score: float | None = None


@dataclass
class DocumentChunk:
    """A chunk of a document with metadata."""

    id: str
    text: str
    metadata: ChunkMetadata


class ChunkingStrategy(ABC):
    """Abstract base class for chunking strategies."""

    @abstractmethod
    async def chunk(self, text: str, doc_id: str, **kwargs: Any) -> list[DocumentChunk]:
        """Chunk a document into smaller pieces."""


class FixedSizeChunkingStrategy(ChunkingStrategy):
    """Fixed-size chunking strategy with overlap."""

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap_size: int = 200,
        respect_sentences: bool = True,
    ):
        """
        Initialize fixed-size chunking.

        Args:
            chunk_size: Target size of each chunk in characters
            overlap_size: Overlap between adjacent chunks
            respect_sentences: Whether to avoid splitting sentences
        """
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.respect_sentences = respect_sentences

    async def chunk(self, text: str, doc_id: str, **kwargs: Any) -> list[DocumentChunk]:
        """Chunk text into fixed-size pieces."""
        chunks = []
        start = 0
        chunk_index = 0

        while start < len(text):
            # Calculate end position
            end = min(start + self.chunk_size, len(text))

            # Respect sentence boundaries if enabled
            if self.respect_sentences and end < len(text):
                # Look for sentence boundary within last 200 chars
                search_start = max(end - 200, start)
                sentence_end = self._find_sentence_boundary(text, search_start, end)
                if sentence_end > start:
                    end = sentence_end

            # Extract chunk text
            chunk_text = text[start:end].strip()

            if chunk_text:
                # Create chunk metadata
                metadata = ChunkMetadata(
                    chunk_index=chunk_index,
                    source_doc_id=doc_id,
                    character_start=start,
                    character_end=end,
                    token_count=self._estimate_tokens(chunk_text),
                )

                # Create chunk
                chunk = DocumentChunk(
                    id=f"{doc_id}_chunk_{chunk_index}",
                    text=chunk_text,
                    metadata=metadata,
                )

                chunks.append(chunk)
                chunk_index += 1

            # Move to next chunk with overlap
            start = max(end - self.overlap_size, start + 1)

        logger.debug(f"Fixed-size chunking produced {len(chunks)} chunks")
        return chunks

    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """Find the last sentence boundary before end position."""
        # Look for sentence endings
        search_text = text[start:end]
        sentence_endings = list(re.finditer(r"[.!?]\s+", search_text))

        if sentence_endings:
            # Return position after the last sentence ending
            last_match = sentence_endings[-1]
            return start + last_match.end()

        return end

    def _estimate_tokens(self, text: str) -> int:
        """Rough token count estimation."""
        # Simple estimation: 1 token ≈ 4 characters
        return len(text) // 4


class SemanticChunkingStrategy(ChunkingStrategy):
    """
    Semantic chunking strategy based on content structure.

    Attempts to split documents at logical boundaries like paragraphs,
    sections, and topic transitions.
    """

    def __init__(
        self,
        max_chunk_size: int = 1500,
        min_chunk_size: int = 100,
        prefer_paragraphs: bool = True,
    ):
        """
        Initialize semantic chunking.

        Args:
            max_chunk_size: Maximum chunk size in characters
            min_chunk_size: Minimum chunk size in characters
            prefer_paragraphs: Whether to prefer paragraph boundaries
        """
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.prefer_paragraphs = prefer_paragraphs

    async def chunk(self, text: str, doc_id: str, **kwargs: Any) -> list[DocumentChunk]:
        """Chunk text based on semantic structure."""
        # Split into paragraphs first
        paragraphs = self._split_into_paragraphs(text)

        chunks = []
        current_chunk = ""
        current_start = 0
        chunk_index = 0

        for para_start, para_text in paragraphs:
            # Check if adding this paragraph would exceed max size
            potential_chunk = (current_chunk + "\n\n" + para_text).strip()

            if (
                len(potential_chunk) > self.max_chunk_size
                and len(current_chunk) >= self.min_chunk_size
            ):
                # Finalize current chunk
                if current_chunk.strip():
                    chunk = await self._create_chunk(
                        current_chunk.strip(),
                        doc_id,
                        chunk_index,
                        current_start,
                        current_start + len(current_chunk),
                    )
                    chunks.append(chunk)
                    chunk_index += 1

                # Start new chunk with current paragraph
                current_chunk = para_text
                current_start = para_start
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + para_text
                else:
                    current_chunk = para_text
                    current_start = para_start

        # Add final chunk
        if current_chunk.strip():
            chunk = await self._create_chunk(
                current_chunk.strip(),
                doc_id,
                chunk_index,
                current_start,
                current_start + len(current_chunk),
            )
            chunks.append(chunk)

        logger.debug(f"Semantic chunking produced {len(chunks)} chunks")
        return chunks

    def _split_into_paragraphs(self, text: str) -> list[tuple[int, str]]:
        """Split text into paragraphs with their start positions."""
        paragraphs = []
        current_pos = 0

        # Split on double newlines (paragraph separators)
        para_texts = re.split(r"\n\s*\n", text)

        for para_text in para_texts:
            para_text = para_text.strip()
            if para_text:
                # Find actual position in original text
                start_pos = text.find(para_text, current_pos)
                if start_pos >= 0:
                    paragraphs.append((start_pos, para_text))
                    current_pos = start_pos + len(para_text)

        return paragraphs

    async def _create_chunk(
        self,
        text: str,
        doc_id: str,
        chunk_index: int,
        char_start: int,
        char_end: int,
    ) -> DocumentChunk:
        """Create a document chunk with metadata."""
        # Detect semantic section if possible
        semantic_section = self._detect_section_type(text)

        metadata = ChunkMetadata(
            chunk_index=chunk_index,
            source_doc_id=doc_id,
            character_start=char_start,
            character_end=char_end,
            token_count=len(text) // 4,  # Rough estimation
            semantic_section=semantic_section,
            importance_score=await self._calculate_importance(text),
        )

        return DocumentChunk(
            id=f"{doc_id}_semantic_{chunk_index}",
            text=text,
            metadata=metadata,
        )

    def _detect_section_type(self, text: str) -> str | None:
        """Detect the type of section based on content patterns."""
        text_lower = text.lower()

        # Simple heuristics for section detection
        if re.match(r"^#+\s+", text) or text.isupper():
            return "heading"
        elif "```" in text or re.search(r"\b(def|class|function)\b", text_lower):
            return "code"
        elif re.search(r"\b(table|figure|chart)\b", text_lower):
            return "table_figure"
        elif len(text.split()) < 20:
            return "short_text"
        else:
            return "paragraph"

    async def _calculate_importance(self, text: str) -> float:
        """
        Calculate importance score for a chunk.

        Simple heuristics - in production, could use ML models.
        """

        def _compute_score():
            score = 0.5  # Base score

            # Boost for headings
            if re.match(r"^#+\s+", text) or text.strip().isupper():
                score += 0.3

            # Boost for questions
            if "?" in text:
                score += 0.1

            # Boost for lists
            if re.search(r"^\s*[-*+•]\s+", text, re.MULTILINE):
                score += 0.1

            # Boost for keywords (simple)
            keywords = ["important", "key", "note", "warning", "summary"]
            for keyword in keywords:
                if keyword in text.lower():
                    score += 0.1

            # Penalty for very short text
            if len(text.split()) < 10:
                score -= 0.2

            return max(0.0, min(1.0, score))

        return await asyncio.to_thread(_compute_score)


class EnhancedChunkingService:
    """
    Enhanced chunking service with multiple strategies.

    Features:
    - Multiple chunking strategies (fixed-size, semantic)
    - Async processing for large documents
    - Metadata-rich chunks for better retrieval
    - Importance scoring for chunk ranking
    """

    def __init__(self, default_strategy: str = "semantic"):
        """
        Initialize chunking service.

        Args:
            default_strategy: Default chunking strategy ("fixed" or "semantic")
        """
        self.strategies = {
            "fixed": FixedSizeChunkingStrategy(),
            "semantic": SemanticChunkingStrategy(),
        }
        self.default_strategy = default_strategy

    async def chunk_document(
        self,
        text: str,
        doc_id: str,
        strategy: str | None = None,
        **strategy_kwargs: Any,
    ) -> list[DocumentChunk]:
        """
        Chunk a document using specified strategy.

        Args:
            text: Document text to chunk
            doc_id: Unique document identifier
            strategy: Chunking strategy to use
            **strategy_kwargs: Additional arguments for strategy

        Returns:
            List of document chunks
        """
        strategy_name = strategy or self.default_strategy

        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown chunking strategy: {strategy_name}")

        chunker = self.strategies[strategy_name]
        chunks = await chunker.chunk(text, doc_id, **strategy_kwargs)

        logger.info(
            f"Chunked document {doc_id} into {len(chunks)} chunks using {strategy_name} strategy"
        )

        return chunks

    async def chunk_documents_batch(
        self,
        documents: Sequence[tuple[str, str]],  # (doc_id, text) pairs
        strategy: str | None = None,
        **strategy_kwargs: Any,
    ) -> dict[str, list[DocumentChunk]]:
        """
        Chunk multiple documents in parallel.

        Args:
            documents: List of (doc_id, text) pairs
            strategy: Chunking strategy to use
            **strategy_kwargs: Additional arguments for strategy

        Returns:
            Dict mapping doc_id to list of chunks
        """
        tasks = [
            self.chunk_document(text, doc_id, strategy, **strategy_kwargs)
            for doc_id, text in documents
        ]

        results = await asyncio.gather(*tasks)

        # Combine results
        doc_chunks = {}
        for (doc_id, _), chunks in zip(documents, results, strict=False):
            doc_chunks[doc_id] = chunks

        total_chunks = sum(len(chunks) for chunks in doc_chunks.values())
        logger.info(
            f"Batch chunking: {len(documents)} documents → {total_chunks} chunks"
        )

        return doc_chunks

    def add_strategy(self, name: str, strategy: ChunkingStrategy) -> None:
        """Add a custom chunking strategy."""
        self.strategies[name] = strategy
        logger.info(f"Added custom chunking strategy: {name}")

    def get_stats(self) -> dict[str, Any]:
        """Get service statistics."""
        return {
            "available_strategies": list(self.strategies.keys()),
            "default_strategy": self.default_strategy,
            "strategy_count": len(self.strategies),
        }


# Legacy compatibility
class ChunkingService(EnhancedChunkingService):
    """Legacy chunking service for backward compatibility."""

    def chunk(self, text: str, doc_id: str | None = None) -> list[str]:
        """
        Legacy sync chunking method.

        Returns:
            List of chunk texts (without metadata)
        """
        import asyncio

        doc_id = doc_id or "legacy_doc"
        chunks = asyncio.run(self.chunk_document(text, doc_id, strategy="fixed"))

        return [chunk.text for chunk in chunks]
