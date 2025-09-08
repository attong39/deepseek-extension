"""Memory model for AI agent memory management."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from apps.backend.data.models.base import Base
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Constants


CASCADE = "CASCADE"


SET_NULL = "SET NULL"


# Table name constants


MEMORIES_TABLE = "memories.id"


MEMORY_EMBEDDINGS_TABLE = "memory_embeddings"


MEMORY_ASSOCIATIONS_TABLE = "memory_associations"


# Memory type constants


MEMORY_EPISODIC = "episodic"


MEMORY_SEMANTIC = "semantic"


MEMORY_PROCEDURAL = "procedural"


MEMORY_WORKING = "working"


MEMORY_META = "meta"


# Memory status constants


STATUS_ACTIVE = "active"


STATUS_ARCHIVED = "archived"


STATUS_DELETED = "deleted"


STATUS_PROCESSING = "processing"


class Memory(Base):
    """
import ValueError
import a
import agent_id
import association_type
import b
import bool
import content
import content_hash
import default
import dict
import embedding_type
import embedding_vector
import float
import importance_score
import include_content
import include_sensitive
import include_vector
import int
import k
import key
import keyword
import kwargs
import len
import list
import max
import max_length
import memory_id
import memory_type
import min
import model_name
import new_score
import other_vector
import parent_memory_id
import result
import self
import sensitive
import source_memory_id
import str
import strength
import strength_boost
import strength_reduction
import sum
import super
import tag
import target_memory_id
import value
import verified
import x
import zip


    Memory model for AI agent memory storage and retrieval.





    Implements a comprehensive memory system with support for different


    memory types, importance scoring, temporal decay, and semantic relationships.


    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "memories"

    # Memory identification

    agent_id: Mapped[UUID] = mapped_column(
        ForeignKey("agents.id", ondelete=CASCADE), nullable=False
    )

    memory_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=MEMORY_EPISODIC
    )

    # Memory content

    content: Mapped[str] = mapped_column(Text, nullable=False)

    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Memory classification

    category: Mapped[str] = mapped_column(
        String(100), nullable=False, default="general"
    )

    subcategory: Mapped[str | None] = mapped_column(String(100), nullable=True)

    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Importance and relevance

    importance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)

    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Temporal information

    event_timestamp: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    last_accessed: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    access_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Memory relationships

    parent_memory_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(MEMORIES_TABLE, ondelete=SET_NULL), nullable=True
    )

    related_memories: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=[]
    )  # Memory IDs

    # Context and source

    context: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default={})

    source_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="conversation"
    )  # conversation, task, system, external

    source_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    # Memory status

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STATUS_ACTIVE
    )

    is_factual: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_sensitive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Embedding and search

    embedding_model: Mapped[str | None] = mapped_column(String(100), nullable=True)

    embedding_dimensions: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Decay and retention

    decay_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.1)

    retention_priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5
    )  # 1-10

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Version control

    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    previous_version_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(MEMORIES_TABLE, ondelete=SET_NULL), nullable=True
    )

    # Memory metadata

    memory_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    processing_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Relationships

    # agent: Mapped["Agent"] = relationship("Agent", back_populates="memories")  # TODO: Add when Agent model exists

    parent_memory: Mapped[Memory | None] = relationship(
        "Memory",
        remote_side="Memory.id",
        foreign_keys=[parent_memory_id],
    )

    child_memories: Mapped[list[Memory]] = relationship(
        "Memory",
        back_populates="parent_memory",
        foreign_keys=lambda: [Memory.parent_memory_id],
    )

    embeddings: Mapped[list[MemoryEmbedding]] = relationship(
        "MemoryEmbedding", back_populates="memory", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        agent_id: UUID,
        content: str,
        memory_type: str = MEMORY_EPISODIC,
        importance_score: float = 0.5,
        **kwargs: Any,
    ) -> None:
        """


        Initialize memory.





        Args:


            agent_id: ID of the agent owning this memory


            content: Memory content


            memory_type: Type of memory


            importance_score: Importance score (0.0 to 1.0)


            **kwargs: Additional model arguments


        """

        super().__init__(**kwargs)

        self.agent_id = agent_id

        self.content = content

        self.memory_type = memory_type

        self.importance_score = max(0.0, min(1.0, importance_score))

        self.event_timestamp = datetime.now(UTC)

    def access_memory(self) -> None:
        """Record memory access and update relevance."""

        self.last_accessed = datetime.now(UTC)

        self.access_count += 1

        # Boost importance slightly when accessed

        self.importance_score = min(1.0, self.importance_score + 0.01)

    def update_importance(self, new_score: float) -> None:
        """Update importance score with validation."""

        self.importance_score = max(0.0, min(1.0, new_score))

    def add_keyword(self, keyword: str) -> None:
        """Add keyword to memory."""

        if self.keywords is None:
            self.keywords = []

        keyword_lower = keyword.lower()

        if keyword_lower not in [k.lower() for k in self.keywords]:
            self.keywords.append(keyword)

    def add_tag(self, tag: str) -> None:
        """Add tag to memory."""

        if self.tags is None:
            self.tags = []

        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove tag from memory."""

        if self.tags and tag in self.tags:
            self.tags.remove(tag)

    def add_related_memory(self, memory_id: str) -> None:
        """Add related memory ID."""

        if self.related_memories is None:
            self.related_memories = []

        if memory_id not in self.related_memories:
            self.related_memories.append(memory_id)

    def remove_related_memory(self, memory_id: str) -> None:
        """Remove related memory ID."""

        if self.related_memories and memory_id in self.related_memories:
            self.related_memories.remove(memory_id)

    def set_context(self, key: str, value: Any) -> None:
        """Set context value."""

        if self.context is None:
            self.context = {}

        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value."""

        return self.context.get(key, default) if self.context else default

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""

        if self.memory_metadata is None:
            self.memory_metadata = {}

        self.memory_metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""

        return (
            self.memory_metadata.get(key, default) if self.memory_metadata else default
        )

    def calculate_decay(self) -> float:
        """


        Calculate memory decay based on time and access patterns.





        Returns:


            Current decay factor (0.0 to 1.0)


        """

        if not self.last_accessed:
            time_since_access = (datetime.now(UTC) - self.created_at).total_seconds()

        else:
            time_since_access = (datetime.now(UTC) - self.last_accessed).total_seconds()

        # Time in days

        days_since_access = time_since_access / (24 * 3600)

        # Exponential decay with configurable rate

        decay_factor = max(0.0, 1.0 - (self.decay_rate * days_since_access))

        # Adjust for access frequency

        access_boost = min(0.3, self.access_count * 0.01)

        return min(1.0, decay_factor + access_boost)

    def get_effective_importance(self) -> float:
        """Get importance score adjusted for decay."""

        decay_factor = self.calculate_decay()

        return self.importance_score * decay_factor

    def archive_memory(self) -> None:
        """Archive the memory."""

        self.status = STATUS_ARCHIVED

    def soft_delete(self) -> None:
        """Soft delete the memory."""

        self.status = STATUS_DELETED

    def mark_verified(self, verified: bool = True) -> None:
        """Mark memory as verified or unverified."""

        self.is_verified = verified

    def mark_sensitive(self, sensitive: bool = True) -> None:
        """Mark memory as sensitive or not."""

        self.is_sensitive = sensitive

    def create_summary(self, max_length: int = 200) -> str:
        """Create or update memory summary."""

        if len(self.content) <= max_length:
            self.summary = self.content

        else:
            # Simple truncation - in practice, you'd use AI summarization

            self.summary = self.content[: max_length - 3] + "..."

        return self.summary or ""

    def is_episodic(self) -> bool:
        """Check if memory is episodic."""

        return self.memory_type == MEMORY_EPISODIC

    def is_semantic(self) -> bool:
        """Check if memory is semantic."""

        return self.memory_type == MEMORY_SEMANTIC

    def is_procedural(self) -> bool:
        """Check if memory is procedural."""

        return self.memory_type == MEMORY_PROCEDURAL

    def is_working(self) -> bool:
        """Check if memory is working memory."""

        return self.memory_type == MEMORY_WORKING

    def is_active(self) -> bool:
        """Check if memory is active."""

        return self.status == STATUS_ACTIVE

    def is_archived(self) -> bool:
        """Check if memory is archived."""

        return self.status == STATUS_ARCHIVED

    def is_expired(self) -> bool:
        """Check if memory has expired."""

        if not self.expires_at:
            return False

        return datetime.now(UTC) > self.expires_at

    def should_be_retained(self) -> bool:
        """Check if memory should be retained based on importance and decay."""

        effective_importance = self.get_effective_importance()

        retention_threshold = 0.1 + (self.retention_priority * 0.05)

        return effective_importance >= retention_threshold

    def to_dict(
        self, include_content: bool = True, include_sensitive: bool = False
    ) -> dict[str, Any]:
        """


        Convert memory to dictionary.





        Args:


            include_content: Whether to include full content


            include_sensitive: Whether to include sensitive data





        Returns:


            Dictionary representation of the memory


        """

        _ = {
            "id": str(self.id),
            "agent_id": str(self.agent_id),
            "memory_type": self.memory_type,
            "category": self.category,
            "subcategory": self.subcategory,
            "importance_score": self.importance_score,
            "effective_importance": self.get_effective_importance(),
            "confidence_score": self.confidence_score,
            "relevance_score": self.relevance_score,
            "status": self.status,
            "is_factual": self.is_factual,
            "is_verified": self.is_verified,
            "access_count": self.access_count,
            "retention_priority": self.retention_priority,
            "version": self.version,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "keywords": self.keywords,
            "tags": self.tags,
            "related_memories": self.related_memories,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "event_timestamp": self.event_timestamp.isoformat()
            if self.event_timestamp
            else None,
            "last_accessed": self.last_accessed.isoformat()
            if self.last_accessed
            else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

        if include_content:
            if self.is_sensitive and not include_sensitive:
                result["content"] = "[SENSITIVE CONTENT HIDDEN]"

                result["summary"] = "[SENSITIVE CONTENT HIDDEN]"

            else:
                result["content"] = self.content

                result["summary"] = self.summary

        if include_sensitive:
            result.update(
                {
                    "context": self.context,
                    "metadata": self.memory_metadata,
                    "processing_metadata": self.processing_metadata,
                    "is_sensitive": self.is_sensitive,
                }
            )

        return result

    def __repr__(self) -> str:
        """String representation of memory."""

        content_preview = (
            self.content[:50] + "..." if len(self.content) > 50 else self.content
        )

        return f"<Memory(id={self.id}, type={self.memory_type}, importance={self.importance_score:.2f}, content='{content_preview}')>"


class MemoryEmbedding(Base):
    """


    Memory embedding model for semantic search and similarity.





    Stores vector embeddings of memory content for efficient


    semantic search and similarity calculations.


    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "memory_embeddings"

    # Embedding identification

    memory_id: Mapped[UUID] = mapped_column(
        ForeignKey(MEMORIES_TABLE, ondelete=CASCADE), nullable=False
    )

    model_name: Mapped[str] = mapped_column(String(100), nullable=False)

    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Embedding data

    embedding_vector: Mapped[list[float]] = mapped_column(JSON, nullable=False)

    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)

    # Embedding metadata

    content_hash: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # Hash of embedded content

    embedding_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="content"
    )  # content, summary, keywords

    # Processing info

    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    embedding_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Relationships

    memory: Mapped[Memory] = relationship("Memory", back_populates="embeddings")

    def __init__(
        self,
        memory_id: UUID,
        model_name: str,
        embedding_vector: list[float],
        content_hash: str,
        embedding_type: str = "content",
        **kwargs: Any,
    ) -> None:
        """


        Initialize memory embedding.





        Args:


            memory_id: ID of the memory


            model_name: Name of embedding model


            embedding_vector: Vector embedding


            content_hash: Hash of embedded content


            embedding_type: Type of embedding


            **kwargs: Additional model arguments


        """

        super().__init__(**kwargs)

        self.memory_id = memory_id

        self.model_name = model_name

        self.embedding_vector = embedding_vector

        self.dimensions = len(embedding_vector)

        self.content_hash = content_hash

        self.embedding_type = embedding_type

    def calculate_similarity(self, other_vector: list[float]) -> float:
        """


        Calculate cosine similarity with another vector.





        Args:


            other_vector: Vector to compare against





        Returns:


            Cosine similarity score (-1 to 1)


        """

        import math

        if len(self.embedding_vector) != len(other_vector):
            raise ValueError("Vector dimensions must match")

        # Calculate dot product

        dot_product = sum(
            a * b for a, b in zip(self.embedding_vector, other_vector, strict=False)
        )

        # Calculate magnitudes

        magnitude_a = math.sqrt(sum(a * a for a in self.embedding_vector))

        magnitude_b = math.sqrt(sum(b * b for b in other_vector))

        # Avoid division by zero

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    def get_vector_magnitude(self) -> float:
        """Get the magnitude of the embedding vector."""

        import math

        return math.sqrt(sum(x * x for x in self.embedding_vector))

    def normalize_vector(self) -> list[float]:
        """Get normalized version of the embedding vector."""

        magnitude = self.get_vector_magnitude()

        if magnitude == 0:
            return self.embedding_vector.copy()

        return [x / magnitude for x in self.embedding_vector]

    def to_dict(self, include_vector: bool = False) -> dict[str, Any]:
        """


        Convert embedding to dictionary.





        Args:


            include_vector: Whether to include the full vector





        Returns:


            Dictionary representation of the embedding


        """

        _ = {
            "id": str(self.id),
            "memory_id": str(self.memory_id),
            "model_name": self.model_name,
            "model_version": self.model_version,
            "dimensions": self.dimensions,
            "content_hash": self.content_hash,
            "embedding_type": self.embedding_type,
            "processing_time_ms": self.processing_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

        if include_vector:
            result["embedding_vector"] = self.embedding_vector

            result["vector_magnitude"] = self.get_vector_magnitude()

        return result

    def __repr__(self) -> str:
        """String representation of memory embedding."""

        return f"<MemoryEmbedding(memory_id={self.memory_id}, model={self.model_name}, dimensions={self.dimensions})>"


class MemoryAssociation(Base):
    """


    Memory association model for tracking relationships between memories.





    Enables the creation of semantic networks and knowledge graphs


    between different memories.


    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "memory_associations"

    # Association identification

    source_memory_id: Mapped[UUID] = mapped_column(
        ForeignKey(MEMORIES_TABLE, ondelete=CASCADE), nullable=False
    )

    target_memory_id: Mapped[UUID] = mapped_column(
        ForeignKey(MEMORIES_TABLE, ondelete=CASCADE), nullable=False
    )

    # Association properties

    association_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="related"
    )  # related, causal, temporal, semantic

    strength: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.5
    )  # 0.0 to 1.0

    confidence: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.5
    )  # 0.0 to 1.0

    # Association metadata

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    context: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default={})

    # Discovery information

    discovered_by: Mapped[str] = mapped_column(
        String(50), nullable=False, default="system"
    )  # system, user, ai

    discovery_method: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Status

    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    is_bidirectional: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # Temporal decay

    decay_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)

    last_reinforced: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships

    source_memory: Mapped[Memory] = relationship(
        "Memory", foreign_keys=[source_memory_id]
    )

    target_memory: Mapped[Memory] = relationship(
        "Memory", foreign_keys=[target_memory_id]
    )

    def __init__(
        self,
        source_memory_id: UUID,
        target_memory_id: UUID,
        association_type: str = "related",
        strength: float = 0.5,
        **kwargs: Any,
    ) -> None:
        """


        Initialize memory association.





        Args:


            source_memory_id: ID of source memory


            target_memory_id: ID of target memory


            association_type: Type of association


            strength: Association strength (0.0 to 1.0)


            **kwargs: Additional model arguments


        """

        super().__init__(**kwargs)

        self.source_memory_id = source_memory_id

        self.target_memory_id = target_memory_id

        self.association_type = association_type

        self.strength = max(0.0, min(1.0, strength))

    def reinforce(self, strength_boost: float = 0.1) -> None:
        """Reinforce the association by increasing strength."""

        self.strength = min(1.0, self.strength + strength_boost)

        self.last_reinforced = datetime.now(UTC)

    def weaken(self, strength_reduction: float = 0.1) -> None:
        """Weaken the association by decreasing strength."""

        self.strength = max(0.0, self.strength - strength_reduction)

    def calculate_decay(self) -> float:
        """Calculate association decay over time."""

        if not self.last_reinforced:
            time_since_reinforcement = (
                datetime.now(UTC) - self.created_at
            ).total_seconds()

        else:
            time_since_reinforcement = (
                datetime.now(UTC) - self.last_reinforced
            ).total_seconds()

        days_since_reinforcement = time_since_reinforcement / (24 * 3600)

        decay_factor = max(0.0, 1.0 - (self.decay_rate * days_since_reinforcement))

        return decay_factor

    def get_effective_strength(self) -> float:
        """Get strength adjusted for temporal decay."""

        decay_factor = self.calculate_decay()

        return self.strength * decay_factor

    def verify_association(self, verified: bool = True) -> None:
        """Mark association as verified or unverified."""

        self.is_verified = verified

    def to_dict(self) -> dict[str, Any]:
        """Convert association to dictionary."""

        return {
            "id": str(self.id),
            "source_memory_id": str(self.source_memory_id),
            "target_memory_id": str(self.target_memory_id),
            "association_type": self.association_type,
            "strength": self.strength,
            "effective_strength": self.get_effective_strength(),
            "confidence": self.confidence,
            "description": self.description,
            "discovered_by": self.discovered_by,
            "discovery_method": self.discovery_method,
            "is_verified": self.is_verified,
            "is_bidirectional": self.is_bidirectional,
            "context": self.context,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_reinforced": self.last_reinforced.isoformat()
            if self.last_reinforced
            else None,
        }

    def __repr__(self) -> str:
        """String representation of memory association."""

        return f"<MemoryAssociation(source={self.source_memory_id}, target={self.target_memory_id}, type={self.association_type}, strength={self.strength:.2f})>"
