"""Memory specifications.





This module contains domain specifications for validating


and enforcing business rules related to memory management.


"""

from __future__ import annotations

import time
from typing import Any

from apps.backend.core.domain.specifications.agent_specifications import Specification
import allow_permanent
import bool
import candidate
import field
import float
import getattr
import hasattr
import int
import isinstance
import len
import list
import max_access_frequency
import max_length
import max_score
import max_size_bytes
import min_length
import min_score
import self
import set
import str
import valid_types


class MemoryContentSpecification(Specification):
    """Specification for validating memory content."""

    def __init__(self, min_length: int = 1, max_length: int = 10000) -> None:
        """Initialize memory content specification.





        Args:


            min_length: Minimum content length.


            max_length: Maximum content length.


        """

        self.min_length = min_length

        self.max_length = max_length

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory content is valid.





        Args:


            candidate: Memory object or content string to validate.





        Returns:


            True if content is valid.


        """

        if hasattr(candidate, "content"):
            content = candidate.content

        elif isinstance(candidate, str):
            content = candidate

        else:
            return False

        if not isinstance(content, str):
            return False

        # Check length

        if len(content.strip()) < self.min_length:
            return False

        if len(content) > self.max_length:
            return False

        # Check for empty or whitespace-only content

        if not content.strip():
            return False

        return True


class MemoryTypeSpecification(Specification):
    """Specification for validating memory types."""

    def __init__(self, valid_types: list[str] | None = None) -> None:
        """Initialize memory type specification.





        Args:


            valid_types: List of valid memory types.


        """

        self.valid_types = valid_types or [
            "episodic",
            "semantic",
            "procedural",
            "working",
            "long_term",
            "short_term",
            "factual",
            "contextual",
            "conversation",
            "task",
            "learning",
        ]

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory type is valid.





        Args:


            candidate: Memory object or type string to validate.





        Returns:


            True if type is valid.


        """

        if hasattr(candidate, "memory_type"):
            memory_type = candidate.memory_type

        elif isinstance(candidate, str):
            memory_type = candidate

        else:
            return False

        return memory_type in self.valid_types


class MemoryRelevanceSpecification(Specification):
    """Specification for validating memory relevance scores."""

    def __init__(self, min_score: float = 0.0, max_score: float = 1.0) -> None:
        """Initialize memory relevance specification.





        Args:


            min_score: Minimum relevance score.


            max_score: Maximum relevance score.


        """

        self.min_score = min_score

        self.max_score = max_score

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory relevance score is valid.





        Args:


            candidate: Memory object or relevance score to validate.





        Returns:


            True if relevance score is valid.


        """

        if hasattr(candidate, "relevance_score"):
            score = candidate.relevance_score

        elif isinstance(candidate, (int, float)):
            score = candidate

        else:
            return False

        if not isinstance(score, (int, float)):
            return False

        return self.min_score <= score <= self.max_score


class MemoryExpirationSpecification(Specification):
    """Specification for validating memory expiration."""

    def __init__(self, allow_permanent: bool = True) -> None:
        """Initialize memory expiration specification.





        Args:


            allow_permanent: Whether to allow permanent memories (no expiration).


        """

        self.allow_permanent = allow_permanent

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory expiration is valid.





        Args:


            candidate: Memory object to validate.





        Returns:


            True if expiration is valid.


        """

        if not hasattr(candidate, "expires_at"):
            return False

        expires_at = candidate.expires_at

        # Allow None for permanent memories if configured

        if expires_at is None:
            return self.allow_permanent

        # Check if expiration is in the future

        if not isinstance(expires_at, (int, float)):
            return False

        current_time = time.time()

        return expires_at > current_time


class MemorySizeSpecification(Specification):
    """Specification for validating memory size limits."""

    def __init__(self, max_size_bytes: int = 1024 * 1024) -> None:  # 1MB default
        """Initialize memory size specification.





        Args:


            max_size_bytes: Maximum memory size in bytes.


        """

        self.max_size_bytes = max_size_bytes

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory size is within limits.





        Args:


            candidate: Memory object to validate.





        Returns:


            True if size is valid.


        """

        if hasattr(candidate, "size_bytes"):
            size = candidate.size_bytes

        elif hasattr(candidate, "content"):
            # Estimate size from content

            content = candidate.content

            size = len(content.encode("utf-8")) if isinstance(content, str) else 0

        else:
            return False

        return isinstance(size, int) and 0 <= size <= self.max_size_bytes


class MemoryAccessPatternSpecification(Specification):
    """Specification for validating memory access patterns."""

    def __init__(self, max_access_frequency: int = 1000) -> None:
        """Initialize memory access pattern specification.





        Args:


            max_access_frequency: Maximum access frequency per hour.


        """

        self.max_access_frequency = max_access_frequency

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory access pattern is valid.





        Args:


            candidate: Memory object to validate.





        Returns:


            True if access pattern is valid.


        """

        if not hasattr(candidate, "access_count") or not hasattr(
            candidate, "created_at"
        ):
            return True  # Skip validation if access tracking not available

        access_count = candidate.access_count

        created_at = candidate.created_at

        if not isinstance(access_count, int) or not isinstance(
            created_at, (int, float)
        ):
            return False

        # Calculate access frequency per hour

        current_time = time.time()

        age_hours = (current_time - created_at) / 3600

        if age_hours < 1:
            age_hours = 1  # Minimum 1 hour for calculation

        access_frequency = access_count / age_hours

        return access_frequency <= self.max_access_frequency


class MemoryConsistencySpecification(Specification):
    """Specification for validating memory consistency."""

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory is internally consistent.





        Args:


            candidate: Memory object to validate.





        Returns:


            True if memory is consistent.


        """

        # Check required fields exist

        required_fields = ["id", "content", "memory_type", "created_at"]

        for field in required_fields:
            if not hasattr(candidate, field):
                return False

        # Check field types

        if not isinstance(candidate.id, str):
            return False

        if not isinstance(candidate.content, str):
            return False

        if not isinstance(candidate.memory_type, str):
            return False

        if not isinstance(candidate.created_at, (int, float)):
            return False

        # Check timestamps consistency

        current_time = time.time()

        if candidate.created_at > current_time:
            return False

        if hasattr(candidate, "updated_at"):
            if candidate.updated_at < candidate.created_at:
                return False

            if candidate.updated_at > current_time:
                return False

        # Check expiration consistency

        if hasattr(candidate, "expires_at") and candidate.expires_at is not None:
            if candidate.expires_at <= candidate.created_at:
                return False

        return True


class MemoryRelationshipSpecification(Specification):
    """Specification for validating memory relationships."""

    def is_satisfied_by(self, candidate: Any) -> bool:
        """Check if memory relationships are valid.





        Args:


            candidate: Memory object to validate.





        Returns:


            True if relationships are valid.


        """

        if not hasattr(candidate, "related_memories"):
            return True  # No relationships to validate

        related_memories = candidate.related_memories

        if not isinstance(related_memories, list):
            return False

        # Check for self-reference

        memory_id = getattr(candidate, "id", None)

        if memory_id and memory_id in related_memories:
            return False

        # Check for duplicate relationships

        if len(related_memories) != len(set(related_memories)):
            return False

        return True
