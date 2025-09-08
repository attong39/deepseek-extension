"""Chat service implementation.

Cung cấp chat inference, streaming, và conversation management.
Refactored để sử dụng new service architecture.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from apps.backend.core.services._base import BaseService, ServiceContext
from apps.backend.core.services.middleware import instrument
from apps.backend.core.services.types import ServiceResult, StreamChunk
import Exception
import ImportError
import chunk
import context
import conversation_id
import ctx
import dict
import doc
import e
import hasattr
import int
import limit
import list
import llm_router
import memory_service
import rule_engine
import self
import str
import super
import token
import user_message


class ChatService(BaseService):
    """Service cho chat operations với LLM providers.

    Hỗ trợ:
    - Single shot chat
    - Streaming responses
    - Context injection từ memory
    - Rule engine integration
    """

    def __init__(
        self,
        ctx: ServiceContext,
        llm_router: Any,  # LLM router/provider
        memory_service: Any | None = None,
        rule_engine: Any | None = None,
    ):
        super().__init__(ctx)
        self.llm = llm_router
        self.memory = memory_service
        self.rules = rule_engine

    # Note: instrument decorator không work với AsyncIterator, use manual logging
    async def stream_chat(
        self,
        conversation_id: str,
        user_message: str,
        context: dict[str, Any] | None = None,
    ) -> AsyncIterator[StreamChunk]:
        """Stream chat response với context injection."""
        self._log_operation("stream", conv_id=conversation_id)

        try:
            # Guard với rule engine
            if self.rules:
                self.rules.guard_prompt(user_message)

            # Retrieve context từ memory
            context_docs = []
            if self.memory:
                context_docs = await self.memory.retrieve_for_chat(
                    conversation_id, user_message, top_k=6
                )

            # Prepare messages với context
            messages = self._build_messages(user_message, context_docs, context)

            # Stream từ LLM
            async for token in self.llm.stream(messages):
                yield StreamChunk(type="token", data=token)

            yield StreamChunk(type="event", data="completed")

        except Exception as e:
            self._log_error("stream", e, conv_id=conversation_id)
            yield StreamChunk(type="error", data=str(e))

    @instrument(name="chat.ask")
    async def ask(
        self,
        conversation_id: str,
        user_message: str,
        context: dict[str, Any] | None = None,
    ) -> ServiceResult[str]:
        """Single shot chat response."""
        self._log_operation("ask", conv_id=conversation_id)

        try:
            # Collect stream tokens
            response_tokens = []
            async for chunk in self.stream_chat(conversation_id, user_message, context):
                if chunk.type == "token":
                    response_tokens.append(chunk.data)
                elif chunk.type == "error":
                    return ServiceResult.failure(chunk.data, "CHAT_ERROR")

            response = "".join(response_tokens)
            return ServiceResult.success(response)

        except Exception as e:
            self._log_error("ask", e, conv_id=conversation_id)
            return ServiceResult.failure(str(e), "CHAT_ERROR")

    async def get_conversation_history(
        self, conversation_id: str, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Get conversation history."""
        if self.memory and hasattr(self.memory, "get_conversation"):
            return await self.memory.get_conversation(conversation_id, limit=limit)
        return []

    def _build_messages(
        self,
        user_message: str,
        context_docs: list[dict[str, Any]],
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Build message array cho LLM."""
        messages = []

        # System context
        if context_docs:
            context_text = "\n".join(doc.get("text", "") for doc in context_docs)
            messages.append({"role": "system", "content": f"Context:\n{context_text}"})

        # Additional context
        if context:
            messages.append(
                {"role": "system", "content": f"Additional context: {context}"}
            )

        # User message
        messages.append({"role": "user", "content": user_message})

        return messages


# Backward compatibility - import old service if exists
try:
    pass

    __all__ = ["ChatService", "LegacyChatService"]
except ImportError:
    __all__ = ["ChatService"]
