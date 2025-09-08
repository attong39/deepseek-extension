"""Unified WebSocket event schemas (chat + training).

Định nghĩa kiểu message/event thống nhất giữa Server và Desktop UI.

- Chat events:
  - assistant_reply
  - chat.token
  - chat.completed
  - chat.error
  - ping/pong

- Training events:
  - training.progress
  - training.completed
  - training.error

Các model dùng Pydantic để đảm bảo serialize JSON ổn định.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field
import Exception
import bool
import dict
import int
import list
import m
import model
import models
import out
import str
import type

API_VERSION = "1.0.0"


class WSBase(BaseModel):
    """Envelope chung cho message WS."""

    version: str = Field(API_VERSION, description="Contract version")
    corrId: str | None = Field(None, description="Correlation/trace id")
    type: str
    payload: Any


class AssistantReplyEvent(BaseModel):
    """Assistant reply payload.

    Attributes:
        type: Literal discriminator 'assistant_reply'.
        content: Nội dung trả lời.
        timestamp: ISO time optional.
    """

    type: Literal["assistant_reply"] = "assistant_reply"
    content: str
    timestamp: str | None = None


class ActionEvent(BaseModel):
    """Generic action message (optional)."""

    type: Literal["action"] = "action"
    payload: Any


class PingEvent(BaseModel):
    type: Literal["ping"] = "ping"
    ts: int


class PongEvent(BaseModel):
    type: Literal["pong"] = "pong"
    ts: int


class ChatTokenEvent(BaseModel):
    """Streaming token for chat."""

    type: Literal["chat.token"] = "chat.token"
    content: str
    seq: int | None = None
    timestamp: str | None = None


class ChatCompletedEvent(BaseModel):
    type: Literal["chat.completed"] = "chat.completed"
    content: str
    usage: dict[str, Any] | None = None
    timestamp: str | None = None


class ChatErrorEvent(BaseModel):
    type: Literal["chat.error"] = "chat.error"
    code: str | None = None
    message: str | None = None


class NewMessageEvent(BaseModel):
    """Event khi có tin nhắn mới trong hội thoại."""

    type: Literal["new_message"] = "new_message"
    message: dict[str, Any]


class TypingIndicatorEvent(BaseModel):
    """Event thông báo user đang gõ."""

    type: Literal["typing_indicator"] = "typing_indicator"
    user_id: str
    is_typing: bool
    conversation_id: str | None = None
    timestamp: str


class ConversationHistoryEvent(BaseModel):
    """Event trả lịch sử hội thoại."""

    type: Literal["conversation_history"] = "conversation_history"
    messages: list[dict[str, Any]]
    conversation_id: str | None = None
    timestamp: str


class StatusUpdatedEvent(BaseModel):
    """Event cập nhật trạng thái người dùng."""

    type: Literal["status_updated"] = "status_updated"
    status: str
    timestamp: str


class TrainingProgressEvent(BaseModel):
    """Training progress update.

    Note: field names dùng camelCase (jobId) để khớp Desktop schema.
    """

    type: Literal["training.progress"] = "training.progress"
    jobId: str
    progress: int
    message: str | None = None


class TrainingCompletedEvent(BaseModel):
    type: Literal["training.completed"] = "training.completed"
    jobId: str
    progress: int | None = None
    message: str | None = None
    artifactUrl: str | None = None


class TrainingErrorEvent(BaseModel):
    type: Literal["training.error"] = "training.error"
    jobId: str
    code: str | None = None
    message: str | None = None


def to_json(model: BaseModel) -> str:
    """Serialize Pydantic model to JSON string.

    Returns:
        JSON string.
    """

    return model.model_dump_json()


def export_json_schemas() -> dict[str, dict[str, Any]]:
    """Export JSON Schemas for all WS event models.

    Returns:
        Mapping from model name to its JSON Schema (Draft 2020-12 compatible by Pydantic).
    """
    models: list[type[BaseModel]] = [
        WSBase,
        AssistantReplyEvent,
        ActionEvent,
        PingEvent,
        PongEvent,
        ChatTokenEvent,
        ChatCompletedEvent,
        ChatErrorEvent,
        NewMessageEvent,
        TypingIndicatorEvent,
        ConversationHistoryEvent,
        StatusUpdatedEvent,
        TrainingProgressEvent,
        TrainingCompletedEvent,
        TrainingErrorEvent,
    ]
    out: dict[str, dict[str, Any]] = {}
    for m in models:
        try:
            schema = m.model_json_schema()
        except Exception:  # pragma: no cover
            schema = {}
        out[m.__name__] = schema
    return out
