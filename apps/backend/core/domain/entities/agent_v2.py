"""
Agent Entity v2 - Domain-driven design pattern with owner tracking.

Entity immutable với strong typing, validation và business logic.
Sử dụng composition thay vì inheritance cho cleaner design.
Includes owner_user_id for multi-tenant support.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Union
from uuid import UUID, uuid4

from app._base_model import DomainModel
from apps.backend.core.domain.value_objects.agent.agent_config import AgentConfig
from apps.backend.core.domain.value_objects.agent.agent_lifecycle_status import (
import ValueError
import bool
import cap
import capabilities
import capability
import caps
import classmethod
import config
import dict
import int
import isinstance
import reason
import self
import set
import sorted
import str
import tag
import tags
import tuple
import update_data
import user_id
import v
    AgentLifecycleStatus,
)
from pydantic import Field, field_validator, model_validator

# Capabilities được phép - business rule
_ALLOWED_CAPABILITIES = {
    "chat",
    "vision",
    "voice",
    "planning",
    "tools",
    "automation",
    "analysis",
    "research",
    "coding",
}


class AgentCapability(str, Enum):
    """Agent capability types."""

    CHAT = "chat"
    VISION = "vision"
    VOICE = "voice"
    PLANNING = "planning"
    TOOLS = "tools"
    AUTOMATION = "automation"
    ANALYSIS = "analysis"
    RESEARCH = "research"
    CODING = "coding"


class AgentStatus(str, Enum):
    """Agent status levels."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    DISABLED = "disabled"
    TRAINING = "training"
    ERROR = "error"


