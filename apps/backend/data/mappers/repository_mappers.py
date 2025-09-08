"""
Repository Mapper Implementation for Domain Entity Alignment.

Maps between SQLAlchemy models and domain entities with proper type safety.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

# Domain imports (cần thêm sau khi domain entities hoàn chỉnh)
# from apps.backend.core.domain.entities.agent import Agent
# from apps.backend.core.domain.value_objects.agent_lifecycle_status import AgentLifecycleStatus
# Database model imports
from apps.backend.data.models._fixed.agent_model import Agent as AgentModel
from apps.backend.data.models._fixed.conversation_model import (
import Exception
import ValueError
import dict
import domain_data
import entity_id
import entity_type
import error
import float
import staticmethod
import str
    Conversation as ConversationModel,
)


class AgentRepositoryMapper:
    """Maps between AgentModel and Agent domain entity."""

    @staticmethod
    def to_domain(model: AgentModel) -> dict[str, Any]:
        """Convert database model to domain entity data.

        Returns dict temporarily until domain entities are finalized.
        """
        return {
            "id": UUID(model.id),
            "name": model.name,
            "description": model.description,
            "agent_type": model.agent_type,
            "version": model.agent_version,
            "model_name": model.model_name,
            "temperature": model.temperature,
            "max_tokens": model.max_tokens,
            "system_prompt": model.system_prompt,
            "capabilities": model.get_capabilities(),
            "tools": model.get_tools(),
            "knowledge_bases": model.get_knowledge_bases(),
            "status": model.status,
            "is_active": model.is_active,
            "current_state": model.get_current_state(),
            "resource_usage": model.get_resource_usage(),
            "total_conversations": model.total_conversations,
            "total_messages": model.total_messages,
            "current_sessions": model.current_sessions,
            "average_response_time": float(model.average_response_time)
            if model.average_response_time != "0.0"
            else 0.0,
            "allowed_users": model.get_allowed_users(),
            "privacy_level": model.privacy_level,
            "last_active_at": model.last_active_at,
            "deployed_at": model.deployed_at,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }

    @staticmethod
    def to_model(domain_data: dict[str, Any]) -> AgentModel:
        """Convert domain entity data to database model."""
        model = AgentModel()

        # Basic info
        if "id" in domain_data:
            model.id = str(domain_data["id"])
        model.name = domain_data.get("name", "")
        model.description = domain_data.get("description")
        model.agent_type = domain_data.get("agent_type", "assistant")
        model.agent_version = domain_data.get("version", "1.0.0")

        # Configuration
        model.model_name = domain_data.get("model_name", "gpt-4")
        model.temperature = domain_data.get("temperature", 0.7)
        model.max_tokens = domain_data.get("max_tokens", 4096)
        model.system_prompt = domain_data.get("system_prompt")

        # Capabilities
        if "capabilities" in domain_data:
            model.set_capabilities(domain_data["capabilities"])
        if "tools" in domain_data:
            model.set_tools(domain_data["tools"])
        if "knowledge_bases" in domain_data:
            model.set_knowledge_bases(domain_data["knowledge_bases"])

        # Status
        model.status = domain_data.get("status", "idle")
        model.is_active = domain_data.get("is_active", True)

        # State
        if "current_state" in domain_data:
            model.update_state(domain_data["current_state"])

        # Privacy
        model.privacy_level = domain_data.get("privacy_level", "standard")

        return model

    @staticmethod
    def update_model_from_domain(
        model: AgentModel, domain_data: dict[str, Any]
    ) -> None:
        """Update existing model with domain data."""
        # Update fields that can change
        if "name" in domain_data:
            model.name = domain_data["name"]
        if "description" in domain_data:
            model.description = domain_data["description"]
        if "system_prompt" in domain_data:
            model.system_prompt = domain_data["system_prompt"]
        if "temperature" in domain_data:
            model.temperature = domain_data["temperature"]
        if "max_tokens" in domain_data:
            model.max_tokens = domain_data["max_tokens"]
        if "capabilities" in domain_data:
            model.set_capabilities(domain_data["capabilities"])
        if "tools" in domain_data:
            model.set_tools(domain_data["tools"])
        if "status" in domain_data:
            model.status = domain_data["status"]
        if "is_active" in domain_data:
            model.is_active = domain_data["is_active"]
        if "current_state" in domain_data:
            model.update_state(domain_data["current_state"])


class ConversationRepositoryMapper:
    """Maps between ConversationModel and domain entity."""

    @staticmethod
    def to_domain(model: ConversationModel) -> dict[str, Any]:
        """Convert database model to domain entity data."""
        return {
            "id": UUID(model.id),
            "title": model.title,
            "summary": model.summary,
            "status": model.status,
            "user_id": model.user_id,
            "agent_id": model.agent_id,
            "context": model.get_context(),
            "settings": model.get_settings(),
            "started_at": model.started_at,
            "ended_at": model.ended_at,
            "last_activity_at": model.last_activity_at,
            "message_count": model.message_count,
            "total_tokens": model.total_tokens,
            "user_rating": model.user_rating,
            "user_feedback": model.user_feedback,
            "satisfaction_score": model.satisfaction_score,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }

    @staticmethod
    def to_model(domain_data: dict[str, Any]) -> ConversationModel:
        """Convert domain entity data to database model."""
        model = ConversationModel()

        if "id" in domain_data:
            model.id = str(domain_data["id"])
        model.title = domain_data.get("title")
        model.summary = domain_data.get("summary")
        model.status = domain_data.get("status", "active")
        model.user_id = domain_data.get("user_id", "")
        model.agent_id = domain_data.get("agent_id")

        if "context" in domain_data:
            model.set_context(domain_data["context"])
        if "settings" in domain_data:
            model.set_settings(domain_data["settings"])

        model.message_count = domain_data.get("message_count", 0)
        model.total_tokens = domain_data.get("total_tokens", 0)

        return model


# Repository Error Mapping
class RepositoryErrorMapper:
    """Maps between database errors and domain exceptions."""

    @staticmethod
    def map_integrity_error(error: Exception, entity_type: str) -> Exception:
        """Map SQLAlchemy IntegrityError to domain exception."""
        # For now, return generic error
        # TODO: Create proper domain exceptions
        error_msg = f"Integrity constraint violation for {entity_type}: {str(error)}"
        return ValueError(error_msg)

    @staticmethod
    def map_not_found_error(entity_id: str, entity_type: str) -> Exception:
        """Map not found to domain exception."""
        error_msg = f"{entity_type} with id {entity_id} not found"
        return ValueError(error_msg)


__all__ = [
    "AgentRepositoryMapper",
    "ConversationRepositoryMapper",
    "RepositoryErrorMapper",
]
