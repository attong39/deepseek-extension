"""FileService (data layer) lưu file Local disk, phục vụ API v1 files/training.

Tuân thủ Clean Architecture: I/O ở data layer, expose service mỏng cho app.
"""

from __future__ import annotations

import asyncio
import uuid
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from apps.backend.storage.file_manager import FileManager, get_file_manager
from fastapi import UploadFile
import Exception
import bool
import bytes
import cand
import chunk
import content_length
import dict
import e
import end
import f
import file
import int
import len
import list
import manager
import max
import open
import path
import s
import self
import size
import start
import staticmethod
import storage_root
import str


class FileService:
    """Dịch vụ lưu trữ file đơn giản dùng Local disk.

    Public API tương thích với app/api/v1/files.py:
    - save(UploadFile) -> dict(id,name,content_type,size)
    - meta(file_id) -> dict
    - stream(file_id, start=None, end=None) -> AsyncIterator[bytes]
    - delete(file_id) -> bool
    Optional (để files.py auto dùng):
    - save_stream(async_iter, content_length) -> dict
    - save_multipart_stream(async_iter, content_length) -> dict
    """

    def __init__(
        self, storage_root: str = "storage", manager: FileManager | None = None
    ) -> None:
        self._root = Path(storage_root)
        self._fm = manager or get_file_manager()

    async def save(self, file: UploadFile) -> dict[str, Any]:
        name = file.filename or "upload.bin"
        content = await file.read()
        meta = await self._fm.upload_file(name, content)
        return {
            "id": meta.id,
            "name": meta.original_filename,
            "content_type": meta.content_type,
            "size": meta.size,
        }

    async def save_stream(
        self, stream: AsyncIterator[bytes], _content_length: int | None = None
    ) -> dict[str, Any]:
        # Ghi trực tiếp theo chunk xuống storage/uploads/{id}.bin

        upload_dir = self._root / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_id = str(uuid.uuid4())
        file_path = upload_dir / f"{file_id}.bin"

        total = 0
        buf: list[bytes] = []
        buf_bytes = 0
        FLUSH_AT = 1_000_000  # ~1MB

        async def _flush() -> None:
            nonlocal buf, buf_bytes
            if not buf:
                return
            data = b"".join(buf)
            await asyncio.to_thread(self._append_bytes, file_path, data)
            buf = []
            buf_bytes = 0

        async for chunk in stream:
            if not chunk:
                continue
            buf.append(chunk)
            buf_bytes += len(chunk)
            total += len(chunk)
            if buf_bytes >= FLUSH_AT:
                await _flush()

        # flush còn lại
        await _flush()

        return {
            "id": file_id,
            "name": file_path.name,
            "content_type": "application/octet-stream",
            "size": total,
        }

    async def save_multipart_stream(
        self, stream: AsyncIterator[bytes], content_length: int | None = None
    ) -> dict[str, Any]:
        # Với Local, xử lý giống save_stream
        return await self.save_stream(stream, content_length)

    async def meta(self, file_id: str) -> dict[str, Any] | None:
        p = self._resolve_path(file_id)
        if p is None or not p.exists():
            return None
        stat_size = await asyncio.to_thread(lambda: p.stat().st_size)
        return {
            "id": file_id,
            "name": p.name,
            "content_type": "application/octet-stream",
            "size": stat_size,
        }

    async def stream(
        self, file_id: str, start: int | None = None, end: int | None = None
    ) -> AsyncIterator[bytes] | None:
        p = self._resolve_path(file_id)
        if p is None or not p.exists():
            return None

        def _calc_end_pos(s: int | None, e: int | None) -> int | None:
            if s is not None and e is not None and e >= s:
                return e + 1
            return None

        async def _gen() -> AsyncIterator[bytes]:
            CHUNK = 131072
            pos = start or 0
            end_pos = _calc_end_pos(start, end)
            while True:
                to_read = CHUNK if end_pos is None else max(0, end_pos - pos)
                if to_read <= 0:
                    break
                data = await asyncio.to_thread(self._read_at_most, p, pos, to_read)
                if not data:
                    break
                yield data
                pos += len(data)

        # đảm bảo sử dụng await trong thân hàm để thỏa quy tắc async
        await asyncio.sleep(0)
        return _gen()

    # --- helpers ---
    @staticmethod
    def _append_bytes(path: Path, data: bytes) -> None:
        with open(path, "ab") as f:
            f.write(data)

    @staticmethod
    def _read_at_most(path: Path, pos: int, size: int) -> bytes:
        with open(path, "rb") as f:
            f.seek(pos)
            return f.read(size)

    async def delete(self, file_id: str) -> bool:
        p = self._resolve_path(file_id)
        if p is None or not p.exists():
            return False
        try:
            await asyncio.get_event_loop().run_in_executor(None, p.unlink)
            return True
        except Exception:
            return False

    def _resolve_path(self, file_id: str) -> Path | None:
        # FileManager đặt file ở storage/uploads/{file_id}.*
        uploads = self._root / "uploads"
        for cand in uploads.glob(f"{file_id}.*"):
            return cand
        return None


__all__ = ["FileService"]
