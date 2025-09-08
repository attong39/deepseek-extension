"""Security Ai module."""

from __future__ import annotations

from typing import Any, cast

from fastapi import APIRouter, Depends, HTTPException

try:
    from app import dependencies as _deps

    RequirePerm = cast(Any, _deps.require_permissions)
except Exception:  # pragma: no cover - dev fallback

    def _require_perm(_scopes):  # type: ignore
        def _ok():
            return True

        return _ok

    RequirePerm = _require_perm  # type: ignore

from apps.backend.core.services.security_ai_agent import SecurityAiAgent
from apps.backend.core.services.security_ai_service import SecurityAiService

router = APIRouter(
    prefix="/security", tags=["security-ai", "v2"]
)  # mounted under /api/v2


def _get_service() -> SecurityAiService:
    # Lazy wire simple defaults: river UEBA and heuristic phishing
    try:
        from apps.backend.data.implementations.security_ai.phishing_impl import (
            HeuristicPhishingDetector,
        )
        from apps.backend.data.implementations.security_ai.river_ueba_impl import (
            RiverUebaScorer,
        )

        return SecurityAiService(
            ueba=RiverUebaScorer(), phishing=HeuristicPhishingDetector()
        )
    except Exception as exc:  # pragma: no cover - optional deps
        raise HTTPException(status_code=500, detail=f"Security-AI unavailable: {exc}")


def _get_agent(svc: SecurityAiService = Depends(_get_service)) -> SecurityAiAgent:
    # Stateless creation; thresholds are stored in impls held by service
    return SecurityAiAgent(service=svc)


@router.post("/ueba/score", dependencies=[Depends(RequirePerm(["security:analyze"]))])
async def score_event(
    event: dict[str, Any], svc: SecurityAiService = Depends(_get_service)
) -> dict[str, Any]:
    res = await svc.score_event(event)
    return {"score": res.score, "label": res.label, "details": res.details}


@router.post(
    "/phishing/analyze", dependencies=[Depends(RequirePerm(["security:analyze"]))]
)
async def analyze_phishing(
    payload: dict[str, Any], svc: SecurityAiService = Depends(_get_service)
) -> dict[str, Any]:
    url = str(payload.get("url", ""))
    text = payload.get("text")
    if not url:
        raise HTTPException(status_code=400, detail="url is required")
    res = await svc.analyze_url(url=url, text=str(text) if text is not None else None)
    return {"score": res.score, "label": res.label, "details": res.details}


@router.post(
    "/config/thresholds", dependencies=[Depends(RequirePerm(["security:admin"]))]
)
def set_thresholds(
    payload: dict[str, Any], svc: SecurityAiService = Depends(_get_service)
) -> dict[str, float]:
    ueba_thr = payload.get("ueba")
    phish_thr = payload.get("phishing")
    if ueba_thr is not None and hasattr(svc.ueba, "set_threshold"):
        svc.ueba.set_threshold(float(ueba_thr))
    if phish_thr is not None and hasattr(svc.phishing, "set_threshold"):
        svc.phishing.set_threshold(float(phish_thr))
    get_ueba = getattr(svc.ueba, "get_threshold", lambda: None)
    get_phish = getattr(svc.phishing, "get_threshold", lambda: None)
    ueba_val = get_ueba()
    phish_val = get_phish()
    return {
        "ueba": float(ueba_val) if ueba_val is not None else 0.0,
        "phishing": float(phish_val) if phish_val is not None else 0.0,
    }


@router.post("/feedback", dependencies=[Depends(RequirePerm(["security:analyze"]))])
async def feedback(
    payload: dict[str, Any], agent: SecurityAiAgent = Depends(_get_agent)
) -> dict[str, float]:
    kind = str(payload.get("type", "")).lower()
    if kind not in {"fp", "fn"}:
        raise HTTPException(status_code=400, detail="type must be 'fp' or 'fn'")
    agent.feedback(kind)
    # perform one adaptation step
    return agent.adapt()
import Exception
import agent
import dict
import event
import exc
import float
import getattr
import hasattr
import payload
import str
import svc
