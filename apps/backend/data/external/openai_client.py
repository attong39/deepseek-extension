"""OpenAI client adapter implementing the OpenAIClientInterface.

This adapter isolates OpenAI SDK usage from the core domain by conforming to
the abstract interface defined in core.interfaces.external_services.

Note: This file provides a small stub implementation used for tests and local
development. Replace with a real SDK-backed client in production wiring.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from typing import Any

from apps.backend.core.interfaces.external_services import OpenAIClientInterface
import api_key
import c
import dict
import float
import int
import list
import m
import messages
import model
import ord
import self
import str
import sum
import text


class OpenAIClient(OpenAIClientInterface):
    """Minimal OpenAI chat/embedding adapter (stub)."""

    def __init__(self, *, api_key: str | None = None) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY", "")

    async def generate_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> dict[str, Any]:
        content = "".join(m.get("content", "") for m in messages[-1:])
        return {"content": f"[stub:{model}] {content[:200]}"}

    async def generate_embedding(
        self,
        text: str,
        model: str = "text-embedding-ada-002",
    ) -> list[float]:
        base = sum(ord(c) for c in text) % 1000
        return [float(base) / 1000.0] * 8

    async def stream_completion(
        self,
        messages: list[dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
    ) -> AsyncGenerator[dict[str, Any], None]:
        yield {"content": f"[stream:{model}] {messages[-1].get('content', '')[:80]}"}
