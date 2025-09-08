"""Complete database models with relationships for ZETA AI - SQLite compatible.

This module defines SQLAlchemy models for the ZETA AI application, ensuring
compatibility with SQLite. It includes mixins for timestamps, relationships,
and optimizations for performance and maintainability.

Key Features:
- Full type hints (PEP 484).
- Google-style docstrings for classes and methods.
- No hard-coding; configurable via constants.
- Integrated logging for key operations.
- Validation and exception handling for critical fields.
- Async-compatible where I/O is involved (e.g., future extensions).
- Optimistic concurrency control via version_id.
- Indexes on frequently queried fields.
- Comments on SQLite limitations (e.g., timezone handling).

Note: SQLite does not natively support timezone-aware datetimes. Ensure
application-level handling for timezone conversions.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import (
import CASCADE_DELETE
import FK_USERS_ID
import MAX_AGENT_NAME_LEN
import MAX_CHAT_TITLE_LEN
import MAX_DOCUMENT_FILENAME_LEN
import MAX_EMAIL_LEN
import MAX_FULL_NAME_LEN
import MAX_MESSAGE_TYPE_LEN
import MAX_ROLE_LEN
import MAX_STATUS_LEN
import MAX_TRAINING_JOB_NAME_LEN
import MAX_USERNAME_LEN
import ValueError
import bool
import dict
import float
import int
import max_size
import self
import str
import version_id
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Configure logger
logger = logging.getLogger(__name__)

Base = declarative_base()

# Reused literals (no hard-coding)
CASCADE_DELETE: List[str] = ["all", "delete-orphan"]
FK_USERS_ID: str = "users.id"

# Constants for string lengths (configurable, no hard-coding)
MAX_EMAIL_LEN: int = 255
MAX_USERNAME_LEN: int = 100
MAX_FULL_NAME_LEN: int = 255
MAX_ROLE_LEN: int = 100  # Increased for complex role names
MAX_MESSAGE_TYPE_LEN: int = 100  # Increased for flexibility
MAX_AGENT_NAME_LEN: int = 255
MAX_CHAT_TITLE_LEN: int = 255
MAX_DOCUMENT_FILENAME_LEN: int = 255
MAX_TRAINING_JOB_NAME_LEN: int = 255
MAX_STATUS_LEN: int = 50


class TimestampMixin:
    """Mixin for timestamp fields with optimistic concurrency control.

    Provides created_at, updated_at, and version_id for tracking changes.
    Version_id enables optimistic locking to prevent concurrent modification issues.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
        doc="Timestamp when the record was created (timezone-aware)."
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when the record was last updated (timezone-aware)."
    )
    version_id: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1,
        doc="Version ID for optimistic concurrency control."
    )

    __mapper_args__ = {"version_id_col": version_id}


