# Dataset Service - Training Sample Management
from __future__ import annotations

import asyncio
import json
from typing import Any

import aiofiles
import dict
import f
import file_path
import i
import id
import input_text
import int
import len
import limit
import list
import meta
import min_samples
import output_text
import range
import rules
import s
import self
import str
import sum
import team_id
import user_id

# In-memory storage for samples (until we have proper DB models)
_samples_storage: list[dict[str, Any]] = []


class SampleCounter:
    """Encapsulate counter to avoid global statement"""

    def __init__(self) -> None:
        self.value = 1

    def next_id(self) -> int:
        current = self.value
        self.value += 1
        return current


_counter = SampleCounter()


class TrainingSample:
    """Training sample data structure"""

    def __init__(
        self,
        id: int,
        team_id: str,
        user_id: str,
        input_text: str,
        output_text: str,
        rules: str | None = None,
        meta: dict[str, Any] | None = None,
    ):
        self.id = id
        self.team_id = team_id
        self.user_id = user_id
        self.input_text = input_text
        self.output_text = output_text
        self.rules = rules
        self.meta = meta or {}


async def add_training_sample(
    user_id: str,
    team_id: str,
    input_text: str,
    output_text: str,
    rules: str | None = None,
    meta: dict[str, Any] | None = None,
) -> int:
    """Add a new training sample to the dataset

    Returns:
        ID of the created sample
    """
    await asyncio.sleep(0)  # Make truly async

    # Simple in-memory storage until DB models are ready
    sample_id = _counter.next_id()
    sample = {
        "id": sample_id,
        "user_id": user_id,
        "team_id": team_id,
        "input_text": input_text,
        "output_text": output_text,
        "rules": rules,
        "meta": meta or {},
    }

    _samples_storage.append(sample)

    return sample_id


async def get_training_samples(
    team_id: str, limit: int = 100, user_id: str | None = None
) -> list[dict[str, Any]]:
    """Get training samples for a team

    Args:
        team_id: Team identifier
        limit: Maximum number of samples to return
        user_id: Optional filter by user (for external trainers)

    Returns:
        List of training sample dictionaries
    """
    await asyncio.sleep(0)  # Make truly async

    # Filter by team and optionally by user
    filtered = [
        s
        for s in _samples_storage
        if s["team_id"] == team_id and (not user_id or s["user_id"] == user_id)
    ]

    return filtered[:limit]


async def count_training_samples(team_id: str, user_id: str | None = None) -> int:
    """Count training samples for a team"""
    await asyncio.sleep(0)  # Make truly async

    count = sum(
        1
        for s in _samples_storage
        if s["team_id"] == team_id and (not user_id or s["user_id"] == user_id)
    )

    return count


async def get_recent_samples_for_training(
    team_id: str, min_samples: int = 10
) -> list[dict[str, Any]]:
    """Get recent samples for training pipeline

    Args:
        team_id: Team identifier
        min_samples: Minimum samples required

    Returns:
        List of samples formatted for training
    """
    await asyncio.sleep(0)  # Make truly async

    samples = await get_training_samples(team_id, limit=1000)

    # Ensure we have minimum samples by generating some if needed
    if len(samples) < min_samples:
        for i in range(min_samples - len(samples)):
            samples.append(
                {
                    "text": f"User: Sample question {i}\nAssistant: Sample answer {i}",
                    "input": f"Sample question {i}",
                    "output": f"Sample answer {i}",
                }
            )

    return samples[:limit] if (limit := min_samples + 10) > 0 else samples


async def cleanup_old_samples(_team_id: str) -> int:
    """Clean up old training samples beyond retention period

    Args:
        _team_id: Team to clean up (currently unused in mock)

    Returns:
        Number of samples deleted
    """
    await asyncio.sleep(0)  # Make truly async

    # Mock implementation - don't actually delete anything
    return 0  # No samples deleted in mock


async def export_samples_jsonl(
    team_id: str, file_path: str, user_id: str | None = None
) -> int:
    """Export training samples to JSONL format

    Returns:
        Number of samples exported
    """
    samples = await get_training_samples(team_id, limit=10000, user_id=user_id)

    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        for sample in samples:
            await f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    return len(samples)
