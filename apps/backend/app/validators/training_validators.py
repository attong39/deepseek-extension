"""Training data validators.





This module provides validation functions for training-related data,


ensuring data quality and compliance with business rules.


"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING
import ValueError
import any
import bool
import char
import chunk
import chunk_index
import content
import data_chunks
import dict
import enumerate
import i
import indicator
import input_type
import int
import isinstance
import key
import len
import list
import metadata
import pattern
import str
import value

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.training_types import TrainingInputType


logger = logging.getLogger(__name__)


# Configuration constants


MAX_CHUNK_SIZE = 10000  # Maximum characters per chunk


MIN_CHUNK_SIZE = 10  # Minimum characters per chunk


MAX_CHUNKS_PER_JOB = 1000  # Maximum chunks per training job


MIN_CHUNKS_PER_JOB = 1  # Minimum chunks per training job


def validate_training_data(
    data_chunks: list[str], input_type: TrainingInputType
) -> None:
    """Validate training data chunks.





    Args:


        data_chunks: List of data chunks to validate


        input_type: Type of training input





    Raises:


        ValueError: If validation fails


    """

    if not data_chunks:
        raise ValueError("Data chunks cannot be empty")

    if len(data_chunks) < MIN_CHUNKS_PER_JOB:
        raise ValueError(f"Must provide at least {MIN_CHUNKS_PER_JOB} data chunk(s)")

    if len(data_chunks) > MAX_CHUNKS_PER_JOB:
        raise ValueError(f"Cannot exceed {MAX_CHUNKS_PER_JOB} data chunks per job")

    # Validate each chunk

    for i, chunk in enumerate(data_chunks):
        validate_data_chunk(chunk, i)

    # Type-specific validation

    if input_type.value == "document":
        _validate_document_chunks(data_chunks)

    elif input_type.value == "dataset":
        _validate_dataset_chunks(data_chunks)

    elif input_type.value == "conversation":
        _validate_conversation_chunks(data_chunks)

    logger.debug(f"Validated {len(data_chunks)} chunks for {input_type.value} training")


def validate_data_chunk(chunk: str, chunk_index: int) -> None:
    """Validate a single data chunk.





    Args:


        chunk: Data chunk content


        chunk_index: Index of the chunk for error reporting





    Raises:


        ValueError: If chunk validation fails


    """

    if not isinstance(chunk, str):
        raise ValueError(f"Chunk {chunk_index}: must be a string")

    if not chunk.strip():
        raise ValueError(f"Chunk {chunk_index}: cannot be empty or whitespace only")

    if len(chunk) < MIN_CHUNK_SIZE:
        raise ValueError(
            f"Chunk {chunk_index}: must be at least {MIN_CHUNK_SIZE} characters"
        )

    if len(chunk) > MAX_CHUNK_SIZE:
        raise ValueError(
            f"Chunk {chunk_index}: cannot exceed {MAX_CHUNK_SIZE} characters"
        )

    # Check for potentially harmful content

    if _contains_harmful_content(chunk):
        raise ValueError(f"Chunk {chunk_index}: contains potentially harmful content")


def _validate_document_chunks(data_chunks: list[str]) -> None:
    """Validate document-specific chunks.





    Args:


        data_chunks: List of document chunks





    Raises:


        ValueError: If document validation fails


    """

    # Check for reasonable text structure

    for i, chunk in enumerate(data_chunks):
        # Documents should have some structure (sentences, paragraphs)

        if not any(char in chunk for char in ".!?"):
            logger.warning(f"Document chunk {i} has no sentence endings")

        # Check for minimum word count

        words = chunk.split()

        if len(words) < 5:
            raise ValueError(f"Document chunk {i}: must contain at least 5 words")


def _validate_dataset_chunks(data_chunks: list[str]) -> None:
    """Validate dataset-specific chunks.





    Args:


        data_chunks: List of dataset chunks





    Raises:


        ValueError: If dataset validation fails


    """

    # Datasets can be more flexible in structure

    for i, chunk in enumerate(data_chunks):
        # Check for basic data structure

        if chunk.count("\n") == 0 and chunk.count(",") == 0 and chunk.count("\t") == 0:
            logger.warning(f"Dataset chunk {i} appears to lack structured data format")


def _validate_conversation_chunks(data_chunks: list[str]) -> None:
    """Validate conversation-specific chunks.





    Args:


        data_chunks: List of conversation chunks





    Raises:


        ValueError: If conversation validation fails


    """

    # Conversations should have dialogue indicators

    dialogue_indicators = [":", ">", "-", "User:", "Assistant:", "Bot:", "Human:"]

    for i, chunk in enumerate(data_chunks):
        # Check for dialogue structure

        has_dialogue = any(indicator in chunk for indicator in dialogue_indicators)

        if not has_dialogue:
            logger.warning(f"Conversation chunk {i} may lack dialogue structure")

        # Check for reasonable conversation length

        lines = chunk.split("\n")

        if len(lines) < 2:
            raise ValueError(f"Conversation chunk {i}: must contain at least 2 lines")


def _contains_harmful_content(content: str) -> bool:
    """Check if content contains potentially harmful material.





    Args:


        content: Content to check





    Returns:


        True if harmful content detected


    """

    # Basic harmful content detection

    harmful_patterns = [
        # Explicit content markers
        "NSFW",
        "explicit",
        "adult content",
        # Potential code injection
        "<script>",
        "javascript:",
        "ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(",
        # Potential SQL injection
        "DROP TABLE",
        "DELETE FROM",
        "UNION SELECT",
        # Personal information patterns
        "password:",
        "secret:",
        "api_key:",
    ]

    content_lower = content.lower()

    return any(pattern.lower() in content_lower for pattern in harmful_patterns)


def validate_chunk_metadata(metadata: dict[str, str] | None) -> None:
    """Validate chunk metadata.





    Args:


        metadata: Metadata dictionary to validate





    Raises:


        ValueError: If metadata validation fails


    """

    if metadata is None:
        return

    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary")

    # Check metadata size limits

    if len(metadata) > 50:
        raise ValueError("Metadata cannot have more than 50 keys")

    for key, value in metadata.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Metadata keys and values must be strings")

        if len(key) > 100:
            raise ValueError(f"Metadata key '{key}' exceeds 100 characters")

        if len(value) > 1000:
            raise ValueError(f"Metadata value for '{key}' exceeds 1000 characters")
