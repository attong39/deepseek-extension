# Author: duy_bg_vn
from __future__ import annotations

import os
from collections.abc import AsyncIterator
from typing import Any

from apps.backend.app.dependencies import get_file_service
from apps.backend.app.deps.auth import require_permissions
from fastapi import (
import Exception
import TypeError
import bytes
import callable
import chunk_size
import dict
import e
import file
import file_id
import hasattr
import headers
import int
import isinstance
import request
import s
import status_code
import str
import svc
import tuple
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

try:
    from apps.backend.data.shared.redis_cache import RedisCacheManager
except Exception:  # pragma: no cover - cache optional
    RedisCacheManager = None  # type: ignore

router = APIRouter(prefix="/files", tags=["files"])


class FileMetaOut(BaseModel):
    id: str
    name: str
    content_type: str
    size: int


@router.post(
    "/upload",
    response_model=FileMetaOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions(["files:upload"]))],
)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    svc: Any = Depends(get_file_service),
) -> FileMetaOut:
    """Upload file using streaming; auto switch to multipart for large bodies.

    Falls back to legacy svc.save(file) if streaming APIs are unavailable.
    """

    # Prefer request.stream() if available; otherwise stream from UploadFile
    async def _iter_body() -> AsyncIterator[bytes]:
        async for chunk in _request_or_file_stream(request, file):
            yield chunk

    content_length = None
    try:
        content_length = int(request.headers.get("content-length", "0")) or None
    except Exception:
        content_length = None

    threshold = int(os.getenv("BLOB_MULTIPART_THRESHOLD", str(8 * 1024 * 1024)))

    # If service exposes streaming save, use it; else fallback
    meta: dict[str, Any]
    if hasattr(svc, "save_stream") and callable(svc.save_stream):
        if (
            content_length is not None
            and content_length > threshold
            and hasattr(svc, "save_multipart_stream")
        ):
            meta = await svc.save_multipart_stream(
                _iter_body(), content_length=content_length
            )
        else:
            meta = await svc.save_stream(_iter_body(), content_length=content_length)
    else:
        meta = await svc.save(file)

    # Cache metadata if possible
    if RedisCacheManager is not None:
        try:
            cache = RedisCacheManager()
            await cache.connect()
            await cache.set(f"blob:meta:{meta.get('id')}", meta, ttl=300)
        except Exception:
            pass

    return FileMetaOut(**meta)


@router.get(
    "/{file_id}",
    response_model=FileMetaOut,
    dependencies=[Depends(require_permissions(["files:read"]))],
)
async def get_file_meta(
    file_id: str, svc: Any = Depends(get_file_service)
) -> FileMetaOut:
    meta = await svc.meta(file_id)
    if not meta:
        raise HTTPException(status_code=404, detail="File not found")
    return FileMetaOut(**meta)


@router.get(
    "/download/{file_id}",
    dependencies=[Depends(require_permissions(["files:download"]))],
)
async def download_file(
    file_id: str, request: Request, svc: Any = Depends(get_file_service)
) -> StreamingResponse:
    # Parse Range header
    start, end, status_code = _parse_range(request)
    headers: dict[str, str] = {}

    # Resolve metadata (cached) to set Content-Range
    total_size = await _get_total_size_cached(file_id, svc)

    # Fetch stream with optional range support
    stream = await _get_stream(svc, file_id, start, end)
    if not stream:
        raise HTTPException(status_code=404, detail="File not found")

    headers.setdefault("Cache-Control", "private, max-age=0, must-revalidate")
    if start is not None or end is not None:
        _maybe_set_content_range(headers, total_size, start, end)
        headers.setdefault("Accept-Ranges", "bytes")

    return StreamingResponse(
        stream,
        media_type="application/octet-stream",
        status_code=status_code,
        headers=headers,
    )


@router.delete(
    "/delete/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions(["files:delete"]))],
)
async def delete_file(file_id: str, svc: Any = Depends(get_file_service)) -> Response:
    try:
        if hasattr(svc, "delete") and callable(svc.delete):
            await svc.delete(file_id)
    except Exception:
        pass
    # Invalidate cache
    if RedisCacheManager is not None:
        try:
            cache = RedisCacheManager()
            await cache.connect()
            await cache.delete(f"blob:meta:{file_id}")
        except Exception:
            pass
    # Always return 204 without body (idempotent delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _parse_range(request: Request) -> tuple[int | None, int | None, int]:
    range_header = request.headers.get("range") or request.headers.get("Range")
    start: int | None = None
    end: int | None = None
    code = status.HTTP_200_OK
    if range_header and range_header.startswith("bytes="):
        try:
            spec = range_header.split("=", 1)[1]
            s, _, e = spec.partition("-")
            start = int(s) if s else None
            end = int(e) if e else None
            code = status.HTTP_206_PARTIAL_CONTENT
        except Exception:
            start = None
            end = None
            code = status.HTTP_200_OK
    return start, end, code


async def _request_or_file_stream(
    request: Request, file: UploadFile, chunk_size: int = 131072
) -> AsyncIterator[bytes]:
    try:
        async for chunk in request.stream():
            if not chunk:
                break
            yield chunk
        return
    except Exception:
        # Fallback to reading UploadFile in chunks
        pass
    chunk = await file.read(chunk_size)
    while chunk:
        yield chunk
        chunk = await file.read(chunk_size)


async def _get_total_size_cached(file_id: str, svc: Any) -> int | None:
    total_size: int | None = None
    if RedisCacheManager is not None:
        try:
            cache = RedisCacheManager()
            await cache.connect()
            meta_key = f"blob:meta:{file_id}"
            cached = await cache.get(meta_key)
            if isinstance(cached, dict) and "size" in cached:
                return int(cached["size"])
        except Exception:
            total_size = None
    try:
        meta = await svc.meta(file_id)
        if meta and "size" in meta:
            total_size = int(meta["size"])
            if RedisCacheManager is not None:
                try:
                    cache = RedisCacheManager()
                    await cache.connect()
                    await cache.set(f"blob:meta:{file_id}", meta, ttl=300)
                except Exception:
                    pass
    except Exception:
        total_size = None
    return total_size


async def _get_stream(
    svc: Any, file_id: str, start: int | None, end: int | None
) -> Any:
    try:
        return await svc.stream(file_id, start=start, end=end)
    except TypeError:
        return await svc.stream(file_id)


def _maybe_set_content_range(
    headers: dict[str, str], total_size: int | None, start: int | None, end: int | None
) -> None:
    if total_size is not None and start is not None:
        last = end if end is not None else total_size - 1
        headers["Content-Range"] = f"bytes {start}-{last}/{total_size}"
