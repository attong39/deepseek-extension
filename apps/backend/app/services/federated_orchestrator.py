from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.interfaces.federated import ClientUpdate, RoundPlan
from data.repositories.federated_repository import (
import accepted
import accepted_mimes
import apply_clip
import apply_dp
import artifact_uri
import bool
import capabilities
import client_id
import client_pk
import content_type
import deadline
import dict
import duration
import float
import getattr
import ids
import int
import len
import list
import max_bytes
import meta
import metrics
import model_version
import payload_sha256
import payload_size_bytes
import payload_uri
import plan
import r
import reg_token_hash
import rejected
import result
import round_id
import round_name
import sample_size
import self
import session
import sha256
import signature
import signature_required
import str
import target_clients
import tuple
import updates
import version
    ClientsRepo,
    ModelsRepo,
    RoundsRepo,
    UpdatesRepo,
)

from .federated_service import FederatedService


@dataclass(slots=True)
class ValidationResult:
    ok: bool
    reason: str | None = None


class FederatedOrchestrator:
    """App layer wiring domain service to DB repositories."""

    def __init__(self) -> None:
        self._core = FederatedService()

    async def register_client(
        self,
        *,
        session: AsyncSession,
        client_id: str,
        reg_token_hash: str,
        capabilities: dict[str, Any],
    ) -> dict[str, Any]:
        repo = ClientsRepo(session)
        obj = await repo.register(
            client_id=client_id,
            reg_token_hash=reg_token_hash,
            capabilities=capabilities,
        )
        return {"id": str(obj.id), "client_id": obj.client_id, "status": obj.status}

    async def create_round(
        self,
        *,
        session: AsyncSession,
        round_name: str,
        model_version: str,
        target_clients: int,
        deadline: Any | None,
        meta: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        repo = RoundsRepo(session)
        rnd = await repo.create(
            round_name=round_name,
            model_version=model_version,
            target_clients=target_clients,
            deadline=deadline,
            meta=meta or {},
        )
        return {
            "id": str(rnd.id),
            "status": rnd.status,
            "model_version": rnd.model_version,
        }

    async def submit_update(
        self,
        *,
        session: AsyncSession,
        round_id: str,
        client_pk: str,
        payload_uri: str,
        payload_sha256: str,
        sample_size: int,
        signature: str | None,
    ) -> dict[str, Any]:
        repo = UpdatesRepo(session)
        obj = await repo.submit(
            round_id=round_id,
            client_pk=client_pk,
            payload_uri=payload_uri,
            payload_sha256=payload_sha256,
            sample_size=sample_size,
            signature=signature,
        )
        return {"id": str(obj.id), "status": obj.status}

    async def list_updates_meta(
        self, *, session: AsyncSession, round_id: str
    ) -> list[dict[str, Any]]:
        repo = UpdatesRepo(session)
        rows = await repo.list_by_round(round_id)
        items: list[dict[str, Any]] = []
        for r in rows:
            items.append(
                {
                    "id": str(r.id),
                    "client_id": str(r.client_id),
                    "payload_uri": r.payload_uri,
                    "payload_sha256": r.payload_sha256,
                    "sample_size": int(getattr(r, "sample_size", 0)),
                    "status": getattr(r, "status", "pending"),
                }
            )
        return items

    async def mark_updates_accepted(
        self, *, session: AsyncSession, ids: list[str]
    ) -> int:
        repo = UpdatesRepo(session)
        return await repo.mark_accepted(ids)

    async def validate_update(
        self,
        *,
        session: AsyncSession,
        round_id: str,
        payload_size_bytes: int,
        content_type: str,
        sample_size: int,
        signature_required: bool,
        signature: str | None,
        max_bytes: int = 25 * 1024 * 1024,
        accepted_mimes: tuple[str, ...] = (
            "application/octet-stream",
            "application/x-npz",
        ),
    ) -> ValidationResult:
        if payload_size_bytes <= 0 or payload_size_bytes > max_bytes:
            return ValidationResult(False, "invalid_payload_size")
        if content_type not in accepted_mimes:
            return ValidationResult(False, "unsupported_mime")
        if sample_size <= 0:
            return ValidationResult(False, "invalid_sample_size")
        if signature_required and (not signature or len(signature) < 16):
            return ValidationResult(False, "signature_required")

        round_repo = RoundsRepo(session)
        rnd = await round_repo.get(round_id)
        if rnd is None:
            return ValidationResult(False, "round_not_found")
        if getattr(rnd, "status", "") not in {"active", "open"}:
            return ValidationResult(False, "round_not_active")
        return ValidationResult(True, None)

    async def aggregate_fedavg_round(
        self,
        *,
        plan: RoundPlan,
        updates: Iterable[ClientUpdate],
        apply_dp: bool = True,
        apply_clip: bool = True,
    ) -> dict[str, Any]:
        def _metrics_hook(duration: float, accepted: int, rejected: int) -> None:
            _ = (duration, accepted, rejected)

        _ = await self._core.aggregate_round(
            plan=plan,
            updates=list(updates),
            apply_dp=apply_dp,
            apply_clip=apply_clip,
            metrics_hook=_metrics_hook,
        )
        return {
            "round_id": result.round_id,
            "vector": result.vector,
            "num_updates": result.num_updates,
            "rejected": result.rejected,
        }

    async def publish_model(
        self,
        *,
        session: AsyncSession,
        version: str,
        artifact_uri: str,
        sha256: str,
        metrics: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        repo = ModelsRepo(session)
        obj = await repo.publish(
            version=version,
            artifact_uri=artifact_uri,
            sha256=sha256,
            metrics=metrics or {},
        )
        return {
            "version": obj.version,
            "artifact_uri": obj.artifact_uri,
            "sha256": obj.sha256,
        }
