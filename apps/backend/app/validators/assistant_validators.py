"""Validators for assistant-related data.





Provides validation functions for assistant names, tools, permissions,


and other business logic constraints.


"""

from __future__ import annotations

import re
from typing import Any
import ValueError
import assistant_data
import assistants
import bool
import config
import current_depth
import dict
import e
import enumerate
import float
import i
import int
import isinstance
import item
import key
import len
import list
import max
import metadata
import name
import obj
import operation_data
import params
import permissions
import required_perm
import set
import sorted
import str
import tool_id
import tools
import type
import user_permissions
import v
import value

# Constants for validation


MIN_NAME_LENGTH = 2


MAX_NAME_LENGTH = 64


MAX_TOOLS_PER_ASSISTANT = 20


VALID_TOOL_ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


RESERVED_NAMES = {
    "admin",
    "system",
    "root",
    "api",
    "bot",
    "assistant",
    "test",
    "demo",
    "default",
    "public",
    "private",
}


class AssistantValidationError(ValueError):
    """Custom exception for assistant validation errors."""


def validate_assistant_name(name: str) -> None:
    """Validate assistant name according to business rules.





    Args:


        name: Assistant name to validate





    Raises:


        AssistantValidationError: If name is invalid


    """

    if not name or not isinstance(name, str):
        raise AssistantValidationError("Assistant name is required")

    name_clean = name.strip()

    if len(name_clean) < MIN_NAME_LENGTH:
        raise AssistantValidationError(
            f"Assistant name must be at least {MIN_NAME_LENGTH} characters"
        )

    if len(name_clean) > MAX_NAME_LENGTH:
        raise AssistantValidationError(
            f"Assistant name must be no more than {MAX_NAME_LENGTH} characters"
        )

    # Check for reserved names

    if name_clean.lower() in RESERVED_NAMES:
        raise AssistantValidationError(
            f"'{name_clean}' is a reserved name and cannot be used"
        )

    # Check for valid characters (alphanumeric, spaces, hyphens, underscores)

    if not re.match(r"^[a-zA-Z0-9\s_-]+$", name_clean):
        raise AssistantValidationError(
            "Assistant name can only contain letters, numbers, spaces, hyphens, and underscores"
        )

    # Check for consecutive spaces

    if re.search(r"\s{2,}", name_clean):
        raise AssistantValidationError("Assistant name cannot have consecutive spaces")

    # Check for leading/trailing special characters

    if re.match(r"^[_-]", name_clean) or re.search(r"[_-]$", name_clean):
        raise AssistantValidationError(
            "Assistant name cannot start or end with special characters"
        )


def validate_assistant_tools(tools: list[str]) -> None:
    """Validate assistant tools list.





    Args:


        tools: List of tool IDs to validate





    Raises:


        AssistantValidationError: If tools list is invalid


    """

    if not isinstance(tools, list):
        raise AssistantValidationError("Tools must be a list")

    if len(tools) > MAX_TOOLS_PER_ASSISTANT:
        raise AssistantValidationError(
            f"Maximum {MAX_TOOLS_PER_ASSISTANT} tools allowed per assistant"
        )

    # Check for duplicates

    if len(tools) != len(set(tools)):
        raise AssistantValidationError("Duplicate tools are not allowed")

    # Validate each tool ID

    for tool_id in tools:
        if not isinstance(tool_id, str):
            raise AssistantValidationError("Tool IDs must be strings")

        if not tool_id.strip():
            raise AssistantValidationError("Tool IDs cannot be empty")

        if len(tool_id) > 50:
            raise AssistantValidationError("Tool IDs must be 50 characters or less")

        if not VALID_TOOL_ID_PATTERN.match(tool_id):
            raise AssistantValidationError(
                f"Invalid tool ID '{tool_id}'. Only alphanumeric characters, hyphens, and underscores are allowed"
            )


