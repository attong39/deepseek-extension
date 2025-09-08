"""
Text Chunking Service Implementation với enhanced strategies.

Provides intelligent text chunking for RAG applications theo ROADMAP specifications.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Literal
import Exception
import any
import default_chunk_size
import default_overlap
import default_strategy
import dict
import enumerate
import i
import int
import keyword
import len
import list
import max
import min
import opts
import original_text
import range
import self
import separator
import str
import sub_chunk
import text

logger = logging.getLogger(__name__)

ChunkStrategy = Literal["semantic", "sentence", "markdown", "simple", "code", "hybrid"]


@dataclass(frozen=True)
class TextChunk:
    """Immutable text chunk với position information."""

    text: str
    start: int
    end: int
    metadata: dict[str, Any] | None = None


class ChunkingService:
    """
    Enhanced chunking service theo ROADMAP specification.

    Features:
    - Multiple chunking strategies (semantic, sentence, markdown, code, hybrid)
    - Smart overlap với sentence awareness
    - Metadata preservation
    - Performance optimized for RAG
    """

    def __init__(
        self,
        default_chunk_size: int = 800,
        default_overlap: int = 100,
        default_strategy: ChunkStrategy = "sentence",
    ) -> None:
        """Initialize chunking service với defaults."""
        self.default_chunk_size = default_chunk_size
        self.default_overlap = default_overlap
        self.default_strategy = default_strategy
        logger.info(
            "Initialized ChunkingService: size=%d, overlap=%d, strategy=%s",
            default_chunk_size,
            default_overlap,
            default_strategy,
        )

    def split(
        self,
        text: str,
        *,
        strategy: ChunkStrategy | None = None,
        overlap: int | None = None,
        size: int | None = None,
    ) -> list[TextChunk]:
        """
        Split text theo strategy với enhanced features.

        Args:
            text: Text to chunk
            strategy: Chunking strategy to use
            overlap: Overlap size in characters
            size: Target chunk size

        Returns:
            List of TextChunk objects với position info
        """
        if not text.strip():
            return []

        strategy = strategy or self.default_strategy
        overlap = overlap or self.default_overlap
        size = size or self.default_chunk_size

        try:
            return self._split_by_strategy(text, strategy, size, overlap)
        except Exception:
            logger.exception("Chunking failed, falling back to simple strategy")
            return self._split_simple(text, size, overlap)

    def estimate_chunks(self, text: str, strategy: ChunkStrategy | None = None) -> int:
        """Estimate number of chunks without actual splitting."""
        strategy = strategy or self.default_strategy
        size = self.default_chunk_size

        if strategy == "simple":
            return max(1, len(text) // size)
        elif strategy == "sentence":
            # Rough estimate based on sentence count
            sentences = len(re.findall(r"[.!?]+", text))
            avg_sentence_length = len(text) // max(1, sentences)
            sentences_per_chunk = max(1, size // avg_sentence_length)
            return max(1, sentences // sentences_per_chunk)
        else:
            # Conservative estimate
            return max(1, len(text) // (size // 2))

    def _split_by_strategy(
        self, text: str, strategy: ChunkStrategy, size: int, overlap: int
    ) -> list[TextChunk]:
        """Route to appropriate splitting method."""
        if strategy == "markdown":
            return self._split_markdown(text, size, overlap)
        elif strategy == "semantic":
            return self._split_semantic(text, size, overlap)
        elif strategy == "sentence":
            return self._split_sentence(text, size, overlap)
        elif strategy == "code":
            return self._split_code(text, size, overlap)
        elif strategy == "hybrid":
            return self._split_hybrid(text, size, overlap)
        else:  # simple
            return self._split_simple(text, size, overlap)

    def _split_simple(self, text: str, size: int, overlap: int) -> list[TextChunk]:
        """Simple fixed-size chunking."""
        chunks = []
        pos = 0
        chunk_id = 0

        while pos < len(text):
            end = min(pos + size, len(text))
            chunk_text = text[pos:end].strip()

            if chunk_text:
                chunks.append(
                    TextChunk(
                        text=chunk_text,
                        start=pos,
                        end=end,
                        metadata={"chunk_id": chunk_id, "strategy": "simple"},
                    )
                )
                chunk_id += 1

            pos += size - overlap

        return chunks

    def _split_sentence(self, text: str, size: int, overlap: int) -> list[TextChunk]:
        """Sentence-aware chunking."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []
        current_chunk = ""
        current_start = 0
        chunk_id = 0

        for sentence in sentences:
            if len(current_chunk) + len(sentence) > size and current_chunk:
                # Save current chunk
                chunks.append(
                    TextChunk(
                        text=current_chunk.strip(),
                        start=current_start,
                        end=current_start + len(current_chunk),
                        metadata={"chunk_id": chunk_id, "strategy": "sentence"},
                    )
                )
                chunk_id += 1

                # Start new chunk with overlap
                if overlap > 0:
                    current_chunk = current_chunk[-overlap:] + " " + sentence
                else:
                    current_chunk = sentence
                    current_start = text.find(sentence, current_start)
            else:
                if not current_chunk:
                    current_start = text.find(sentence)
                current_chunk += " " + sentence if current_chunk else sentence

        # Add final chunk
        if current_chunk.strip():
            chunks.append(
                TextChunk(
                    text=current_chunk.strip(),
                    start=current_start,
                    end=current_start + len(current_chunk),
                    metadata={"chunk_id": chunk_id, "strategy": "sentence"},
                )
            )

        return chunks

    def _split_markdown(self, text: str, size: int, overlap: int) -> list[TextChunk]:
        """Markdown-aware chunking preserving headers."""
        sections = re.split(r"(?m)^(#{1,6}\s+.*?)$", text)
        chunks = []
        chunk_id = 0

        for _i, section in enumerate(sections):
            if not section.strip():
                continue

            if re.match(r"^#{1,6}\s+", section):
                # Header - start new chunk
                header_level = len(section) - len(section.lstrip("#"))
                metadata = {
                    "chunk_id": chunk_id,
                    "strategy": "markdown",
                    "header_level": header_level,
                }
            else:
                metadata = {"chunk_id": chunk_id, "strategy": "markdown"}

            if len(section) <= size:
                chunks.append(
                    TextChunk(
                        text=section.strip(),
                        start=text.find(section),
                        end=text.find(section) + len(section),
                        metadata=metadata,
                    )
                )
                chunk_id += 1
            else:
                # Split large sections
                sub_chunks = self._split_simple(section, size, overlap)
                for sub_chunk in sub_chunks:
                    chunks.append(
                        TextChunk(
                            text=sub_chunk.text,
                            start=sub_chunk.start,
                            end=sub_chunk.end,
                            metadata={**metadata, "sub_chunk": True},
                        )
                    )
                    chunk_id += 1

        return chunks

    def _split_semantic(self, text: str, size: int, overlap: int) -> list[TextChunk]:
        """Semantic chunking using paragraph and sentence boundaries."""
        # Split by double newlines (paragraphs) then by strong punctuation
        sections = re.split(r"\n{2,}|[。！？.!?]{2,}\s+", text)
        return self._process_sections(sections, text, size, overlap, "semantic")

    def _split_code(self, text: str, size: int, overlap: int) -> list[TextChunk]:
        """Code-aware chunking preserving function/class boundaries."""
        # Simple heuristic for code blocks
        if "```" in text:
            sections = re.split(r"```.*?```", text, flags=re.DOTALL)
        else:
            # Split by function/class definitions
            sections = re.split(r"(?m)^(def |class |function |var )", text)

        return self._process_sections(sections, text, size, overlap, "code")

    def _split_hybrid(self, text: str, size: int, overlap: int) -> list[TextChunk]:
        """Hybrid approach combining multiple strategies."""
        # Try markdown first, fall back to semantic
        if re.search(r"^#{1,6}\s+", text, re.MULTILINE):
            return self._split_markdown(text, size, overlap)
        elif "```" in text or any(
            keyword in text.lower() for keyword in ["def ", "class ", "function"]
        ):
            return self._split_code(text, size, overlap)
        else:
            return self._split_semantic(text, size, overlap)

    def _process_sections(
        self,
        sections: list[str],
        original_text: str,
        size: int,
        overlap: int,
        strategy: str,
    ) -> list[TextChunk]:
        """Process sections into chunks với position tracking."""
        chunks = []
        chunk_id = 0
        pos = 0

        for section in sections:
            section = section.strip()
            if not section:
                continue

            section_start = original_text.find(section, pos)
            if section_start == -1:
                section_start = pos

            if len(section) <= size:
                chunks.append(
                    TextChunk(
                        text=section,
                        start=section_start,
                        end=section_start + len(section),
                        metadata={"chunk_id": chunk_id, "strategy": strategy},
                    )
                )
                chunk_id += 1
            else:
                # Split large sections
                sub_chunks = self._split_simple(section, size, overlap)
                for sub_chunk in sub_chunks:
                    chunks.append(
                        TextChunk(
                            text=sub_chunk.text,
                            start=section_start + sub_chunk.start,
                            end=section_start + sub_chunk.end,
                            metadata={"chunk_id": chunk_id, "strategy": strategy},
                        )
                    )
                    chunk_id += 1

            pos = section_start + len(section)

        return chunks

    def chunk(self, text: str, **opts: Any) -> list[str]:
        """
        Split text into chunks using configured strategy.

        Args:
            text: Input text to chunk
            **opts: Override options (chunk_size, overlap_size, strategy)

        Returns:
            List of text chunks
        """
        if not text.strip():
            return []

        # Extract options with defaults
        chunk_size = opts.get("chunk_size", self.chunk_size)
        overlap_size = opts.get("overlap_size", self.overlap_size)
        strategy = opts.get("strategy", self.strategy)

        # Choose chunking strategy
        if strategy == "sentence":
            return self._chunk_by_sentences(text, chunk_size, overlap_size)
        elif strategy == "paragraph":
            return self._chunk_by_paragraphs(text, chunk_size, overlap_size)
        else:  # recursive (default)
            return self._chunk_recursive(text, chunk_size, overlap_size)

    def _chunk_recursive(
        self, text: str, chunk_size: int, overlap_size: int
    ) -> list[str]:
        """
        Recursive chunking with hierarchy of separators.

        Tries to split on:
        1. Double newlines (paragraphs)
        2. Single newlines
        3. Sentences (periods)
        4. Clauses (commas)
        5. Words (spaces)
        6. Characters (last resort)
        """
        separators = [
            "\n\n",  # Paragraphs
            "\n",  # Lines
            ". ",  # Sentences
            ", ",  # Clauses
            " ",  # Words
            "",  # Characters
        ]

        return self._split_text_recursive(text, chunk_size, overlap_size, separators)

    def _split_text_recursive(
        self, text: str, chunk_size: int, overlap_size: int, separators: list[str]
    ) -> list[str]:
        """Recursive text splitting implementation."""
        if len(text) <= chunk_size:
            return [text]

        # Try each separator in order
        for separator in separators:
            if separator in text:
                chunks = []
                splits = text.split(separator)
                current_chunk = ""

                for split in splits:
                    # Add separator back (except for empty separator)
                    part = split + (separator if separator and split else "")

                    # Check if adding this part would exceed chunk size
                    if len(current_chunk) + len(part) <= chunk_size:
                        current_chunk += part
                    else:
                        # Save current chunk if not empty
                        if current_chunk.strip():
                            chunks.append(current_chunk.strip())

                        # Start new chunk with overlap
                        if overlap_size > 0 and chunks:
                            overlap_text = current_chunk[-overlap_size:]
                            current_chunk = overlap_text + part
                        else:
                            current_chunk = part

                # Add final chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                return chunks

        # If no separator worked, split by character
        chunks = []
        for i in range(0, len(text), chunk_size - overlap_size):
            end_idx = min(i + chunk_size, len(text))
            chunk = text[i:end_idx]
            if chunk.strip():
                chunks.append(chunk.strip())

        return chunks

    def _chunk_by_sentences(
        self, text: str, chunk_size: int, overlap_size: int
    ) -> list[str]:
        """
        Chunk text by sentences, respecting chunk size limits.
        """
        # Simple sentence splitting by periods, exclamation marks, question marks
        sentence_pattern = r"[.!?]+\s+"
        sentences = re.split(sentence_pattern, text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if adding sentence would exceed chunk size
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                # Save current chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Start new chunk with overlap
                if overlap_size > 0 and chunks:
                    overlap_text = current_chunk[-overlap_size:]
                    current_chunk = overlap_text + " " + sentence
                else:
                    current_chunk = sentence

        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _chunk_by_paragraphs(
        self, text: str, chunk_size: int, overlap_size: int
    ) -> list[str]:
        """
        Chunk text by paragraphs, respecting chunk size limits.
        """
        paragraphs = text.split("\n\n")

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # Check if adding paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) + 2 <= chunk_size:  # +2 for \n\n
                current_chunk += ("\n\n" if current_chunk else "") + paragraph
            else:
                # Save current chunk
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Handle large paragraphs by further chunking
                if len(paragraph) > chunk_size:
                    # Recursively chunk large paragraph
                    para_chunks = self._chunk_recursive(
                        paragraph, chunk_size, overlap_size
                    )

                    # Add overlap with previous chunk
                    if overlap_size > 0 and chunks and para_chunks:
                        overlap_text = current_chunk[-overlap_size:]
                        para_chunks[0] = overlap_text + " " + para_chunks[0]

                    chunks.extend(para_chunks)
                    current_chunk = ""
                else:
                    # Start new chunk with overlap
                    if overlap_size > 0 and chunks:
                        overlap_text = current_chunk[-overlap_size:]
                        current_chunk = overlap_text + "\n\n" + paragraph
                    else:
                        current_chunk = paragraph

        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def get_chunk_metadata(self, chunks: list[str]) -> list[dict[str, Any]]:
        """
        Generate metadata for chunks.

        Args:
            chunks: List of text chunks

        Returns:
            List of metadata dicts for each chunk
        """
        metadata = []

        for i, chunk in enumerate(chunks):
            meta = {
                "chunk_index": i,
                "chunk_size": len(chunk),
                "word_count": len(chunk.split()),
                "char_count": len(chunk),
                "strategy": self.strategy,
            }
            metadata.append(meta)

        return metadata
