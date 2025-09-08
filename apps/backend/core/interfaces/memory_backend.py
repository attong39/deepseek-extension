from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field, field_validator
import ValueError
import bool
import classmethod
import count
import data
import dict
import enumerate
import error
import i
import int
import isinstance
import len
import list
import metadata
import namespace
import operation
import record
import records
import status
import str
import v

"""Type-safe Memory Backend Interface với Protocol và Pydantic validation.
Module này cung cấp:
- MemoryBackend Protocol với strict typing
- MemoryResult Pydantic model với schema validation
- Type-safe backend implementations
"""


class MemoryResult(BaseModel):
    """Standardized result model cho memory operations."""

    model_config = ConfigDict(extra="forbid")  # Strict schema validation
    status: str = Field(..., description="Operation status")
    namespace: str = Field(..., description="Target namespace")
    operation: str = Field(..., description="Operation type")
    count: int | None = Field(None, description="Number of records processed")
    data: dict[str, Any] | None = Field(None, description="Operation data")
    error: str | None = Field(None, description="Error message if any")
    metadata: dict[str, Any] | None = Field(None, description="Additional metadata")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status is one of allowed values."""
        allowed = {"success", "error", "partial", "pending"}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v

    @field_validator("operation")
    @classmethod
    def validate_operation(cls, v: str) -> str:
        """Validate operation is one of allowed values."""
        allowed = {"upsert", "query", "delete", "rebuild", "batch_upsert"}
        if v not in allowed:
            raise ValueError(f"Operation must be one of {allowed}")
        return v


@runtime_checkable
class MemoryBackend(Protocol):
    """Type-safe Protocol cho memory backend implementations."""

    def upsert(
        self,
        namespace: str,
        records: list[dict[str, Any]],
        embedding_model: str | None = None,
    ) -> MemoryResult:
        """Upsert records vào namespace.
        Args:
            namespace: Target namespace
            records: List of record dictionaries
            embedding_model: Optional embedding model name
        Returns:
            MemoryResult với operation status
        """
        ...

    def query(
        self,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> MemoryResult:
        """Query records từ namespace.
        Args:
            namespace: Target namespace
            query: Search query string
            top_k: Number of results to return
            filters: Optional metadata filters
        Returns:
            MemoryResult với query results
        """
        ...

    def delete(
        self,
        namespace: str,
        ids: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        hard: bool = False,
    ) -> MemoryResult:
        """Delete records từ namespace.
        Args:
            namespace: Target namespace
            ids: Optional list of record IDs to delete
            filters: Optional filters for soft delete
            hard: Whether to hard delete (permanent)
        Returns:
            MemoryResult với delete status
        """
        ...

    def rebuild_embeddings(
        self, namespace: str, target_model: str, batch_size: int = 256
    ) -> MemoryResult:
        """Rebuild embeddings cho namespace.
        Args:
            namespace: Target namespace
            target_model: Target embedding model
            batch_size: Batch size for processing
        Returns:
            MemoryResult với rebuild status
        """
        ...


class BaseMemoryBackend:
    """Base implementation với common functionality."""

    def _create_result(
        self,
        status: str,
        namespace: str,
        operation: str,
        count: int | None = None,
        data: dict[str, Any] | None = None,
        error: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryResult:
        """Helper method để tạo MemoryResult."""
        return MemoryResult(
            status=status,
            namespace=namespace,
            operation=operation,
            count=count,
            data=data,
            error=error,
            metadata=metadata,
        )

    def _validate_namespace(self, namespace: str) -> None:
        """Validate namespace format."""
        if not namespace or not isinstance(namespace, str):
            raise ValueError("Namespace must be a non-empty string")
        if len(namespace) > 100:
            raise ValueError("Namespace must be <= 100 characters")

    def _validate_records(self, records: list[dict[str, Any]]) -> None:
        """Validate records format."""
        if not records:
            raise ValueError("Records list cannot be empty")
        if len(records) > 10000:
            raise ValueError("Cannot process more than 10,000 records at once")
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                raise ValueError(f"Record {i} must be a dictionary")
            if "id" not in record:
                raise ValueError(f"Record {i} must have an 'id' field")
            if "content" not in record and "text" not in record:
                raise ValueError(f"Record {i} must have 'content' or 'text' field")


__all__ = [
    "BaseMemoryBackend",
    "MemoryBackend",
    "MemoryResult",
    "allowed",
    "delete",
    "model_config",
    "query",
    "rebuild_embeddings",
    "upsert",
    "validate_operation",
    "validate_status",
]
