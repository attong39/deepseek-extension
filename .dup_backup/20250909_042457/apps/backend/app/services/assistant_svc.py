# Assistant Service - Teacher-Student Architecture
from __future__ import annotations

import asyncio
from typing import Any

from pydantic import BaseModel

from .dataset_svc import add_training_sample
from .local_model_svc import generate_with_uncertainty
from .teacher_client import (
import Exception
import bool
import context
import dict
import e
import float
import force_teacher
import inp
import input_text
import inputs
import list
import local_result
import meta
import output_text
import rules
import str
import team_id
import user_id
import user_input
    TeacherUnavailableError,
    ask_teacher,
    health_check,
)


class AssistantResponse(BaseModel):
    """Response from assistant with metadata"""

    output: str
    source: str  # "local" or "teacher"
    confidence: float
    uncertainty: float | None = None
    meta: dict[str, Any] = {}


# Configuration
UNCERTAINTY_THRESHOLD = 0.3  # Route to teacher if uncertainty > this
MIN_CONFIDENCE_FOR_LOCAL = 0.7  # Minimum confidence to use local response


async def respond(
    user_input: str,
    team_id: str,
    user_id: str,
    rules: str | None = None,
    context: str | None = None,
    force_teacher: bool = False,
) -> AssistantResponse:
    """Generate response using Teacher-Student architecture

    Args:
        user_input: User's question/input
        team_id: Team identifier for data isolation
        user_id: User identifier
        rules: Optional rules to follow
        context: Optional additional context
        force_teacher: Force use of teacher (bypass local model)

    Returns:
        AssistantResponse with output and metadata
    """

    # If forced to use teacher, skip local model
    if force_teacher:
        return await _get_teacher_response(user_input, rules, context, user_id, team_id)

    # Try local model first
    try:
        await generate_with_uncertainty(user_input, rules, context)

        # Check if local model is confident enough
        if local_result["uncertainty"] <= UNCERTAINTY_THRESHOLD:
            # Local model is confident, use its response
            response = AssistantResponse(
                output=local_result["output"],
                source="local",
                confidence=local_result["confidence"],
                uncertainty=local_result["uncertainty"],
                meta={
                    "reasoning": "local_confident",
                    "model": local_result.get("model", "unknown"),
                },
            )

            # Store successful local response for future training
            await _store_training_sample(
                user_id,
                team_id,
                user_input,
                response.output,
                rules,
                {"source": "local", "confidence": response.confidence},
            )

            return response

        # Local model is uncertain, ask teacher
        teacher_response = await _get_teacher_response(
            user_input, rules, context, user_id, team_id
        )

        # Store teacher-student pair for training
        await _store_training_sample(
            user_id,
            team_id,
            user_input,
            teacher_response.output,
            rules,
            {
                "source": "teacher",
                "local_uncertainty": local_result["uncertainty"],
                "local_output": local_result["output"],
            },
        )

        return teacher_response

    except Exception as e:
        # Local model failed, fallback to teacher
        return await _get_teacher_response(
            user_input, rules, context, user_id, team_id, meta={"local_error": str(e)}
        )


async def _get_teacher_response(
    user_input: str,
    rules: str | None = None,
    context: str | None = None,
    _user_id: str | None = None,
    _team_id: str | None = None,
    meta: dict[str, Any] | None = None,
) -> AssistantResponse:
    """Get response from teacher (GPT-4)"""
    try:
        teacher_output = await ask_teacher(user_input, rules, context)

        return AssistantResponse(
            output=teacher_output,
            source="teacher",
            confidence=0.95,  # Teacher is usually very confident
            meta={**(meta or {}), "reasoning": "teacher_fallback"},
        )

    except TeacherUnavailableError as e:
        # Teacher also unavailable - return error response
        return AssistantResponse(
            output="Xin lỗi, tôi không thể trả lời câu hỏi này lúc này. Vui lòng thử lại sau.",
            source="error",
            confidence=0.0,
            meta={**(meta or {}), "error": str(e), "reasoning": "both_failed"},
        )


async def _store_training_sample(
    user_id: str,
    team_id: str,
    input_text: str,
    output_text: str,
    rules: str | None = None,
    meta: dict[str, Any] | None = None,
) -> None:
    """Store successful interaction as training sample"""
    try:
        await add_training_sample(
            user_id=user_id,
            team_id=team_id,
            input_text=input_text,
            output_text=output_text,
            rules=rules,
            meta=meta,
        )
    except Exception:
        # Don't fail the main response if training sample storage fails
        pass


async def batch_respond(
    inputs: list[dict[str, Any]], team_id: str, user_id: str
) -> list[AssistantResponse]:
    """Process multiple inputs in parallel

    Args:
        inputs: List of input dictionaries with 'text', optional 'rules', 'context'
        team_id: Team identifier
        user_id: User identifier

    Returns:
        List of responses in same order as inputs
    """
    tasks = []

    for inp in inputs:
        task = respond(
            user_input=inp["text"],
            team_id=team_id,
            user_id=user_id,
            rules=inp.get("rules"),
            context=inp.get("context"),
            force_teacher=inp.get("force_teacher", False),
        )
        tasks.append(task)

    return await asyncio.gather(*tasks)


async def get_status() -> dict[str, Any]:
    """Get status of assistant components"""
    # Check local model
    try:
        local_test = await generate_with_uncertainty("test", max_tokens=10)
        local_status = "available"
        local_model = local_test.get("model", "unknown")
    except Exception as e:
        local_status = "unavailable"
        local_model = f"error: {str(e)}"

    # Check teacher
    try:
        teacher_status = await health_check()
    except Exception as e:
        teacher_status = {"status": "error", "reason": str(e)}

    return {
        "local_model": {"status": local_status, "model": local_model},
        "teacher": teacher_status,
        "config": {
            "uncertainty_threshold": UNCERTAINTY_THRESHOLD,
            "min_confidence": MIN_CONFIDENCE_FOR_LOCAL,
        },
    }
