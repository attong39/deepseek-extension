"""API configuration for ZETA AI system.

This module provides API-specific settings including versioning,
rate limiting, CORS, and API documentation.
"""

from __future__ import annotations

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import bool
import dict
import int
import isinstance
import list
import origin
import range
import str
import v
import version


class APISettings(BaseSettings):
    """API configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Basic API Settings
    api_title: str = Field(default="ZETA AI API")
    api_description: str = Field(default="Advanced AI Agent API for ZETA AI System")
    api_version: str = Field(default="1.0.0")
    api_prefix: str = Field(default="/api")

    # API Documentation
    docs_url: str = Field(default="/docs")
    redoc_url: str = Field(default="/redoc")
    openapi_url: str = Field(default="/openapi.json")
    enable_docs: bool = Field(default=True)
    include_in_schema: bool = Field(default=True)

    # API Versioning
    current_version: str = Field(default="v1")
    supported_versions: list[str] = Field(default=["v1", "v2"])
    default_version: str = Field(default="v1")
    version_header: str = Field(default="Accept-Version")

    # Request/Response Settings
    max_request_size: int = Field(default=10485760)  # 10MB
    max_response_size: int = Field(default=52428800)  # 50MB
    request_timeout: int = Field(default=30)  # seconds
    default_page_size: int = Field(default=20)
    max_page_size: int = Field(default=100)

    # Rate Limiting
    enable_rate_limiting: bool = Field(default=True)
    rate_limit_requests_per_minute: int = Field(default=100)
    rate_limit_burst_size: int = Field(default=20)
    rate_limit_storage: str = Field(default="redis")  # redis, memory, database

    # CORS Configuration
    enable_cors: bool = Field(default=True)
    cors_allow_origins: list[str] = Field(default=["*"])
    cors_allow_methods: list[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    )
    cors_allow_headers: list[str] = Field(default=["*"])
    cors_allow_credentials: bool = Field(default=True)
    cors_expose_headers: list[str] = Field(default=["X-Total-Count", "X-Page-Count"])
    cors_max_age: int = Field(default=86400)  # 24 hours

    # Security Headers
    enable_security_headers: bool = Field(default=True)
    security_headers: dict[str, str] = Field(
        default={
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
    )

    # Content Negotiation
    default_content_type: str = Field(default="application/json")
    supported_content_types: list[str] = Field(
        default=[
            "application/json",
            "application/xml",
            "text/csv",
            "application/yaml",
        ]
    )

    # API Key Authentication
    api_key_header: str = Field(default="X-API-Key")
    api_key_query_param: str = Field(default="api_key")
    require_api_key: bool = Field(default=False)

    # JWT Configuration
    jwt_header_name: str = Field(default="Authorization")
    jwt_header_type: str = Field(default="Bearer")
    jwt_token_location: list[str] = Field(
        default=["headers"]
    )  # headers, cookies, query_string

    # Caching
    enable_response_caching: bool = Field(default=True)
    cache_control_max_age: int = Field(default=300)  # 5 minutes
    etag_enabled: bool = Field(default=True)

    # Logging and Monitoring
    log_requests: bool = Field(default=True)
    log_responses: bool = Field(default=False)
    log_request_body: bool = Field(default=False)
    log_response_body: bool = Field(default=False)
    enable_metrics: bool = Field(default=True)

    # Error Handling
    include_error_details: bool = Field(default=True)
    include_stack_trace: bool = Field(default=False)
    error_response_format: str = Field(default="json")  # json, xml, plain

    # Feature Flags
    enable_webhooks: bool = Field(default=True)
    enable_websockets: bool = Field(default=True)
    enable_file_uploads: bool = Field(default=True)
    enable_batch_operations: bool = Field(default=True)
    enable_async_operations: bool = Field(default=True)

    # Pagination
    pagination_style: str = Field(default="offset")  # offset, cursor, page
    max_items_per_page: int = Field(default=1000)
    include_total_count: bool = Field(default=True)

    # API Deprecation
    deprecation_warning_header: str = Field(default="X-API-Deprecation-Warning")
    sunset_header: str = Field(default="Sunset")

    # Health Check
    health_check_endpoint: str = Field(default="/health")
    include_detailed_health: bool = Field(default=True)
    health_check_dependencies: list[str] = Field(
        default=["database", "redis", "external_apis"]
    )

    # Development Settings
    debug_mode: bool = Field(default=False)
    enable_profiling: bool = Field(default=False)
    profiling_endpoint: str = Field(default="/profiling")

    @validator("cors_allow_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @validator("supported_versions", pre=True)
    def parse_supported_versions(cls, v):
        """Parse supported versions from string or list."""
        if isinstance(v, str):
            return [version.strip() for version in v.split(",") if version.strip()]
        return v


def get_api_settings() -> APISettings:
    """Get API settings instance."""
    return APISettings()


# HTTP Status Code Groups
class HTTPStatusGroups:
    """HTTP status code group constants."""

    SUCCESS = range(200, 300)
    REDIRECT = range(300, 400)
    CLIENT_ERROR = range(400, 500)
    SERVER_ERROR = range(500, 600)


# API Response Formats
class ResponseFormat:
    """API response format constants."""

    JSON = "application/json"
    XML = "application/xml"
    CSV = "text/csv"
    YAML = "application/yaml"
    PLAIN_TEXT = "text/plain"


# API Endpoint Categories
class EndpointCategory:
    """API endpoint category constants."""

    AUTH = "authentication"
    USERS = "users"
    AGENTS = "agents"
    CONVERSATIONS = "conversations"
    MEMORY = "memory"
    FILES = "files"
    ANALYTICS = "analytics"
    ADMIN = "admin"
    SYSTEM = "system"


# Default API Responses
DEFAULT_RESPONSES = {
    400: {"description": "Bad Request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    404: {"description": "Not Found"},
    422: {"description": "Validation Error"},
    429: {"description": "Too Many Requests"},
    500: {"description": "Internal Server Error"},
    503: {"description": "Service Unavailable"},
}

# Common API Headers
COMMON_HEADERS = {
    "X-Request-ID": "Unique request identifier",
    "X-Response-Time": "Response time in milliseconds",
    "X-Rate-Limit-Remaining": "Remaining requests in current window",
    "X-Rate-Limit-Reset": "Time when rate limit window resets",
    "X-API-Version": "API version used for this request",
    "X-Correlation-ID": "Correlation ID for distributed tracing",
}

# Webhook Event Types
WEBHOOK_EVENTS = [
    "user.created",
    "user.updated",
    "user.deleted",
    "agent.created",
    "agent.updated",
    "agent.deleted",
    "conversation.created",
    "conversation.updated",
    "conversation.completed",
    "message.created",
    "memory.created",
    "memory.updated",
    "file.uploaded",
    "file.processed",
    "system.error",
    "system.warning",
]
