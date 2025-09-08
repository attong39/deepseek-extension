"""Event schema versioning và upcasting system."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

# Type alias for upcaster function
Upcaster = Callable[[dict[str, Any]], dict[str, Any]]

# Registry of all upcasters: (event_type, from_version) -> upcaster_function
_UPCASTERS: dict[tuple[str, int], Upcaster] = {}


def register_upcaster(event_type: str, from_version: int):
    """
import Exception
import dict
import e
import event_type
import evt_type
import fn
import from_version
import int
import len
import list
import max
import payload
import result
import str
import tuple
import version
import versions
    Decorator to register an upcaster for a specific event type and version.

    Args:
        event_type: The event type to upcast (e.g., "MemoryChunked")
        from_version: The version to upcast from (e.g., 1 -> 2)

    Example:
        @register_upcaster("MemoryChunked", 1)
        def memory_chunked_v1_to_v2(payload: dict) -> dict:
            # Add source field if missing
            payload.setdefault("source", "unknown")
            return payload
    """

    def _decorator(fn: Upcaster) -> Upcaster:
        key = (event_type, from_version)
        if key in _UPCASTERS:
            logger.warning(
                f"Overriding existing upcaster for {event_type} v{from_version}"
            )

        _UPCASTERS[key] = fn
        logger.info(
            f"Registered upcaster: {event_type} v{from_version} -> v{from_version + 1}"
        )
        return fn

    return _decorator


def upcast_event(
    event_type: str, version: int, payload: dict[str, Any]
) -> tuple[int, dict[str, Any]]:
    """
    Upcast an event payload to the latest version.

    Args:
        event_type: The type of event to upcast
        version: Current version of the payload
        payload: The event payload data

    Returns:
        Tuple of (new_version, new_payload)

    Example:
        >>> new_ver, new_payload = upcast_event("MemoryChunked", 1, old_data)
        >>> assert new_ver == 2
        >>> assert "source" in new_payload
    """
    current_version = version
    current_payload = payload.copy()  # Don't mutate original

    upcasts_applied = 0
    max_upcasts = 10  # Prevent infinite loops

    while upcasts_applied < max_upcasts:
        key = (event_type, current_version)

        if key not in _UPCASTERS:
            # No more upcasters available
            break

        try:
            upcaster = _UPCASTERS[key]
            logger.debug(
                f"Applying upcaster for {event_type} v{current_version} -> v{current_version + 1}"
            )

            current_payload = upcaster(current_payload)
            current_version += 1
            upcasts_applied += 1

        except Exception as e:
            logger.error(f"Failed to upcast {event_type} from v{current_version}: {e}")
            # Return what we have so far rather than failing completely
            break

    if upcasts_applied > 0:
        logger.info(
            f"Upcasted {event_type} from v{version} to v{current_version} ({upcasts_applied} steps)"
        )

    return current_version, current_payload


def get_latest_version(event_type: str) -> int:
    """
    Get the latest known version for an event type.

    Args:
        event_type: The event type to check

    Returns:
        The highest version number available
    """
    max_version = 1  # Default starting version

    for evt_type, version in _UPCASTERS:
        if evt_type == event_type:
            max_version = max(
                max_version, version + 1
            )  # +1 because upcaster produces next version

    return max_version


def list_available_upcasters() -> dict[str, list[int]]:
    """
    List all available upcasters grouped by event type.

    Returns:
        Dict mapping event_type -> list of available from_versions
    """
    result: dict[str, list[int]] = {}

    for event_type, from_version in _UPCASTERS:
        if event_type not in result:
            result[event_type] = []
        result[event_type].append(from_version)

    # Sort versions for each event type
    for versions in result.values():
        versions.sort()

    return result


# Standard upcasters for common events
@register_upcaster("MemoryChunked", 1)
def memory_chunked_v1_to_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """
    MemoryChunked v1 -> v2: Add source field.

    Changes:
    - Add 'source' field with default value 'unknown'
    - Ensure metadatas list has same length as texts
    """
    # Add source field if missing
    payload.setdefault("source", "unknown")

    # Ensure metadatas exists and has correct length
    texts = payload.get("texts", [])
    metadatas = payload.get("metadatas", [])

    # Pad metadatas to match texts length
    while len(metadatas) < len(texts):
        metadatas.append({})

    payload["metadatas"] = metadatas

    return payload


@register_upcaster("AgentCreated", 1)
def agent_created_v1_to_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """
    AgentCreated v1 -> v2: Add capabilities field.

    Changes:
    - Add 'capabilities' field with default capabilities
    - Add 'created_by' field for audit trail
    """
    # Add default capabilities
    payload.setdefault(
        "capabilities", ["text_generation", "memory_storage", "conversation"]
    )

    # Add audit field
    payload.setdefault("created_by", "system")

    return payload


@register_upcaster("MemoryIngested", 1)
def memory_ingested_v1_to_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """
    MemoryIngested v1 -> v2: Add processing metrics.

    Changes:
    - Add 'processing_time_ms' field
    - Add 'chunk_sizes' distribution info
    """
    # Add processing metrics
    payload.setdefault("processing_time_ms", 0)
    payload.setdefault("chunk_sizes", [])

    # If chunks_count exists but chunk_sizes is empty, estimate
    chunks_count = payload.get("chunks_count", 0)
    if chunks_count > 0 and not payload["chunk_sizes"]:
        # Estimate average chunk size
        payload["chunk_sizes"] = [100] * chunks_count  # Default 100 chars per chunk

    return payload


# Example of more complex migration
@register_upcaster("AgentActivated", 1)
def agent_activated_v1_to_v2(payload: dict[str, Any]) -> dict[str, Any]:
    """
    AgentActivated v1 -> v2: Restructure status field.

    Changes:
    - Convert 'status' string to 'activation' object
    - Add 'activated_at' timestamp
    """
    # Convert status to activation object
    old_status = payload.get("status", "active")

    activation = {
        "state": old_status,
        "activated_at": payload.get("activated_at", "1970-01-01T00:00:00Z"),
        "reason": "automatic",
    }

    # Remove old field and add new structure
    if "status" in payload:
        del payload["status"]

    payload["activation"] = activation

    return payload
