"""Media storage manager for ZETA AI Server.





This module provides comprehensive media file management including:


- Image storage and processing


- Video storage and transcoding


- Audio storage and processing


- Document storage with previews


- Metadata extraction and indexing


- Thumbnail generation


"""

import hashlib
import logging
import mimetypes
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any
import Exception
import ImportError
import allowed_extensions
import bool
import chunk
import classmethod
import cls
import created_at
import custom_id
import data
import dict
import e
import error_msg
import extensions
import extract_metadata
import f
import generate_thumbnails
import int
import is_valid
import iter
import len
import limit
import list
import m
import max_file_size
import offset
import open
import self
import storage_dir
import str
import sum
import tag_id
import thumbnail_size
import tuple
import value
import x

logger = logging.getLogger(__name__)


class MediaType:
    """Media type constants."""

    IMAGE = "image"

    VIDEO = "video"

    AUDIO = "audio"

    DOCUMENT = "document"

    UNKNOWN = "unknown"


class MediaConfig:
    """Configuration for media storage."""

    def __init__(
        self,
        storage_dir: str | Path,
        max_file_size: int = 100 * 1024 * 1024,  # 100MB
        thumbnail_size: tuple[int, int] = (300, 300),
        allowed_extensions: dict[str, list[str]] | None = None,
        generate_thumbnails: bool = True,
        extract_metadata: bool = True,
    ):
        """Initialize media configuration.





        Args:


            storage_dir: Directory for media storage


            max_file_size: Maximum file size in bytes


            thumbnail_size: Thumbnail dimensions (width, height)


            allowed_extensions: Allowed extensions by media type


            generate_thumbnails: Whether to generate thumbnails


            extract_metadata: Whether to extract metadata


        """

        self.storage_dir = Path(storage_dir)

        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.max_file_size = max_file_size

        self.thumbnail_size = thumbnail_size

        self.generate_thumbnails = generate_thumbnails

        self.extract_metadata = extract_metadata

        # Default allowed extensions

        self.allowed_extensions = allowed_extensions or {
            MediaType.IMAGE: [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
            MediaType.VIDEO: [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm"],
            MediaType.AUDIO: [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
            MediaType.DOCUMENT: [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
        }

        # Create subdirectories

        for media_type in self.allowed_extensions.keys():
            (self.storage_dir / media_type).mkdir(exist_ok=True)

            (self.storage_dir / media_type / "thumbnails").mkdir(exist_ok=True)


class MediaMetadata:
    """Metadata for media files."""

    def __init__(
        self,
        file_id: str,
        original_name: str,
        media_type: str,
        file_path: str,
        file_size: int,
        mime_type: str,
        checksum: str,
        created_at: datetime,
        thumbnail_path: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Initialize media metadata.





        Args:


            file_id: Unique file identifier


            original_name: Original filename


            media_type: Type of media (image, video, etc.)


            file_path: Path to stored file


            file_size: File size in bytes


            mime_type: MIME type of file


            checksum: File checksum


            created_at: Upload timestamp


            thumbnail_path: Path to thumbnail (if generated)


            metadata: Extracted metadata dictionary


        """

        self.file_id = file_id

        self.original_name = original_name

        self.media_type = media_type

        self.file_path = file_path

        self.file_size = file_size

        self.mime_type = mime_type

        self.checksum = checksum

        self.created_at = created_at

        self.thumbnail_path = thumbnail_path

        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""

        return {
            "file_id": self.file_id,
            "original_name": self.original_name,
            "media_type": self.media_type,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "checksum": self.checksum,
            "created_at": self.created_at.isoformat(),
            "thumbnail_path": self.thumbnail_path,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MediaMetadata":
        """Create from dictionary."""

        return cls(
            file_id=data["file_id"],
            original_name=data["original_name"],
            media_type=data["media_type"],
            file_path=data["file_path"],
            file_size=data["file_size"],
            mime_type=data["mime_type"],
            checksum=data["checksum"],
            created_at=datetime.fromisoformat(data["created_at"]),
            thumbnail_path=data.get("thumbnail_path"),
            metadata=data.get("metadata", {}),
        )


class MediaStorage:
    """Comprehensive media storage manager."""

    def __init__(self, config: MediaConfig):
        """Initialize media storage.





        Args:


            config: Media storage configuration


        """

        self.config = config

        self._metadata_store: dict[str, MediaMetadata] = {}

    def _generate_file_id(self) -> str:
        """Generate unique file ID."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        return f"media_{timestamp}"

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum."""

        hash_sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()

    def _detect_media_type(self, file_path: Path) -> str:
        """Detect media type from file extension."""

        extension = file_path.suffix.lower()

        for media_type, extensions in self.config.allowed_extensions.items():
            if extension in extensions:
                return media_type

        return MediaType.UNKNOWN

    def _validate_file(self, file_path: Path) -> tuple[bool, str]:
        """Validate uploaded file.





        Returns:


            Tuple of (is_valid, error_message)


        """

        # Check file exists

        if not file_path.exists():
            return False, "File does not exist"

        # Check file size

        file_size = file_path.stat().st_size

        if file_size > self.config.max_file_size:
            return (
                False,
                f"File too large: {file_size} bytes > {self.config.max_file_size} bytes",
            )

        # Check file extension

        media_type = self._detect_media_type(file_path)

        if media_type == MediaType.UNKNOWN:
            return False, f"Unsupported file type: {file_path.suffix}"

        return True, ""

    def _extract_metadata(self, file_path: Path, media_type: str) -> dict[str, Any]:
        """Extract metadata from media file."""

        metadata = {}

        try:
            if media_type == MediaType.IMAGE:
                metadata.update(self._extract_image_metadata(file_path))

            elif media_type == MediaType.VIDEO:
                metadata.update(self._extract_video_metadata(file_path))

            elif media_type == MediaType.AUDIO:
                metadata.update(self._extract_audio_metadata(file_path))

            elif media_type == MediaType.DOCUMENT:
                metadata.update(self._extract_document_metadata(file_path))

        except Exception as e:
            logger.warning(f"Failed to extract metadata from {file_path}: {e}")

        return metadata

    def _extract_image_metadata(self, file_path: Path) -> dict[str, Any]:
        """Extract metadata from image file."""

        metadata = {}

        try:
            # Try to use Pillow for image metadata

            try:
                from PIL import Image
                from PIL.ExifTags import TAGS

                with Image.open(file_path) as img:
                    metadata.update(
                        {
                            "width": img.width,
                            "height": img.height,
                            "format": img.format,
                            "mode": img.mode,
                        }
                    )

                    # Extract EXIF data

                    exif_dict = img.getexif()

                    if exif_dict:
                        exif_data = {}

                        for tag_id, value in exif_dict.items():
                            tag = TAGS.get(tag_id, tag_id)

                            exif_data[tag] = str(
                                value
                            )  # Convert to string for JSON serialization

                        metadata["exif"] = exif_data

            except ImportError:
                logger.warning("Pillow not available for image metadata extraction")

        except Exception as e:
            logger.error(f"Failed to extract image metadata: {e}")

        return metadata

    def _extract_video_metadata(self, file_path: Path) -> dict[str, Any]:
        """Extract metadata from video file."""

        metadata = {}

        try:
            # Basic file info

            stat = file_path.stat()

            metadata.update(
                {
                    "file_size": stat.st_size,
                    "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )

            # Note: For production, you might want to use ffmpeg-python

            # or similar library for proper video metadata extraction

        except Exception as e:
            logger.error(f"Failed to extract video metadata: {e}")

        return metadata

    def _extract_audio_metadata(self, file_path: Path) -> dict[str, Any]:
        """Extract metadata from audio file."""

        metadata = {}

        try:
            # Basic file info

            stat = file_path.stat()

            metadata.update(
                {
                    "file_size": stat.st_size,
                    "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )

            # Note: For production, you might want to use mutagen

            # or similar library for proper audio metadata extraction

        except Exception as e:
            logger.error(f"Failed to extract audio metadata: {e}")

        return metadata

    def _extract_document_metadata(self, file_path: Path) -> dict[str, Any]:
        """Extract metadata from document file."""

        metadata = {}

        try:
            # Basic file info

            stat = file_path.stat()

            metadata.update(
                {
                    "file_size": stat.st_size,
                    "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )

            # For text files, get basic info

            if file_path.suffix.lower() == ".txt":
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                    metadata.update(
                        {
                            "character_count": len(content),
                            "line_count": content.count("\n") + 1,
                            "word_count": len(content.split()),
                        }
                    )

        except Exception as e:
            logger.error(f"Failed to extract document metadata: {e}")

        return metadata

    def _generate_thumbnail(self, file_path: Path, media_type: str) -> Path | None:
        """Generate thumbnail for media file."""

        if not self.config.generate_thumbnails:
            return None

        try:
            thumbnail_dir = self.config.storage_dir / media_type / "thumbnails"

            thumbnail_path = thumbnail_dir / f"{file_path.stem}_thumb.jpg"

            if media_type == MediaType.IMAGE:
                return self._generate_image_thumbnail(file_path, thumbnail_path)

            # Note: Video and document thumbnails would require additional libraries

        except Exception as e:
            logger.error(f"Failed to generate thumbnail for {file_path}: {e}")

        return None

    def _generate_image_thumbnail(
        self, source_path: Path, thumbnail_path: Path
    ) -> Path | None:
        """Generate thumbnail for image file."""

        try:
            from PIL import Image

            with Image.open(source_path) as img:
                # Convert to RGB if necessary

                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                # Generate thumbnail

                img.thumbnail(self.config.thumbnail_size, Image.Resampling.LANCZOS)

                img.save(thumbnail_path, "JPEG", quality=85)

                return thumbnail_path

        except ImportError:
            logger.warning("Pillow not available for thumbnail generation")

        except Exception as e:
            logger.error(f"Failed to generate image thumbnail: {e}")

        return None

    def store_file(
        self,
        file_path: str | Path,
        original_name: str | None = None,
        custom_id: str | None = None,
    ) -> MediaMetadata | None:
        """Store a media file.





        Args:


            file_path: Path to file to store


            original_name: Original filename (optional)


            custom_id: Custom file ID (optional)





        Returns:


            MediaMetadata if successful, None otherwise


        """

        try:
            source_path = Path(file_path)

            # Validate file

            is_valid, error_msg = self._validate_file(source_path)

            if not is_valid:
                logger.error(f"File validation failed: {error_msg}")

                return None

            # Generate file ID and detect type

            file_id = custom_id or self._generate_file_id()

            media_type = self._detect_media_type(source_path)

            original_name = original_name or source_path.name

            # Determine storage path

            file_extension = source_path.suffix

            storage_filename = f"{file_id}{file_extension}"

            storage_path = self.config.storage_dir / media_type / storage_filename

            # Copy file to storage

            shutil.copy2(source_path, storage_path)

            # Calculate file properties

            file_size = storage_path.stat().st_size

            mime_type = (
                mimetypes.guess_type(str(storage_path))[0] or "application/octet-stream"
            )

            checksum = self._calculate_checksum(storage_path)

            # Extract metadata

            extracted_metadata = {}

            if self.config.extract_metadata:
                extracted_metadata = self._extract_metadata(storage_path, media_type)

            # Generate thumbnail

            thumbnail_path = None

            if self.config.generate_thumbnails:
                thumb_path = self._generate_thumbnail(storage_path, media_type)

                if thumb_path:
                    thumbnail_path = str(thumb_path)

            # Create metadata

            metadata = MediaMetadata(
                file_id=file_id,
                original_name=original_name,
                media_type=media_type,
                file_path=str(storage_path),
                file_size=file_size,
                mime_type=mime_type,
                checksum=checksum,
                created_at=datetime.now(),
                thumbnail_path=thumbnail_path,
                metadata=extracted_metadata,
            )

            # Store metadata

            self._metadata_store[file_id] = metadata

            logger.info(f"Stored media file: {file_id} ({original_name})")

            return metadata

        except Exception as e:
            logger.error(f"Failed to store media file {file_path}: {e}")

            return None

    def get_file(self, file_id: str) -> MediaMetadata | None:
        """Get file metadata by ID.





        Args:


            file_id: File identifier





        Returns:


            MediaMetadata if found, None otherwise


        """

        return self._metadata_store.get(file_id)

    def get_file_path(self, file_id: str) -> Path | None:
        """Get file path by ID.





        Args:


            file_id: File identifier





        Returns:


            Path to file if found, None otherwise


        """

        metadata = self.get_file(file_id)

        if metadata and Path(metadata.file_path).exists():
            return Path(metadata.file_path)

        return None

    def get_thumbnail_path(self, file_id: str) -> Path | None:
        """Get thumbnail path by file ID.





        Args:


            file_id: File identifier





        Returns:


            Path to thumbnail if found, None otherwise


        """

        metadata = self.get_file(file_id)

        if (
            metadata
            and metadata.thumbnail_path
            and Path(metadata.thumbnail_path).exists()
        ):
            return Path(metadata.thumbnail_path)

        return None

    def delete_file(self, file_id: str) -> bool:
        """Delete a stored file.





        Args:


            file_id: File identifier





        Returns:


            True if successful, False otherwise


        """

        try:
            metadata = self.get_file(file_id)

            if not metadata:
                logger.error(f"File not found: {file_id}")

                return False

            # Delete main file

            file_path = Path(metadata.file_path)

            if file_path.exists():
                file_path.unlink()

            # Delete thumbnail

            if metadata.thumbnail_path:
                thumbnail_path = Path(metadata.thumbnail_path)

                if thumbnail_path.exists():
                    thumbnail_path.unlink()

            # Remove from metadata store

            del self._metadata_store[file_id]

            logger.info(f"Deleted media file: {file_id}")

            return True

        except Exception as e:
            logger.error(f"Failed to delete file {file_id}: {e}")

            return False

    def list_files(
        self,
        media_type: str | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[MediaMetadata]:
        """List stored files.





        Args:


            media_type: Filter by media type


            limit: Maximum number of results


            offset: Number of results to skip





        Returns:


            List of MediaMetadata


        """

        results = []

        for metadata in self._metadata_store.values():
            if media_type and metadata.media_type != media_type:
                continue

            results.append(metadata)

        # Sort by creation date (newest first)

        results.sort(key=lambda x: x.created_at, reverse=True)

        # Apply pagination

        if offset > 0:
            results = results[offset:]

        if limit:
            results = results[:limit]

        return results

    def get_storage_stats(self) -> dict[str, Any]:
        """Get storage statistics.





        Returns:


            Dictionary with storage statistics


        """

        total_files = len(self._metadata_store)

        total_size = sum(m.file_size for m in self._metadata_store.values())

        # Group by media type

        by_type = {}

        for metadata in self._metadata_store.values():
            if metadata.media_type not in by_type:
                by_type[metadata.media_type] = {"count": 0, "size": 0}

            by_type[metadata.media_type]["count"] += 1

            by_type[metadata.media_type]["size"] += metadata.file_size

        return {
            "total_files": total_files,
            "total_size": total_size,
            "by_type": by_type,
            "storage_directory": str(self.config.storage_dir),
            "max_file_size": self.config.max_file_size,
        }


# Convenience functions for quick media operations


def create_media_storage(storage_dir: str | Path) -> MediaStorage:
    """Create media storage with default configuration.





    Args:


        storage_dir: Directory for media storage





    Returns:


        MediaStorage instance


    """

    config = MediaConfig(storage_dir)

    return MediaStorage(config)


def quick_store_file(
    file_path: str | Path,
    storage_dir: str | Path,
    original_name: str | None = None,
) -> MediaMetadata | None:
    """Quick file storage with minimal setup.





    Args:


        file_path: File to store


        storage_dir: Storage directory


        original_name: Original filename





    Returns:


        MediaMetadata if successful


    """

    storage = create_media_storage(storage_dir)

    return storage.store_file(file_path, original_name=original_name)
