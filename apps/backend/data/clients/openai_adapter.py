"""OpenAI LLM adapter (SDK-first) with HTTP fallback.

Implements the core LLMProvider protocol using the official OpenAI Python SDK
and falls back to HTTP streaming when the SDK path fails (network/SDK issues).

Notes:
- This module resides in the data layer and depends on the core interface only.
- It requires the optional "llm" extra (openai) to be installed to use SDK.
  HTTP fallback still needs a compatible API endpoint (OpenAI-style).
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from collections.abc import AsyncIterator
from typing import Any, cast

import httpx
from apps.backend.core.interfaces.llm_provider import LLMProvider
from openai import AsyncOpenAI
import Exception
import api_key
import base_url
import chunk
import dict
import exc
import float
import getattr
import int
import kwargs
import line
import list
import messages
import min
import model
import path
import payload
import self
import str
import stream_any
import temperature
import timeout
import tok
import tools

logger = logging.getLogger(__name__)


class OpenAIAdapter(LLMProvider):
    """OpenAI-backed LLM adapter implementing LLMProvider.

    Prefers the official SDK and falls back to HTTP for resilience.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 30,
    ) -> None:
        """Initialize the adapter.

        Args:
            api_key: OpenAI API key (defaults to env OPENAI_API_KEY).
            base_url: API base URL (defaults to env OPENAI_BASE_URL or official).
            model: Default model (defaults to env OPENAI_MODEL or "gpt-4o").
            timeout: Timeout in seconds for both SDK and HTTP client.
        """

        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.base_url = base_url or os.environ.get(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o")
        self.timeout = timeout

        if not self.api_key:
            logger.warning(
                "OpenAIAdapter initialized without API key; calls will fail."
            )

        # SDK client
        self._sdk = AsyncOpenAI(
            api_key=self.api_key, base_url=self.base_url, timeout=timeout
        )

        # HTTP fallback client (tuned)
        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            limits=httpx.Limits(
                max_connections=128, max_keepalive_connections=64, keepalive_expiry=15.0
            ),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

    # --------------------- SDK (preferred) ---------------------
    async def complete(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> str:
        try:
            # Casts silence strict type checks against openai SDK typed params.
            resp = await self._sdk.chat.completions.create(
                model=self.model,
                messages=cast(Any, messages),  # type: ignore[arg-type]
                temperature=temperature,
                tools=cast(Any, tools),  # type: ignore[arg-type]
                **kwargs,
            )
            content = resp.choices[0].message.content
            return content or ""
        except Exception as exc:  # pragma: no cover - resilience path
            logger.warning("OpenAI SDK complete failed; falling back to HTTP: %s", exc)
            return await self._complete_http(
                messages, temperature=temperature, tools=tools, **kwargs
            )

    async def stream(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        try:
            stream_any: Any = await self._sdk.chat.completions.create(
                model=self.model,
                messages=cast(Any, messages),  # type: ignore[arg-type]
                temperature=temperature,
                tools=cast(Any, tools),  # type: ignore[arg-type]
                stream=True,
                **kwargs,
            )
            async for chunk in stream_any:  # type: ignore[assignment]
                try:
                    delta = chunk.choices[0].delta  # type: ignore[attr-defined]
                    content = getattr(delta, "content", None)
                    if content:
                        yield content
                except Exception:  # pragma: no cover - defensive
                    continue
        except Exception as exc:  # pragma: no cover - resilience path
            logger.warning("OpenAI SDK stream failed; falling back to HTTP: %s", exc)
            async for tok in self._stream_http(
                messages, temperature=temperature, tools=tools, **kwargs
            ):
                yield tok

    # --------------------- HTTP fallback ---------------------
    async def _complete_http(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            payload["tools"] = tools
        r = await self._http_post_with_retries("/chat/completions", json=payload)
        j: dict[str, Any] = r.json()
        return j["choices"][0]["message"].get("content") or ""

    async def _stream_http(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        if tools:
            payload["tools"] = tools

        attempt = 0
        while True:
            try:
                async with self._http.stream(
                    "POST", "/chat/completions", json=payload
                ) as r:
                    if r.status_code in (429,) or r.status_code >= 500:
                        raise httpx.HTTPStatusError(
                            "retryable", request=r.request, response=r
                        )
                    r.raise_for_status()
                    async for line in r.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        data = line.removeprefix("data:").strip()
                        if data in ("[DONE]", "\n", ""):
                            if data == "[DONE]":
                                break
                            continue
                        try:
                            j = json.loads(data)
                            delta = j["choices"][0]["delta"].get("content")
                            if delta:
                                yield delta
                        except Exception:  # pragma: no cover - lenient parsing
                            continue
                break
            except httpx.HTTPError:
                attempt += 1
                if attempt >= 3:
                    break
                await asyncio.sleep(min(2**attempt, 5))

    async def _http_post_with_retries(
        self, path: str, *, json: dict[str, Any]
    ) -> httpx.Response:
        attempt = 0
        while True:
            try:
                r = await self._http.post(path, json=json)
                if r.status_code in (429,) or r.status_code >= 500:
                    raise httpx.HTTPStatusError(
                        "retryable", request=r.request, response=r
                    )
                r.raise_for_status()
                return r
            except httpx.HTTPError as exc:
                attempt += 1
                if attempt >= 3:
                    raise exc
                await asyncio.sleep(min(2**attempt, 5))

    async def aclose(self) -> None:
        """Close underlying clients."""
        await asyncio.gather(self._http.aclose(), self._sdk.close())
