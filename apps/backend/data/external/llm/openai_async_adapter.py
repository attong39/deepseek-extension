"""Async OpenAI adapter to unify complete and stream operations.

Provides a thin facade over EnhancedOpenAIClient with simple stream and
fallback behaviors to standardize the API for callers.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any, cast
import Exception
import chunk
import classmethod
import client
import cls
import dict
import estimated_prompt_tokens
import float
import functions
import getattr
import int
import isinstance
import kwargs
import list
import max_tokens
import messages
import model
import opts
import self
import str
import temperature
import tools

try:
    from openai.types.chat import ChatCompletion  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    from typing import Any

    ChatCompletion = Any

from apps.backend.data.external.llm.enhanced_openai_client import (
    ChatMessage,
    EnhancedOpenAIClient,
    FunctionDefinition,
    OpenAIConfig,
)


class OpenAIAsyncAdapter:
    """Async adapter exposing unified complete/stream methods."""

    def __init__(self, client: EnhancedOpenAIClient):
        self.client = client

    @classmethod
    def from_settings(cls) -> OpenAIAsyncAdapter:
        from apps.backend.config.ml_config import get_ml_settings

        ml = get_ml_settings()
        cfg = OpenAIConfig(
            api_key=ml.openai_api_key or "",
            organization=ml.openai_organization,
            base_url=ml.openai_base_url,
            max_retries=ml.openai_max_retries,
            timeout=float(ml.openai_timeout),
            default_model=ml.default_chat_model,
            default_embedding_model=ml.default_embedding_model,
            use_long_context=True,
            long_context_model=ml.long_context_model,
        )
        return cls(EnhancedOpenAIClient(cfg))

    async def complete(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        functions: list[FunctionDefinition] | None = None,
        tools: list[dict[str, Any]] | None = None,
        estimated_prompt_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        """Return full text completion string."""
        opts: dict[str, Any] = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "functions": functions,
            "tools": tools,
            "estimated_prompt_tokens": estimated_prompt_tokens,
            **kwargs,
        }
        resp = cast(
            ChatCompletion,
            await self.client.chat_completion(
                messages,
                model=model,
                stream=False,
                opts=opts,
            ),
        )
        # Extract content
        # Type: ChatCompletion
        return getattr(resp.choices[0].message, "content", "") or ""

    async def stream(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        functions: list[FunctionDefinition] | None = None,
        tools: list[dict[str, Any]] | None = None,
        estimated_prompt_tokens: int | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """Yield text deltas as they arrive; fallback to non-stream if needed."""
        try:
            opts: dict[str, Any] = {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "functions": functions,
                "tools": tools,
                "estimated_prompt_tokens": estimated_prompt_tokens,
                **kwargs,
            }
            gen = await self.client.chat_completion(
                messages,
                model=model,
                stream=True,
                opts=opts,
            )
            assert isinstance(gen, AsyncGenerator)
            async for chunk in gen:
                try:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        yield delta
                except Exception:
                    continue
            return
        except Exception:
            # Fallback to non-streaming
            content = await self.complete(
                messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                functions=functions,
                tools=tools,
                estimated_prompt_tokens=estimated_prompt_tokens,
                **kwargs,
            )
            if content:
                yield content
