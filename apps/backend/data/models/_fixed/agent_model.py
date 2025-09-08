"""
Agent Database Model - SQLAlchemy 2.x Fixed Version.

Represents AI agents with proper type safety.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from apps.backend.data.models.base_model import BaseModel
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
import TypeError
import bool
import capabilities
import capability
import conversations_delta
import dict
import float
import int
import isinstance
import kb_id
import kb_ids
import len
import list
import max
import messages_delta
import min
import new_state
import response_time
import round
import self
import str
import tools
import user_id


class Agent(BaseModel):
    """Agent model for AI agent instances."""

    # Basic Information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    agent_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default="assistant"
    )
    agent_version: Mapped[str] = mapped_column(
        String(50), nullable=False, default="1.0.0"
    )

    # Configuration
    model_name: Mapped[str] = mapped_column(
        String(100), nullable=False, default="gpt-4"
    )
    temperature: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=4096)
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Capabilities
    capabilities_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    tools_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    knowledge_bases_json: Mapped[str] = mapped_column(
        Text, nullable=False, default="[]"
    )

    # Status
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="idle")
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    current_state_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")

    # Performance Metrics
    resource_usage_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    total_conversations: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_messages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_sessions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_response_time: Mapped[str] = mapped_column(
        String(50), default="0.0", nullable=False
    )

    # Access Control
    allowed_users_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    privacy_level: Mapped[str] = mapped_column(
        String(20), nullable=False, default="standard"
    )

    # Timestamps
    last_active_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deployed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def get_capabilities(self) -> list[str]:
        """Get agent capabilities."""
        try:
            parsed = json.loads(self.capabilities_json)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def set_capabilities(self, capabilities: list[str]) -> None:
        """Set agent capabilities."""
        self.capabilities_json = json.dumps(capabilities)

    def add_capability(self, capability: str) -> None:
        """Add a capability to the agent."""
        current = self.get_capabilities()
        if capability not in current:
            current.append(capability)
            self.set_capabilities(current)

    def remove_capability(self, capability: str) -> None:
        """Remove a capability from the agent."""
        current = self.get_capabilities()
        if capability in current:
            current.remove(capability)
            self.set_capabilities(current)

    def get_tools(self) -> list[dict[str, Any]]:
        """Get agent tools."""
        try:
            parsed = json.loads(self.tools_json)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def set_tools(self, tools: list[dict[str, Any]]) -> None:
        """Set agent tools."""
        self.tools_json = json.dumps(tools)

    def get_knowledge_bases(self) -> list[str]:
        """Get knowledge base IDs."""
        try:
            parsed = json.loads(self.knowledge_bases_json)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def set_knowledge_bases(self, kb_ids: list[str]) -> None:
        """Set knowledge base IDs."""
        self.knowledge_bases_json = json.dumps(kb_ids)

    def add_knowledge_base(self, kb_id: str) -> None:
        """Add a knowledge base to the agent."""
        current = self.get_knowledge_bases()
        if kb_id not in current:
            current.append(kb_id)
            self.set_knowledge_bases(current)

    def get_current_state(self) -> dict[str, Any]:
        """Get current state."""
        try:
            parsed = json.loads(self.current_state_json)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}

    def update_state(self, new_state: dict[str, Any]) -> None:
        """Update current state."""
        current = self.get_current_state()
        current.update(new_state)
        self.current_state_json = json.dumps(current)

    def get_resource_usage(self) -> dict[str, Any]:
        """Get resource usage statistics."""
        try:
            parsed = json.loads(self.resource_usage_json)
            return parsed if isinstance(parsed, dict) else {}
        except (json.JSONDecodeError, TypeError):
            return {}

    def update_conversation_stats(
        self,
        conversations_delta: int = 0,
        messages_delta: int = 0,
        response_time: float | None = None,
    ) -> None:
        """Update conversation statistics."""
        self.total_conversations += conversations_delta
        self.total_messages += messages_delta

        # Update average response time
        if response_time is not None:
            current_avg = (
                float(self.average_response_time)
                if self.average_response_time != "0.0"
                else 0.0
            )
            total_responses = max(self.total_messages, 1)

            if current_avg > 0:
                new_avg = (
                    (current_avg * (total_responses - 1)) + response_time
                ) / total_responses
                self.average_response_time = str(round(new_avg, 2))
            else:
                self.average_response_time = str(response_time)

    def start_session(self) -> None:
        """Start a new session."""
        self.current_sessions = min(self.current_sessions + 1, 100)  # Cap at 100
        self.last_active_at = datetime.now(UTC)

    def end_session(self) -> None:
        """End a session."""
        self.current_sessions = max(self.current_sessions - 1, 0)

    def is_online(self) -> bool:
        """Check if agent is online."""
        return self.status == "active" and self.is_active

    def get_allowed_users(self) -> list[str]:
        """Get list of allowed user IDs."""
        try:
            parsed = json.loads(self.allowed_users_json)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []

    def is_user_allowed(self, user_id: str) -> bool:
        """Check if user is allowed to access this agent."""
        if self.privacy_level == "public":
            return True
        allowed = self.get_allowed_users()
        return len(allowed) == 0 or user_id in allowed


__all__ = ["Agent"]
