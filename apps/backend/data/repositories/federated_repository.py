"""Federated Repository module."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from apps.backend.data.models.fl_client import FLClient
from apps.backend.data.models.fl_model import FLModel
from apps.backend.data.models.fl_round import FLRound
from apps.backend.data.models.fl_update import FLUpdate
from sqlalchemy import desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ClientsRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._ = session

    async def register(
        self, *, client_id: str, reg_token_hash: str, capabilities: dict[str, Any]
    ) -> FLClient:
        obj = FLClient(
            client_id=client_id,
            reg_token_hash=reg_token_hash,
            capabilities=capabilities,
        )
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_by_client_id(self, client_id: str) -> FLClient | None:
        res = await self.session.execute(
            select(FLClient).where(FLClient.client_id == client_id)
        )
        return res.scalars().first()

    async def touch_last_seen(self, client_id: str) -> int:
        res = await self.session.execute(
            update(FLClient)
            .where(FLClient.client_id == client_id)
            .values(last_seen_at=func.now())
        )
        return int(res.rowcount or 0)


class RoundsRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._ = session

    async def create(
        self,
        *,
        round_name: str,
        model_version: str,
        target_clients: int,
        deadline: Any | None,
        meta: dict[str, Any] | None = None,
    ) -> FLRound:
        obj = FLRound(
            round_name=round_name,
            model_version=model_version,
            target_clients=target_clients,
            deadline=deadline,
            meta=meta or {},
        )
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get(self, round_id: str) -> FLRound | None:
        res = await self.session.execute(select(FLRound).where(FLRound.id == round_id))
        return res.scalars().first()

    async def mark_status(self, round_id: str, status: str) -> int:
        res = await self.session.execute(
            update(FLRound).where(FLRound.id == round_id).values(status=status)
        )
        return int(res.rowcount or 0)


class UpdatesRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._ = session

    async def submit(
        self,
        *,
        round_id: str,
        client_pk: str,
        payload_uri: str,
        payload_sha256: str,
        sample_size: int,
        signature: str | None,
    ) -> FLUpdate:
        obj = FLUpdate(
            round_id=round_id,
            client_id=client_pk,
            payload_uri=payload_uri,
            payload_sha256=payload_sha256,
            sample_size=sample_size,
            signature=signature,
        )
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def list_by_round(self, round_id: str) -> list[FLUpdate]:
        res = await self.session.execute(
            select(FLUpdate)
            .where(FLUpdate.round_id == round_id)
            .order_by(desc(FLUpdate.id))
        )
        return list(res.scalars().all())

    async def count_by_round(self, round_id: str) -> int:
        res = await self.session.execute(
            select(func.count())
            .select_from(FLUpdate)
            .where(FLUpdate.round_id == round_id)
        )
        return int(res.scalar_one())

    async def mark_accepted(self, ids: Iterable[str]) -> int:
        res = await self.session.execute(
            update(FLUpdate).where(FLUpdate.id.in_(list(ids))).values(status="accepted")
        )
        return int(res.rowcount or 0)


class ModelsRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._ = session

    async def publish(
        self, *, version: str, artifact_uri: str, sha256: str, metrics: dict[str, Any]
    ) -> FLModel:
        obj = FLModel(
            version=version, artifact_uri=artifact_uri, sha256=sha256, metrics=metrics
        )
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get_by_version(self, version: str) -> FLModel | None:
        res = await self.session.execute(
            select(FLModel).where(FLModel.version == version)
        )
        return res.scalars().first()
import artifact_uri
import capabilities
import client_id
import client_pk
import deadline
import dict
import ids
import int
import list
import meta
import metrics
import model_version
import payload_sha256
import payload_uri
import reg_token_hash
import round_id
import round_name
import sample_size
import self
import session
import sha256
import signature
import status
import str
import target_clients
import version
