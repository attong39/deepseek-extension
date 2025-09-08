import os
import Exception
import ImportError
import bool
import current_user
import dict
import e
import getattr
import i
import int
import isinstance
import iter
import len
import list
import orchestrator
import range
import request
import request_id
import result
import self
import str
import token

# zeta_vn/app/api/v1/streaming.py


"""


Streaming Chat API v1 - E2E Blueprint 2025





Implements streaming chat endpoints theo chuẩn E2E:


- Chat → Plan → Act pipeline


- Request-ID tracking


- Structured logging


- Plan DSL generation với HMAC signing


"""

from __future__ import annotations

import asyncio
import hmac
import json
import logging
from collections.abc import AsyncGenerator
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

router = APIRouter(prefix="/chat", tags=["chat", "streaming"])
EVENT_STREAM_MT = "text/event-stream"

# Logger (ruff often suggests replacing print() with logging)
logger = logging.getLogger(__name__)


class StreamChatIn(BaseModel):
    """Schema cho streaming chat request."""

    agent_id: str = Field(..., description="ID của agent")

    message: str = Field(..., description="Tin nhắn từ user")

    context: dict[str, Any] = Field(default_factory=dict, description="Context desktop")

    stream: bool = Field(True, description="Enable streaming response")


class PlanStep(BaseModel):
    """Schema cho một bước trong plan."""

    tool: str = Field(..., description="Tên tool")

    args: dict[str, Any] = Field(..., description="Arguments cho tool")

    preconditions: list[str] = Field(
        default_factory=list, description="Điều kiện trước"
    )


class PlanDSL(BaseModel):
    """Schema cho Plan DSL theo E2E Blueprint."""

    id: str = Field(..., description="Plan ID")

    steps: list[PlanStep] = Field(..., description="Danh sách steps")

    ttl_s: int = Field(120, description="TTL in seconds")

    max_duration: int = Field(300, description="Max execution duration")

    signature: str = Field(..., description="HMAC signature")


class StreamChatOut(BaseModel):
    """Schema cho streaming chat response."""

    reply: str = Field(..., description="AI reply")

    plan: PlanDSL | None = Field(None, description="Execution plan nếu có")

    request_id: str = Field(..., description="Request tracking ID")


# Dependencies


try:
    from app.dependencies import get_agent_orchestrator, get_current_user
    from app.middleware.observability import get_request_id
except ImportError:  # Fallback stubs for local tools/docs
    from typing import Any as _Any

    class _MockOrchestrator:
        async def process_chat(self, *_a: _Any, **_k: _Any) -> _Any:
            # small await to emulate async work and satisfy linters
            await asyncio.sleep(0)

            class _R:
                reply = "mock reply"
                plan = None

                def model_dump(self) -> dict[str, _Any]:
                    return {
                        "reply": self.reply,
                        "plan": None,
                        "request_id": "req_mock_123",
                    }

            return _R()

    def get_agent_orchestrator(*_a: _Any, **_k: _Any) -> _Any:  # type: ignore
        return _MockOrchestrator()

    def get_current_user(*_a: _Any, **_k: _Any) -> _Any:  # type: ignore
        return {"sub": "mock", "id": "user_123"}

    def get_request_id(*_a: _Any, **_k: _Any) -> str:  # type: ignore
        return "req_mock_123"


def generate_plan_signature(plan_data: dict[str, Any]) -> str:
    """Tạo HMAC signature cho plan."""

    # In production, này sẽ dùng secret từ environment

    secret = os.getenv("SECRET")

    message = json.dumps(plan_data, sort_keys=True).encode()

    signature = hmac.new(secret.encode(), message, "sha256").hexdigest()

    return signature


