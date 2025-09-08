"""Text chunking algorithms for RAG pipeline.





Provides various text splitting strategies without vendor dependencies.


All implementations are pure Python algorithms.


"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Any

from apps.backend.core.services.ai.rag.types import Chunk, ChunkingStrategy
import ValueError
import chunk_id
import chunk_size
import content
import dict
import end_index
import enumerate
import i
import int
import kwargs
import len
import list
import max
import max_chars
import max_paragraphs
import max_sentences
import metadata
import min
import overlap
import p
import paragraph
import part
import range
import s
import self
import sentence
import separator_index
import source_id
import start_index
import str
import strategy
import text


class TextChunker(ABC):
    """Abstract base class for text chunking algorithms."""

    @abstractmethod
    def chunk_text(
        self, text: str, source_id: str, metadata: dict[str, Any] | None = None
    ) -> list[Chunk]:
        """Split text into chunks.





        Args:


            text: Text to split


            source_id: Identifier for the source document


            metadata: Additional metadata to attach to chunks





        Returns:


            List of text chunks with positions and metadata


        """

    def _create_chunk(
        self,
        content: str,
        source_id: str,
        start_index: int,
        end_index: int,
        metadata: dict[str, Any] | None = None,
        chunk_id: str | None = None,
    ) -> Chunk:
        """Create a chunk with proper metadata."""

        chunk_metadata = {
            "chunk_length": len(content),
            "word_count": len(content.split()),
            **(metadata or {}),
        }

        return Chunk(
            id=chunk_id or f"{source_id}_chunk_{start_index}_{end_index}",
            content=content.strip(),
            source_id=source_id,
            start_index=start_index,
            end_index=end_index,
            metadata=chunk_metadata,
        )


class FixedSizeChunker(TextChunker):
    """Splits text into fixed-size chunks with optional overlap."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        """Initialize fixed-size chunker.





        Args:


            chunk_size: Maximum characters per chunk


            overlap: Number of characters to overlap between chunks


        """

        self.chunk_size = chunk_size

        self.overlap = overlap

    def chunk_text(
        self, text: str, source_id: str, metadata: dict[str, Any] | None = None
    ) -> list[Chunk]:
        """Split text into fixed-size chunks."""

        chunks = []

        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            # Try to break at word boundary if not at end of text

            if end < len(text):
                # Look for last whitespace within reasonable distance

                break_point = text.rfind(" ", start, end)

                if (
                    break_point > start + self.chunk_size * 0.8
                ):  # At least 80% of chunk size
                    end = break_point

            chunk_content = text[start:end]

            if chunk_content.strip():
                chunk = self._create_chunk(
                    content=chunk_content,
                    source_id=source_id,
                    start_index=start,
                    end_index=end,
                    metadata={
                        **(metadata or {}),
                        "chunking_strategy": ChunkingStrategy.FIXED_SIZE.value,
                        "chunk_size": self.chunk_size,
                        "overlap": self.overlap,
                    },
                )

                chunks.append(chunk)

            # Move start position with overlap

            start = max(end - self.overlap, start + 1)

        return chunks


class SentenceChunker(TextChunker):
    """Splits text at sentence boundaries."""

    def __init__(self, max_sentences: int = 5, max_chars: int = 2000):
        """Initialize sentence chunker.





        Args:


            max_sentences: Maximum sentences per chunk


            max_chars: Maximum characters per chunk (override)


        """

        self.max_sentences = max_sentences

        self.max_chars = max_chars

        # Improved sentence boundary detection

        self.sentence_pattern = re.compile(
            r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?]["\']\s)\s*(?=[A-Z])'
        )

    def chunk_text(
        self, text: str, source_id: str, metadata: dict[str, Any] | None = None
    ) -> list[Chunk]:
        """Split text at sentence boundaries."""

        # Split into sentences

        sentences = self._split_sentences(text)

        chunks = []

        current_chunk_sentences = []

        current_start = 0

        for i, sentence in enumerate(sentences):
            current_chunk_sentences.append(sentence)

            # Check if we should create a chunk

            should_chunk = (
                len(current_chunk_sentences) >= self.max_sentences
                or len(" ".join(current_chunk_sentences)) >= self.max_chars
                or i == len(sentences) - 1  # Last sentence
            )

            if should_chunk and current_chunk_sentences:
                chunk_content = " ".join(current_chunk_sentences)

                chunk_end = current_start + len(chunk_content)

                chunk = self._create_chunk(
                    content=chunk_content,
                    source_id=source_id,
                    start_index=current_start,
                    end_index=chunk_end,
                    metadata={
                        **(metadata or {}),
                        "chunking_strategy": ChunkingStrategy.SENTENCE.value,
                        "sentence_count": len(current_chunk_sentences),
                        "max_sentences": self.max_sentences,
                    },
                )

                chunks.append(chunk)

                # Reset for next chunk

                current_start = chunk_end

                current_chunk_sentences = []

        return chunks

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences using regex."""

        sentences = self.sentence_pattern.split(text)

        return [s.strip() for s in sentences if s.strip()]


