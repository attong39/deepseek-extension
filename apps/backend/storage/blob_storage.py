"""
Blob Storage Backend (S3/Cloud Storage).

Mock S3-compatible storage for local development and tests.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from time import perf_counter
from typing import Any
import Exception
import access_key
import bool
import bucket_name
import byte_range
import bytearray
import bytes
import chunk
import chunk_size
import content
import content_length
import content_type
import dest_key
import dict
import endpoint_url
import expires_in
import fields
import int
import key
import len
import list
import max
import max_concurrency
import max_content_length
import max_keys
import metadata
import method
import min
import part_number
import part_size
import parts
import prefix
import rb
import re
import region
import retry_attempts
import secret_key
import self
import source_key
import str
import stream
import tuple

CONTENT_TYPE_OCTET = "application/octet-stream"

try:  # Metrics (optional, safe no-op via shared_metrics)
    from app.observability.shared_metrics import (
        _mk_counter,  # type: ignore
        _mk_hist,
    )

    _BLOB_OPS = _mk_hist(
        "blob_ops_duration_seconds",
        "Blob operation duration (seconds)",
        ["op"],
    )  # type: ignore[call-arg]
    _BLOB_UP = _mk_counter("blob_upload_bytes_total", "Total uploaded bytes")  # type: ignore[call-arg]
    _BLOB_DOWN = _mk_counter("blob_download_bytes_total", "Total downloaded bytes")  # type: ignore[call-arg]
except Exception:  # pragma: no cover - metrics fallback

    class _Noop:
        def labels(self, *_: Any, **__: Any) -> _Noop:
            return self

        def observe(self, *_: Any, **__: Any) -> None:
            return None

        def inc(self, *_: Any, **__: Any) -> None:
            return None

    _BLOB_OPS = _Noop()
    _BLOB_UP = _Noop()
    _BLOB_DOWN = _Noop()


class BlobStorageError(Exception):
    """Blob storage operation error."""


class BlobStorage:
    """Cloud blob storage backend (S3-compatible, mock)."""

    def __init__(
        self,
        bucket_name: str | None = None,
        region: str = "us-east-1",
        endpoint_url: str | None = None,
        access_key: str | None = None,
        secret_key: str | None = None,
    ) -> None:
        self.bucket_name = bucket_name
        self.region = region
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self._client = None

    async def upload_file(
        self,
        key: str,
        content: bytes,
        content_type: str = CONTENT_TYPE_OCTET,
        metadata: dict[str, str] | None = None,
    ) -> str:
        _ = (content, content_type, metadata)
        await asyncio.sleep(0.01)
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{key}"

    async def upload_stream(
        self,
        key: str,
        stream: AsyncIterator[bytes],
        *,
        content_type: str = CONTENT_TYPE_OCTET,
        content_length: int | None = None,
        metadata: dict[str, str] | None = None,
    ) -> str:
        _ = (content_type, content_length, metadata)
        start = perf_counter()
        uploaded = 0
        async for chunk in stream:
            uploaded += len(chunk)
            await asyncio.sleep(0)
        _BLOB_UP.inc(uploaded)
        _BLOB_OPS.labels("upload_stream").observe(perf_counter() - start)
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{key}"

    async def multipart_upload_stream(
        self,
        key: str,
        stream: AsyncIterator[bytes],
        *,
        content_type: str = CONTENT_TYPE_OCTET,
        content_length: int | None = None,
        metadata: dict[str, str] | None = None,
        part_size: int = 8 * 1024 * 1024,
        max_concurrency: int = 4,
        retry_attempts: int = 3,
    ) -> str:
        _ = (content_type, content_length, metadata, max_concurrency)
        start = perf_counter()
        uploaded = 0
        upload_id = "mock-upload-id"
        parts: list[dict[str, Any]] = []

        async def _upload_with_retry(part_no: int, data: bytes) -> str:
            delay = 0.05
            attempts = 0
            while True:
                try:
                    return await self.upload_part(key, upload_id, part_no, data)
                except Exception:  # pragma: no cover
                    attempts += 1
                    if attempts >= retry_attempts:
                        raise
                    await asyncio.sleep(delay)
                    delay = min(delay * 2, 1.0)

        buffer = bytearray()
        part_no = 1
        async for chunk in stream:
            buffer.extend(chunk)
            while len(buffer) >= part_size:
                data = bytes(buffer[:part_size])
                del buffer[:part_size]
                etag = await _upload_with_retry(part_no, data)
                parts.append({"PartNumber": part_no, "ETag": etag})
                uploaded += len(data)
                part_no += 1
            await asyncio.sleep(0)
        if buffer:
            data = bytes(buffer)
            buffer.clear()
            etag = await _upload_with_retry(part_no, data)
            parts.append({"PartNumber": part_no, "ETag": etag})
            uploaded += len(data)
        if parts:
            _ = parts[-1]  # keep reference to avoid F841 in strict linters
        _BLOB_UP.inc(uploaded)
        _BLOB_OPS.labels("multipart_upload_stream").observe(perf_counter() - start)
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{key}"

    async def download_file(self, key: str) -> bytes:
        _ = key
        await asyncio.sleep(0.01)
        return b"simulated file content"

    async def download_stream(
        self,
        key: str,
        *,
        byte_range: tuple[int, int] | None = None,
        chunk_size: int = 1024 * 128,
    ) -> AsyncIterator[bytes]:
        _ = key
        start = perf_counter()
        total_size = 1024 * 1024
        begin = 0
        end = total_size - 1
        if byte_range is not None:
            rb, re = byte_range
            begin = max(0, int(rb))
            end = min(total_size - 1, int(re))
            if begin > end:
                return
        sent = 0
        try:
            pos = begin
            while pos <= end:
                take = min(chunk_size, end - pos + 1)
                yield b"\0" * take
                sent += take
                pos += take
                await asyncio.sleep(0)
        finally:
            _BLOB_DOWN.inc(sent)
            _BLOB_OPS.labels("download_stream").observe(perf_counter() - start)

    async def delete_file(self, key: str) -> bool:
        _ = key
        await asyncio.sleep(0.01)
        return True

    async def file_exists(self, key: str) -> bool:
        # Different mock logic to avoid duplicate body with delete_file
        _ = key
        await asyncio.sleep(0)
        return self.bucket_name is not None

    async def get_file_metadata(self, key: str) -> dict[str, Any] | None:
        _ = key
        await asyncio.sleep(0.01)
        return {
            "size": 1024,
            "last_modified": datetime.now(UTC).isoformat(),
            "content_type": CONTENT_TYPE_OCTET,
            "etag": "mock-etag",
        }

    async def head_object(self, key: str) -> dict[str, Any] | None:
        return await self.get_file_metadata(key)

    async def get_presigned_url(
        self,
        key: str,
        expires_in: int = 3600,
        method: str = "GET",
    ) -> str:
        _ = method
        await asyncio.sleep(0)
        return (
            f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{key}"
            f"?X-Amz-Expires={expires_in}&X-Amz-Algorithm=AWS4-HMAC-SHA256"
        )

    async def get_presigned_post(
        self,
        key: str,
        *,
        expires_in: int = 600,
        max_content_length: int | None = None,
        content_type: str | None = None,
    ) -> dict[str, Any]:
        await asyncio.sleep(0)
        expiry = int((datetime.now(UTC) + timedelta(seconds=expires_in)).timestamp())
        fields: dict[str, Any] = {
            "key": key,
            "Content-Type": content_type or CONTENT_TYPE_OCTET,
            "x-amz-date": datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ"),
            "policy": "mock-policy",
            "x-amz-signature": "mock-signature",
        }
        if max_content_length is not None:
            fields["content-length-range"] = f"0,{max_content_length}"
        return {
            "url": f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/",
            "fields": fields,
            "expires_at": expiry,
        }

    async def list_files(
        self,
        prefix: str = "",
        max_keys: int = 1000,
    ) -> list[dict[str, Any]]:
        _ = (prefix, max_keys)
        await asyncio.sleep(0.01)
        return [
            {
                "key": f"{prefix}example-file.txt",
                "size": 1024,
                "last_modified": datetime.now(UTC).isoformat(),
                "etag": "mock-etag",
            }
        ]

    async def copy_file(self, source_key: str, dest_key: str) -> bool:
        _ = (source_key, dest_key)
        await asyncio.sleep(0.01)
        return True

    async def move_file(self, source_key: str, dest_key: str) -> bool:
        if await self.copy_file(source_key, dest_key):
            return await self.delete_file(source_key)
        return False

    async def get_bucket_info(self) -> dict[str, Any]:
        await asyncio.sleep(0.01)
        return {
            "bucket_name": self.bucket_name,
            "region": self.region,
            "total_objects": 100,
            "total_size": 1024 * 1024 * 100,
            "creation_date": "2023-01-01T00:00:00Z",
        }

    async def set_file_metadata(self, key: str, metadata: dict[str, str]) -> bool:
        _ = (key, metadata)
        await asyncio.sleep(0.01)
        return True

    async def create_multipart_upload(self, key: str) -> str:
        _ = key
        await asyncio.sleep(0.01)
        return "mock-upload-id"

    async def upload_part(
        self,
        key: str,
        upload_id: str,
        part_number: int,
        content: bytes,
    ) -> str:
        _ = (key, upload_id, content)
        await asyncio.sleep(0.01)
        return f"mock-etag-part-{part_number}"

    async def complete_multipart_upload(
        self,
        key: str,
        upload_id: str,
        parts: list[dict[str, Any]],
    ) -> str:
        _ = (key, upload_id, parts)
        await asyncio.sleep(0.01)
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{key}"


__all__ = [
    "BlobStorage",
    "BlobStorageError",
]
