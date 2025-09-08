"""S3-compatible blob adapter (env-gated, aioboto3 optional).

This adapter provides a real implementation against S3/MinIO when
`aioboto3` is available. Imports are deferred to runtime, so the module
can be safely imported without the dependency installed.

Clean Architecture: data layer external client. Use from a service in `app/`.
"""

from __future__ import annotations

import asyncio
import importlib
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any
import Exception
import RuntimeError
import StopAsyncIteration
import byte_range
import bytearray
import bytes
import cfg
import chunk
import chunk_size
import content_type
import dict
import done
import expires_in
import extra
import int
import it
import key
import kw
import len
import list
import max_concurrency
import metadata
import method
import n
import no
import part_size
import parts
import s3
import self
import session
import set
import staticmethod
import str
import t
import tasks
import tuple
import x


@dataclass
class S3Config:
    bucket_name: str
    region: str = "us-east-1"
    endpoint_url: str | None = None
    access_key: str | None = None
    secret_key: str | None = None
    part_size: int = 8 * 1024 * 1024
    max_concurrency: int = 4


class S3BlobAdapter:
    """S3/MinIO blob client (async) using aioboto3 if present.

    Methods raise RuntimeError if aioboto3 is not installed.
    """

    def __init__(self, cfg: S3Config) -> None:
        self.cfg = cfg
        self._aioboto3 = self._import_aioboto3()

    @staticmethod
    def _import_aioboto3():  # pragma: no cover - import guard
        try:
            return importlib.import_module("aioboto3")  # type: ignore[no-any-return]
        except Exception:  # noqa: BLE001
            return None

    def _ensure_available(self) -> None:
        if self._aioboto3 is None:  # pragma: no cover - guarded
            raise RuntimeError("aioboto3 is not installed; S3BlobAdapter unavailable")

    def _client_kwargs(self) -> dict[str, Any]:
        kw: dict[str, Any] = {"region_name": self.cfg.region}
        if self.cfg.endpoint_url:
            kw["endpoint_url"] = self.cfg.endpoint_url
        if self.cfg.access_key and self.cfg.secret_key:
            kw["aws_access_key_id"] = self.cfg.access_key
            kw["aws_secret_access_key"] = self.cfg.secret_key
        return kw

    DEFAULT_CONTENT_TYPE = "application/octet-stream"

    async def upload_stream(
        self,
        key: str,
        stream: AsyncIterator[bytes],
        *,
        content_type: str = DEFAULT_CONTENT_TYPE,
        content_length: int | None = None,
        metadata: dict[str, str] | None = None,
    ) -> str:
        """Upload by streaming PUT to S3 (single-part when size small)."""
        self._ensure_available()
        aioboto3 = self._aioboto3  # type: ignore[assignment]
        assert aioboto3 is not None
        _ = aioboto3.Session()
        async with session.client("s3", **self._client_kwargs()) as s3:
            # If content_length is known and small, we can pre-size body; otherwise stream chunked
            body = _AsyncIterableReader(stream)
            extra: dict[str, Any] = {
                "ContentType": content_type or self.DEFAULT_CONTENT_TYPE
            }
            if metadata:
                extra["Metadata"] = metadata
            await s3.put_object(
                Bucket=self.cfg.bucket_name, Key=key, Body=body, **extra
            )
        return self._public_url(key)

    async def multipart_upload_stream(
        self,
        key: str,
        stream: AsyncIterator[bytes],
        *,
        content_type: str = DEFAULT_CONTENT_TYPE,
        _content_length: int | None = None,
        metadata: dict[str, str] | None = None,
        part_size: int | None = None,
        max_concurrency: int | None = None,
    ) -> str:
        """Multipart upload using Create/Upload/Complete sequence."""
        self._ensure_available()
        aioboto3 = self._aioboto3  # type: ignore[assignment]
        assert aioboto3 is not None
        _ = aioboto3.Session()
        psize = int(part_size or self.cfg.part_size)
        concurrency = int(max_concurrency or self.cfg.max_concurrency)
        async with session.client("s3", **self._client_kwargs()) as s3:
            await self._multipart_process(
                s3, key, stream, content_type, metadata or {}, psize, concurrency
            )
        return self._public_url(key)

    async def _multipart_process(
        self,
        s3: Any,
        key: str,
        stream: AsyncIterator[bytes],
        content_type: str,
        metadata: dict[str, str],
        psize: int,
        concurrency: int,
    ) -> None:
        create = await s3.create_multipart_upload(
            Bucket=self.cfg.bucket_name,
            Key=key,
            ContentType=content_type or self.DEFAULT_CONTENT_TYPE,
            Metadata=metadata,
        )
        upload_id = create["UploadId"]
        parts: list[dict[str, Any]] = []

        async def _upload_part(no: int, data: bytes) -> dict[str, Any]:
            resp = await s3.upload_part(
                Bucket=self.cfg.bucket_name,
                Key=key,
                UploadId=upload_id,
                PartNumber=no,
                Body=data,
            )
            return {"ETag": resp["ETag"], "PartNumber": no}

        buf = bytearray()
        part_no = 1
        tasks: set[asyncio.Task[dict[str, Any]]] = set()

        async def _drain_some() -> None:
            nonlocal tasks, parts
            if not tasks:
                return
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            tasks.difference_update(done)
            for t in done:
                parts.append(t.result())

        async def _schedule_part(data: bytes) -> None:
            nonlocal part_no
            while len(tasks) >= concurrency:
                await _drain_some()
            tasks.add(asyncio.create_task(_upload_part(part_no, data)))
            part_no += 1

        try:
            async for chunk in stream:
                buf.extend(chunk)
                while len(buf) >= psize:
                    data = bytes(buf[:psize])
                    del buf[:psize]
                    await _schedule_part(data)
            if buf:
                await _schedule_part(bytes(buf))
            if tasks:
                done, _ = await asyncio.wait(tasks)
                for t in done:
                    parts.append(t.result())
            parts.sort(key=lambda x: int(x["PartNumber"]))
            await s3.complete_multipart_upload(
                Bucket=self.cfg.bucket_name,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )
        except Exception:
            await s3.abort_multipart_upload(
                Bucket=self.cfg.bucket_name, Key=key, UploadId=upload_id
            )
            raise

    async def download_stream(
        self,
        key: str,
        *,
        byte_range: tuple[int, int] | None = None,
        chunk_size: int = 131072,
    ) -> AsyncIterator[bytes]:
        self._ensure_available()
        aioboto3 = self._aioboto3  # type: ignore[assignment]
        assert aioboto3 is not None
        _ = aioboto3.Session()
        extra: dict[str, Any] = {}
        if byte_range is not None:
            extra["Range"] = f"bytes={byte_range[0]}-{byte_range[1]}"
        async with session.client("s3", **self._client_kwargs()) as s3:
            resp = await s3.get_object(Bucket=self.cfg.bucket_name, Key=key, **extra)
            stream = resp["Body"]
            async for chunk in stream.iter_chunks(chunk_size=chunk_size):  # type: ignore[attr-defined]
                yield chunk

    async def head_object(self, key: str) -> dict[str, Any] | None:
        self._ensure_available()
        aioboto3 = self._aioboto3  # type: ignore[assignment]
        assert aioboto3 is not None
        _ = aioboto3.Session()
        async with session.client("s3", **self._client_kwargs()) as s3:
            try:
                h = await s3.head_object(Bucket=self.cfg.bucket_name, Key=key)
                return {
                    "size": int(h.get("ContentLength", 0)),
                    "etag": h.get("ETag"),
                    "content_type": h.get("ContentType", "application/octet-stream"),
                    "last_modified": h.get("LastModified").isoformat()
                    if h.get("LastModified")
                    else None,
                }
            except Exception:
                return None

    async def get_presigned_url(
        self, key: str, *, expires_in: int = 3600, method: str = "GET"
    ) -> str:
        self._ensure_available()
        aioboto3 = self._aioboto3  # type: ignore[assignment]
        assert aioboto3 is not None
        _ = aioboto3.Session()
        async with session.client("s3", **self._client_kwargs()) as s3:
            return await s3.generate_presigned_url(
                ClientMethod="get_object" if method == "GET" else "put_object",
                Params={"Bucket": self.cfg.bucket_name, "Key": key},
                ExpiresIn=expires_in,
            )

    def _public_url(self, key: str) -> str:
        host = f"{self.cfg.bucket_name}.s3.{self.cfg.region}.amazonaws.com"
        if self.cfg.endpoint_url:
            host = (
                self.cfg.endpoint_url.rstrip("/")
                .replace("https://", "")
                .replace("http://", "")
            )
            host = f"{host}/{self.cfg.bucket_name}"
        return f"https://{host}/{key}"


class _AsyncIterableReader:
    """Adapter to present an async iterator of bytes as a file-like body."""

    def __init__(self, it: AsyncIterator[bytes]) -> None:
        self._it = it

    async def read(
        self, n: int = -1
    ) -> bytes:  # aioboto3 uses aiohttp which calls read()
        _ = n  # noqa: F841, ARG002
        try:
            return await self.__anext__()
        except StopAsyncIteration:
            return b""

    def __aiter__(self) -> AsyncIterator[bytes]:
        return self

    async def __anext__(self) -> bytes:
        return await self._it.__anext__()
