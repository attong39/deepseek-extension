"""Core constants and shared values for the application.

This module contains application-wide constants, enums, and configuration values
that are shared across different layers of the application.
"""

from __future__ import annotations

from enum import Enum, IntEnum
import str


class AgentStatus(str, Enum):
    """Agent status enumeration."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AgentCapability(str, Enum):
    """Agent capability enumeration."""

    CHAT = "chat"
    ANALYSIS = "analysis"
    REASONING = "reasoning"
    PLANNING = "planning"
    LEARNING = "learning"
    MEMORY = "memory"
    VISION = "vision"
    VOICE = "voice"
    CODE = "code"
    RESEARCH = "research"


class ChatStatus(str, Enum):
    """Chat status enumeration."""

    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    ERROR = "error"


class ChatType(str, Enum):
    """Chat type enumeration."""

    INDIVIDUAL = "individual"
    GROUP = "group"
    AGENT_CHAT = "agent_chat"
    SYSTEM = "system"


class MessageType(str, Enum):
    """Message type enumeration."""

    # Legacy chat tests expect USER and ASSISTANT as message types
    USER = "user"
    ASSISTANT = "assistant"
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"
    SYSTEM = "system"
    ERROR = "error"


class MessageStatus(str, Enum):
    """Message delivery/processing status enumeration (legacy compatibility)."""

    SENT = "sent"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    FAILED = "failed"


class MessageRole(str, Enum):
    """Message role enumeration."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"


class MemoryType(str, Enum):
    """Memory type enumeration."""

    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    WORKING = "working"
    AUTOBIOGRAPHICAL = "autobiographical"


class MemoryImportance(IntEnum):
    """Memory importance levels."""

    LOW = 1
    MEDIUM = 3
    HIGH = 5
    CRITICAL = 7
    ESSENTIAL = 10


class PlanStatus(str, Enum):
    """Plan status enumeration."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PlanPriority(IntEnum):
    """Plan priority levels."""

    LOW = 1
    NORMAL = 3
    HIGH = 5
    URGENT = 7
    CRITICAL = 10


class TaskStatus(str, Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"


class UserRole(str, Enum):
    """User role enumeration."""

    GUEST = "guest"
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class UserStatus(str, Enum):
    """User status enumeration."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class EventType(str, Enum):
    """Event type enumeration."""

    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    AGENT_CREATED = "agent_created"
    AGENT_ACTIVATED = "agent_activated"
    AGENT_DEACTIVATED = "agent_deactivated"
    CHAT_STARTED = "chat_started"
    CHAT_ENDED = "chat_ended"
    MESSAGE_SENT = "message_sent"
    MEMORY_CREATED = "memory_created"
    PLAN_CREATED = "plan_created"
    PLAN_EXECUTED = "plan_executed"
    ERROR_OCCURRED = "error_occurred"


class LogLevel(str, Enum):
    """Logging level enumeration."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


# Application Constants
APP_NAME = "Zeta AI Server"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Advanced AI Agent Server with Memory, Planning, and Reflection"

# Database Constants
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 1000
DEFAULT_TIMEOUT = 30  # seconds

# Memory Constants
DEFAULT_MEMORY_RETENTION_DAYS = 365
MAX_MEMORY_SIZE = 1000000  # characters
MEMORY_COMPRESSION_THRESHOLD = 100  # number of memories

# Agent Constants
MAX_AGENTS_PER_USER = 10
DEFAULT_AGENT_TIMEOUT = 300  # seconds
MAX_CONCURRENT_CHATS = 5

# Chat Constants
MAX_MESSAGE_LENGTH = 10000  # characters
MAX_CHAT_HISTORY = 1000  # messages
CHAT_INACTIVITY_TIMEOUT = 3600  # seconds

# File Constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_FILE_TYPES = {
    "text/plain",
    "text/markdown",
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/gif",
    "audio/mpeg",
    "audio/wav",
    "video/mp4",
}

# API Constants
API_V1_PREFIX = "/api/v1"
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
RATE_LIMIT_PER_MINUTE = 60

# Security Constants
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24
PASSWORD_MIN_LENGTH = 8
SESSION_TIMEOUT_HOURS = 24

# Cache Constants
CACHE_TTL_SECONDS = 3600  # 1 hour
CACHE_MAX_SIZE = 1000

# Error Messages
ERROR_MESSAGES = {
    "INVALID_INPUT": "Invalid input provided",
    "NOT_FOUND": "Resource not found",
    "UNAUTHORIZED": "Unauthorized access",
    "FORBIDDEN": "Access forbidden",
    "RATE_LIMITED": "Rate limit exceeded",
    "SERVER_ERROR": "Internal server error",
    "DATABASE_ERROR": "Database operation failed",
    "VALIDATION_ERROR": "Validation failed",
}

# Success Messages
SUCCESS_MESSAGES = {
    "CREATED": "Resource created successfully",
    "UPDATED": "Resource updated successfully",
    "DELETED": "Resource deleted successfully",
    "RETRIEVED": "Resource retrieved successfully",
}

# Default Values
DEFAULT_VALUES = {
    "agent_status": AgentStatus.INACTIVE,
    "chat_status": ChatStatus.ACTIVE,
    "message_role": MessageRole.USER,
    "memory_importance": MemoryImportance.MEDIUM,
    "plan_priority": PlanPriority.NORMAL,
    "user_role": UserRole.USER,
    "user_status": UserStatus.ACTIVE,
}
