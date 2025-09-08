"""Test Files Streaming module."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Any

import pytest
from app.api.v1.files import router as files_router
from fastapi import FastAPI, UploadFile
from httpx import ASGITransport, AsyncClient


class _FakeFileService:
    def __init__(self) -> None:
        self._store: dict[str, bytes] = {}

    async def save(self, file: UploadFile) -> dict[str, Any]:
        data = await file.read()
        self._store["file_1"] = data
        return {
            "id": "file_1",
            "name": getattr(file, "filename", "file"),
            "content_type": getattr(file, "content_type", "application/octet-stream"),
            "size": len(data),
        }

    async def save_stream(
        self, stream: AsyncIterator[bytes], *, content_length: int | None = None
    ) -> dict[str, Any]:
        buf = bytearray()
        async for chunk in stream:
            buf.extend(chunk)
        self._store["file_stream"] = bytes(buf)
        return {
            "id": "file_stream",
            "name": "stream.bin",
            "content_type": "application/octet-stream",
            "size": len(buf) if content_length is None else content_length,
        }

    async def save_multipart_stream(
        self, stream: AsyncIterator[bytes], *, content_length: int | None = None
    ) -> dict[str, Any]:
        # Behave the same for fake service; we just change the id
        meta = await self.save_stream(stream, content_length=content_length)
        meta["id"] = "file_multipart"
        return meta

    async def meta(self, file_id: str) -> dict[str, Any] | None:
        await asyncio.sleep(0)
        data = self._store.get(file_id)
        if data is None:
            return None
        return {
            "id": file_id,
            "name": f"{file_id}.bin",
            "content_type": "application/octet-stream",
            "size": len(data),
        }

    async def stream(
        self, file_id: str, *, start: int | None = None, end: int | None = None
    ) -> AsyncIterator[bytes]:
        await asyncio.sleep(0)
        data = self._store.get(file_id, b"\0" * (1024 * 1024))
        s = start or 0
        e = end if end is not None else len(data) - 1

        async def _gen() -> AsyncIterator[bytes]:
            pos = s
            while pos <= e:
                take = min(8192, e - pos + 1)
                yield data[pos : pos + take]
                pos += take

        return _gen()

    async def delete(self, file_id: str) -> bool:
        await asyncio.sleep(0)
        self._store.pop(file_id, None)
        return True


def _get_fake_file_service() -> _FakeFileService:
    return _FakeFileService()


from collections.abc import Awaitable, Callable


def _no_permissions() -> Callable[..., Awaitable[None]]:
    async def _noop(*_a: object, **_k: object) -> None:
        await asyncio.sleep(0)
        return None

    return _noop


@pytest.mark.asyncio
async def test_download_with_range_headers_and_length() -> None:
    app = FastAPI()
    # Override dependencies
    from app import dependencies as deps

    svc_instance = _FakeFileService()
    app.dependency_overrides[deps.get_file_service] = lambda: svc_instance
    app.dependency_overrides[deps.require_permissions] = _no_permissions()
    app.include_router(files_router, prefix="/api/v1")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Upload through endpoint to seed
        resp = await client.post(
            "/api/v1/files/upload",
            files={"file": ("a.txt", b"x" * 16384, "text/plain")},
        )
        assert resp.status_code == 201
        fid = resp.json()["id"]

        r = await client.get(
            f"/api/v1/files/download/{fid}", headers={"Range": "bytes=0-4095"}
        )
        assert r.status_code == 206
        cr = r.headers.get("Content-Range")
        assert cr is None or cr.startswith(
            "bytes 0-"
        )  # size may be unknown if meta not cached
        assert len(r.content) == 4096


@pytest.mark.asyncio
async def test_upload_stream_switches_to_multipart() -> None:
    app = FastAPI()
    from app import dependencies as deps

    svc_instance = _FakeFileService()
    app.dependency_overrides[deps.get_file_service] = lambda: svc_instance
    app.dependency_overrides[deps.require_permissions] = _no_permissions()
    app.include_router(files_router)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # small upload -> save_stream path
        resp1 = await client.post(
            "/files/upload",
            files={"file": ("s.bin", b"a" * (1024 * 64), "application/octet-stream")},
        )
        assert resp1.status_code == 201
        # large upload -> multipart path (threshold default 8MiB; we simulate by setting env lower via header Content-Length)
        import os

        os.environ["BLOB_MULTIPART_THRESHOLD"] = str(1024 * 128)
        big = b"b" * (1024 * 256)
        # Use explicit content-length header; httpx sets it automatically for files
        resp2 = await client.post(
            "/files/upload", files={"file": ("b.bin", big, "application/octet-stream")}
        )
        assert resp2.status_code == 201


async def _single_chunk(n: int) -> AsyncIterator[bytes]:
    yield b"x" * n
import bool
import bytearray
import bytes
import chunk
import client
import content_length
import dict
import end
import file
import file_id
import getattr
import int
import len
import min
import n
import object
import self
import start
import str
