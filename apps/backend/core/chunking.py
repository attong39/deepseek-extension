"""
Enhanced Chunking System for zeta-monorepo backend.

This module provides functions for semantic and simple text chunking with overlap,
ensuring better context preservation and error handling.

Auto-fixed by comprehensive_init_fixer.py
"""

from __future__ import annotations

import re
from typing import List, Optional

# Imports from project structure (adjust paths if needed)
from zeta_monorepo.apps.backend.core.observability.logging import get_logger
import Exception
import ValueError
import chunk_size
import e
import int
import len
import next_sentence
import overlap
import p
import para
import s
import sentence
import str
import target
import text

# Global logger instance
logger = get_logger(__name__)


def _validate_chunk_params(
    target: int, overlap: int, chunk_size: Optional[int] = None
) -> None:
    """
    Validate chunking parameters.

    Args:
        target (int): Target chunk size.
        overlap (int): Overlap size.
        chunk_size (Optional[int]): Chunk size for simple chunking.

    Raises:
        ValueError: If parameters are invalid.
    """
    if target <= 0:
        raise ValueError("target must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= target:
        raise ValueError("overlap must be less than target")
    if chunk_size is not None and chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")


def _split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.

    Args:
        text (str): Input text.

    Returns:
        List[str]: List of sentences.
    """
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text.strip()) if p.strip()]
    sentences: List[str] = []
    for para in paragraphs:
        para_sentences = re.split(r"(?<=[.!?。！？])\s+", para)
        sentences.extend([s.strip() for s in para_sentences if s.strip()])
    return sentences


def _create_chunk_with_overlap(
    sentences: List[str], target: int, overlap: int
) -> List[str]:
    """
    Create chunks from sentences with overlap.

    Args:
        sentences (List[str]): List of sentences.
        target (int): Target chunk size.
        overlap (int): Overlap size.

    Returns:
        List[str]: List of chunks.
    """
    if not sentences:
        return []
    chunks: List[str] = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > target and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = _get_overlap_tail(current_chunk, overlap, sentence)
        else:
            current_chunk = (current_chunk + " " + sentence).strip()
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def _get_overlap_tail(current_chunk: str, overlap: int, next_sentence: str) -> str:
    """
    Get the overlapping tail for the next chunk.

    Args:
        current_chunk (str): Current chunk text.
        overlap (int): Overlap size.
        next_sentence (str): Next sentence.

    Returns:
        str: Overlapping tail.
    """
    if overlap > 0:
        tail = (
            current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
        )
        return (tail + " " + next_sentence).strip()
    return next_sentence


async def semantic_chunks(text: str, target: int = 600, overlap: int = 80) -> List[str]:
    """
    Split text into semantic chunks with overlap.

    Strategy:
    1. Split by paragraphs (double newlines).
    2. Split further by sentences within paragraphs.
    3. Group sentences up to target size.
    4. Add overlap between chunks for context preservation.

    Args:
        text (str): Input text to chunk.
        target (int): Target chunk size in characters.
        overlap (int): Overlap size in characters.

    Returns:
        List[str]: List of text chunks.

    Raises:
        ValueError: If target or overlap are invalid.
    """
    _validate_chunk_params(target, overlap)
    if not text.strip():
        logger.debug("Empty text provided, returning empty list")
        return []
    try:
        sentences = _split_into_sentences(text)
        if not sentences:
            logger.debug("No sentences found, returning original text")
            return [text]
        chunks = _create_chunk_with_overlap(sentences, target, overlap)
        result = chunks or [text]
        logger.info(f"Split {len(text)} characters into {len(result)} semantic chunks")
        return result
    except Exception as e:
        logger.error(f"Error during semantic chunking: {e}")
        raise


async def simple_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into simple chunks based on characters with overlap.

    Fallback method when semantic chunking is not feasible.

    Args:
        text (str): Input text to chunk.
        chunk_size (int): Chunk size in characters.
        overlap (int): Overlap size in characters.

    Returns:
        List[str]: List of text chunks.

    Raises:
        ValueError: If chunk_size or overlap are invalid.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be less than chunk_size")
    if len(text) <= chunk_size:
        return [text]
    try:
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
            if start >= len(text):
                break
        logger.info(f"Split {len(text)} characters into {len(chunks)} simple chunks")
        return chunks
    except Exception as e:
        logger.error(f"Error during simple chunking: {e}")
        raise


__all__ = [
    "semantic_chunks",
    "simple_chunks",
]
