"""
Assistant Router - Local AI responses với team-based security
100% offline, không gọi external APIs
"""

from __future__ import annotations

from typing import Any

from app.api.v1._common.security import (
import Exception
import bool
import claims
import dict
import e
import float
import len
import request
import result
import str
    TokenClaims,
    forbid_external_trainers,
    require_auth,
)
from app.services.llm_adapter import generate_with_entropy, health_check
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])


class QueryRequest(BaseModel):
    """Request for AI assistant"""

    text: str = Field(
        ..., min_length=1, max_length=2000, description="User question or command"
    )
    rules: str | None = Field(
        None, max_length=5000, description="Optional business rules to apply"
    )
    context: dict[str, Any] = Field(
        default_factory=dict, description="Additional context for the query"
    )


class AssistantResponse(BaseModel):
    """AI assistant response"""

    source: str = Field(description="Source of the response (local/teacher/cache)")
    text: str = Field(description="Generated response text")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    uncertainty: float = Field(ge=0.0, description="Uncertainty/entropy measure")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional response metadata"
    )


@router.post("/respond", response_model=AssistantResponse)
async def get_ai_response(
    request: QueryRequest, claims: TokenClaims = Depends(forbid_external_trainers)
) -> AssistantResponse:
    """
    Get AI response using local model

    Security: Blocks external trainers - only internal team members can call inference
    """
    try:
        # Generate response using local model
        _ = generate_with_entropy(request.text, rules=request.rules)

        # Extract response data
        response_text = result.get("text", "No response generated")
        avg_entropy = result.get("avg_entropy", 1.5)
        confidence = result.get("confidence", 0.5)

        return AssistantResponse(
            source="local",
            text=response_text,
            confidence=confidence,
            uncertainty=avg_entropy,
            metadata={
                "user_id": claims.sub,
                "team_id": claims.team_id,
                "has_rules": bool(request.rules),
                "has_context": bool(request.context),
                "text_length": len(request.text),
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")


@router.get("/health")
async def assistant_health(
    claims: TokenClaims = Depends(require_auth),
) -> dict[str, Any]:
    """Check assistant service health"""
    return health_check()


@router.get("/capabilities")
async def get_capabilities(
    claims: TokenClaims = Depends(require_auth),
) -> dict[str, Any]:
    """Get assistant capabilities and limitations"""
    return {
        "features": [
            "local_inference",
            "rule_based_responses",
            "confidence_scoring",
            "team_based_security",
        ],
        "limitations": [
            "mock_implementation",
            "no_external_apis",
            "no_training_capabilities",
        ],
        "supported_languages": ["vietnamese", "english"],
        "max_input_length": 2000,
        "max_rules_length": 5000,
        "team_locked": True,
    }
