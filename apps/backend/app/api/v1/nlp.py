"""
NLP Parser - Offline command processing
100% local, không sử dụng external APIs như GPT-4
"""

from __future__ import annotations

import json
import re
from typing import Any

from app.api.v1._common.security import TokenClaims, require_auth
from app.services.llm_adapter import generate_local
from fastapi import APIRouter, Depends
from pydantic import BaseModel
import Exception
import ValueError
import any
import claims
import dict
import float
import int
import isinstance
import keyword
import language
import len
import llm_result
import request
import result
import str
import test_result
import text

router = APIRouter(prefix="/api/v1/nlp", tags=["nlp"])


class ParseRequest(BaseModel):
    """Request for NLP parsing"""

    text: str
    language: str = "vi"  # vi, en
    context: dict[str, Any] = {}


class ParseResponse(BaseModel):
    """NLP parsing response"""

    action: str
    parameters: dict[str, Any]
    confidence: float
    original_text: str
    detected_language: str


def _detect_language(text: str) -> str:
    """Simple language detection"""
    vietnamese_chars = re.findall(
        r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
        text.lower(),
    )
    english_words = re.findall(r"\b[a-zA-Z]+\b", text)

    if len(vietnamese_chars) > 0:
        return "vi"
    elif len(english_words) > 3:
        return "en"
    else:
        return "unknown"


def _extract_with_rules(text: str) -> dict[str, Any]:
    """Rule-based extraction for common patterns"""
    text_lower = text.lower()

    # Automation commands
    if any(keyword in text_lower for keyword in ["click", "nhấn", "bấm"]):
        # Extract coordinates or element names
        coords = re.findall(r"(\d+)[,\s]*(\d+)", text)
        if coords:
            return {
                "action": "click",
                "parameters": {
                    "x": int(coords[0][0]),
                    "y": int(coords[0][1]),
                    "method": "coordinate",
                },
            }

        # Extract button/element names
        button_match = re.search(
            r'(?:button|nút|element)\s*["\']([^"\']+)["\']', text_lower
        )
        if button_match:
            return {
                "action": "click",
                "parameters": {"element": button_match.group(1), "method": "element"},
            }

    # Text input commands
    if any(keyword in text_lower for keyword in ["type", "gõ", "nhập"]):
        text_match = re.search(r'["\']([^"\']+)["\']', text)
        if text_match:
            return {"action": "type", "parameters": {"text": text_match.group(1)}}

    # Wait commands
    if any(keyword in text_lower for keyword in ["wait", "đợi", "chờ"]):
        time_match = re.search(r"(\d+)\s*(?:second|giây|s)", text_lower)
        duration = int(time_match.group(1)) if time_match else 1
        return {
            "action": "wait",
            "parameters": {"duration": duration, "unit": "seconds"},
        }

    # Screenshot commands
    if any(keyword in text_lower for keyword in ["screenshot", "chụp", "capture"]):
        return {"action": "screenshot", "parameters": {"save_path": "auto"}}

    # File operations
    if any(keyword in text_lower for keyword in ["open", "mở", "file"]):
        file_match = re.search(r'["\']([^"\']+)["\']', text)
        if file_match:
            return {"action": "open_file", "parameters": {"path": file_match.group(1)}}

    # Question/search commands
    if any(
        keyword in text_lower for keyword in ["what", "how", "gì", "như thế nào", "tìm"]
    ):
        return {"action": "search", "parameters": {"query": text, "type": "question"}}

    # Default: general command
    return {"action": "general", "parameters": {"text": text, "type": "unrecognized"}}


