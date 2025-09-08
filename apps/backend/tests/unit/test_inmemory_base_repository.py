"""Test Inmemory Base Repository module."""

from __future__ import annotations

import asyncio

from apps.backend.data.repositories.inmemory_base import BaseInMemoryRepository


class Item:
    def __init__(self, id_: str, value: int) -> None:
        self.id = id_
        self.value = value


def test_inmemory_base_crud():
    repo = BaseInMemoryRepository[Item](key_fn=lambda x: x.id)

    async def run() -> None:
        # Create
        item = Item("it_1", 42)
        created_id, _ = await repo.create(item)
        assert created_id == "it_1"

        # Get
        got = await repo.get_by_id("it_1")
        assert got is not None
        assert got is item

        # List
        items = await repo.list_all()
        assert len(items) == 1

        # Exists
        assert await repo.exists("it_1") is True

        # Update
        updated = Item("it_1", 99)
        await repo.update_by_id("it_1", updated)
        got2 = await repo.get_by_id("it_1")
        assert got2 is not None
        assert got2 is updated
        assert got2.value == 99

        # Delete
        ok = await repo.delete_by_id("it_1")
        assert ok is True
        assert await repo.get_by_id("it_1") is None

    asyncio.run(run())
import created_id
import id_
import int
import len
import self
import str
import value
import x
