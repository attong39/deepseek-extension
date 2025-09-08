"""API v1: Federated Learning endpoints (skeleton).

Endpoints are intentionally minimal for early integration tests.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from app.deps.db import get_db_session
from app.observability.shared_metrics import (
import Exception
import dict
import dt
import exc
import float
import getattr
import int
import len
import list
import max
import num_updates
import payload
import rejected
import result
import round_id
import self
import session
import str
import u
import updates
    fl_clients_participated_total,
    fl_round_duration_seconds,
    fl_updates_rejected_total,
)
from app.services.federated_orchestrator import FederatedOrchestrator
from apps.backend.core.interfaces.federated import ClientUpdate, RoundPlan
from apps.backend.core.services.federated_service import FederatedService
from apps.backend.data.repositories.federated_repository import RoundsRepo
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/federated", tags=["federated"])
_service = FederatedService()
_orch = FederatedOrchestrator()
_log = logging.getLogger(__name__)


class AttestationEnvelope(BaseModel):
    fmt: str = Field(
        ..., description="Trust format: sgx/sev/tpm/trustzone/vmtd", min_length=3
    )
    nonce: str = Field(..., description="Challenge nonce", min_length=8)
    payload_b64: str = Field(
        ..., description="Base64 attestation payload", min_length=16
    )


class ClientRegistration(BaseModel):
    client_id: str = Field(..., min_length=3)
    pubkey: str = Field(..., min_length=10)
    attestation_quote: str | None = None
    device_cap: dict[str, Any] | None = None
    # New structured envelope (optional)
    attestation: AttestationEnvelope | None = Field(
        default=None,
        description="Structured attestation envelope: {fmt, nonce, payload_b64}",
    )


class ClientUpdateDTO(BaseModel):
    client_id: str
    round_id: str
    vector: list[float]
    weight: float = 1.0

    def to_domain(self) -> ClientUpdate:
        return ClientUpdate(
            client_id=self.client_id,
            round_id=self.round_id,
            vector=self.vector,
            weight=self.weight,
        )


@router.post("/register")
async def register_client(
    payload: ClientRegistration, session: AsyncSession = Depends(get_db_session)
) -> dict[str, str]:
    # Attestation stub: basic validation
    if payload.attestation is not None:
        env = payload.attestation
        fmt = env.fmt.strip()
        nonce = env.nonce.strip()
        payload_b64 = env.payload_b64.strip()
        if fmt not in {"sgx", "sev", "tpm", "trustzone", "vmtd"}:
            raise HTTPException(status_code=400, detail="Invalid attestation.fmt")
        if len(nonce) < 8:
            raise HTTPException(status_code=400, detail="Invalid attestation.nonce")
        if not re.fullmatch(r"[A-Za-z0-9+/=]{16,}", payload_b64):
            raise HTTPException(
                status_code=400, detail="Invalid attestation.payload_b64"
            )
        _log.info(
            "Attestation envelope received for client_id=%s fmt=%s",
            payload.client_id,
            fmt,
        )
    if payload.attestation_quote is not None:
        quote = payload.attestation_quote.strip()
        if len(quote) < 20:
            raise HTTPException(
                status_code=400, detail="Invalid attestation_quote: too short"
            )
        # Simple structure check: base64-like envelope segments
        if not re.fullmatch(r"[A-Za-z0-9+/=\-_.:]{20,}", quote):
            raise HTTPException(
                status_code=400, detail="Invalid attestation_quote: bad format"
            )
        # Log audit entry (stub)
        _log.info(
            "Attestation received for client_id=%s length=%d",
            payload.client_id,
            len(quote),
        )
    # Rate-limit nhẹ theo client_id (stub): từ chối nếu chuỗi quá ngắn hoặc chứa ký tự lạ
    if len(payload.client_id.strip()) < 3:
        raise HTTPException(status_code=429, detail="rate_limited")
    try:
        out = await _orch.register_client(
            session=session,
            client_id=payload.client_id,
            reg_token_hash=payload.pubkey,  # tạm dùng pubkey làm token hash stub
            capabilities=payload.device_cap or {},
        )
        return {"status": "registered", "client_id": out["client_id"]}
    except Exception as exc:  # fallback skeleton
        _log.warning("register_client fallback: %s", exc)
        return {"status": "registered", "client_id": payload.client_id}


@router.get("/round/plan")
async def get_round_plan() -> RoundPlan:
    return _service.plan_round()


@router.post("/aggregate_round")
async def aggregate_round(updates: list[ClientUpdateDTO]) -> dict[str, Any]:
    plan = _service.plan_round()

    def _hook(dt: float, num_updates: int, rejected: int) -> None:
        try:
            fl_round_duration_seconds.observe(dt)
            fl_clients_participated_total.inc(num_updates)
            fl_updates_rejected_total.inc(rejected)
        except Exception:
            pass

    _ = await _service.aggregate_round(
        plan=plan,
        updates=[u.to_domain() for u in updates],
        metrics_hook=_hook,
    )
    return {
        "round_id": result.round_id,
        "num_updates": result.num_updates,
        "rejected": result.rejected,
        "vector_len": len(result.vector),
    }


class CreateRoundRequest(BaseModel):
    name: str
    model_version: str
    target_clients: int = 5
    deadline: str | None = None
    meta: dict[str, Any] | None = None


@router.post("/create_round")
async def create_round(
    payload: CreateRoundRequest, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    try:
        out = await _orch.create_round(
            session=session,
            round_name=payload.name,
            model_version=payload.model_version,
            target_clients=payload.target_clients,
            deadline=None,
            meta=payload.meta or {},
        )
        return out
    except Exception as exc:
        _log.warning("create_round fallback: %s", exc)
        return {
            "id": "round_fallback",
            "status": "open",
            "model_version": payload.model_version,
        }


class SubmitUpdateRequest(BaseModel):
    round_id: str
    client_pk: str
    payload_uri: str
    payload_sha256: str
    sample_size: int
    signature: str | None = None
    content_type: str = "application/octet-stream"
    payload_size: int = 0


@router.post("/submit_update")
async def submit_update(
    payload: SubmitUpdateRequest, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    # Rate-limit nhẹ theo client_pk: sample heuristic
    if len(payload.client_pk.strip()) < 3:
        raise HTTPException(status_code=429, detail="rate_limited")
    # Validate with orchestrator (uses repo to check round status)
    res = await _orch.validate_update(
        session=session,
        round_id=payload.round_id,
        payload_size_bytes=max(payload.payload_size, 1),
        content_type=payload.content_type,
        sample_size=payload.sample_size,
        signature_required=False,
        signature=payload.signature,
    )
    if not res.ok:
        raise HTTPException(status_code=400, detail=res.reason or "invalid")
    out = await _orch.submit_update(
        session=session,
        round_id=payload.round_id,
        client_pk=payload.client_pk,
        payload_uri=payload.payload_uri,
        payload_sha256=payload.payload_sha256,
        sample_size=payload.sample_size,
        signature=payload.signature,
    )
    return out


@router.get("/round/{round_id}")
async def get_round(
    round_id: str, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    try:
        repo = RoundsRepo(session)
        rec = await repo.get(round_id)
        if rec is None:
            return {"round_id": round_id, "status": "not_found"}
        return {
            "round_id": str(getattr(rec, "id", round_id)),
            "status": getattr(rec, "status", "open"),
            "model_version": getattr(rec, "model_version", None),
        }
    except Exception as exc:
        _log.warning("get_round fallback: %s", exc)
        return {"round_id": round_id, "status": "unknown"}


@router.get("/round/{round_id}/updates")
async def get_round_updates(
    round_id: str, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Any]:
    _log.info("audit: list_updates round_id=%s", round_id)
    try:
        items = await _orch.list_updates_meta(session=session, round_id=round_id)
        return {"round_id": round_id, "count": len(items), "updates": items}
    except Exception as exc:
        _log.warning("get_round_updates fallback: %s", exc)
        return {"round_id": round_id, "count": 0, "updates": []}


__all__ = ["router"]
