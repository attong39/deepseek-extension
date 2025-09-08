"""Storage configuration for ZETA AI system.

This module provides storage settings for file management,
cloud storage, and data persistence.
"""

from __future__ import annotations

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import bool
import ext
import int
import isinstance
import list
import size
import str
import v


class StorageSettings(BaseSettings):
    """Storage configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Local Storage
    local_storage_enabled: bool = Field(default=True)
    upload_directory: str = Field(default="storage/uploads")
    temp_directory: str = Field(default="storage/temp")
    cache_directory: str = Field(default="storage/cache")
    log_directory: str = Field(default="storage/logs")
    backup_directory: str = Field(default="storage/backups")
    export_directory: str = Field(default="storage/exports")

    # File Upload Settings
    max_file_size: int = Field(default=52428800)  # 50MB
    max_total_size: int = Field(default=1073741824)  # 1GB
    allowed_extensions: list[str] = Field(
        default=[
            ".txt",
            ".md",
            ".pdf",
            ".doc",
            ".docx",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".svg",
            ".mp3",
            ".wav",
            ".mp4",
            ".avi",
            ".mov",
            ".json",
            ".csv",
            ".xml",
            ".yaml",
            ".yml",
        ]
    )

    # Cloud Storage
    cloud_storage_enabled: bool = Field(default=False)
    cloud_storage_provider: str = Field(default="aws")  # aws, gcp, azure

    # AWS S3 Configuration
    aws_access_key_id: str | None = Field(default=None)
    aws_secret_access_key: str | None = Field(default=None)
    aws_region: str = Field(default="us-east-1")
    aws_bucket_name: str | None = Field(default=None)
    aws_endpoint_url: str | None = Field(default=None)  # For S3-compatible services

    # Google Cloud Storage Configuration
    gcp_project_id: str | None = Field(default=None)
    gcp_bucket_name: str | None = Field(default=None)
    gcp_credentials_path: str | None = Field(default=None)

    # Azure Blob Storage Configuration
    azure_account_name: str | None = Field(default=None)
    azure_account_key: str | None = Field(default=None)
    azure_container_name: str | None = Field(default=None)
    azure_connection_string: str | None = Field(default=None)

    # File Processing
    enable_virus_scanning: bool = Field(default=True)
    enable_content_analysis: bool = Field(default=True)
    enable_thumbnail_generation: bool = Field(default=True)
    enable_metadata_extraction: bool = Field(default=True)

    # Image Processing
    image_quality: int = Field(default=85)
    max_image_width: int = Field(default=2048)
    max_image_height: int = Field(default=2048)
    thumbnail_sizes: list[int] = Field(default=[150, 300, 600])

    # Video Processing
    max_video_duration: int = Field(default=3600)  # 1 hour in seconds
    video_compression_quality: str = Field(default="medium")  # low, medium, high
    enable_video_transcoding: bool = Field(default=False)

    # Audio Processing
    max_audio_duration: int = Field(default=1800)  # 30 minutes in seconds
    audio_quality: str = Field(default="medium")  # low, medium, high
    enable_audio_transcription: bool = Field(default=True)

    # Document Processing
    enable_ocr: bool = Field(default=True)
    enable_text_extraction: bool = Field(default=True)
    enable_document_preview: bool = Field(default=True)

    # Cleanup and Maintenance
    temp_file_cleanup_interval: int = Field(default=3600)  # 1 hour
    temp_file_max_age: int = Field(default=86400)  # 24 hours
    cache_cleanup_interval: int = Field(default=7200)  # 2 hours
    cache_max_size: int = Field(default=1073741824)  # 1GB

    # Backup Configuration
    enable_automatic_backup: bool = Field(default=True)
    backup_interval: int = Field(default=86400)  # Daily
    backup_retention_days: int = Field(default=30)
    backup_compression: bool = Field(default=True)

    # Security
    enable_encryption_at_rest: bool = Field(default=True)
    encryption_key: str | None = Field(default=None)
    enable_access_logging: bool = Field(default=True)
    signed_url_expiry: int = Field(default=3600)  # 1 hour

    # CDN Configuration
    cdn_enabled: bool = Field(default=False)
    cdn_provider: str = Field(default="cloudflare")  # cloudflare, aws, gcp
    cdn_base_url: str | None = Field(default=None)
    cdn_cache_ttl: int = Field(default=86400)  # 24 hours

    # Performance
    enable_caching: bool = Field(default=True)
    cache_max_age: int = Field(default=3600)  # 1 hour
    enable_compression: bool = Field(default=True)
    compression_algorithm: str = Field(default="gzip")  # gzip, brotli

    @validator("allowed_extensions", pre=True)
    def parse_allowed_extensions(cls, v):
        """Parse allowed extensions from string or list."""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",") if ext.strip()]
        return v

    @validator("thumbnail_sizes", pre=True)
    def parse_thumbnail_sizes(cls, v):
        """Parse thumbnail sizes from string or list."""
        if isinstance(v, str):
            return [
                int(size.strip()) for size in v.split(",") if size.strip().isdigit()
            ]
        return v


def get_storage_settings() -> StorageSettings:
    """Get storage settings instance."""
    return StorageSettings()


# Storage Provider Constants
class StorageProvider:
    """Storage provider constants."""

    LOCAL = "local"
    AWS_S3 = "aws"
    GOOGLE_CLOUD = "gcp"
    AZURE_BLOB = "azure"
    MINIO = "minio"


# File Type Categories
class FileCategory:
    """File category constants."""

    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"
    CODE = "code"
    DATA = "data"


# File Extensions by Category
FILE_EXTENSIONS = {
    FileCategory.DOCUMENT: [
        ".txt",
        ".md",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".rtf",
        ".odt",
        ".ods",
        ".odp",
    ],
    FileCategory.IMAGE: [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".svg",
        ".webp",
        ".tiff",
        ".ico",
        ".heic",
        ".heif",
    ],
    FileCategory.VIDEO: [
        ".mp4",
        ".avi",
        ".mov",
        ".wmv",
        ".flv",
        ".webm",
        ".mkv",
        ".m4v",
        ".3gp",
        ".ogv",
    ],
    FileCategory.AUDIO: [
        ".mp3",
        ".wav",
        ".flac",
        ".aac",
        ".ogg",
        ".wma",
        ".m4a",
        ".opus",
        ".amr",
    ],
    FileCategory.ARCHIVE: [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    FileCategory.CODE: [
        ".py",
        ".js",
        ".html",
        ".css",
        ".java",
        ".cpp",
        ".c",
        ".php",
        ".rb",
        ".go",
        ".rs",
        ".swift",
        ".kt",
    ],
    FileCategory.DATA: [".json", ".xml", ".csv", ".yaml", ".yml", ".sql", ".db"],
}

# MIME Types
MIME_TYPES = {
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".json": "application/json",
    ".xml": "application/xml",
    ".csv": "text/csv",
    ".yaml": "application/x-yaml",
    ".yml": "application/x-yaml",
}


# Storage Paths
class StoragePath:
    """Storage path constants."""

    UPLOADS = "uploads"
    TEMP = "temp"
    CACHE = "cache"
    LOGS = "logs"
    BACKUPS = "backups"
    EXPORTS = "exports"
    THUMBNAILS = "thumbnails"
    PROCESSED = "processed"


# File Processing Status
class ProcessingStatus:
    """File processing status constants."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Default Storage Policies
STORAGE_POLICIES = {
    "default": {
        "max_file_size": 52428800,  # 50MB
        "allowed_extensions": [".txt", ".md", ".pdf", ".jpg", ".png"],
        "virus_scan": True,
        "auto_delete_days": 30,
    },
    "documents": {
        "max_file_size": 104857600,  # 100MB
        "allowed_extensions": [".txt", ".md", ".pdf", ".doc", ".docx"],
        "ocr_enabled": True,
        "auto_delete_days": 365,
    },
    "images": {
        "max_file_size": 20971520,  # 20MB
        "allowed_extensions": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "thumbnail_generation": True,
        "auto_delete_days": 90,
    },
    "videos": {
        "max_file_size": 1073741824,  # 1GB
        "allowed_extensions": [".mp4", ".avi", ".mov", ".webm"],
        "transcoding": True,
        "auto_delete_days": 30,
    },
}
