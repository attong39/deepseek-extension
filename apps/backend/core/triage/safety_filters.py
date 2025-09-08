"""Safety filters for data triage system.

Cung cấp các safety filters để đánh giá độ an toàn của dữ liệu
trước khi đưa vào training pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any
import content
import content_type
import dict
import float
import len
import list
import pattern
import str


class SafetyLevel(str, Enum):
    """Mức độ an toàn của dữ liệu."""

    SAFE = "safe"
    MODERATE = "moderate"
    HIGH_RISK = "high_risk"
    CRITICAL = "critical"


@dataclass
class SafetyResult:
    """Kết quả đánh giá safety."""

    level: SafetyLevel
    confidence: float
    reasons: list[str]
    metadata: dict[str, Any]


def evaluate_data_safety(
    content: str, content_type: str = "text", context: dict[str, Any] | None = None
) -> SafetyResult:
    """Đánh giá mức độ an toàn của dữ liệu.

    Args:
        content: Nội dung cần đánh giá
        content_type: Loại nội dung (text, image, etc.)
        context: Context thêm cho đánh giá

    Returns:
        SafetyResult: Kết quả đánh giá safety
    """
    # Basic safety check implementation
    reasons = []
    confidence = 0.8

    # Check for basic unsafe patterns
    unsafe_patterns = [
        "password",
        "secret",
        "key",
        "token",
        "personal",
        "private",
        "confidential",
    ]

    content_lower = content.lower()
    for pattern in unsafe_patterns:
        if pattern in content_lower:
            reasons.append(f"Contains potentially sensitive term: {pattern}")

    # Determine safety level based on findings
    if len(reasons) == 0:
        level = SafetyLevel.SAFE
    elif len(reasons) <= 2:
        level = SafetyLevel.MODERATE
    elif len(reasons) <= 4:
        level = SafetyLevel.HIGH_RISK
    else:
        level = SafetyLevel.CRITICAL

    return SafetyResult(
        level=level,
        confidence=confidence,
        reasons=reasons,
        metadata={
            "content_type": content_type,
            "content_length": len(content),
            "patterns_found": len(reasons),
        },
    )
