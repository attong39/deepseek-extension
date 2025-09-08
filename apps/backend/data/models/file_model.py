"""File model for document and media management."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from apps.backend.data.models.base import Base
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Constants
CASCADE = "CASCADE"
SET_NULL = "SET NULL"

# File status constants
STATUS_UPLOADING = "uploading"
STATUS_PROCESSING = "processing"
STATUS_READY = "ready"
STATUS_ERROR = "error"
STATUS_DELETED = "deleted"

# Storage provider constants
STORAGE_LOCAL = "local"
STORAGE_S3 = "s3"
STORAGE_GCS = "gcs"


class File(Base):
    """
import bool
import content_type
import created_by
import default
import dict
import error_message
import expires_at
import file_hash
import file_id
import file_path
import file_size
import filename
import float
import include_sensitive
import int
import key
import kwargs
import list
import original_filename
import processor
import result
import self
import str
import super
import tag
import unit
import uploaded_by
import value
import version_number
    File model for managing uploaded documents, images, and other media.

    Provides comprehensive file management with support for multiple storage
    providers, metadata extraction, processing pipelines, and access control.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "files"

    # File identification
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # File metadata
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    file_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)  # SHA-256
    encoding: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # File categorization
    file_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="document"
    )  # document, image, video, audio, archive
    category: Mapped[str] = mapped_column(
        String(100), nullable=False, default="general"
    )
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Storage information
    storage_provider: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STORAGE_LOCAL
    )
    storage_bucket: Mapped[str | None] = mapped_column(String(255), nullable=True)
    storage_region: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Processing status
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STATUS_UPLOADING
    )
    processing_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending"
    )
    virus_scan_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending"
    )

    # File relationships
    uploaded_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete=SET_NULL), nullable=True
    )
    parent_file_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("files.id", ondelete=SET_NULL), nullable=True
    )

    # Access control
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_temporary: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    access_permissions: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Expiration and cleanup
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    auto_delete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # File content metadata
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    exif_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Thumbnail and preview
    thumbnail_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    preview_path: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    has_thumbnail: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    has_preview: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Processing results
    processing_results: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Usage tracking
    download_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_accessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    parent_file: Mapped[File | None] = relationship("File", remote_side="File.id")
    child_files: Mapped[list[File]] = relationship("File", back_populates="parent_file")

    def __init__(
        self,
        filename: str,
        original_filename: str,
        file_path: str,
        content_type: str,
        file_size: int,
        uploaded_by: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize file record.

        Args:
            filename: Stored filename
            original_filename: Original filename from upload
            file_path: Storage path
            content_type: MIME content type
            file_size: File size in bytes
            uploaded_by: ID of user who uploaded the file
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.filename = filename
        self.original_filename = original_filename
        self.file_path = file_path
        self.content_type = content_type
        self.file_size = file_size
        self.uploaded_by = uploaded_by
        self.file_type = self._determine_file_type(content_type)

    def _determine_file_type(self, content_type: str) -> str:
        """Determine file type from content type."""
        if content_type.startswith("image/"):
            return "image"
        elif content_type.startswith("video/"):
            return "video"
        elif content_type.startswith("audio/"):
            return "audio"
        elif content_type in [
            "application/zip",
            "application/x-rar",
            "application/x-tar",
        ]:
            return "archive"
        else:
            return "document"

    def mark_ready(self) -> None:
        """Mark file as ready for use."""
        self.status = STATUS_READY
        self.processing_status = "completed"

    def mark_error(self, error_message: str) -> None:
        """Mark file processing as failed."""
        self.status = STATUS_ERROR
        self.processing_status = "failed"
        self.error_message = error_message
        self.processing_attempts += 1

    def mark_processing(self) -> None:
        """Mark file as currently being processed."""
        self.status = STATUS_PROCESSING
        self.processing_status = "processing"
        self.processing_attempts += 1

    def mark_virus_clean(self) -> None:
        """Mark file as clean from virus scan."""
        self.virus_scan_status = "clean"

    def mark_virus_infected(self) -> None:
        """Mark file as infected by virus scan."""
        self.virus_scan_status = "infected"
        self.status = STATUS_ERROR

    def increment_download_count(self) -> None:
        """Increment download counter."""
        self.download_count += 1
        self.last_accessed_at = datetime.now(UTC)

    def increment_view_count(self) -> None:
        """Increment view counter."""
        self.view_count += 1
        self.last_accessed_at = datetime.now(UTC)

    def add_tag(self, tag: str) -> None:
        """Add tag to file."""
        if self.tags is None:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove tag from file."""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""
        if self.file_metadata is None:
            self.file_metadata = {}
        self.file_metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        return self.file_metadata.get(key, default) if self.file_metadata else default

    def set_processing_result(self, processor: str, result: Any) -> None:
        """Set processing result for a specific processor."""
        if self.processing_results is None:
            self.processing_results = {}
        self.processing_results[processor] = result

    def get_processing_result(self, processor: str, default: Any = None) -> Any:
        """Get processing result for a specific processor."""
        return (
            self.processing_results.get(processor, default)
            if self.processing_results
            else default
        )

    def is_image(self) -> bool:
        """Check if file is an image."""
        return self.file_type == "image"

    def is_video(self) -> bool:
        """Check if file is a video."""
        return self.file_type == "video"

    def is_audio(self) -> bool:
        """Check if file is audio."""
        return self.file_type == "audio"

    def is_document(self) -> bool:
        """Check if file is a document."""
        return self.file_type == "document"

    def is_archive(self) -> bool:
        """Check if file is an archive."""
        return self.file_type == "archive"

    def is_ready(self) -> bool:
        """Check if file is ready for use."""
        return self.status == STATUS_READY

    def is_processing(self) -> bool:
        """Check if file is currently being processed."""
        return self.status == STATUS_PROCESSING

    def has_error(self) -> bool:
        """Check if file has processing errors."""
        return self.status == STATUS_ERROR

    def is_expired(self) -> bool:
        """Check if file has expired."""
        if not self.expires_at:
            return False
        return datetime.now(UTC) > self.expires_at

    def is_virus_clean(self) -> bool:
        """Check if file passed virus scan."""
        return self.virus_scan_status == "clean"

    def can_be_viewed(self) -> bool:
        """Check if file can be viewed (has preview or is an image)."""
        return self.has_preview or self.is_image()

    def get_file_size_mb(self) -> float:
        """Get file size in megabytes."""
        return self.file_size / (1024 * 1024)

    def get_file_size_human(self) -> str:
        """Get human-readable file size."""
        size = self.file_size
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def get_file_extension(self) -> str:
        """Get file extension from original filename."""
        return (
            self.original_filename.split(".")[-1].lower()
            if "." in self.original_filename
            else ""
        )

    def soft_delete(self) -> None:
        """Soft delete the file."""
        self.status = STATUS_DELETED
        self.deleted_at = datetime.now(UTC)

    def schedule_deletion(self, expires_at: datetime) -> None:
        """Schedule file for automatic deletion."""
        self.expires_at = expires_at
        self.auto_delete = True

    def to_dict(self, include_sensitive: bool = False) -> dict[str, Any]:
        """
        Convert file to dictionary.

        Args:
            include_sensitive: Whether to include sensitive file paths

        Returns:
            Dictionary representation of the file
        """
        _ = {
            "id": str(self.id),
            "filename": self.filename,
            "original_filename": self.original_filename,
            "content_type": self.content_type,
            "file_size": self.file_size,
            "file_size_human": self.get_file_size_human(),
            "file_type": self.file_type,
            "category": self.category,
            "tags": self.tags,
            "status": self.status,
            "processing_status": self.processing_status,
            "virus_scan_status": self.virus_scan_status,
            "is_public": self.is_public,
            "is_temporary": self.is_temporary,
            "has_thumbnail": self.has_thumbnail,
            "has_preview": self.has_preview,
            "download_count": self.download_count,
            "view_count": self.view_count,
            "uploaded_by": str(self.uploaded_by) if self.uploaded_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_accessed_at": self.last_accessed_at.isoformat()
            if self.last_accessed_at
            else None,
        }

        if include_sensitive:
            result.update(
                {
                    "file_path": self.file_path,
                    "file_url": self.file_url,
                    "thumbnail_path": self.thumbnail_path,
                    "preview_path": self.preview_path,
                    "storage_provider": self.storage_provider,
                    "storage_bucket": self.storage_bucket,
                    "file_hash": self.file_hash,
                    "metadata": self.metadata,
                    "processing_results": self.processing_results,
                }
            )

        return result

    def __repr__(self) -> str:
        """String representation of file."""
        return f"<File(id={self.id}, filename={self.original_filename}, size={self.get_file_size_human()})>"


class FileVersion(Base):
    """
    File version model for tracking file history and versions.

    Enables version control for files with support for rollback,
    comparison, and audit trails.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "file_versions"

    # Version identification
    file_id: Mapped[UUID] = mapped_column(
        ForeignKey("files.id", ondelete=CASCADE), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    version_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Version metadata
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # Version tracking
    created_by: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete=SET_NULL), nullable=True
    )
    change_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Storage
    storage_provider: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STORAGE_LOCAL
    )
    file_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Relationships
    file: Mapped[File] = relationship("File")

    def __init__(
        self,
        file_id: UUID,
        version_number: int,
        filename: str,
        file_path: str,
        file_size: int,
        file_hash: str,
        content_type: str,
        created_by: UUID | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initialize file version.

        Args:
            file_id: ID of parent file
            version_number: Version number
            filename: Version filename
            file_path: Storage path
            file_size: File size
            file_hash: File hash
            content_type: Content type
            created_by: ID of user creating version
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.file_id = file_id
        self.version_number = version_number
        self.filename = filename
        self.file_path = file_path
        self.file_size = file_size
        self.file_hash = file_hash
        self.content_type = content_type
        self.created_by = created_by

    def mark_as_current(self) -> None:
        """Mark this version as the current version."""
        self.is_current = True

    def get_file_size_human(self) -> str:
        """Get human-readable file size."""
        size = self.file_size
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def to_dict(self) -> dict[str, Any]:
        """Convert file version to dictionary."""
        return {
            "id": str(self.id),
            "file_id": str(self.file_id),
            "version_number": self.version_number,
            "version_name": self.version_name,
            "filename": self.filename,
            "file_size": self.file_size,
            "file_size_human": self.get_file_size_human(),
            "file_hash": self.file_hash,
            "content_type": self.content_type,
            "is_current": self.is_current,
            "change_description": self.change_description,
            "created_by": str(self.created_by) if self.created_by else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        """String representation of file version."""
        return f"<FileVersion(file_id={self.file_id}, version={self.version_number}, current={self.is_current})>"
