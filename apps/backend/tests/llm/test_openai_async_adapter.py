"""Test Openai Async Adapter module."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from apps.backend.data.external.llm.openai_async_adapter import OpenAIAsyncAdapter


class DummyClient:
    def __init__(self):
        self.calls: list[tuple[str, dict]] = []
        self.mode: str = "complete"  # or "stream", "stream_error"

    async def chat_completion(self, messages, model=None, *, stream=False, opts=None):
        self.calls.append(("chat_completion", {"stream": stream, "opts": opts or {}}))
        if stream:
            if self.mode == "stream_error":
                raise RuntimeError("stream failed")

            async def gen():
                # yield 3 chunks with incremental deltas
                for delta in ["Hello", " ", "world"]:
                    yield SimpleNamespace(
                        choices=[SimpleNamespace(delta=SimpleNamespace(content=delta))]
                    )

            return gen()
        # Non-stream: ensure async context by awaiting a no-op
        import asyncio

        await asyncio.sleep(0)
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="OK CONTENT"))]
        )


@pytest.mark.asyncio
async def test_complete_returns_content():
    client = DummyClient()
    client.mode = "complete"
    adapter = OpenAIAsyncAdapter(client)  # type: ignore[arg-type]

    out = await adapter.complete(messages=[])
    assert out == "OK CONTENT"
    # Ensure non-stream path used
    assert client.calls and client.calls[-1][1]["stream"] is False


@pytest.mark.asyncio
async def test_stream_yields_deltas_in_order():
    client = DummyClient()
    client.mode = "stream"
    adapter = OpenAIAsyncAdapter(client)  # type: ignore[arg-type]

    chunks = []
    async for part in adapter.stream(messages=[]):
        chunks.append(part)
    assert "".join(chunks) == "Hello world"
    assert client.calls and client.calls[-1][1]["stream"] is True


@pytest.mark.asyncio
async def test_stream_fallback_to_complete_on_error():
    client = DummyClient()
    client.mode = "stream_error"
    adapter = OpenAIAsyncAdapter(client)  # type: ignore[arg-type]

    parts = []
    async for part in adapter.stream(messages=[]):
        parts.append(part)
    # Fallback returns the complete() content
    assert parts == ["OK CONTENT"]
    # Last call should be non-stream after fallback
    assert client.calls and client.calls[-1][1]["stream"] is False
import RuntimeError
import delta
import dict
import list
import opts
import part
import self
import str
import stream
import tuple
