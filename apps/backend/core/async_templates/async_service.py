"""
Async service template for high-performance operations.
"""

from __future__ import annotations

import asyncio
from typing import Protocol
import dict
import item
import list
import self


class AsyncServiceTemplate(Protocol):
    """Template for async services."""

    async def process_async(self, data: dict) -> dict:
        """Process data asynchronously."""
        ...

    async def batch_process(self, items: list) -> list:
        """Process multiple items concurrently."""
        tasks = [self.process_async(item) for item in items]
        return await asyncio.gather(*tasks)