def validate_assistant_permissions(
    permissions: list[str], user_permissions: list[str]
) -> None:
    """Validate that user has required permissions for assistant operations.





    Args:


        permissions: Required permissions for the operation


        user_permissions: User's current permissions





    Raises:


        AssistantValidationError: If user lacks required permissions


    """

    if not isinstance(permissions, list) or not isinstance(user_permissions, list):
        raise AssistantValidationError("Permissions must be lists")

    # Check if user has admin wildcard permission

    if "*" in user_permissions or "admin:*" in user_permissions:
        return

    # Check each required permission

    missing_permissions = []

    for required_perm in permissions:
        if required_perm not in user_permissions:
            # Check for wildcard permissions (e.g., assistant:* covers assistant:create)

            perm_category = (
                required_perm.split(":")[0] if ":" in required_perm else required_perm
            )

            wildcard_perm = f"{perm_category}:*"

            if wildcard_perm not in user_permissions:
                missing_permissions.append(required_perm)

    if missing_permissions:
        raise AssistantValidationError(
            f"Missing required permissions: {', '.join(missing_permissions)}"
        )


def _validate_base_model(config: dict[str, Any]) -> None:
    """Validate base model in configuration."""

    if "base_model" not in config:
        return

    base_model = config["base_model"]

    if not isinstance(base_model, str) or not base_model.strip():
        raise AssistantValidationError("Base model must be a non-empty string")

    # List of supported models (extend as needed)

    supported_models = {
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "claude-3-haiku",
        "claude-3-sonnet",
        "claude-3-opus",
        "gemini-pro",
        "gemini-ultra",
    }

    if base_model not in supported_models:
        raise AssistantValidationError(
            f"Unsupported base model '{base_model}'. "
            f"Supported models: {', '.join(sorted(supported_models))}"
        )


def _validate_temperature(config: dict[str, Any]) -> None:
    """Validate temperature in configuration."""

    if "temperature" not in config:
        return

    temp = config["temperature"]

    if not isinstance(temp, (int, float)) or temp < 0 or temp > 2:
        raise AssistantValidationError("Temperature must be a number between 0 and 2")


def _validate_max_tokens(config: dict[str, Any]) -> None:
    """Validate max_tokens in configuration."""

    if "max_tokens" not in config:
        return

    max_tokens = config["max_tokens"]

    if not isinstance(max_tokens, int) or max_tokens < 1 or max_tokens > 128000:
        raise AssistantValidationError(
            "Max tokens must be an integer between 1 and 128000"
        )


def _validate_instructions(config: dict[str, Any]) -> None:
    """Validate instructions in configuration."""

    if "instructions" not in config:
        return

    instructions = config["instructions"]

    if isinstance(instructions, str) and len(instructions) > 10000:
        raise AssistantValidationError("Instructions must be 10000 characters or less")


def validate_assistant_config(config: dict[str, Any]) -> None:
    """Validate assistant configuration data.





    Args:


        config: Configuration dictionary to validate





    Raises:


        AssistantValidationError: If configuration is invalid


    """

    if not isinstance(config, dict):
        raise AssistantValidationError("Configuration must be a dictionary")

    _validate_base_model(config)

    _validate_temperature(config)

    _validate_max_tokens(config)

    _validate_instructions(config)


def _validate_metadata_keys(metadata: dict[str, Any]) -> None:
    """Validate metadata keys."""

    for key in metadata:
        if not isinstance(key, str):
            raise AssistantValidationError("Metadata keys must be strings")

        if len(key) > 100:
            raise AssistantValidationError(
                "Metadata keys must be 100 characters or less"
            )

        # Check for reserved metadata keys

        if key.startswith("_system_") or key.startswith("_internal_"):
            raise AssistantValidationError(f"Metadata key '{key}' is reserved")


def _validate_metadata_values(metadata: dict[str, Any]) -> None:
    """Validate metadata values."""

    for value in metadata.values():
        # Validate value types (allow basic JSON-serializable types)

        if not isinstance(value, (str, int, float, bool, type(None))):
            if isinstance(value, (list, dict)):
                # Allow simple lists and dicts but check nesting depth

                if _get_nesting_depth(value) > 3:
                    raise AssistantValidationError(
                        "Metadata values cannot be nested more than 3 levels deep"
                    )

            else:
                raise AssistantValidationError(
                    "Metadata values must be strings, numbers, booleans, null, or simple lists/objects"
                )


