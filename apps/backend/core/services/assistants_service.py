"""Assistants service for managing AI assistants.





Cung cấp business logic cho quản lý AI assistants,


bao gồm CRUD operations, analytics, configuration management,


và tích hợp với các hệ thống khác.


"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from apps.backend.core.common.base_classes import BaseService
import a
import bool
import change_summary
import created_by
import data
import days
import dict
import int
import isinstance
import key
import len
import list
import next
import search_params
import self
import soft_delete
import sorted
import str
import v
import version
import version_id

logger = logging.getLogger(__name__)


class AssistantsService(BaseService):
    """Service for AI assistants management."""

    def _setup(self) -> None:
        """Initialize assistants service specific state."""

        # In-memory storage for development

        self._assistants: dict[str, dict[str, Any]] = {}

        self._config_versions: dict[str, list[dict[str, Any]]] = {}

        self._analytics_data: dict[str, dict[str, Any]] = {}

    async def create_assistant(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new AI assistant.





        Args:


            data: Assistant configuration data





        Returns:


            Created assistant data


        """

        await asyncio.sleep(0.01)  # Simulate async operation

        assistant_id = str(uuid4())

        now = datetime.now(UTC)

        assistant = {
            "id": assistant_id,
            "name": data.get("name", "Untitled Assistant"),
            "base_model": data.get("base_model", "gpt-3.5-turbo"),
            "instructions": data.get("instructions", ""),
            "tools": data.get("tools", []),
            "capabilities": data.get("capabilities", []),
            "status": "inactive",
            "owner_id": data.get("owner_id"),
            "created_by": data.get("created_by"),
            "created_at": now,
            "updated_at": now,
            "metadata": data.get("metadata", {}),
            "performance_metrics": {
                "total_interactions": 0,
                "successful_interactions": 0,
                "avg_response_time_ms": 0.0,
                "total_tokens_used": 0,
            },
        }

        self._assistants[assistant_id] = assistant

        # Create initial config version

        config_version = {
            "version_id": str(uuid4()),
            "assistant_id": assistant_id,
            "version_number": 1,
            "config_data": {
                "base_model": assistant["base_model"],
                "instructions": assistant["instructions"],
                "tools": assistant["tools"],
                "capabilities": assistant["capabilities"],
            },
            "created_at": now,
            "created_by": data.get("created_by"),
            "is_active": True,
            "change_summary": "Initial configuration",
        }

        self._config_versions[assistant_id] = [config_version]

        logger.info(f"Created assistant '{assistant['name']}' ({assistant_id})")

        return assistant

    async def get_assistant(self, assistant_id: str) -> dict[str, Any] | None:
        """Get assistant by ID.





        Args:


            assistant_id: ID of the assistant





        Returns:


            Assistant data or None if not found


        """

        await asyncio.sleep(0.01)

        return self._assistants.get(assistant_id)

    async def list_assistants(
        self, search_params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """List assistants with optional filtering.





        Args:


            search_params: Search and filter parameters





        Returns:


            List of assistant data


        """

        await asyncio.sleep(0.01)

        assistants = list(self._assistants.values())

        if not search_params:
            return assistants

        # Apply filters

        if search_params.get("owner_id"):
            assistants = [
                a for a in assistants if a.get("owner_id") == search_params["owner_id"]
            ]

        if search_params.get("status"):
            assistants = [
                a for a in assistants if a.get("status") == search_params["status"]
            ]

        if search_params.get("base_model"):
            assistants = [
                a
                for a in assistants
                if a.get("base_model") == search_params["base_model"]
            ]

        if search_params.get("capability"):
            capability = search_params["capability"]

            assistants = [
                a for a in assistants if capability in a.get("capabilities", [])
            ]

        if search_params.get("search"):
            query = search_params["search"].lower()

            assistants = [
                a
                for a in assistants
                if query in a.get("name", "").lower()
                or query in a.get("instructions", "").lower()
            ]

        # Apply sorting

        sort_by = search_params.get("sort_by", "created_at")

        sort_order = search_params.get("sort_order", "desc")

        def sort_key(assistant: dict[str, Any]) -> Any:
            value = assistant.get(sort_by)

            if isinstance(value, datetime):
                return value

            return str(value) if value is not None else ""

        assistants.sort(key=sort_key, reverse=(sort_order == "desc"))

        # Apply pagination

        offset = search_params.get("offset", 0)

        limit = search_params.get("limit", 50)

        return assistants[offset : offset + limit]

    async def update_assistant(
        self, assistant_id: str, data: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Update assistant configuration.





        Args:


            assistant_id: ID of the assistant


            data: Update data





        Returns:


            Updated assistant data or None if not found


        """

        await asyncio.sleep(0.01)

        assistant = self._assistants.get(assistant_id)

        if not assistant:
            return None

        # Track what's being updated

        updated_fields = []

        config_changed = False

        # Update fields

        for key, value in data.items():
            if key in (
                "name",
                "base_model",
                "instructions",
                "tools",
                "capabilities",
                "metadata",
                "status",
            ):
                if assistant.get(key) != value:
                    assistant[key] = value

                    updated_fields.append(key)

                    if key in ("base_model", "instructions", "tools", "capabilities"):
                        config_changed = True

        if updated_fields:
            assistant["updated_at"] = datetime.now(UTC)

            assistant["updated_by"] = data.get("updated_by")

            # Create new config version if config changed

            if config_changed:
                await self._create_config_version(assistant_id, data.get("updated_by"))

        logger.info(f"Updated assistant {assistant_id}, fields: {updated_fields}")

        return assistant

    async def delete_assistant(
        self, assistant_id: str, soft_delete: bool = True
    ) -> bool:
        """Delete assistant.





        Args:


            assistant_id: ID of the assistant


            soft_delete: Whether to soft delete (default) or permanently delete





        Returns:


            True if deleted successfully


        """

        await asyncio.sleep(0.01)

        if assistant_id not in self._assistants:
            return False

        if soft_delete:
            # Soft delete - mark as deleted

            self._assistants[assistant_id]["status"] = "deleted"

            self._assistants[assistant_id]["deleted_at"] = datetime.now(UTC)

        else:
            # Permanent delete

            del self._assistants[assistant_id]

            self._config_versions.pop(assistant_id, None)

            self._analytics_data.pop(assistant_id, None)

        logger.info(f"Deleted assistant {assistant_id} (soft_delete={soft_delete})")

        return True

    async def activate_assistant(self, assistant_id: str) -> bool:
        """Activate an assistant.





        Args:


            assistant_id: ID of the assistant





        Returns:


            True if activated successfully


        """

        await asyncio.sleep(0.01)

        assistant = self._assistants.get(assistant_id)

        if not assistant:
            return False

        assistant["status"] = "active"

        assistant["activated_at"] = datetime.now(UTC)

        logger.info(f"Activated assistant {assistant_id}")

        return True

    async def deactivate_assistant(self, assistant_id: str) -> bool:
        """Deactivate an assistant.





        Args:


            assistant_id: ID of the assistant





        Returns:


            True if deactivated successfully


        """

        await asyncio.sleep(0.01)

        assistant = self._assistants.get(assistant_id)

        if not assistant:
            return False

        assistant["status"] = "inactive"

        assistant["deactivated_at"] = datetime.now(UTC)

        logger.info(f"Deactivated assistant {assistant_id}")

        return True

    async def get_assistant_status(self, assistant_id: str) -> dict[str, Any]:
        """Get real-time status for an assistant.





        Args:


            assistant_id: ID of the assistant





        Returns:


            Status information


        """

        await asyncio.sleep(0.01)

        assistant = self._assistants.get(assistant_id)

        if not assistant:
            return {}

        return {
            "assistant_id": assistant_id,
            "status": assistant.get("status", "unknown"),
            "health": "healthy",
            "last_interaction": assistant.get("last_interaction_at"),
            "uptime_seconds": 3600,  # Mock data
            "load_level": "low",
            "active_conversations": 0,
            "queue_length": 0,
        }

    async def get_assistant_config_versions(
        self, assistant_id: str, limit: int = 20
    ) -> list[dict[str, Any]]:
        """Get configuration version history.





        Args:


            assistant_id: ID of the assistant


            limit: Maximum number of versions to return





        Returns:


            List of configuration versions


        """

        await asyncio.sleep(0.01)

        versions = self._config_versions.get(assistant_id, [])

        return sorted(versions, key=lambda v: v["created_at"], reverse=True)[:limit]

    async def rollback_assistant_config(
        self, assistant_id: str, version_id: str
    ) -> dict[str, Any] | None:
        """Rollback assistant configuration to a previous version.





        Args:


            assistant_id: ID of the assistant


            version_id: ID of the version to rollback to





        Returns:


            Updated assistant data or None if not found


        """

        await asyncio.sleep(0.01)

        assistant = self._assistants.get(assistant_id)

        if not assistant:
            return None

        # Find the version

        versions = self._config_versions.get(assistant_id, [])

        target_version = next(
            (v for v in versions if v["version_id"] == version_id), None
        )

        if not target_version:
            return None

        # Apply the configuration

        config_data = target_version["config_data"]

        assistant.update(config_data)

        assistant["updated_at"] = datetime.now(UTC)

        # Create new version for the rollback

        await self._create_config_version(
            assistant_id,
            "system",
            f"Rollback to version {target_version['version_number']}",
        )

        logger.info(f"Rolled back assistant {assistant_id} to version {version_id}")

        return assistant

    async def _create_config_version(
        self,
        assistant_id: str,
        created_by: str | None = None,
        change_summary: str | None = None,
    ) -> None:
        """Create a new configuration version.





        Args:


            assistant_id: ID of the assistant


            created_by: User who made the change


            change_summary: Summary of changes made


        """

        assistant = self._assistants.get(assistant_id)

        if not assistant:
            return

        versions = self._config_versions.get(assistant_id, [])

        # Mark previous version as inactive

        for version in versions:
            version["is_active"] = False

        # Create new version

        new_version = {
            "version_id": str(uuid4()),
            "assistant_id": assistant_id,
            "version_number": len(versions) + 1,
            "config_data": {
                "base_model": assistant["base_model"],
                "instructions": assistant["instructions"],
                "tools": assistant["tools"],
                "capabilities": assistant["capabilities"],
            },
            "created_at": datetime.now(UTC),
            "created_by": created_by,
            "is_active": True,
            "change_summary": change_summary or "Configuration updated",
        }

        versions.append(new_version)

        self._config_versions[assistant_id] = versions

    async def get_assistant_analytics(
        self, assistant_id: str, days: int = 30
    ) -> dict[str, Any]:
        """Get analytics for an assistant.





        Args:


            assistant_id: ID of the assistant


            days: Number of days to analyze





        Returns:


            Analytics data


        """

        await asyncio.sleep(0.01)

        assistant = self._assistants.get(assistant_id)

        if not assistant:
            return {}

        # Mock analytics data

        metrics = assistant.get("performance_metrics", {})

        return {
            "assistant_id": assistant_id,
            "period_days": days,
            "total_interactions": metrics.get("total_interactions", 0),
            "successful_interactions": metrics.get("successful_interactions", 0),
            "success_rate": 0.95 if metrics.get("total_interactions", 0) > 0 else 0.0,
            "avg_response_time_ms": metrics.get("avg_response_time_ms", 250.0),
            "total_tokens_used": metrics.get("total_tokens_used", 0),
            "error_count": metrics.get("error_count", 0),
            "performance_trend": [
                {"date": "2024-01-01", "interactions": 45, "success_rate": 0.95},
                {"date": "2024-01-02", "interactions": 52, "success_rate": 0.96},
                {"date": "2024-01-03", "interactions": 38, "success_rate": 0.94},
            ],
            "usage_patterns": {
                "peak_hours": [9, 10, 14, 15, 16],
                "busiest_day": "Tuesday",
                "avg_session_length": 15.5,
            },
            "top_tools_used": [
                {"tool_id": "search", "usage_count": 156, "success_rate": 0.98},
                {"tool_id": "calculator", "usage_count": 89, "success_rate": 0.99},
                {"tool_id": "weather", "usage_count": 34, "success_rate": 0.92},
            ],
        }