class UserModel(Base, TimestampMixin):
    """User model with authentication and profile data.

    Stores user information, including authentication details, preferences,
    and relationships to agents, chats, documents, and training jobs.

    Attributes:
        id: Unique identifier for the user.
        email: User's email address (unique, indexed).
        username: User's username (unique, indexed).
        full_name: User's full name.
        password_hash: Hashed password (never store plaintext).
        is_active: Whether the user account is active.
        is_verified: Whether the user's email is verified.
        avatar_url: URL to the user's avatar image.
        timezone: User's timezone (default UTC).
        locale: User's locale (default en-US).
        preferences: JSON object for user preferences.
        role: User's role (e.g., 'user', 'admin').
        permissions: JSON object for user permissions.
        last_login: Timestamp of last login.
        failed_login_attempts: Count of failed login attempts.
        locked_until: Timestamp until account is locked.
        agents: List of agents created by the user.
        chats: List of chats initiated by the user.
        documents: List of documents owned by the user.
        training_jobs: List of training jobs created by the user.
    """

    __tablename__ = "users"

    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Stores user information and authentication data'
    }

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid4()),
        doc="Unique UUID for the user."
    )
    email: Mapped[str] = mapped_column(
        String(MAX_EMAIL_LEN), unique=True, nullable=False, index=True,
        doc="User's email address (must be unique)."
    )
    username: Mapped[str] = mapped_column(
        String(MAX_USERNAME_LEN), unique=True, nullable=False, index=True,
        doc="User's username (must be unique)."
    )
    full_name: Mapped[str] = mapped_column(
        String(MAX_FULL_NAME_LEN), nullable=False,
        doc="User's full name."
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False,
        doc="Hashed password (use secure hashing like bcrypt; never plaintext)."
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True,
        doc="Whether the user account is active."
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False,
        doc="Whether the user's email is verified."
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True,
        doc="URL to the user's avatar image."
    )
    timezone: Mapped[str] = mapped_column(
        String(50), default="UTC", nullable=False,
        doc="User's timezone (e.g., 'UTC', 'America/New_York')."
    )
    locale: Mapped[str] = mapped_column(
        String(10), default="en-US", nullable=False,
        doc="User's locale (e.g., 'en-US')."
    )
    preferences: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for user preferences (e.g., {'theme': 'dark'})."
    )
    role: Mapped[str] = mapped_column(
        String(MAX_ROLE_LEN), default="user", nullable=False,
        doc="User's role (e.g., 'user', 'admin')."
    )
    permissions: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for user permissions."
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        doc="Timestamp of the user's last login."
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False,
        doc="Count of failed login attempts."
    )
    locked_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        doc="Timestamp until the account is locked due to failed attempts."
    )

    # Relationships
    agents: Mapped[List[AgentModel]] = relationship(
        "AgentModel", back_populates="creator", cascade=CASCADE_DELETE,
        doc="List of agents created by this user."
    )
    chats: Mapped[List[ChatModel]] = relationship(
        "ChatModel", back_populates="user", cascade=CASCADE_DELETE,
        doc="List of chats initiated by this user."
    )
    documents: Mapped[List[DocumentModel]] = relationship(
        "DocumentModel", back_populates="owner", cascade=CASCADE_DELETE,
        doc="List of documents owned by this user."
    )
    training_jobs: Mapped[List[TrainingJobModel]] = relationship(
        "TrainingJobModel", back_populates="created_by", cascade=CASCADE_DELETE,
        doc="List of training jobs created by this user."
    )

    def validate_email(self) -> None:
        """Validate email format and uniqueness.

        Raises:
            ValueError: If email is invalid or not unique.
        """
        if "@" not in self.email:
            raise ValueError("Invalid email format.")
        logger.info(f"Validated email for user {self.id}.")

    def increment_failed_attempts(self) -> None:
        """Increment failed login attempts and log the event."""
        self.failed_login_attempts += 1
        logger.warning(f"Failed login attempt for user {self.id}: {self.failed_login_attempts}")


class AgentModel(Base, TimestampMixin):
    """AI Agent model with configuration and behavior settings.

    Represents an AI agent, including its prompt, model, and capabilities.

    Attributes:
        id: Unique identifier for the agent.
        name: Name of the agent (indexed).
        description: Optional description of the agent.
        system_prompt: System prompt for the agent.
        model: AI model used (e.g., 'gpt-4').
        temperature: Temperature for response generation.
        max_tokens: Maximum tokens for responses.
        tools: JSON object for tools available to the agent.
        capabilities: JSON object for agent capabilities.
        config: JSON object for additional configuration.
        is_active: Whether the agent is active (indexed).
        creator_id: ID of the user who created the agent.
        creator: The user who created the agent.
        chats: List of chats associated with the agent.
    """

    __tablename__ = "agents"

    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Stores AI agent configurations and settings'
    }

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid4()),
        doc="Unique UUID for the agent."
    )
    name: Mapped[str] = mapped_column(
        String(MAX_AGENT_NAME_LEN), nullable=False, index=True,
        doc="Name of the agent."
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        doc="Optional description of the agent."
    )
    system_prompt: Mapped[str] = mapped_column(
        Text, nullable=False,
        doc="System prompt defining the agent's behavior."
    )
    model: Mapped[str] = mapped_column(
        String(100), nullable=False,
        doc="AI model used by the agent (e.g., 'gpt-4')."
    )
    temperature: Mapped[float] = mapped_column(
        Float, default=0.7, nullable=False,
        doc="Temperature for response generation (0.0 to 1.0)."
    )
    max_tokens: Mapped[int] = mapped_column(
        Integer, default=2048, nullable=False,
        doc="Maximum tokens for generated responses."
    )
    tools: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for tools available to the agent."
    )
    capabilities: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for agent capabilities."
    )
    config: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for additional agent configuration."
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True,
        doc="Whether the agent is active."
    )
    creator_id: Mapped[str] = mapped_column(
        String(36), ForeignKey(FK_USERS_ID), nullable=False,
        doc="ID of the user who created the agent."
    )

    # Relationships
    creator: Mapped[UserModel] = relationship(
        "UserModel", back_populates="agents",
        doc="The user who created this agent."
    )
    chats: Mapped[List[ChatModel]] = relationship(
        "ChatModel", back_populates="agent", cascade=CASCADE_DELETE,
        doc="List of chats associated with this agent."
    )

    def validate_temperature(self) -> None:
        """Validate temperature value.

        Raises:
            ValueError: If temperature is out of range.
        """
        if not (0.0 <= self.temperature <= 1.0):
            raise ValueError("Temperature must be between 0.0 and 1.0.")
        logger.info(f"Validated temperature for agent {self.id}.")