def validate_assistant_metadata(metadata: dict[str, Any]) -> None:
    """Validate assistant metadata.





    Args:


        metadata: Metadata dictionary to validate





    Raises:


        AssistantValidationError: If metadata is invalid


    """

    if not isinstance(metadata, dict):
        raise AssistantValidationError("Metadata must be a dictionary")

    # Check metadata size

    if len(metadata) > 50:
        raise AssistantValidationError("Maximum 50 metadata fields allowed")

    _validate_metadata_keys(metadata)

    _validate_metadata_values(metadata)


def _get_nesting_depth(obj: Any, current_depth: int = 0) -> int:
    """Calculate the nesting depth of a data structure.





    Args:


        obj: Object to analyze


        current_depth: Current depth level





    Returns:


        Maximum nesting depth


    """

    if current_depth > 10:  # Prevent infinite recursion
        return current_depth

    if isinstance(obj, dict):
        if not obj:  # Empty dict
            return current_depth

        return max(_get_nesting_depth(v, current_depth + 1) for v in obj.values())

    elif isinstance(obj, list):
        if not obj:  # Empty list
            return current_depth

        return max(_get_nesting_depth(item, current_depth + 1) for item in obj)

    else:
        return current_depth


def _validate_batch_assistants(assistants: list[Any]) -> None:
    """Validate assistants list in batch operation."""

    if not isinstance(assistants, list):
        raise AssistantValidationError("Assistants must be a list")

    if len(assistants) == 0:
        raise AssistantValidationError("At least one assistant is required")

    if len(assistants) > 50:
        raise AssistantValidationError("Maximum 50 assistants per batch operation")

    # Validate each assistant in the batch

    for i, assistant_data in enumerate(assistants):
        try:
            if isinstance(assistant_data, dict) and "name" in assistant_data:
                validate_assistant_name(assistant_data["name"])

            if isinstance(assistant_data, dict) and "tools" in assistant_data:
                validate_assistant_tools(assistant_data["tools"])

        except AssistantValidationError as e:
            raise AssistantValidationError(f"Assistant {i + 1}: {e!s}") from e


def validate_batch_operation(operation_data: dict[str, Any]) -> None:
    """Validate batch operation parameters.





    Args:


        operation_data: Batch operation data to validate





    Raises:


        AssistantValidationError: If batch operation is invalid


    """

    if not isinstance(operation_data, dict):
        raise AssistantValidationError("Batch operation data must be a dictionary")

    # Check batch size limits

    if "assistants" in operation_data:
        _validate_batch_assistants(operation_data["assistants"])


def _validate_pagination_params(params: dict[str, Any]) -> None:
    """Validate pagination parameters."""

    if "limit" in params:
        limit = params["limit"]

        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise AssistantValidationError("Limit must be an integer between 1 and 100")

    if "offset" in params:
        offset = params["offset"]

        if not isinstance(offset, int) or offset < 0:
            raise AssistantValidationError("Offset must be a non-negative integer")


def _validate_sort_params(params: dict[str, Any]) -> None:
    """Validate sort parameters."""

    if "sort_by" in params:
        sort_by = params["sort_by"]

        valid_sort_fields = {"name", "created_at", "updated_at", "status", "base_model"}

        if sort_by not in valid_sort_fields:
            raise AssistantValidationError(
                f"Invalid sort field '{sort_by}'. "
                f"Valid fields: {', '.join(sorted(valid_sort_fields))}"
            )

    if "sort_order" in params:
        sort_order = params["sort_order"]

        if sort_order not in ("asc", "desc"):
            raise AssistantValidationError("Sort order must be 'asc' or 'desc'")


def _validate_search_query(params: dict[str, Any]) -> None:
    """Validate search query."""

    if "search" in params:
        search = params["search"]

        if isinstance(search, str) and len(search) > 500:
            raise AssistantValidationError(
                "Search query must be 500 characters or less"
            )


def validate_search_parameters(params: dict[str, Any]) -> None:
    """Validate search parameters for assistant listing.





    Args:


        params: Search parameters to validate





    Raises:


        AssistantValidationError: If search parameters are invalid


    """

    if not isinstance(params, dict):
        raise AssistantValidationError("Search parameters must be a dictionary")

    _validate_pagination_params(params)

    _validate_sort_params(params)

    _validate_search_query(params)
