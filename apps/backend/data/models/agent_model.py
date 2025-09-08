"""


Agent Database Model.





Represents AI agents with their configurations, capabilities, and state.


"""

import json
from typing import Any

from apps.backend.data.models.base_model import FullFeaturedBaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
import TypeError
import ValueError
import bool
import capability
import conversations_delta
import dict
import float
import int
import kb_id
import list
import max
import messages_delta
import min
import response_time
import round
import self
import state_update
import str
import tool_config
import user_id


class Agent(FullFeaturedBaseModel):
    """AI Agent model with full feature set."""

    __tablename__ = "agents"

    # Basic Information

    name = Column(String(255), nullable=False, index=True, doc="Agent display name")

    description = Column(Text, nullable=True, doc="Agent description and purpose")

    agent_type = Column(
        String(50),
        nullable=False,
        default="conversational",
        index=True,
        doc="Type of agent (conversational, task, workflow, etc.)",
    )

    status = Column(
        String(20),
        nullable=False,
        default="inactive",
        index=True,
        doc="Agent status (active, inactive, training, error)",
    )

    # Configuration

    model_name = Column(
        String(100), nullable=False, default="gpt-3.5-turbo", doc="AI model being used"
    )

    model_provider = Column(
        String(50),
        nullable=False,
        default="openai",
        doc="Model provider (openai, anthropic, huggingface, etc.)",
    )

    system_prompt = Column(Text, nullable=True, doc="System prompt for the agent")

    temperature = Column(
        String(10), nullable=False, default="0.7", doc="Model temperature setting"
    )

    max_tokens = Column(
        Integer, nullable=False, default=2048, doc="Maximum tokens for responses"
    )

    # Capabilities

    capabilities = Column(Text, nullable=True, doc="Agent capabilities in JSON format")

    tools = Column(Text, nullable=True, doc="Available tools in JSON format")

    knowledge_bases = Column(
        Text, nullable=True, doc="Connected knowledge bases in JSON format"
    )

    # Behavior Configuration

    memory_enabled = Column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether agent has memory capabilities",
    )

    learning_enabled = Column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether agent can learn from interactions",
    )

    context_window = Column(
        Integer, nullable=False, default=4096, doc="Context window size"
    )

    # Performance Metrics

    total_conversations = Column(
        Integer, nullable=False, default=0, doc="Total number of conversations"
    )

    total_messages = Column(
        Integer, nullable=False, default=0, doc="Total number of messages processed"
    )

    average_response_time = Column(
        String(20), nullable=True, doc="Average response time in milliseconds"
    )

    success_rate = Column(
        String(10), nullable=True, default="0.0", doc="Success rate percentage"
    )

    # Resource Management

    max_concurrent_sessions = Column(
        Integer, nullable=False, default=10, doc="Maximum concurrent sessions"
    )

    current_sessions = Column(
        Integer, nullable=False, default=0, doc="Current active sessions"
    )

    resource_usage = Column(
        Text, nullable=True, doc="Resource usage statistics in JSON format"
    )

    # Training and Learning

    training_data_sources = Column(
        Text, nullable=True, doc="Training data sources in JSON format"
    )

    last_training_date = Column(
        DateTime(timezone=True), nullable=True, doc="Last training date"
    )

    model_version = Column(String(50), nullable=True, doc="Current model version")

    # Security and Access

    owner_id = Column(String(36), nullable=False, index=True, doc="Owner user ID")

    visibility = Column(
        String(20),
        nullable=False,
        default="private",
        doc="Agent visibility (private, public, organization)",
    )

    allowed_users = Column(Text, nullable=True, doc="Allowed user IDs in JSON format")

    # Integration Settings

    webhook_url = Column(
        String(500), nullable=True, doc="Webhook URL for notifications"
    )

    api_endpoints = Column(
        Text, nullable=True, doc="Custom API endpoints in JSON format"
    )

    external_integrations = Column(
        Text, nullable=True, doc="External integrations configuration in JSON"
    )

    # State Management

    current_state = Column(
        Text, nullable=True, doc="Current agent state in JSON format"
    )

    checkpoint_data = Column(
        Text, nullable=True, doc="Checkpoint data for state recovery"
    )

    # Relationships

    conversations = relationship(
        "Conversation", back_populates="agent", cascade="all, delete-orphan"
    )

    agent_memories = relationship(
        "AgentMemory", back_populates="agent", cascade="all, delete-orphan"
    )

    # Helper Methods

    def get_capabilities(self) -> list[str]:
        """


        Get agent capabilities as list.





        Returns:


            List of capabilities


        """

        if not self.capabilities:
            return []

        try:
            return json.loads(self.capabilities)

        except json.JSONDecodeError:
            return []

    def add_capability(self, capability: str) -> None:
        """


        Add a capability to the agent.





        Args:


            capability: Capability to add


        """

        capabilities = self.get_capabilities()

        if capability not in capabilities:
            capabilities.append(capability)

            self.capabilities = json.dumps(capabilities)

    def remove_capability(self, capability: str) -> None:
        """


        Remove a capability from the agent.





        Args:


            capability: Capability to remove


        """

        capabilities = self.get_capabilities()

        if capability in capabilities:
            capabilities.remove(capability)

            self.capabilities = json.dumps(capabilities)

    def get_tools(self) -> list[dict[str, Any]]:
        """


        Get agent tools as list.





        Returns:


            List of tool configurations


        """

        if not self.tools:
            return []

        try:
            return json.loads(self.tools)

        except json.JSONDecodeError:
            return []

    def add_tool(self, tool_config: dict[str, Any]) -> None:
        """


        Add a tool to the agent.





        Args:


            tool_config: Tool configuration


        """

        tools = self.get_tools()

        tools.append(tool_config)

        self.tools = json.dumps(tools)

    def get_knowledge_bases(self) -> list[str]:
        """


        Get connected knowledge bases.





        Returns:


            List of knowledge base IDs


        """

        if not self.knowledge_bases:
            return []

        try:
            return json.loads(self.knowledge_bases)

        except json.JSONDecodeError:
            return []

    def connect_knowledge_base(self, kb_id: str) -> None:
        """


        Connect a knowledge base to the agent.





        Args:


            kb_id: Knowledge base ID


        """

        kb_list = self.get_knowledge_bases()

        if kb_id not in kb_list:
            kb_list.append(kb_id)

            self.knowledge_bases = json.dumps(kb_list)

    def get_current_state(self) -> dict[str, Any]:
        """


        Get current agent state.





        Returns:


            Agent state dictionary


        """

        if not self.current_state:
            return {}

        try:
            return json.loads(self.current_state)

        except json.JSONDecodeError:
            return {}

    def update_state(self, state_update: dict[str, Any]) -> None:
        """


        Update agent state.





        Args:


            state_update: State updates to apply


        """

        current = self.get_current_state()

        current.update(state_update)

        self.current_state = json.dumps(current)

    def get_resource_usage(self) -> dict[str, Any]:
        """


        Get resource usage statistics.





        Returns:


            Resource usage dictionary


        """

        if not self.resource_usage:
            return {}

        try:
            return json.loads(self.resource_usage)

        except json.JSONDecodeError:
            return {}

    def update_metrics(
        self,
        conversations_delta: int = 0,
        messages_delta: int = 0,
        response_time: float | None = None,
    ) -> None:
        """


        Update agent performance metrics.





        Args:


            conversations_delta: Change in conversation count


            messages_delta: Change in message count


            response_time: Latest response time in milliseconds


        """

        self.total_conversations += conversations_delta

        self.total_messages += messages_delta

        if response_time is not None:
            try:
                current_avg = float(self.average_response_time or "0")

                total_responses = max(self.total_messages, 1)

                # Calculate new average

                new_avg = (
                    (current_avg * (total_responses - 1)) + response_time
                ) / total_responses

                self.average_response_time = str(round(new_avg, 2))

            except (ValueError, TypeError):
                self.average_response_time = str(response_time)

    def increment_session_count(self) -> None:
        """Increment current session count."""

        self.current_sessions = min(
            self.current_sessions + 1, self.max_concurrent_sessions
        )

    def decrement_session_count(self) -> None:
        """Decrement current session count."""

        self.current_sessions = max(self.current_sessions - 1, 0)

    def is_available(self) -> bool:
        """


        Check if agent is available for new sessions.





        Returns:


            True if agent can accept new sessions


        """

        return (
            self.status == "active"
            and self.current_sessions < self.max_concurrent_sessions
        )

    def can_user_access(self, user_id: str) -> bool:
        """


        Check if user can access this agent.





        Args:


            user_id: User ID to check





        Returns:


            True if user has access


        """

        if self.owner_id == user_id:
            return True

        if self.visibility == "public":
            return True

        if self.visibility == "private" and self.allowed_users:
            try:
                allowed = json.loads(self.allowed_users)

                return user_id in allowed

            except json.JSONDecodeError:
                return False

        return False

    def to_dict_public(self) -> dict[str, Any]:
        """


        Get public representation of agent.





        Returns:


            Public agent data


        """

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agent_type": self.agent_type,
            "status": self.status,
            "capabilities": self.get_capabilities(),
            "model_name": self.model_name,
            "model_provider": self.model_provider,
            "visibility": self.visibility,
            "total_conversations": self.total_conversations,
            "success_rate": self.success_rate,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        """String representation."""

        return f"<Agent(id={self.id}, name={self.name}, type={self.agent_type}, status={self.status})>"
