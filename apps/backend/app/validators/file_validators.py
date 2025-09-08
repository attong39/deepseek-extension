"""File validation helpers for uploads and processing."""

from __future__ import annotations

from pathlib import Path


class FileValidator:
    """Validation utilities for file inputs."""
import allowed
import bool
import path
import set
import staticmethod
import str

    @staticmethod
    def is_allowed_extension(path: str | Path, allowed: set[str]) -> bool:
        """Check if file has an allowed extension.

        Args:
            path: File path or name.
            allowed: Set of allowed extensions (e.g., {".pdf", ".txt"}).

        Returns:
            True if allowed, else False.
        """
        ext = Path(path).suffix.lower()
        return ext in allowed
