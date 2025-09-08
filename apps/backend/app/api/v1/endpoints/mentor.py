"""Mentor module."""

from __future__ import annotations

from collections.abc import AsyncIterator
from time import perf_counter
from typing import Any

from app.dependencies import get_llm
from app.deps.auth import require_permissions
from app.observability.shared_metrics import (
    api_request_duration_seconds,
    llm_tokens_consumed_total,
)
from apps.backend.core.interfaces.llm_provider import LLMProvider
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

router = APIRouter(prefix="/mentor", tags=["mentor"])


class MentorIn(BaseModel):
    role: str = Field("teacher", description="teacher|coach|reviewer")
    objective: str
    context: str | None = None
    messages: list[dict[str, str]] = Field(default_factory=list)
    temperature: float = 0.2
    tools: list[dict[str, Any]] | None = None


class MentorOut(BaseModel):
    content: str


# We expose LLM directly for generic mentor usage; DI currently returns a trainer.
# Provide a lightweight get_llm dependency for this router.
# DI comes from app.dependencies


@router.post(
    "/guide",
    response_model=MentorOut,
    dependencies=[Depends(require_permissions(["mentor:guide", "llm:use"]))],
)
async def guide(payload: MentorIn, llm: LLMProvider = Depends(get_llm)) -> MentorOut:
    _t0 = perf_counter()
    sys = f"You are a {payload.role}. Help the user achieve the objective. Be structured and actionable."
    messages = [{"role": "system", "content": sys}]
    if payload.context:
        messages.append({"role": "system", "content": f"Context:\n{payload.context}"})
    messages += payload.messages
    content = await llm.complete(
        messages, temperature=payload.temperature, tools=payload.tools
    )
    # Approximate token usage (heuristic ~4 chars/token)
    approx_prompt_chars = sum(len(m.get("content", "")) for m in messages)
    approx_completion_chars = len(content or "")
    approx_tokens = int((approx_prompt_chars + approx_completion_chars) / 4) or 1
    llm_tokens_consumed_total.inc(approx_tokens)
    api_request_duration_seconds.observe(perf_counter() - _t0)
    return MentorOut(content=content)


@router.post(
    "/guide/stream",
    dependencies=[Depends(require_permissions(["mentor:stream", "llm:use"]))],
)
async def guide_stream(payload: MentorIn, llm: LLMProvider = Depends(get_llm)):
    _t0 = perf_counter()
    sys = f"You are a {payload.role}. Help the user achieve the objective. Stream concise steps."
    messages = [{"role": "system", "content": sys}]
    if payload.context:
        messages.append({"role": "system", "content": f"Context:\n{payload.context}"})
    messages += payload.messages

    async def gen() -> AsyncIterator[bytes]:
        llm.stream(messages, temperature=payload.temperature, tools=payload.tools)
        # Some implementations may return an awaitable of an async iterator.
        iterator: Any = stream_result
        if hasattr(stream_result, "__await__"):
            iterator = await stream_result
        total_chars = 0
        async for tok in iterator:
            total_chars += len(tok)
            yield tok.encode("utf-8")
        # Finished
        approx_prompt_chars = sum(len(m.get("content", "")) for m in messages)
        approx_tokens = int((approx_prompt_chars + total_chars) / 4) or 1
        llm_tokens_consumed_total.inc(approx_tokens)
        api_request_duration_seconds.observe(perf_counter() - _t0)

    return StreamingResponse(gen(), media_type="text/plain")
import bytes
import dict
import float
import hasattr
import int
import len
import list
import llm
import m
import payload
import str
import stream_result
import sum
import tok
