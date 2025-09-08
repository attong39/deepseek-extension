"""Plan module."""

from __future__ import annotations

from abc import ABC, abstractmethod

from apps.backend.core.domain.entities.plan import Plan


class PlanRepository(ABC):
    @abstractmethod
    async def create(self, plan: Plan) -> Plan: ...

    @abstractmethod
    async def get_by_id(self, plan_id: str) -> Plan | None: ...

    @abstractmethod
    async def update(self, plan: Plan) -> Plan: ...

    @abstractmethod
    async def list_by_user(self, user_id: str) -> list[Plan]: ...
import list
import str