class ParagraphChunker(TextChunker):
    """Splits text at paragraph boundaries."""

    def __init__(self, max_paragraphs: int = 3, max_chars: int = 3000):
        """Initialize paragraph chunker.





        Args:


            max_paragraphs: Maximum paragraphs per chunk


            max_chars: Maximum characters per chunk


        """

        self.max_paragraphs = max_paragraphs

        self.max_chars = max_chars

    def chunk_text(
        self, text: str, source_id: str, metadata: dict[str, Any] | None = None
    ) -> list[Chunk]:
        """Split text at paragraph boundaries."""

        # Split by double newlines (paragraph breaks)

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        chunks = []

        current_chunk_paragraphs = []

        current_start = 0

        for i, paragraph in enumerate(paragraphs):
            current_chunk_paragraphs.append(paragraph)

            # Check if we should create a chunk

            should_chunk = (
                len(current_chunk_paragraphs) >= self.max_paragraphs
                or len("\n\n".join(current_chunk_paragraphs)) >= self.max_chars
                or i == len(paragraphs) - 1  # Last paragraph
            )

            if should_chunk and current_chunk_paragraphs:
                chunk_content = "\n\n".join(current_chunk_paragraphs)

                chunk_end = current_start + len(chunk_content)

                chunk = self._create_chunk(
                    content=chunk_content,
                    source_id=source_id,
                    start_index=current_start,
                    end_index=chunk_end,
                    metadata={
                        **(metadata or {}),
                        "chunking_strategy": ChunkingStrategy.PARAGRAPH.value,
                        "paragraph_count": len(current_chunk_paragraphs),
                        "max_paragraphs": self.max_paragraphs,
                    },
                )

                chunks.append(chunk)

                # Reset for next chunk

                current_start = chunk_end

                current_chunk_paragraphs = []

        return chunks


class RecursiveChunker(TextChunker):
    """Recursively splits text using hierarchical delimiters."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 100):
        """Initialize recursive chunker.





        Args:


            chunk_size: Target chunk size in characters


            overlap: Overlap between chunks


        """

        self.chunk_size = chunk_size

        self.overlap = overlap

        # Hierarchical separators (from largest to smallest units)

        self.separators = [
            "\n\n",  # Paragraphs
            "\n",  # Lines
            ". ",  # Sentences
            "! ",  # Exclamations
            "? ",  # Questions
            "; ",  # Semicolons
            ", ",  # Commas
            " ",  # Words
            "",  # Characters (last resort)
        ]

    def chunk_text(
        self, text: str, source_id: str, metadata: dict[str, Any] | None = None
    ) -> list[Chunk]:
        """Split text recursively using hierarchical separators."""

        chunks = self._recursive_split(text, 0)

        # Convert to Chunk objects

        result_chunks = []

        current_pos = 0

        for chunk_text in chunks:
            if chunk_text.strip():
                start_pos = text.find(chunk_text, current_pos)

                if start_pos == -1:
                    start_pos = current_pos

                end_pos = start_pos + len(chunk_text)

                chunk = self._create_chunk(
                    content=chunk_text,
                    source_id=source_id,
                    start_index=start_pos,
                    end_index=end_pos,
                    metadata={
                        **(metadata or {}),
                        "chunking_strategy": ChunkingStrategy.RECURSIVE.value,
                        "chunk_size": self.chunk_size,
                        "overlap": self.overlap,
                    },
                )

                result_chunks.append(chunk)

                current_pos = end_pos

        return result_chunks

    def _recursive_split(self, text: str, separator_index: int) -> list[str]:
        """Recursively split text using separators."""

        if len(text) <= self.chunk_size or separator_index >= len(self.separators):
            return [text] if text.strip() else []

        separator = self.separators[separator_index]

        if not separator:  # Character-level splitting (last resort)
            return [
                text[i : i + self.chunk_size]
                for i in range(0, len(text), self.chunk_size - self.overlap)
            ]

        parts = text.split(separator)

        chunks = []

        current_chunk = ""

        for part in parts:
            potential_chunk = (
                current_chunk + (separator if current_chunk else "") + part
            )

            if len(potential_chunk) <= self.chunk_size:
                current_chunk = potential_chunk

            else:
                # Current chunk is ready

                if current_chunk:
                    chunks.append(current_chunk)

                # Handle oversized part recursively

                if len(part) > self.chunk_size:
                    chunks.extend(self._recursive_split(part, separator_index + 1))

                    current_chunk = ""

                else:
                    current_chunk = part

        # Add remaining chunk

        if current_chunk:
            chunks.append(current_chunk)

        return chunks


def create_chunker(strategy: ChunkingStrategy, **kwargs: Any) -> TextChunker:
    """Factory function to create chunkers based on strategy.





    Args:


        strategy: Chunking strategy to use


        **kwargs: Strategy-specific parameters





    Returns:


        Configured text chunker





    Raises:


        ValueError: If strategy is not supported


    """

    if strategy == ChunkingStrategy.FIXED_SIZE:
        return FixedSizeChunker(
            chunk_size=kwargs.get("chunk_size", 1000),
            overlap=kwargs.get("overlap", 100),
        )

    elif strategy == ChunkingStrategy.SENTENCE:
        return SentenceChunker(
            max_sentences=kwargs.get("max_sentences", 5),
            max_chars=kwargs.get("max_chars", 2000),
        )

    elif strategy == ChunkingStrategy.PARAGRAPH:
        return ParagraphChunker(
            max_paragraphs=kwargs.get("max_paragraphs", 3),
            max_chars=kwargs.get("max_chars", 3000),
        )

    elif strategy == ChunkingStrategy.RECURSIVE:
        return RecursiveChunker(
            chunk_size=kwargs.get("chunk_size", 1000),
            overlap=kwargs.get("overlap", 100),
        )

    else:
        raise ValueError(f"Unsupported chunking strategy: {strategy}")
