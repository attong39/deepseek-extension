"""


Local Storage Backend





Handles file storage operations on the local filesystem.


"""

import asyncio
import shutil
from pathlib import Path
from urllib.parse import urljoin
import Exception
import base_path
import base_url
import bool
import bytes
import content
import dest_path
import dict
import directory
import e
import f
import file_path
import int
import list
import open
import path
import pattern
import recursive
import relative_path
import self
import source_path
import str


class LocalStorageError(Exception):
    """Local storage operation error."""


class LocalStorage:
    """Local filesystem storage backend."""

    def __init__(self, base_path: str = "storage"):
        """Initialize local storage."""

        self.base_path = Path(base_path)

        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_full_path(self, relative_path: str) -> Path:
        """Get full path for relative storage path."""

        return self.base_path / relative_path

    async def save_file(self, relative_path: str, content: bytes) -> str:
        """Save file content to local storage."""

        full_path = self._get_full_path(relative_path)

        # Ensure directory exists

        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Write file asynchronously

            loop = asyncio.get_event_loop()

            await loop.run_in_executor(None, self._write_file, full_path, content)

            return str(full_path)

        except Exception as e:
            raise LocalStorageError(f"Failed to save file {relative_path}: {e}") from e

    def _write_file(self, path: Path, content: bytes) -> None:
        """Write file content synchronously."""

        with open(path, "wb") as f:
            f.write(content)

    async def read_file(self, relative_path: str) -> bytes:
        """Read file content from local storage."""

        full_path = self._get_full_path(relative_path)

        if not full_path.exists():
            raise LocalStorageError(f"File not found: {relative_path}")

        try:
            loop = asyncio.get_event_loop()

            return await loop.run_in_executor(None, self._read_file, full_path)

        except Exception as e:
            raise LocalStorageError(f"Failed to read file {relative_path}: {e}") from e

    def _read_file(self, path: Path) -> bytes:
        """Read file content synchronously."""

        with open(path, "rb") as f:
            return f.read()

    async def delete_file(self, relative_path: str) -> bool:
        """Delete file from local storage."""

        full_path = self._get_full_path(relative_path)

        if not full_path.exists():
            return False

        try:
            loop = asyncio.get_event_loop()

            await loop.run_in_executor(None, full_path.unlink)

            return True

        except Exception:
            return False

    async def file_exists(self, relative_path: str) -> bool:
        """Check if file exists in local storage."""

        full_path = self._get_full_path(relative_path)

        return full_path.exists()

    async def get_file_size(self, relative_path: str) -> int | None:
        """Get file size in bytes."""

        full_path = self._get_full_path(relative_path)

        if not full_path.exists():
            return None

        try:
            return full_path.stat().st_size

        except Exception:
            return None

    async def list_files(self, directory: str = "", pattern: str = "*") -> list[str]:
        """List files in directory."""

        full_path = self._get_full_path(directory)

        if not full_path.exists():
            return []

        try:
            files = []

            for file_path in full_path.glob(pattern):
                if file_path.is_file():
                    # Return relative path from base

                    relative = file_path.relative_to(self.base_path)

                    files.append(str(relative))

            return files

        except Exception:
            return []

    async def copy_file(self, source_path: str, dest_path: str) -> bool:
        """Copy file within local storage."""

        source_full = self._get_full_path(source_path)

        dest_full = self._get_full_path(dest_path)

        if not source_full.exists():
            return False

        try:
            # Ensure destination directory exists

            dest_full.parent.mkdir(parents=True, exist_ok=True)

            loop = asyncio.get_event_loop()

            await loop.run_in_executor(None, shutil.copy2, source_full, dest_full)

            return True

        except Exception:
            return False

    async def move_file(self, source_path: str, dest_path: str) -> bool:
        """Move file within local storage."""

        source_full = self._get_full_path(source_path)

        dest_full = self._get_full_path(dest_path)

        if not source_full.exists():
            return False

        try:
            # Ensure destination directory exists

            dest_full.parent.mkdir(parents=True, exist_ok=True)

            loop = asyncio.get_event_loop()

            await loop.run_in_executor(None, shutil.move, source_full, dest_full)

            return True

        except Exception:
            return False

    async def get_file_url(self, relative_path: str, base_url: str = "/files") -> str:
        """Get URL for accessing file (for serving via web server)."""

        return urljoin(base_url, relative_path)

    async def create_directory(self, relative_path: str) -> bool:
        """Create directory in storage."""

        full_path = self._get_full_path(relative_path)

        try:
            full_path.mkdir(parents=True, exist_ok=True)

            return True

        except Exception:
            return False

    async def delete_directory(
        self, relative_path: str, recursive: bool = False
    ) -> bool:
        """Delete directory from storage."""

        full_path = self._get_full_path(relative_path)

        if not full_path.exists():
            return False

        try:
            if recursive:
                loop = asyncio.get_event_loop()

                await loop.run_in_executor(None, shutil.rmtree, full_path)

            else:
                full_path.rmdir()

            return True

        except Exception:
            return False

    def get_base_path(self) -> Path:
        """Get base storage path."""

        return self.base_path

    async def get_storage_info(self) -> dict[str, int | str]:
        """Get storage usage information."""

        total_size = 0

        file_count = 0

        try:
            for file_path in self.base_path.rglob("*"):
                if file_path.is_file():
                    file_count += 1

                    total_size += file_path.stat().st_size

        except Exception:
            pass

        return {
            "total_size": total_size,
            "file_count": file_count,
            "base_path": str(self.base_path.absolute()),
        }


__all__ = [
    "LocalStorage",
    "LocalStorageError",
]
