"""


File Manager - Central File Management System





Handles all file operations including upload, download, validation, and metadata management.


Supports multiple storage backends (local, S3, etc.).


"""

import asyncio
import hashlib
import mimetypes
import os
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.backend.storage.blob_storage import BlobStorage
from apps.backend.storage.local_storage import LocalStorage
import Exception
import OSError
import allowed_extensions
import bool
import bytes
import dict
import dir_path
import directory
import expires_in
import file_path
import int
import len
import list
import max_age_hours
import max_file_size
import metadata
import new_filename
import new_path
import s3_bucket
import self
import source_metadata
import str
import use_s3


@dataclass
class FileMetadata:
    """File metadata information."""

    id: str

    filename: str

    original_filename: str

    content_type: str

    size: int

    checksum: str

    storage_path: str

    storage_backend: str

    created_at: datetime

    updated_at: datetime

    metadata: dict[str, Any]


class FileValidationError(Exception):
    """File validation error."""


class FileManager:
    """Central file management system."""

    def __init__(
        self,
        storage_path: str = "storage",
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        allowed_extensions: list[str] | None = None,
        use_s3: bool = False,
        s3_bucket: str | None = None,
    ):
        """Initialize file manager."""

        self.storage_path = Path(storage_path)

        self.max_file_size = max_file_size

        self.allowed_extensions = allowed_extensions or [
            "txt",
            "pdf",
            "doc",
            "docx",
            "md",
            "csv",
            "xlsx",
            "json",
            "xml",
        ]

        # Initialize storage backends

        self.local_storage = LocalStorage(str(self.storage_path))

        self.blob_storage = BlobStorage() if use_s3 else None

        self.use_s3 = use_s3 and s3_bucket is not None

        # Ensure storage directories exist

        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""

        directories = [
            self.storage_path / "uploads",
            self.storage_path / "temp",
            self.storage_path / "processed",
            self.storage_path / "cache",
            self.storage_path / "backups",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _validate_file(self, filename: str, content: bytes) -> None:
        """Validate file before processing."""

        # Check file size

        if len(content) > self.max_file_size:
            raise FileValidationError(
                f"File size {len(content)} exceeds maximum {self.max_file_size}"
            )

        # Check file extension

        extension = Path(filename).suffix.lower().lstrip(".")

        if extension not in self.allowed_extensions:
            raise FileValidationError(
                f"File extension '{extension}' not allowed. "
                f"Allowed: {', '.join(self.allowed_extensions)}"
            )

        # Check for empty files

        if len(content) == 0:
            raise FileValidationError("Empty files are not allowed")

    def _generate_file_id(self) -> str:
        """Generate unique file ID."""

        return str(uuid.uuid4())

    def _calculate_checksum(self, content: bytes) -> str:
        """Calculate file checksum."""

        return hashlib.sha256(content).hexdigest()

    def _get_content_type(self, filename: str) -> str:
        """Get content type from filename."""

        content_type, _ = mimetypes.guess_type(filename)

        return content_type or "application/octet-stream"

    def _generate_storage_path(self, file_id: str, filename: str) -> str:
        """Generate storage path for file."""

        extension = Path(filename).suffix

        return f"uploads/{file_id}{extension}"

    async def upload_file(
        self, filename: str, content: bytes, metadata: dict[str, Any] | None = None
    ) -> FileMetadata:
        """Upload a file to storage."""

        # Validate file

        self._validate_file(filename, content)

        # Generate file metadata

        file_id = self._generate_file_id()

        checksum = self._calculate_checksum(content)

        content_type = self._get_content_type(filename)

        storage_path = self._generate_storage_path(file_id, filename)

        now = datetime.now(UTC)

        # Choose storage backend

        if self.use_s3 and self.blob_storage:
            # Upload to S3
            await self.blob_storage.upload_file(storage_path, content, content_type)

            storage_backend = "s3"

        else:
            # Upload to local storage

            await self.local_storage.save_file(storage_path, content)

            storage_backend = "local"

        # Create file metadata

        file_metadata = FileMetadata(
            id=file_id,
            filename=f"{file_id}{Path(filename).suffix}",
            original_filename=filename,
            content_type=content_type,
            size=len(content),
            checksum=checksum,
            storage_path=storage_path,
            storage_backend=storage_backend,
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
        )

        return file_metadata

    async def download_file(self, file_metadata: FileMetadata) -> bytes:
        """Download file content."""

        if file_metadata.storage_backend == "s3" and self.blob_storage:
            return await self.blob_storage.download_file(file_metadata.storage_path)

        else:
            return await self.local_storage.read_file(file_metadata.storage_path)

    async def delete_file(self, file_metadata: FileMetadata) -> bool:
        """Delete file from storage."""

        try:
            if file_metadata.storage_backend == "s3" and self.blob_storage:
                await self.blob_storage.delete_file(file_metadata.storage_path)

            else:
                await self.local_storage.delete_file(file_metadata.storage_path)

            return True

        except Exception:
            return False

    async def get_file_url(
        self, file_metadata: FileMetadata, expires_in: int = 3600
    ) -> str:
        """Get temporary URL for file access."""

        if file_metadata.storage_backend == "s3" and self.blob_storage:
            return await self.blob_storage.get_presigned_url(
                file_metadata.storage_path, expires_in
            )

        else:
            return await self.local_storage.get_file_url(file_metadata.storage_path)

    async def copy_file(
        self, source_metadata: FileMetadata, new_filename: str | None = None
    ) -> FileMetadata:
        """Copy an existing file."""

        # Download source file

        content = await self.download_file(source_metadata)

        # Upload as new file

        filename = new_filename or source_metadata.original_filename

        return await self.upload_file(filename, content, source_metadata.metadata)

    async def move_file(
        self, file_metadata: FileMetadata, new_path: str
    ) -> FileMetadata:
        """Move file to new location (copy + delete)."""

        content = await self.download_file(file_metadata)

        if self.use_s3 and self.blob_storage:
            await self.blob_storage.upload_file(
                new_path, content, file_metadata.content_type
            )
        else:
            await self.local_storage.save_file(new_path, content)

        await self.delete_file(file_metadata)

        file_metadata.storage_path = new_path
        file_metadata.updated_at = datetime.now(UTC)

        return file_metadata

    async def get_storage_stats(self) -> dict[str, Any]:
        """Get storage usage statistics."""

        def _scan(dir_path: Path) -> dict[str, Any]:
            s = {
                "total_files": 0,
                "total_size": 0,
                "storage_backends": {},
                "file_types": {},
            }
            if dir_path.exists():
                for file_path in dir_path.rglob("*"):
                    if file_path.is_file():
                        s["total_files"] += 1
                        try:
                            s["total_size"] += file_path.stat().st_size
                        except Exception:
                            pass
            return s

        uploads_dir = self.storage_path / "uploads"
        return await asyncio.to_thread(_scan, uploads_dir)

    async def cleanup_temp_files(self, max_age_hours: int = 24) -> int:
        """Clean up temporary files older than specified age."""

        temp_dir = self.storage_path / "temp"
        if not temp_dir.exists():
            return 0

        max_age_seconds = max_age_hours * 3600
        current_time = datetime.now().timestamp()

        def _cleanup(dir_path: Path) -> int:
            cnt = 0
            for file_path in dir_path.rglob("*"):
                if file_path.is_file():
                    try:
                        file_age = current_time - file_path.stat().st_mtime
                        if file_age > max_age_seconds:
                            file_path.unlink()
                            cnt += 1
                    except OSError:
                        pass
            return cnt

        return await asyncio.to_thread(_cleanup, temp_dir)


# Global file manager instance


_file_manager: FileManager | None = None


def get_file_manager() -> FileManager:
    """Get global file manager instance."""

    global _file_manager  # noqa: PLW0603

    if _file_manager is None:
        # Đọc env để cấu hình mặc định
        allowed_exts_env = os.getenv("TRAINING_ALLOWED_EXTS", "")
        allowed_exts = [
            s.strip().lower().lstrip(".")
            for s in allowed_exts_env.split(",")
            if s.strip()
        ]
        max_mb = os.getenv("TRAINING_MAX_FILE_SIZE_MB")
        try:
            max_bytes = int(max_mb) * 1024 * 1024 if max_mb else 10 * 1024 * 1024
        except Exception:
            max_bytes = 10 * 1024 * 1024

        _file_manager = FileManager(
            max_file_size=max_bytes,
            allowed_extensions=allowed_exts or None,
        )

    return _file_manager


__all__ = [
    "FileManager",
    "FileMetadata",
    "FileValidationError",
    "get_file_manager",
]