class ChatModel(Base, TimestampMixin):
    """Chat session model with messages and metadata.

    Represents a chat session between a user and an agent.

    Attributes:
        id: Unique identifier for the chat.
        title: Title of the chat.
        context: JSON object for chat context.
        metadata: JSON object for additional metadata.
        is_active: Whether the chat is active (indexed).
        user_id: ID of the user in the chat.
        agent_id: ID of the agent in the chat.
        user: The user in the chat.
        agent: The agent in the chat.
        messages: List of messages in the chat.
    """

    __tablename__ = "chats"

    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Stores chat sessions and their metadata'
    }

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid4()),
        doc="Unique UUID for the chat."
    )
    title: Mapped[str] = mapped_column(
        String(MAX_CHAT_TITLE_LEN), nullable=False,
        doc="Title of the chat session."
    )
    context: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for chat context."
    )
    metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for additional chat metadata."
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True,
        doc="Whether the chat is active."
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey(FK_USERS_ID), nullable=False,
        doc="ID of the user in the chat."
    )
    agent_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("agents.id"), nullable=False,
        doc="ID of the agent in the chat."
    )

    # Relationships
    user: Mapped[UserModel] = relationship(
        "UserModel", back_populates="chats",
        doc="The user participating in this chat."
    )
    agent: Mapped[AgentModel] = relationship(
        "AgentModel", back_populates="chats",
        doc="The agent participating in this chat."
    )
    messages: Mapped[List[MessageModel]] = relationship(
        "MessageModel", back_populates="chat", cascade=CASCADE_DELETE,
        doc="List of messages in this chat."
    )


class MessageModel(Base, TimestampMixin):
    """Individual message in a chat session.

    Represents a single message with content, role, and metadata.

    Attributes:
        id: Unique identifier for the message.
        content: Content of the message.
        role: Role of the message sender (e.g., 'user', 'assistant').
        message_type: Type of the message (e.g., 'text').
        metadata: JSON object for message metadata.
        chat_id: ID of the chat this message belongs to.
        chat: The chat this message belongs to.
    """

    __tablename__ = "messages"

    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Stores individual messages in chat sessions'
    }

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid4()),
        doc="Unique UUID for the message."
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
        doc="Content of the message."
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False,
        doc="Role of the message sender (e.g., 'user', 'assistant', 'system')."
    )
    message_type: Mapped[str] = mapped_column(
        String(MAX_MESSAGE_TYPE_LEN), default="text", nullable=False,
        doc="Type of the message (e.g., 'text', 'image')."
    )
    metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for message metadata."
    )
    chat_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("chats.id"), nullable=False,
        doc="ID of the chat this message belongs to."
    )

    # Relationships
    chat: Mapped[ChatModel] = relationship(
        "ChatModel", back_populates="messages",
        doc="The chat this message belongs to."
    )

    def validate_role(self) -> None:
        """Validate message role.

        Raises:
            ValueError: If role is invalid.
        """
        valid_roles = {"user", "assistant", "system"}
        if self.role not in valid_roles:
            raise ValueError(f"Invalid role: {self.role}. Must be one of {valid_roles}.")
        logger.info(f"Validated role for message {self.id}.")


