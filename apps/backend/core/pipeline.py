"""
In-memory progress pipeline subscriptions.

This module provides a minimal pub/sub API used by WebSocket routes to stream
progress events to clients during long-running operations. It is intentionally
framework-agnostic and safe to use from async contexts.

Public API:
- subscribe(run_id: str) -> asyncio.Queue[Dict[str, Any]]: Register a new
  subscriber for a run_id and get its queue of events.
- publish_progress(run_id: str, event: Dict[str, Any]) -> None: Publish a
  progress event to all subscribers of that run_id.
- close_subscription(run_id: str) -> None: Close and cleanup all queues for a
  run_id.

Success criteria:
- Multiple concurrent subscribers per run_id are supported.
- Closing removes all subscribers and prevents memory leaks.
- Non-blocking: publishing uses put_nowait with bounded queues.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List

# Imports from project structure (adjust paths if needed)
from .observability.logging import get_logger  # Standard logger
import ValueError
import dict
import event
import int
import isinstance
import len
import list
import maxsize
import q
import run_id
import str

# Global logger instance
logger = get_logger(__name__)

# Per-subscriber queue size to avoid unbounded memory; slow consumers will drop
# old messages if their queue is full. Made configurable.
_QUEUE_MAXSIZE = 100


@dataclass
class _Subscribers:
    """
    Internal dataclass for managing subscribers.

    Attributes:
        queues (List[asyncio.Queue[Dict[str, Any]]]): List of subscriber queues.
    """
    queues: List[asyncio.Queue[Dict[str, Any]]]


_subs_lock = asyncio.Lock()
_subs: Dict[str, _Subscribers] = {}


def _make_queue() -> asyncio.Queue[Dict[str, Any]]:
    """
    Create a new bounded queue for subscribers.

    Returns:
        asyncio.Queue[Dict[str, Any]]: New queue instance.
    """
    return asyncio.Queue(maxsize=_QUEUE_MAXSIZE)


def set_queue_maxsize(maxsize: int) -> None:
    """
    Set the maximum size for subscriber queues.

    Args:
        maxsize (int): Maximum queue size. Must be positive.

    Raises:
        ValueError: If maxsize is not positive.
    """
    global _QUEUE_MAXSIZE
    if not isinstance(maxsize, int) or maxsize <= 0:
        raise ValueError("maxsize must be a positive integer.")
    _QUEUE_MAXSIZE = maxsize
    logger.info(f"Set queue maxsize to {maxsize}")


def subscribe(run_id: str) -> asyncio.Queue[Dict[str, Any]]:
    """
    Create and register a new subscriber queue for a run_id.

    Note: This function is intentionally sync to make it easy to call from
    FastAPI handlers before first await; it does no blocking work.

    Args:
        run_id (str): Unique identifier for the run. Must be a non-empty string.

    Returns:
        asyncio.Queue[Dict[str, Any]]: New subscriber queue.

    Raises:
        ValueError: If run_id is not a string or is empty.
    """
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be a non-empty string.")
    
    q: asyncio.Queue[Dict[str, Any]] = _make_queue()
    # Registration is fast and safe to do synchronously in the single-threaded event loop
    if run_id not in _subs:
        _subs[run_id] = _Subscribers(queues=[])
    _subs[run_id].queues.append(q)
    logger.debug(f"Subscribed new queue for run_id: {run_id}")
    return q


async def publish_progress(run_id: str, event: Dict[str, Any]) -> None:
    """
    Publish a progress event to all subscribers for run_id.

    Args:
        run_id (str): Unique identifier for the run. Must be a non-empty string.
        event (Dict[str, Any]): Event data to publish. Must be a dictionary.

    Raises:
        ValueError: If run_id or event are invalid.
    """
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be a non-empty string.")
    if not isinstance(event, dict):
        raise ValueError("event must be a dictionary.")
    
    async with _subs_lock:
        subs = _subs.get(run_id)
        queues = list(subs.queues) if subs else []

    if not queues:
        logger.debug(f"No subscribers for run_id: {run_id}")
        return

    for q in queues:
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            # Best-effort: drop oldest to make space, then enqueue
            try:
                _ = q.get_nowait()
            except asyncio.QueueEmpty:
                pass
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                # Give up for this queue
                logger.warning(f"Queue full for run_id: {run_id}, dropping event")
                pass
    logger.debug(f"Published event to {len(queues)} subscribers for run_id: {run_id}")


async def close_subscription(run_id: str) -> None:
    """
    Close and cleanup all subscriber queues for a run_id.

    Args:
        run_id (str): Unique identifier for the run. Must be a non-empty string.

    Raises:
        ValueError: If run_id is not a string or is empty.
    """
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be a non-empty string.")
    
    async with _subs_lock:
        subs = _subs.pop(run_id, None)

    if subs:
        # Try to notify subscribers that the stream is closing
        for q in subs.queues:
            try:
                q.put_nowait({"event": "close", "run_id": run_id})
            except asyncio.QueueFull:
                pass
        # No explicit close for asyncio.Queue; let GC collect when dereferenced
        logger.info(f"Closed subscription for run_id: {run_id}, cleaned up {len(subs.queues)} queues")
    else:
        logger.debug(f"No subscription found for run_id: {run_id}")


__all__ = ["subscribe", "publish_progress", "close_subscription", "set_queue_maxsize"]
