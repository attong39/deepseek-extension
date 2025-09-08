"""Common serializers and base classes for Zeta AI Server.

This module provides common serializers, error responses, pagination cursors,
and other shared API contract models for the interface layer.

Purpose:
    - Define common API contracts and DTOs
    - Provide base serializer classes with validation
    - Standardize error responses and pagination
    - Enable type-safe Entity ↔ DTO mapping

Context:
    - Interface layer serializers for API contract standardization
    - Used by app layer controllers for request/response serialization
    - Independent of external frameworks (FastAPI, etc.)

Public API:
    - BaseSerializer: Base class for all serializers
    - ErrorResponse: Standard error response model
    - PageCursor: Pagination cursor model
    - ValidationErrorDetail: Validation error details
    - MetaResponse: Response metadata

Error Cases:
    - Validation errors with detailed field-level feedback
    - Serialization errors with context information
    - Type conversion errors with helpful messages

Dependencies:
    - pydantic: For serialization and validation
    - typing: For type hints and generics
    - datetime: For timestamp handling
    - uuid: For UUID handling
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

from app.serializers.base_serializers import OrjsonModel
from pydantic import BaseModel, ConfigDict, Field, field_validator
import ValueError
import action
import bool
import classmethod
import cls
import cursor
import data
import details
import dict
import field_errors
import float
import has_next
import has_prev
import identifier
import int
import limit
import list
import message
import meta_kwargs
import request_id
import resource
import str
import total_count
import v

# Type variable for generic serializers
T = TypeVar("T")
EntityType = TypeVar("EntityType")


class BaseSerializer(OrjsonModel, ABC, Generic[EntityType]):
    """Base serializer class with common configuration and utilities.

    Provides:
        - Standard Pydantic configuration
        - Common validation utilities
        - Type-safe entity conversion methods
        - Error handling helpers
    """

    # Pydantic v2 configuration is provided by OrjsonModel (json load/dump, from_attributes)
    # and we augment model behavior via model_config here if needed.
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        extra="forbid",
        validate_assignment=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None,
            UUID: lambda v: str(v) if v else None,
        },
    )

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: EntityType) -> BaseSerializer[EntityType]:
        """Convert domain entity to serializer DTO.

        Args:
            entity: Domain entity to convert

        Returns:
            Serializer DTO instance

        Raises:
            ValidationError: If entity data is invalid
        """

    @abstractmethod
    def to_entity_dict(self) -> dict[str, Any]:
        """Convert serializer DTO to entity creation dictionary.

        Returns:
            Dictionary suitable for entity creation

        Raises:
            ValidationError: If serializer data is invalid
        """


class ErrorResponse(BaseModel):
    """Standard error response model for all API errors."""

    # Error classification
    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")

    # Optional context
    details: dict[str, Any] | None = Field(
        None, description="Additional error context and details"
    )
    field_errors: list[ValidationErrorDetail] | None = Field(
        None, description="Field-level validation errors"
    )

    # Metadata
    request_id: str | None = Field(None, description="Request tracking ID")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Error occurrence timestamp"
    )

    # API version for debugging
    api_version: str = Field(default="v1", description="API version")

    @classmethod
    def validation_error(
        cls,
        message: str = "Validation failed",
        field_errors: list[ValidationErrorDetail] | None = None,
        details: dict[str, Any] | None = None,
        request_id: str | None = None,
    ) -> ErrorResponse:
        """Create validation error response."""
        return cls(
            error_code="VALIDATION_ERROR",
            message=message,
            field_errors=field_errors or [],
            details=details,
            request_id=request_id,
        )

    @classmethod
    def not_found(
        cls, resource: str, identifier: str, request_id: str | None = None
    ) -> ErrorResponse:
        """Create not found error response."""
        return cls(
            error_code="NOT_FOUND",
            message=f"{resource} not found",
            field_errors=[],
            details={"resource": resource, "identifier": identifier},
            request_id=request_id,
        )

    @classmethod
    def permission_denied(
        cls, action: str, resource: str, request_id: str | None = None
    ) -> ErrorResponse:
        """Create permission denied error response."""
        return cls(
            error_code="PERMISSION_DENIED",
            message=f"Permission denied for {action} on {resource}",
            field_errors=[],
            details={"action": action, "resource": resource},
            request_id=request_id,
        )

    @classmethod
    def internal_error(
        cls, details: dict[str, Any] | None = None, request_id: str | None = None
    ) -> ErrorResponse:
        """Create internal server error response."""
        return cls(
            error_code="INTERNAL_ERROR",
            message="An internal error occurred",
            field_errors=[],
            details=details,
            request_id=request_id,
        )


class ValidationErrorDetail(BaseModel):
    """Details for field-level validation errors."""

    field: str = Field(..., description="Field name that failed validation")
    message: str = Field(..., description="Validation error message")
    invalid_value: Any = Field(None, description="The invalid value provided")
    constraint: str | None = Field(
        None, description="Validation constraint that failed"
    )


class PageCursor(BaseModel):
    """Pagination cursor for efficient pagination."""

    # Cursor data
    cursor: str | None = Field(None, description="Opaque cursor for next page")
    limit: int = Field(default=20, ge=1, le=100, description="Number of items per page")

    # Result metadata
    has_next: bool = Field(default=False, description="Whether more items exist")
    has_prev: bool = Field(default=False, description="Whether previous items exist")
    total_count: int | None = Field(None, description="Total items (if available)")

    @field_validator("limit")
    def validate_limit(cls, v: int) -> int:
        """Validate pagination limit."""
        if v < 1:
            raise ValueError("Limit must be at least 1")
        if v > 100:
            raise ValueError("Limit cannot exceed 100")
        return v


class MetaResponse(BaseModel):
    """Response metadata for API responses."""

    # Request tracking
    request_id: str | None = Field(None, description="Request tracking ID")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Response timestamp"
    )

    # API information
    api_version: str = Field(default="v1", description="API version")
    endpoint: str | None = Field(None, description="API endpoint")

    # Performance metrics
    execution_time_ms: int | None = Field(
        None, description="Request execution time in milliseconds"
    )

    # Feature flags (optional)
    features: dict[str, bool] = Field(
        default_factory=dict, description="Enabled features for this response"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""

    # Data
    data: list[T] = Field(..., description="Response data items")

    # Pagination
    pagination: PageCursor = Field(..., description="Pagination information")

    # Metadata
    meta: MetaResponse = Field(
        default_factory=lambda: MetaResponse(
            request_id="", endpoint="", execution_time_ms=0
        ),
        description="Response metadata",
    )

    @classmethod
    def create(
        cls,
        data: list[T],
        cursor: str | None = None,
        limit: int = 20,
        has_next: bool = False,
        has_prev: bool = False,
        total_count: int | None = None,
        **meta_kwargs: Any,
    ) -> PaginatedResponse[T]:
        """Create paginated response with data and pagination info."""
        pagination = PageCursor(
            cursor=cursor,
            limit=limit,
            has_next=has_next,
            has_prev=has_prev,
            total_count=total_count,
        )

        meta = MetaResponse(**meta_kwargs)

        return cls(data=data, pagination=pagination, meta=meta)


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Overall system status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Health check timestamp"
    )

    # Component statuses
    components: dict[str, str] = Field(
        default_factory=dict, description="Individual component statuses"
    )

    # Performance metrics
    uptime_seconds: int | None = Field(None, description="System uptime in seconds")
    memory_usage_mb: float | None = Field(None, description="Memory usage in MB")
    cpu_usage_percent: float | None = Field(None, description="CPU usage percentage")


# Response wrapper types for common patterns
SuccessResponse = dict[str, Any]  # For simple success responses
DataResponse = dict[str, T]  # For single item responses
