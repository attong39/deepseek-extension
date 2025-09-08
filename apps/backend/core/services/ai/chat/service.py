"""
Chat service implementation for conversational AI.

Provides conversation management, context tracking, intent recognition,
and response generation for chat-based AI interactions.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from apps.backend.core.observability.logging import get_logger
from apps.backend.core.services.ai.orchestrator import (
import Exception
import ValueError
import bool
import conv_id
import dict
import e
import float
import include_context
import int
import intent_name
import keyword
import keywords
import len
import limit
import list
import max
import message
import metadata
import msg
import num
import offset
import property
import request
import self
import str
import sum
import super
import tenant_id
import user_id
import word
import x
    AIRequest,
    AIResponse,
    BaseAIService,
)
from apps.backend.core.services.ai.registry import CapabilityProvider

logger = get_logger(__name__)


class MessageType(Enum):
    """Chat message types."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class ConversationStatus(Enum):
    """Conversation status enumeration."""

    ACTIVE = "active"
    PAUSED = "paused"
    ENDED = "ended"
    ARCHIVED = "archived"


@dataclass
class ChatMessage:
    """Chat message structure."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str = ""
    message_type: MessageType = MessageType.USER
    content: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    user_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "message_type": self.message_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
        }


@dataclass
class ConversationContext:
    """Conversation context and state."""

    conversation_id: str
    user_id: str
    tenant_id: str | None = None
    status: ConversationStatus = ConversationStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    # Context tracking
    intent_history: list[str] = field(default_factory=list)
    entity_context: dict[str, Any] = field(default_factory=dict)
    conversation_summary: str = ""
    message_count: int = 0

    def update_context(
        self, intent: str | None = None, entities: dict[str, Any] | None = None
    ) -> None:
        """Update conversation context."""
        self.updated_at = datetime.now(UTC)
        self.message_count += 1

        if intent:
            self.intent_history.append(intent)
            # Keep only last 10 intents
            if len(self.intent_history) > 10:
                self.intent_history = self.intent_history[-10:]

        if entities:
            self.entity_context.update(entities)


@dataclass
class Intent:
    """Recognized user intent."""

    name: str
    confidence: float
    entities: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatResponse:
    """Chat response structure."""

    message: str
    intent: Intent | None = None
    suggestions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    processing_time_ms: float = 0.0


class IntentClassifier:
    """Simple intent classification service."""

    def __init__(self) -> None:
        # Simple keyword-based intent mapping
        self._intent_keywords = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
            "question": ["what", "how", "when", "where", "why", "who"],
            "request": ["please", "can you", "could you", "would you"],
            "complaint": ["problem", "issue", "wrong", "error", "bug"],
            "compliment": ["great", "awesome", "excellent", "good job", "thank you"],
            "goodbye": ["bye", "goodbye", "see you", "farewell"],
        }

    async def classify_intent(self, message: str) -> Intent:
        """Classify user intent from message."""
        message_lower = message.lower()

        # Simple keyword matching
        intent_scores = {}
        for intent_name, keywords in self._intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent_name] = score / len(keywords)

        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return Intent(
                name=best_intent[0],
                confidence=best_intent[1],
                metadata={"all_scores": intent_scores},
            )

        return Intent(name="unknown", confidence=0.0)

    async def extract_entities(self, message: str) -> dict[str, Any]:
        """Extract entities from message."""
        # Simple entity extraction (placeholder implementation)
        entities = {}

        # Extract basic entities
        words = message.split()

        # Look for potential names (capitalized words)
        names = [word for word in words if word.istitle() and len(word) > 2]
        if names:
            entities["names"] = names

        # Look for numbers
        numbers = [word for word in words if word.isdigit()]
        if numbers:
            entities["numbers"] = [int(num) for num in numbers]

        return entities


class ConversationManager:
    """Manages chat conversations and context."""

    def __init__(self) -> None:
        self._conversations: dict[str, ConversationContext] = {}
        self._messages: dict[str, list[ChatMessage]] = {}
        self._logger = get_logger(__name__)

    async def create_conversation(
        self,
        user_id: str,
        tenant_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ConversationContext:
        """Create a new conversation."""
        conversation_id = str(uuid.uuid4())

        context = ConversationContext(
            conversation_id=conversation_id,
            user_id=user_id,
            tenant_id=tenant_id,
            metadata=metadata or {},
        )

        self._conversations[conversation_id] = context
        self._messages[conversation_id] = []

        self._logger.info(f"Created conversation {conversation_id} for user {user_id}")
        return context

    async def get_conversation(
        self, conversation_id: str
    ) -> ConversationContext | None:
        """Get conversation context."""
        return self._conversations.get(conversation_id)

    async def add_message(self, conversation_id: str, message: ChatMessage) -> None:
        """Add message to conversation."""
        if conversation_id not in self._messages:
            raise ValueError(f"Conversation {conversation_id} not found")

        message.conversation_id = conversation_id
        self._messages[conversation_id].append(message)

        # Update conversation context
        context = self._conversations[conversation_id]
        context.message_count += 1
        context.updated_at = datetime.now(UTC)

    async def get_messages(
        self, conversation_id: str, limit: int = 50, offset: int = 0
    ) -> list[ChatMessage]:
        """Get messages from conversation."""
        messages = self._messages.get(conversation_id, [])
        return messages[offset : offset + limit]

    async def get_conversation_history(
        self, conversation_id: str, include_context: bool = True
    ) -> dict[str, Any]:
        """Get full conversation history."""
        context = await self.get_conversation(conversation_id)
        messages = await self.get_messages(conversation_id)

        history = {
            "conversation_id": conversation_id,
            "messages": [msg.to_dict() for msg in messages],
        }

        if include_context and context:
            history["context"] = {
                "user_id": context.user_id,
                "status": context.status.value,
                "created_at": context.created_at.isoformat(),
                "updated_at": context.updated_at.isoformat(),
                "message_count": context.message_count,
                "intent_history": context.intent_history,
                "entity_context": context.entity_context,
                "metadata": context.metadata,
            }

        return history


class ResponseGenerator:
    """Generates responses for chat messages."""

    def __init__(self) -> None:
        self._response_templates = {
            "greeting": [
                "Hello! How can I help you today?",
                "Hi there! What can I do for you?",
                "Good to see you! How may I assist?",
            ],
            "question": [
                "That's an interesting question. Let me think about that.",
                "I'd be happy to help you with that.",
                "Let me provide you with some information about that.",
            ],
            "request": [
                "I'll do my best to help you with that request.",
                "Certainly, I can help you with that.",
                "I'd be glad to assist you with that.",
            ],
            "complaint": [
                "I understand your concern. Let me see how I can help.",
                "I'm sorry to hear about this issue. Let's work on resolving it.",
                "I apologize for the problem. Let me help you fix this.",
            ],
            "compliment": [
                "Thank you for the kind words!",
                "I appreciate your feedback!",
                "That's very nice of you to say!",
            ],
            "goodbye": ["Goodbye! Have a great day!", "See you later!", "Take care!"],
            "unknown": [
                "I'm not sure I understand. Could you please rephrase that?",
                "Could you provide more details about what you need?",
                "I'd like to help, but I need more information.",
            ],
        }

    async def generate_response(
        self, message: str, intent: Intent, context: ConversationContext
    ) -> ChatResponse:
        """Generate response based on message, intent, and context."""
        start_time = asyncio.get_event_loop().time()

        # Get response template for intent
        templates = self._response_templates.get(
            intent.name, self._response_templates["unknown"]
        )

        # Simple template selection (could be more sophisticated)
        template_index = len(context.intent_history) % len(templates)
        response_text = templates[template_index]

        # Generate suggestions based on intent
        suggestions = self._generate_suggestions(intent, context)

        processing_time = (asyncio.get_event_loop().time() - start_time) * 1000

        return ChatResponse(
            message=response_text,
            intent=intent,
            suggestions=suggestions,
            metadata={
                "template_used": template_index,
                "context_length": context.message_count,
            },
            processing_time_ms=processing_time,
        )

    def _generate_suggestions(
        self, intent: Intent, context: ConversationContext
    ) -> list[str]:
        """Generate conversation suggestions."""
        suggestions = []

        if intent.name == "greeting":
            suggestions = [
                "Tell me about your services",
                "I have a question",
                "I need help with something",
            ]
        elif intent.name == "question":
            suggestions = [
                "Can you explain more?",
                "What are the options?",
                "How does this work?",
            ]
        elif intent.name == "request":
            suggestions = [
                "What information do you need?",
                "When can this be done?",
                "Are there any requirements?",
            ]

        return suggestions


class ChatService(BaseAIService, CapabilityProvider):
    """
    Chat service for conversational AI interactions.

    Manages conversations, classifies intents, maintains context,
    and generates appropriate responses.
    """

    def __init__(self) -> None:
        super().__init__("chat_service")
        self._conversation_manager = ConversationManager()
        self._intent_classifier = IntentClassifier()
        self._response_generator = ResponseGenerator()

    @property
    def capability_name(self) -> str:
        """Capability name."""
        return "chat"

    @property
    def capability_version(self) -> str:
        """Capability version."""
        return "1.0.0"

    async def _start_service(self) -> None:
        """Start the chat service."""
        logger.info("Chat service started")

    async def _stop_service(self) -> None:
        """Stop the chat service."""
        logger.info("Chat service stopped")

    async def initialize(self) -> None:
        """Initialize the capability."""
        await self.start()

    async def shutdown(self) -> None:
        """Shutdown the capability."""
        await self.stop()

    async def process(self, request: AIRequest) -> AIResponse:
        """Process chat request."""
        try:
            # Extract message from request
            message_content = request.payload.get("message", "")
            conversation_id = request.payload.get("conversation_id")

            if not message_content:
                return AIResponse(
                    request_id=request.request_id,
                    success=False,
                    error="No message content provided",
                )

            # Get or create conversation
            if conversation_id:
                context = await self._conversation_manager.get_conversation(
                    conversation_id
                )
                if not context:
                    return AIResponse(
                        request_id=request.request_id,
                        success=False,
                        error=f"Conversation {conversation_id} not found",
                    )
            else:
                context = await self._conversation_manager.create_conversation(
                    user_id=request.user_id, tenant_id=request.tenant_id
                )
                conversation_id = context.conversation_id

            # Create user message
            user_message = ChatMessage(
                conversation_id=conversation_id,
                message_type=MessageType.USER,
                content=message_content,
                user_id=request.user_id,
            )

            # Add user message to conversation
            await self._conversation_manager.add_message(conversation_id, user_message)

            # Classify intent
            intent = await self._intent_classifier.classify_intent(message_content)

            # Extract entities
            entities = await self._intent_classifier.extract_entities(message_content)

            # Update conversation context
            context.update_context(intent.name, entities)

            # Generate response
            chat_response = await self._response_generator.generate_response(
                message_content, intent, context
            )

            # Create assistant message
            assistant_message = ChatMessage(
                conversation_id=conversation_id,
                message_type=MessageType.ASSISTANT,
                content=chat_response.message,
                metadata={
                    "intent": intent.name,
                    "confidence": intent.confidence,
                    "entities": entities,
                    "suggestions": chat_response.suggestions,
                },
            )

            # Add assistant message to conversation
            await self._conversation_manager.add_message(
                conversation_id, assistant_message
            )

            return AIResponse(
                request_id=request.request_id,
                success=True,
                result={
                    "message": chat_response.message,
                    "conversation_id": conversation_id,
                    "intent": intent.name,
                    "confidence": intent.confidence,
                    "entities": entities,
                    "suggestions": chat_response.suggestions,
                },
                metadata={
                    "processing_time_ms": chat_response.processing_time_ms,
                    "message_count": context.message_count,
                },
            )

        except Exception as e:
            logger.error(f"Error processing chat request: {e}")
            return AIResponse(
                request_id=request.request_id,
                success=False,
                error=f"Chat processing error: {str(e)}",
            )

    async def get_conversation_history(
        self, conversation_id: str, user_id: str
    ) -> dict[str, Any] | None:
        """Get conversation history for user."""
        context = await self._conversation_manager.get_conversation(conversation_id)

        # Verify user access
        if not context or context.user_id != user_id:
            return None

        return await self._conversation_manager.get_conversation_history(
            conversation_id
        )

    async def list_user_conversations(
        self, user_id: str, limit: int = 20
    ) -> list[dict[str, Any]]:
        """List conversations for a user."""
        user_conversations = []

        for conv_id, context in self._conversation_manager._conversations.items():
            if context.user_id == user_id:
                user_conversations.append(
                    {
                        "conversation_id": conv_id,
                        "status": context.status.value,
                        "created_at": context.created_at.isoformat(),
                        "updated_at": context.updated_at.isoformat(),
                        "message_count": context.message_count,
                        "summary": context.conversation_summary or "No summary",
                    }
                )

        # Sort by updated_at descending
        user_conversations.sort(key=lambda x: x["updated_at"], reverse=True)

        return user_conversations[:limit]
