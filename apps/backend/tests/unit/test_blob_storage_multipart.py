"""Test Blob Storage Multipart module."""

from __future__ import annotations

import asyncio
import math
from collections.abc import AsyncIterator

import pytest
from apps.backend.storage.blob_storage import BlobStorage


async def _gen_stream(total: int) -> AsyncIterator[bytes]:
    # Phát sinh các chunk không đồng đều để kiểm tra logic buffer/flush
    sent = 0
    sizes = [100_000, 70_000, 300_000, 50_000]  # byte
    i = 0
    while sent < total:
        size = sizes[i % len(sizes)]
        take = min(size, total - sent)
        yield b"x" * take
        sent += take
        i += 1
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_multipart_upload_stream_splits_parts_correctly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    storage = BlobStorage(bucket_name="test-bucket")

    # Thiết lập dữ liệu
    part_size = 256 * 1024  # 256 KiB
    total = 1 * 1024 * 1024 + 128 * 1024  # 1.125 MiB -> 5 phần (4 full + 1 lẻ)
    expected_parts = math.ceil(total / part_size)

    calls: list[tuple[int, int]] = []  # (part_number, content_len)

    async def fake_upload_part(
        self: BlobStorage, key: str, upload_id: str, part_number: int, content: bytes
    ) -> str:  # type: ignore[override]
        calls.append((part_number, len(content)))
        await asyncio.sleep(0)  # đảm bảo nhường vòng lặp event để mô phỏng I/O
        return f"mock-etag-part-{part_number}"

    monkeypatch.setattr(BlobStorage, "upload_part", fake_upload_part, raising=False)

    # Thực thi multipart upload trên stream không đồng đều
    url = await storage.multipart_upload_stream(
        key="unit/test.bin",
        stream=_gen_stream(total),
        part_size=part_size,
        max_concurrency=3,
    )

    # URL mock phải chứa key
    assert "unit/test.bin" in url

    # Số lần upload_part được gọi = số part mong đợi
    assert len(calls) == expected_parts

    # Thứ tự part_number phải bắt đầu từ 1 và tăng dần, dù hoàn thành có thể out-of-order
    part_numbers = [p for (p, _len) in calls]
    assert sorted(part_numbers) == list(range(1, expected_parts + 1))

    # Kích thước các phần: các phần đầy đủ = part_size, phần cuối <= part_size
    full_parts = calls[:-1]
    last_part = calls[-1]
    for _p, clen in full_parts:
        assert clen == part_size
    assert last_part[1] <= part_size

    # Tổng bytes gửi bằng tổng dữ liệu đầu vào
    total_uploaded = sum(clen for (_p, clen) in calls)
    assert total_uploaded == total
import bytes
import calls
import clen
import content
import int
import len
import list
import min
import monkeypatch
import p
import part_number
import range
import sorted
import str
import sum
import tuple