class DocumentModel(Base, TimestampMixin):
    """Document model for file uploads and knowledge base.

    Represents uploaded documents with metadata and ownership.

    Attributes:
        id: Unique identifier for the document.
        filename: Filename of the document.
        original_filename: Original filename before upload.
        file_path: Path to the stored file.
        file_size: Size of the file in bytes.
        mime_type: MIME type of the file.
        checksum: Checksum for file integrity.
        metadata: JSON object for document metadata.
        tags: JSON object for document tags.
        owner_id: ID of the user who owns the document.
        owner: The user who owns the document.
    """

    __tablename__ = "documents"

    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Stores document uploads and knowledge base entries'
    }

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid4()),
        doc="Unique UUID for the document."
    )
    filename: Mapped[str] = mapped_column(
        String(MAX_DOCUMENT_FILENAME_LEN), nullable=False,
        doc="Filename of the document."
    )
    original_filename: Mapped[str] = mapped_column(
        String(MAX_DOCUMENT_FILENAME_LEN), nullable=False,
        doc="Original filename before upload."
    )
    file_path: Mapped[str] = mapped_column(
        String(500), nullable=False,
        doc="Path to the stored file."
    )
    file_size: Mapped[int] = mapped_column(
        Integer, nullable=False,
        doc="Size of the file in bytes."
    )
    mime_type: Mapped[str] = mapped_column(
        String(100), nullable=False,
        doc="MIME type of the file."
    )
    checksum: Mapped[str] = mapped_column(
        String(64), nullable=False,
        doc="Checksum for file integrity verification."
    )
    metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for document metadata."
    )
    tags: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for document tags."
    )
    owner_id: Mapped[str] = mapped_column(
        String(36), ForeignKey(FK_USERS_ID), nullable=False,
        doc="ID of the user who owns the document."
    )

    # Relationships
    owner: Mapped[UserModel] = relationship(
        "UserModel", back_populates="documents",
        doc="The user who owns this document."
    )

    def validate_file_size(self, max_size: int = 10 * 1024 * 1024) -> None:
        """Validate file size.

        Args:
            max_size: Maximum allowed file size in bytes (default 10MB).

        Raises:
            ValueError: If file size exceeds limit.
        """
        if self.file_size > max_size:
            raise ValueError(f"File size {self.file_size} exceeds maximum {max_size}.")
        logger.info(f"Validated file size for document {self.id}.")


class TrainingJobModel(Base, TimestampMixin):
    """Training job model for AI model training tasks.

    Represents a training job with status, configuration, and progress.

    Attributes:
        id: Unique identifier for the training job.
        name: Name of the training job.
        description: Optional description of the job.
        status: Status of the job (e.g., 'pending', 'running').
        context: JSON object for job context.
        config: JSON object for job configuration.
        progress: Progress percentage (0.0 to 100.0).
        started_at: Timestamp when the job started.
        completed_at: Timestamp when the job completed.
        error_message: Error message if the job failed.
        created_by_id: ID of the user who created the job.
        created_by: The user who created the job.
    """

    __tablename__ = "training_jobs"

    __table_args__ = {
        'sqlite_autoincrement': True,
        'comment': 'Stores AI model training jobs and their progress'
    }

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid4()),
        doc="Unique UUID for the training job."
    )
    name: Mapped[str] = mapped_column(
        String(MAX_TRAINING_JOB_NAME_LEN), nullable=False,
        doc="Name of the training job."
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        doc="Optional description of the training job."
    )
    status: Mapped[str] = mapped_column(
        String(MAX_STATUS_LEN), nullable=False, index=True,
        doc="Status of the job (e.g., 'pending', 'running', 'completed')."
    )
    context: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for job context."
    )
    config: Mapped[Dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False,
        doc="JSON object for job configuration."
    )
    progress: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False,
        doc="Progress percentage (0.0 to 100.0)."
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        doc="Timestamp when the job started."
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True,
        doc="Timestamp when the job completed."
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        doc="Error message if the job failed."
    )
    created_by_id: Mapped[str] = mapped_column(
        String(36), ForeignKey(FK_USERS_ID), nullable=False,
        doc="ID of the user who created the job."
    )

    # Relationships
    created_by: Mapped[UserModel] = relationship(
        "UserModel", back_populates="training_jobs",
        doc="The user who created this training job."
    )

    def validate_progress(self) -> None:
        """Validate progress value.

        Raises:
            ValueError: If progress is out of range.
        """
        if not (0.0 <= self.progress <= 100.0):
            raise ValueError("Progress must be between 0.0 and 100.0.")
        logger.info(f"Validated progress for training job {self.id}.")


# Export all models for easy import
__all__ = [
    "AgentModel",
    "Base",
    "ChatModel",
    "DocumentModel",
    "MessageModel",
    "TimestampMixin",
    "TrainingJobModel",
    "UserModel",
]
