# Assistant API Router - Teacher-Student Architecture Endpoints
from __future__ import annotations

from typing import Any

from apps.backend.app.api.v1._common.security import TokenClaims, require_auth
from apps.backend.app.services.assistant_svc import batch_respond, get_status, respond
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
import Exception
import bool
import claims
import dict
import e
import float
import inp
import len
import list
import request
import resp
import str

router = APIRouter(prefix="/assistant", tags=["assistant"])


class AssistantRequest(BaseModel):
    """Request for assistant response"""

    text: str = Field(..., description="User input text")
    rules: str | None = Field(None, description="Optional rules for response")
    context: str | None = Field(None, description="Optional additional context")
    force_teacher: bool = Field(False, description="Force use of teacher model")


class BatchAssistantRequest(BaseModel):
    """Request for batch assistant responses"""

    inputs: list[AssistantRequest] = Field(..., description="List of inputs to process")


class AssistantResponseModel(BaseModel):
    """Response from assistant"""

    output: str
    source: str  # "local" or "teacher" or "error"
    confidence: float
    uncertainty: float | None = None
    meta: dict[str, Any] = {}


@router.post("/respond", response_model=AssistantResponseModel)
async def assistant_respond(
    request: AssistantRequest, claims: TokenClaims = Depends(require_auth)
) -> AssistantResponseModel:
    """Get response from assistant using Teacher-Student architecture

    The assistant first tries the local model. If the local model's uncertainty
    is too high, it falls back to the teacher (GPT-4) model.
    """
    try:
        response = await respond(
            user_input=request.text,
            team_id=claims.team_id,
            user_id=claims.user_id,
            rules=request.rules,
            context=request.context,
            force_teacher=request.force_teacher,
        )

        return AssistantResponseModel(
            output=response.output,
            source=response.source,
            confidence=response.confidence,
            uncertainty=response.uncertainty,
            meta=response.meta,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assistant error: {str(e)}",
        )


@router.post("/batch", response_model=list[AssistantResponseModel])
async def assistant_batch_respond(
    request: BatchAssistantRequest, claims: TokenClaims = Depends(require_auth)
) -> list[AssistantResponseModel]:
    """Process multiple inputs in parallel"""
    try:
        if len(request.inputs) > 50:  # Limit batch size
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size cannot exceed 50 items",
            )

        # Convert to dict format expected by service
        inputs = []
        for inp in request.inputs:
            inputs.append(
                {
                    "text": inp.text,
                    "rules": inp.rules,
                    "context": inp.context,
                    "force_teacher": inp.force_teacher,
                }
            )

        responses = await batch_respond(
            inputs=inputs, team_id=claims.team_id, user_id=claims.user_id
        )

        return [
            AssistantResponseModel(
                output=resp.output,
                source=resp.source,
                confidence=resp.confidence,
                uncertainty=resp.uncertainty,
                meta=resp.meta,
            )
            for resp in responses
        ]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch processing error: {str(e)}",
        )


@router.get("/status")
async def assistant_status(
    claims: TokenClaims = Depends(require_auth),
) -> dict[str, Any]:
    """Get status of assistant components (local model + teacher)"""
    try:
        status_info = await get_status()

        return {"status": "ok", "components": status_info, "team_id": claims.team_id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status check error: {str(e)}",
        )


@router.post("/teacher-only", response_model=AssistantResponseModel)
async def teacher_only_respond(
    request: AssistantRequest, claims: TokenClaims = Depends(require_auth)
) -> AssistantResponseModel:
    """Force response from teacher model only (bypass local model)"""
    try:
        response = await respond(
            user_input=request.text,
            team_id=claims.team_id,
            user_id=claims.user_id,
            rules=request.rules,
            context=request.context,
            force_teacher=True,  # Always use teacher
        )

        return AssistantResponseModel(
            output=response.output,
            source=response.source,
            confidence=response.confidence,
            uncertainty=response.uncertainty,
            meta=response.meta,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Teacher response error: {str(e)}",
        )