@router.post("/stream", response_model=StreamChatOut)
async def stream_chat(
    request: StreamChatIn,
    orchestrator: Annotated[Any, Depends(get_agent_orchestrator)],
    current_user: Annotated[Any, Depends(get_current_user)],
    request_id: Annotated[str, Depends(get_request_id)],
) -> StreamChatOut | StreamingResponse:
    """


    Chat endpoint với plan generation theo E2E Blueprint.





    Flow:


    1. Validate input + context


    2. Agent Orchestrator → LLM + Memory Manager


    3. SecurityManager duyệt plan


    4. Generate signed plan DSL


    5. Return reply + plan


    """

    try:
        # Log request start
        logger.info(
            "[%s] Processing chat: agent=%s, user=%s",
            request_id,
            request.agent_id,
            current_user["id"],
        )

        # Process via orchestrator and normalize to StreamChatOut

        raw = await orchestrator.process_chat(request, current_user)

        # Normalize raw result into StreamChatOut for typing safety
        if isinstance(raw, dict):
            out = StreamChatOut(**(raw | {"request_id": request_id}))
        else:
            # try to extract serializable data
            try:
                data = raw.model_dump()
            except Exception:
                data = {
                    "reply": getattr(raw, "reply", ""),
                    "plan": getattr(raw, "plan", None),
                }
            data["request_id"] = request_id
            out = StreamChatOut(**data)

        # Log completion
        logger.info(
            "[%s] Chat completed: plan_id=%s",
            request_id,
            out.plan.id if out.plan else "none",
        )

        if not request.stream:
            return out

        async def _gen() -> AsyncGenerator[str, None]:
            # stream token-by-token
            reply = out.reply or ""
            chunk = 40
            seq = 0
            for i in range(0, len(reply), chunk):
                piece = reply[i : i + chunk]
                yield f'data: {{"type": "chat.token", "content": {piece!r}, "seq": {seq}, "request_id": {request_id!r} }}\n\n'
                seq += 1
                await asyncio.sleep(0)
            # send completed with plan payload
            payload = {
                "type": "chat.completed",
                "request_id": request_id,
                "plan": out.plan.model_dump() if out.plan else None,
            }
            yield f"data: {json.dumps(payload)}\n\n"

        return StreamingResponse(
            _gen(),
            media_type=EVENT_STREAM_MT,
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        logger.exception("[%s] Chat error: %s", request_id, e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {e!s}",
        ) from e


async def generate_stream_response(
    request: StreamChatIn,
    orchestrator: Any,
    current_user: dict[str, Any],
    request_id: str,
) -> AsyncGenerator[str, None]:
    """Generate streaming response content."""

    # Mock streaming implementation

    tokens = [
        "I'll ",
        "help ",
        "you ",
        "with ",
        "that ",
        "task. ",
        "Let ",
        "me ",
        "analyze ",
        "the ",
        "context ",
        "and ",
        "create ",
        "a ",
        "plan.\n\n",
        "**Generated Plan:**\n",
        "1. Find PNG files\n",
        "2. Rename using pattern\n",
        "3. Confirm completion\n",
    ]

    seq = 0
    for token in tokens:
        yield f"data: {json.dumps({'type': 'chat.token', 'content': token, 'seq': seq, 'request_id': request_id})}\n\n"
        seq += 1
        await asyncio.sleep(0)

    # Send plan

    _ = await orchestrator.process_chat(request, current_user)

    plan_data = result.plan.model_dump() if result.plan else None

    yield f"data: {json.dumps({'type': 'chat.completed', 'plan': plan_data, 'request_id': request_id})}\n\n"

    # End stream

    # explicit end marker is optional; clients can treat chat.completed as terminal


@router.post("/stream-sse")
async def stream_chat_sse(
    request: StreamChatIn,
    orchestrator: Annotated[Any, Depends(get_agent_orchestrator)],
    current_user: Annotated[Any, Depends(get_current_user)],
    request_id: Annotated[str, Depends(get_request_id)],
) -> StreamingResponse:
    """Server-Sent Events streaming endpoint."""

    if not request.stream:
        # Fallback to regular endpoint: return single SSE event with full payload
        _ = await stream_chat(request, orchestrator, current_user, request_id)
        if isinstance(result, StreamingResponse):
            return result
        payload = result.model_dump()
        return StreamingResponse(
            iter([f"data: {json.dumps(payload)}\n\n"]),
            media_type="text/event-stream",
        )

    return StreamingResponse(
        generate_stream_response(request, orchestrator, current_user, request_id),
        media_type=EVENT_STREAM_MT,
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Request-ID": request_id,
        },
    )