def _parse_with_local_llm(text: str, language: str) -> dict[str, Any]:
    """Use local LLM for complex parsing"""
    # Prepare prompt based on language
    if language == "vi":
        prompt = f"""Phân tích lệnh sau và trả về JSON với format: {{"action": string, "parameters": object}}
Chỉ trả về JSON thuần, không giải thích.

Các action hỗ trợ:
- click: nhấn chuột (parameters: x, y hoặc element)
- type: gõ text (parameters: text)
- wait: chờ đợi (parameters: duration)
- screenshot: chụp màn hình
- open_file: mở file (parameters: path)
- search: tìm kiếm (parameters: query)
- general: lệnh tổng quát

Lệnh: "{text}"
JSON:"""
    else:
        prompt = f"""Parse this command and return JSON with format: {{"action": string, "parameters": object}}
Return only pure JSON, no explanations.

Supported actions:
- click: mouse click (parameters: x, y or element)
- type: text input (parameters: text)
- wait: delay (parameters: duration)
- screenshot: capture screen
- open_file: open file (parameters: path)
- search: search query (parameters: query)
- general: general command

Command: "{text}"
JSON:"""

    try:
        response = generate_local(
            prompt, temperature=0.1
        )  # Low temperature for consistency

        # Clean up response and extract JSON
        response = response.strip()

        # Remove code blocks if present
        if response.startswith("```"):
            response = re.sub(r"^```(?:json)?\n?", "", response)
            response = re.sub(r"\n?```$", "", response)

        # Try to parse JSON
        _ = json.loads(response)

        # Validate structure
        if isinstance(result, dict) and "action" in result and "parameters" in result:
            return result
        else:
            raise ValueError("Invalid JSON structure")

    except (json.JSONDecodeError, ValueError):
        # Fallback to rule-based if LLM fails
        return _extract_with_rules(text)


@router.post("/parse", response_model=ParseResponse)
async def parse_command(
    request: ParseRequest, claims: TokenClaims = Depends(require_auth)
) -> ParseResponse:
    """
    Parse natural language command into structured action

    Security: Requires authentication, all team members can use
    """
    # Detect language if not specified
    detected_lang = (
        _detect_language(request.text)
        if request.language == "auto"
        else request.language
    )

    # Try rule-based parsing first (faster)
    _ = _extract_with_rules(request.text)
    confidence = 0.8  # High confidence for rule-based matches

    # If rule-based parsing returns generic action, try LLM
    if result["action"] == "general":
        try:
            _parse_with_local_llm(request.text, detected_lang)
            if llm_result["action"] != "general":
                _ = llm_result
                confidence = 0.6  # Lower confidence for LLM parsing
        except Exception:
            # Keep rule-based result if LLM fails
            confidence = 0.3

    return ParseResponse(
        action=result["action"],
        parameters=result["parameters"],
        confidence=confidence,
        original_text=request.text,
        detected_language=detected_lang,
    )


@router.get("/supported-actions")
async def get_supported_actions(
    claims: TokenClaims = Depends(require_auth),
) -> dict[str, Any]:
    """Get list of supported NLP actions"""
    return {
        "actions": {
            "click": {
                "description": "Mouse click operation",
                "parameters": ["x", "y", "element"],
                "examples": ["Click at 100,200", "Nhấn nút OK"],
            },
            "type": {
                "description": "Text input operation",
                "parameters": ["text"],
                "examples": ["Type 'Hello World'", "Gõ 'Xin chào'"],
            },
            "wait": {
                "description": "Wait/delay operation",
                "parameters": ["duration"],
                "examples": ["Wait 5 seconds", "Đợi 3 giây"],
            },
            "screenshot": {
                "description": "Screenshot capture",
                "parameters": ["save_path"],
                "examples": ["Take screenshot", "Chụp màn hình"],
            },
            "open_file": {
                "description": "File operations",
                "parameters": ["path"],
                "examples": ["Open 'file.txt'", "Mở file 'data.csv'"],
            },
            "search": {
                "description": "Search operations",
                "parameters": ["query", "type"],
                "examples": ["What is AI?", "Tìm thông tin về Python"],
            },
        },
        "languages": ["vi", "en", "auto"],
        "processing_methods": ["rule_based", "local_llm"],
        "team_id": claims.team_id,
    }


@router.get("/health")
async def nlp_health(claims: TokenClaims = Depends(require_auth)) -> dict[str, Any]:
    """NLP service health check"""
    # Test parsing
    _extract_with_rules("Click at 100,100")

    return {
        "status": "healthy",
        "rule_engine": "active",
        "llm_fallback": "available",
        "supported_languages": ["vi", "en"],
        "test_parsing": test_result["action"] == "click",
        "team_id": claims.team_id,
    }
