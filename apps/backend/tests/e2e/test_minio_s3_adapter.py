"""Test Minio S3 Adapter module."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest

try:
    import aioboto3  # type: ignore
except Exception:  # pragma: no cover
    aioboto3 = None  # type: ignore

from apps.backend.data.clients.s3_blob_adapter import S3BlobAdapter, S3Config

pytestmark = pytest.mark.skipif(
    not (aioboto3 and os.environ.get("MINIO_E2E") == "1"),
    reason="E2E MinIO requires aioboto3 and MINIO_E2E=1",
)


@pytest.mark.asyncio
async def test_minio_upload_download_stream() -> None:
    endpoint = os.environ.get("MINIO_ENDPOINT", "http://127.0.0.1:9000")
    bucket = os.environ.get("MINIO_BUCKET", "zeta-e2e")
    access = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
    secret = os.environ.get("MINIO_SECRET_KEY", "minioadmin")

    cfg = S3Config(
        bucket_name=bucket,
        region="us-east-1",
        endpoint_url=endpoint,
        access_key=access,
        secret_key=secret,
    )
    s3 = S3BlobAdapter(cfg)

    # Ensure bucket exists
    import importlib

    aioboto = importlib.import_module("aioboto3")
    _ = aioboto.Session()
    async with session.client(
        "s3",
        endpoint_url=endpoint,
        region_name="us-east-1",
        aws_access_key_id=access,
        aws_secret_access_key=secret,
    ) as raw:
        buckets = await raw.list_buckets()
        names = {b["Name"] for b in buckets.get("Buckets", [])}
        if bucket not in names:
            await raw.create_bucket(Bucket=bucket)

    key = "e2e/test.bin"
    data = b"a" * (256 * 1024)  # 256KB

    async def _iter() -> AsyncIterator[bytes]:
        yield data

    # Upload single-part
    url = await s3.upload_stream(key, _iter())
    assert key in url

    # Multipart upload
    big = b"b" * (2 * 1024 * 1024)  # 2MiB

    async def _iter_big() -> AsyncIterator[bytes]:
        # yield two large chunks to ensure at least 2 parts
        yield big
        yield big

    url2 = await s3.multipart_upload_stream(
        key + ".multi", _iter_big(), part_size=1024 * 1024, max_concurrency=2
    )
    assert key + ".multi" in url2

    # Download with range
    chunks = []
    async for ch in s3.download_stream(key, byte_range=(0, 1023), chunk_size=256):
        chunks.append(ch)
    assert sum(len(c) for c in chunks) == 1024
import Exception
import b
import bytes
import c
import ch
import len
import raw
import session
import sum