class AgentTier(str, Enum):
    """Agent tier levels."""

    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class Agent(DomainModel):
    """
    Agent entity v2 theo pattern DDD với owner tracking.

    Immutable entity với strong business rules và type safety.
    Includes owner_user_id for multi-tenant support.

    Business Rules:
    - name không được rỗng và unique trong namespace
    - capabilities phải trong danh sách cho phép
    - agent BUSY/TRAINING phải có ít nhất 1 capability
    - config phải valid theo AgentConfig schema
    - owner_user_id phải được cung cấp

    Examples:
        # Tạo agent mới
        _ = Agent(
            owner_user_id="user123",
            name="Research Assistant",
            capabilities=("research", "analysis"),
            config=AgentConfig(max_concurrency=3)
        )

        # Kích hoạt agent
        active__ = agent.activate()

        # Thêm capabilities
        enhanced = agent.with_capabilities(("voice", "chat"))
    """

    # Identity
    id: UUID = Field(default_factory=uuid4, description="Unique identifier cho Agent")

    # Ownership
    owner_user_id: str = Field(
        ..., min_length=1, max_length=36, description="ID của user sở hữu agent"
    )

    # Core attributes
    name: str = Field(
        ..., min_length=1, max_length=200, description="Tên hiển thị của agent"
    )

    # Status và capabilities
    status: AgentLifecycleStatus = Field(
        default=AgentLifecycleStatus.INACTIVE,
        description="Trạng thái lifecycle hiện tại",
    )

    capabilities: tuple[str, ...] = Field(
        default=(), description="Danh sách khả năng của agent"
    )

    # Configuration
    config: Union[dict[str, Any], AgentConfig] = Field(
        default_factory=dict, description="Cấu hình runtime của agent"
    )

    # Version control for optimistic concurrency
    version: int = Field(
        default=1, description="Version for optimistic concurrency control"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when agent was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when agent was last updated"
    )

    # Metadata
    tags: tuple[str, ...] = Field(default=(), description="Tags để phân loại và search")

    description: str = Field(
        default="", max_length=1000, description="Mô tả chi tiết về agent"
    )

    @field_validator("name")
    @classmethod
    def _validate_name(cls, v: str) -> str:
        """Validate name không rỗng và trim whitespace."""
        if not v.strip():
            raise ValueError("Agent name must not be empty")
        return v.strip()

    @field_validator("owner_user_id")
    @classmethod
    def _validate_owner_user_id(cls, v: str) -> str:
        """Validate owner_user_id không rỗng và trim whitespace."""
        if not v.strip():
            raise ValueError("Owner user ID must not be empty")
        return v.strip()

    @field_validator("capabilities")
    @classmethod
    def _validate_capabilities(cls, caps: Iterable[str]) -> tuple[str, ...]:
        """
        Validate capabilities trong danh sách cho phép và unique.

        Returns:
            Sorted tuple of unique valid capabilities

        Raises:
            ValueError: Nếu có capability không hợp lệ
        """
        unique_caps = tuple(
            sorted({cap.lower().strip() for cap in caps if cap.strip()})
        )

        invalid_caps = [cap for cap in unique_caps if cap not in _ALLOWED_CAPABILITIES]
        if invalid_caps:
            raise ValueError(
                f"Invalid capabilities: {invalid_caps}. Allowed: {sorted(_ALLOWED_CAPABILITIES)}"
            )

        return unique_caps

    @field_validator("tags")
    @classmethod
    def _validate_tags(cls, tags: Iterable[str]) -> tuple[str, ...]:
        """Validate và normalize tags."""
        return tuple(sorted({tag.lower().strip() for tag in tags if tag.strip()}))

    @field_validator("config", mode="before")
    @classmethod
    def _validate_config(cls, config: Union[dict[str, Any], AgentConfig]) -> AgentConfig:
        """Convert dict config to AgentConfig if needed."""
        if isinstance(config, dict):
            # Convert dict to AgentConfig, using defaults for missing keys
            return AgentConfig(
                model=config.get("model", "gpt-4o-mini"),
                temperature=config.get("temperature", 0.7),
                top_p=config.get("top_p", 1.0),
                max_tokens=config.get("max_tokens", 1024),
                presence_penalty=config.get("presence_penalty", 0.0),
                frequency_penalty=config.get("frequency_penalty", 0.0),
            )
        return config

    @model_validator(mode="after")
    def _validate_busy_has_capabilities(self) -> Agent:
        """
        Business rule: Agent BUSY hoặc TRAINING phải có capabilities.
        """
        operational_statuses = {
            AgentLifecycleStatus.BUSY,
            AgentLifecycleStatus.TRAINING,
        }

        if self.status in operational_statuses and not self.capabilities:
            raise ValueError(
                f"Agent with status {self.status.value} must have at least one capability"
            )

        return self

    # === Business Methods (trả về bản sao mới do immutability) ===

    def activate(self) -> Agent:
        """
        Kích hoạt agent (chuyển sang ACTIVE).

        Returns:
            Agent mới với status ACTIVE và updated timestamp
        """
        return self.model_copy(
            update={
                "status": AgentLifecycleStatus.ACTIVE,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def assign_task(self) -> Agent:
        """
        Chuyển agent sang BUSY khi gán task.

        Returns:
            Agent mới với status BUSY

        Raises:
            ValueError: Nếu agent không thể nhận task
        """
        if self.status not in {AgentLifecycleStatus.ACTIVE}:
            raise ValueError(
                f"Cannot assign task to agent with status {self.status.value}"
            )

        return self.model_copy(
            update={
                "status": AgentLifecycleStatus.BUSY,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def complete_task(self) -> Agent:
        """
        Hoàn thành task và về ACTIVE.
        """
        if self.status != AgentLifecycleStatus.BUSY:
            raise ValueError("Only BUSY agents can complete tasks")

        return self.model_copy(
            update={
                "status": AgentLifecycleStatus.ACTIVE,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def with_capabilities(self, caps: Iterable[str]) -> Agent:
        """
        Tạo bản sao với capabilities mới.

        Args:
            caps: Danh sách capabilities mới

        Returns:
            Agent mới với capabilities được cập nhật
        """
        return self.model_copy(
            update={
                "capabilities": self._validate_capabilities(caps),
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def add_capability(self, capability: str) -> Agent:
        """
        Thêm một capability mới.

        Args:
            capability: Capability cần thêm

        Returns:
            Agent mới với capability đã thêm
        """
        new_caps = set(self.capabilities)
        new_caps.add(capability.lower().strip())
        return self.with_capabilities(new_caps)

    def remove_capability(self, capability: str) -> Agent:
        """
        Xóa một capability.

        Args:
            capability: Capability cần xóa

        Returns:
            Agent mới với capability đã xóa
        """
        new_caps = set(self.capabilities)
        new_caps.discard(capability.lower().strip())
        return self.with_capabilities(new_caps)

    def with_config(self, config: AgentConfig) -> Agent:
        """
        Cập nhật configuration.

        Args:
            config: Configuration mới

        Returns:
            Agent mới với config đã cập nhật
        """
        return self.model_copy(
            update={
                "config": config,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def suspend(self, reason: str = "") -> Agent:
        """
        Tạm ngưng agent.

        Args:
            reason: Lý do suspend (optional)

        Returns:
            Agent mới với status SUSPENDED
        """
        update_data: dict[str, Any] = {
            "status": AgentLifecycleStatus.SUSPENDED,
            "updated_at": datetime.now(UTC),
            "version": self.version + 1,
        }

        if reason:
            # Thêm reason vào tags để track
            new_tags = set(self.tags)
            new_tags.add(f"suspended:{reason.lower()}")
            update_data["tags"] = tuple(sorted(new_tags))

        return self.model_copy(update=update_data)

    # === Query Methods ===

    def has_capability(self, capability: str) -> bool:
        """Kiểm tra agent có capability không."""
        return capability.lower().strip() in self.capabilities

    def has_any_capability(self, capabilities: Iterable[str]) -> bool:
        """Kiểm tra agent có bất kỳ capability nào không."""
        caps_set = {cap.lower().strip() for cap in capabilities}
        return bool(caps_set.intersection(self.capabilities))

    def has_all_capabilities(self, capabilities: Iterable[str]) -> bool:
        """Kiểm tra agent có tất cả capabilities không."""
        caps_set = {cap.lower().strip() for cap in capabilities}
        return caps_set.issubset(set(self.capabilities))

    def is_operational(self) -> bool:
        """Kiểm tra agent có thể hoạt động không."""
        return self.status.is_operational()

    def can_accept_tasks(self) -> bool:
        """Kiểm tra agent có thể nhận task mới không."""
        return self.status == AgentLifecycleStatus.ACTIVE

    def is_owned_by(self, user_id: str) -> bool:
        """Kiểm tra agent có được sở hữu bởi user không."""
        return self.owner_user_id == user_id


__all__ = ["Agent", "AgentCapability", "AgentStatus", "AgentTier"]
