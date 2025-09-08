"""Generic LLM provider protocol (core-only, no SDK deps).

Defines a unified interface for completion and streaming across different
LLM vendors (OpenAI, Anthropic, local models). Keep this in core so domain
services can depend on it without coupling to data/adapters.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, Protocol
import dict
import float
import list
import str


class LLMProvider(Protocol):
    """Unified interface for chat-completion style LLMs.

    Methods are async to support network-backed providers. Adapters in the
    data layer will implement these methods using vendor SDKs or HTTP.
    """

    async def complete(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> str:  # pragma: no cover - protocol
        """Return a full completion string.

        Args:
            messages: Chat messages in role/content format.
            temperature: Sampling temperature.
            tools: Optional tool-call schema for tool-augmented models.
            **kwargs: Extra provider-specific parameters.

        Returns:
            The assistant message content as a string.
        """
        ...

    async def stream(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:  # pragma: no cover - protocol
        """Yield completion chunks as strings.

        Args:
            messages: Chat messages in role/content format.
            temperature: Sampling temperature.
            tools: Optional tool-call schema.
            **kwargs: Extra provider-specific parameters.

        Yields:
            Text chunks of the assistant response.
        """
        ...
