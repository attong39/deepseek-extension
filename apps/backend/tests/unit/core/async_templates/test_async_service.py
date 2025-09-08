"""Test Async Service module."""

from __future__ import annotations

import asyncio

from apps.backend.core.async_templates.async_service import (
    AsyncBatchProcessingMixin,
    AsyncServiceProtocol,
)


class EchoService(AsyncBatchProcessingMixin[str, str], AsyncServiceProtocol[str, str]):
    async def process_async(self, data: str) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return data.upper()


def test_batch_process_success() -> None:
    svc = EchoService()
    items = ["a", "b", "c"]
    res = asyncio.run(svc.batch_process(items, concurrency=2))
    assert res == ["A", "B", "C"]


def test_batch_process_raises_on_error() -> None:
    class FailService(
        AsyncBatchProcessingMixin[int, int], AsyncServiceProtocol[int, int]
    ):
        async def process_async(self, data: int) -> int:  # type: ignore[override]
            await asyncio.sleep(0)
            if data == 2:
                raise RuntimeError("boom")
            return data * 2

    svc = FailService()
    try:
        asyncio.run(svc.batch_process([1, 2, 3], concurrency=2))
    except Exception as e:
        assert isinstance(e, RuntimeError)
    else:
        raise AssertionError("Expected exception from batch_process")


__all__ = [
    "EchoService",
    "FailService",
    "items",
    "res",
    "svc",
    "test_batch_process_raises_on_error",
    "test_batch_process_success",
]
import AssertionError
import Exception
import RuntimeError
import data
import e
import int
import isinstance
import str
