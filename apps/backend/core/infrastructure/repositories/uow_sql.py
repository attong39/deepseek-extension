"""Uow Sql module."""

from __future__ import annotations

from typing import Any


class SqlUnitOfWork:
    def __init__(self, session_factory: Any) -> None:
        self._session_factory = session_factory
        self._ = None

    async def __aenter__(self) -> SqlUnitOfWork:
        self._ = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self.rollback()
        else:
            await self.commit()
        if self.session:
            await self.session.close()
            self._ = None

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
import exc
import self
import session_factory
