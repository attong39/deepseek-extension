# Teacher Client Service - GPT-4 Integration for Training
from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx
from httpx import Timeout
import Exception
import attempt
import client
import context
import dict
import e
import error
import float
import int
import len
import range
import rules
import str
import user_text

# Configuration constants
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
TEACHER_MODEL = os.getenv("TEACHER_MODEL", "gpt-4o-mini")
MAX_RETRIES = int(os.getenv("TEACHER_MAX_RETRIES", "3"))
TIMEOUT_SECONDS = float(os.getenv("TEACHER_TIMEOUT", "45.0"))


class TeacherUnavailableError(Exception):
    """Raised when teacher service is not available"""


async def ask_teacher(
    user_text: str, rules: str | None = None, context: str | None = None
) -> str:
    """Ask GPT-4 teacher for response

    Args:
        user_text: User input text
        rules: Optional rules for teacher
        context: Optional additional context

    Returns:
        Teacher response text

    Raises:
        TeacherUnavailableError: When teacher cannot respond
    """
    if not OPENAI_API_KEY:
        raise TeacherUnavailableError("Teacher API key not configured")

    payload = _build_request_payload(user_text, rules, context)

    # Make API call with retry logic
    for attempt in range(MAX_RETRIES):
        try:
            response_text = await _make_teacher_api_call(payload)
            return response_text

        except httpx.TimeoutException:
            await _handle_timeout_error(attempt)

        except httpx.HTTPStatusError as e:
            await _handle_http_error(e, attempt)

        except Exception as e:
            await _handle_general_error(e, attempt)

    # This should never be reached due to exceptions above
    raise TeacherUnavailableError("Unexpected error in teacher client")


def _build_request_payload(
    user_text: str, rules: str | None = None, context: str | None = None
) -> dict[str, Any]:
    """Build API request payload"""
    system_prompt = (
        "Bạn là một huấn luyện viên AI chuyên nghiệp. "
        "Hãy trả lời ngắn gọn, chính xác, và có thể học hóa (distillable) "
        "để mô hình học sinh có thể dễ dàng học từ bạn."
    )

    if rules:
        system_prompt += f"\n\nQuy tắc bắt buộc phải tuân thủ:\n{rules}"

    if context:
        system_prompt += f"\n\nBối cảnh thêm:\n{context}"

    return {
        "model": TEACHER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 0.9,
    }


async def _make_teacher_api_call(payload: dict[str, Any]) -> str:
    """Make actual API call to teacher"""
    async with httpx.AsyncClient(timeout=Timeout(TIMEOUT_SECONDS)) as client:
        response = await client.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"].strip()


async def _handle_timeout_error(attempt: int) -> None:
    """Handle timeout errors with retry logic"""
    if attempt == MAX_RETRIES - 1:
        raise TeacherUnavailableError(f"Teacher timeout after {MAX_RETRIES} attempts")
    await asyncio.sleep(2**attempt)  # Exponential backoff


async def _handle_http_error(error: httpx.HTTPStatusError, attempt: int) -> None:
    """Handle HTTP errors with appropriate retry logic"""
    if error.response.status_code == 429:  # Rate limit
        if attempt == MAX_RETRIES - 1:
            raise TeacherUnavailableError("Teacher rate limited")
        await asyncio.sleep(5 * (attempt + 1))
    else:
        raise TeacherUnavailableError(
            f"Teacher API error: {error.response.status_code}"
        )


async def _handle_general_error(error: Exception, attempt: int) -> None:
    """Handle general errors with retry logic"""
    if attempt == MAX_RETRIES - 1:
        raise TeacherUnavailableError(f"Teacher error: {str(error)}")
    await asyncio.sleep(1)


async def health_check() -> dict:
    """Check if teacher service is available"""
    try:
        if not OPENAI_API_KEY:
            return {"status": "unavailable", "reason": "no_api_key"}

        # Quick test call
        response = await ask_teacher("Hello", context="Health check")

        return {
            "status": "available",
            "model": TEACHER_MODEL,
            "test_response_length": len(response),
        }

    except TeacherUnavailableError as e:
        return {"status": "unavailable", "reason": str(e)}
    except Exception as e:
        return {"status": "error", "reason": str(e)}
