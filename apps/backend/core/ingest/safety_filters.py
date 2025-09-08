"""Safety filters for data quality control and security compliance.

Tự động phân loại và lọc dữ liệu đầu vào để đảm bảo chất lượng
và tuân thủ bảo mật trong hệ thống học liên tục.
"""

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from pydantic import BaseModel
import Exception
import bool
import c
import category
import content
import dict
import e
import enabled
import enumerate
import error_result
import f
import filter_instance
import filter_name
import float
import i
import int
import keywords
import kw
import len
import list
import max
import max_length
import min
import min_length
import name
import pattern
import patterns
import pii_type
import result
import safety_level
import self
import set
import str
import sum
import super
import tuple
import vuln_type

logger = logging.getLogger(__name__)


class SafetyLevel(str, Enum):
    """Mức độ bảo mật của dữ liệu."""

    SAFE = "safe"
    WARNING = "warning"
    BLOCKED = "blocked"
    QUARANTINE = "quarantine"


class DataCategory(str, Enum):
    """Loại dữ liệu để phân loại xử lý."""

    TEXT = "text"
    CODE = "code"
    CONVERSATION = "conversation"
    DOCUMENT = "document"
    IMAGE = "image"
    SYSTEM_LOG = "system_log"
    PERSONAL_INFO = "personal_info"
    FINANCIAL = "financial"
    MEDICAL = "medical"


@dataclass
class SafetyResult:
    """Kết quả đánh giá bảo mật dữ liệu."""

    level: SafetyLevel
    category: DataCategory
    confidence: float  # 0.0 - 1.0
    reasons: list[str]
    suggestions: list[str]
    metadata: dict[str, Any]


class ContentFilter(BaseModel):
    """Schema cho cấu hình bộ lọc nội dung."""

    name: str
    enabled: bool = True
    severity: SafetyLevel = SafetyLevel.WARNING
    patterns: list[str] = []
    keywords: set[str] = set()
    max_confidence: float = 1.0


class BaseSafetyFilter(ABC):
    """Abstract base class cho safety filters."""

    def __init__(self, name: str, enabled: bool = True):
        self.name = name
        self.enabled = enabled

    @abstractmethod
    def evaluate(self, content: str, metadata: dict[str, Any] = None) -> SafetyResult:
        """Đánh giá mức độ an toàn của nội dung."""


class PersonalInfoFilter(BaseSafetyFilter):
    """Lọc thông tin cá nhân (PII) trong dữ liệu."""

    def __init__(self):
        super().__init__("personal_info_filter")

        # Regex patterns cho PII detection
        self.patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
            "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            "url": r"https?://[^\s<>\"{}|\\^`\[\]]+",
        }

    def evaluate(self, content: str, metadata: dict[str, Any] = None) -> SafetyResult:
        """Detect PII trong nội dung."""
        if not self.enabled:
            return SafetyResult(
                level=SafetyLevel.SAFE,
                category=DataCategory.TEXT,
                confidence=1.0,
                reasons=[],
                suggestions=[],
                metadata={},
            )

        detected_pii = []
        confidence_score = 0.0

        for pii_type, pattern in self.patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                detected_pii.append(f"{pii_type}: {len(matches)} matches")
                confidence_score += 0.2

        if detected_pii:
            level = (
                SafetyLevel.BLOCKED if confidence_score > 0.6 else SafetyLevel.WARNING
            )
            return SafetyResult(
                level=level,
                category=DataCategory.PERSONAL_INFO,
                confidence=min(confidence_score, 1.0),
                reasons=detected_pii,
                suggestions=[
                    "Mask or remove personal information",
                    "Use synthetic data for training",
                    "Apply differential privacy techniques",
                ],
                metadata={"pii_types": list(self.patterns.keys())},
            )

        return SafetyResult(
            level=SafetyLevel.SAFE,
            category=DataCategory.TEXT,
            confidence=1.0,
            reasons=[],
            suggestions=[],
            metadata={},
        )


class ToxicityFilter(BaseSafetyFilter):
    """Lọc nội dung độc hại hoặc không phù hợp."""

    def __init__(self):
        super().__init__("toxicity_filter")

        # Keywords cho toxic content detection
        self.toxic_keywords = {
            "hate_speech": {"hate", "racist", "sexist", "discrimination"},
            "profanity": {"damn", "hell", "stupid", "idiot"},
            "violence": {"kill", "murder", "attack", "violence", "destroy"},
            "harassment": {"harassment", "bully", "threaten", "intimidate"},
        }

    def evaluate(self, content: str, metadata: dict[str, Any] = None) -> SafetyResult:
        """Detect toxic content."""
        if not self.enabled:
            return SafetyResult(
                level=SafetyLevel.SAFE,
                category=DataCategory.TEXT,
                confidence=1.0,
                reasons=[],
                suggestions=[],
                metadata={},
            )

        content_lower = content.lower()
        detected_issues = []
        confidence_score = 0.0

        for category, keywords in self.toxic_keywords.items():
            found_keywords = [kw for kw in keywords if kw in content_lower]
            if found_keywords:
                detected_issues.append(f"{category}: {found_keywords}")
                confidence_score += 0.25

        if detected_issues:
            level = (
                SafetyLevel.BLOCKED if confidence_score > 0.5 else SafetyLevel.WARNING
            )
            return SafetyResult(
                level=level,
                category=DataCategory.TEXT,
                confidence=min(confidence_score, 1.0),
                reasons=detected_issues,
                suggestions=[
                    "Filter out toxic content",
                    "Apply content moderation",
                    "Use cleaned datasets only",
                ],
                metadata={"toxic_categories": list(self.toxic_keywords.keys())},
            )

        return SafetyResult(
            level=SafetyLevel.SAFE,
            category=DataCategory.TEXT,
            confidence=1.0,
            reasons=[],
            suggestions=[],
            metadata={},
        )


class CodeSecurityFilter(BaseSafetyFilter):
    """Lọc code có thể có lỗ hổng bảo mật."""

    def __init__(self):
        super().__init__("code_security_filter")

        # Patterns cho security vulnerabilities
        self.security_patterns = {
            "sql_injection": [
                r"SELECT\s+\*\s+FROM\s+\w+\s+WHERE.*=.*['\"].*['\"]",
                r"DROP\s+TABLE",
                r"DELETE\s+FROM.*WHERE.*=.*['\"].*['\"]",
            ],
            "command_injection": [
                r"os\.system\(",
                r"subprocess\.call\(",
                r"eval\(",
                r"exec\(",
            ],
            "path_traversal": [
                r"\.\./",
                r"\.\.\\",
                r"/etc/passwd",
                r"..\\windows\\system32",
            ],
            "hardcoded_secrets": [
                r"password\s*=\s*['\"][^'\"]+['\"]",
                r"api_key\s*=\s*['\"][^'\"]+['\"]",
                r"secret\s*=\s*['\"][^'\"]+['\"]",
            ],
        }

    def evaluate(self, content: str, metadata: dict[str, Any] = None) -> SafetyResult:
        """Detect security vulnerabilities in code."""
        if not self.enabled:
            return SafetyResult(
                level=SafetyLevel.SAFE,
                category=DataCategory.CODE,
                confidence=1.0,
                reasons=[],
                suggestions=[],
                metadata={},
            )

        detected_vulns = []
        confidence_score = 0.0

        for vuln_type, patterns in self.security_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    detected_vulns.append(f"{vuln_type}: pattern matched")
                    confidence_score += 0.3
                    break  # Chỉ count một lần per vulnerability type

        if detected_vulns:
            level = (
                SafetyLevel.BLOCKED if confidence_score > 0.6 else SafetyLevel.WARNING
            )
            return SafetyResult(
                level=level,
                category=DataCategory.CODE,
                confidence=min(confidence_score, 1.0),
                reasons=detected_vulns,
                suggestions=[
                    "Review code for security vulnerabilities",
                    "Use static analysis tools",
                    "Apply secure coding practices",
                    "Sanitize user inputs",
                ],
                metadata={"vulnerability_types": list(self.security_patterns.keys())},
            )

        return SafetyResult(
            level=SafetyLevel.SAFE,
            category=DataCategory.CODE,
            confidence=1.0,
            reasons=[],
            suggestions=[],
            metadata={},
        )


class QualityFilter(BaseSafetyFilter):
    """Lọc dữ liệu kém chất lượng."""

    def __init__(self, min_length: int = 10, max_length: int = 100000):
        super().__init__("quality_filter")
        self.min_length = min_length
        self.max_length = max_length

    def evaluate(self, content: str, metadata: dict[str, Any] = None) -> SafetyResult:
        """Đánh giá chất lượng dữ liệu."""
        if not self.enabled:
            return SafetyResult(
                level=SafetyLevel.SAFE,
                category=DataCategory.TEXT,
                confidence=1.0,
                reasons=[],
                suggestions=[],
                metadata={},
            )

        issues = []
        confidence_score = 1.0

        # Check length
        if len(content) < self.min_length:
            issues.append(f"Content too short: {len(content)} < {self.min_length}")
            confidence_score -= 0.3

        if len(content) > self.max_length:
            issues.append(f"Content too long: {len(content)} > {self.max_length}")
            confidence_score -= 0.2

        # Check for garbled text (high ratio of special characters)
        special_chars = sum(1 for c in content if not c.isalnum() and not c.isspace())
        special_ratio = special_chars / len(content) if content else 0

        if special_ratio > 0.3:
            issues.append(f"High special character ratio: {special_ratio:.2f}")
            confidence_score -= 0.4

        # Check for excessive repetition
        words = content.split()
        if len(words) > 5:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.3:
                issues.append(f"Low word diversity: {unique_ratio:.2f}")
                confidence_score -= 0.3

        confidence_score = max(confidence_score, 0.0)

        if issues:
            level = (
                SafetyLevel.WARNING if confidence_score > 0.5 else SafetyLevel.BLOCKED
            )
            return SafetyResult(
                level=level,
                category=DataCategory.TEXT,
                confidence=1.0 - confidence_score,
                reasons=issues,
                suggestions=[
                    "Filter out low-quality content",
                    "Apply text preprocessing",
                    "Use quality scoring metrics",
                    "Implement content validation",
                ],
                metadata={
                    "length": len(content),
                    "special_ratio": special_ratio,
                    "unique_ratio": len(set(words)) / len(words) if words else 0,
                },
            )

        return SafetyResult(
            level=SafetyLevel.SAFE,
            category=DataCategory.TEXT,
            confidence=1.0,
            reasons=[],
            suggestions=[],
            metadata={"quality_score": confidence_score},
        )


class SafetyTriageSystem:
    """Hệ thống triage tự động cho data safety."""

    def __init__(self):
        self.filters: list[BaseSafetyFilter] = [
            PersonalInfoFilter(),
            ToxicityFilter(),
            CodeSecurityFilter(),
            QualityFilter(),
        ]

    def add_filter(self, filter_instance: BaseSafetyFilter) -> None:
        """Thêm safety filter mới."""
        self.filters.append(filter_instance)

    def remove_filter(self, filter_name: str) -> bool:
        """Remove safety filter theo tên."""
        for i, f in enumerate(self.filters):
            if f.name == filter_name:
                del self.filters[i]
                return True
        return False

    def evaluate_content(
        self, content: str, metadata: dict[str, Any] = None
    ) -> tuple[SafetyLevel, list[SafetyResult]]:
        """Đánh giá toàn diện nội dung qua tất cả filters."""
        if metadata is None:
            metadata = {}

        results = []
        overall_level = SafetyLevel.SAFE

        for filter_instance in self.filters:
            if not filter_instance.enabled:
                continue

            try:
                _ = filter_instance.evaluate(content, metadata)
                results.append(result)

                # Update overall safety level (take most restrictive)
                if result.level == SafetyLevel.BLOCKED:
                    overall_level = SafetyLevel.BLOCKED
                elif (
                    result.level == SafetyLevel.QUARANTINE
                    and overall_level != SafetyLevel.BLOCKED
                ):
                    overall_level = SafetyLevel.QUARANTINE
                elif (
                    result.level == SafetyLevel.WARNING
                    and overall_level == SafetyLevel.SAFE
                ):
                    overall_level = SafetyLevel.WARNING

            except Exception as e:
                logger.error(f"Error in filter {filter_instance.name}: {e}")
                # Create error result
                SafetyResult(
                    level=SafetyLevel.QUARANTINE,
                    category=DataCategory.TEXT,
                    confidence=0.0,
                    reasons=[f"Filter error: {str(e)}"],
                    suggestions=["Manual review required"],
                    metadata={"error": str(e)},
                )
                results.append(error_result)
                if overall_level == SafetyLevel.SAFE:
                    overall_level = SafetyLevel.QUARANTINE

        return overall_level, results

    def should_allow_training(self, safety_level: SafetyLevel) -> bool:
        """Quyết định có cho phép sử dụng dữ liệu cho training không."""
        return safety_level in [SafetyLevel.SAFE, SafetyLevel.WARNING]

    def get_filter_stats(self) -> dict[str, Any]:
        """Thống kê về các filters đang active."""
        return {
            "total_filters": len(self.filters),
            "enabled_filters": sum(1 for f in self.filters if f.enabled),
            "filter_names": [f.name for f in self.filters if f.enabled],
        }


# Singleton instance
_triage_system = None


def get_triage_system() -> SafetyTriageSystem:
    """Get singleton instance của triage system."""
    global _triage_system
    if _triage_system is None:
        _triage_system = SafetyTriageSystem()
    return _triage_system


def evaluate_data_safety(
    content: str, metadata: dict[str, Any] = None
) -> tuple[SafetyLevel, list[SafetyResult]]:
    """Convenience function để đánh giá data safety."""
    triage = get_triage_system()
    return triage.evaluate_content(content, metadata)


def is_safe_for_training(content: str, metadata: dict[str, Any] = None) -> bool:
    """Kiểm tra nhanh xem dữ liệu có an toàn cho training không."""
    safety_level, _ = evaluate_data_safety(content, metadata)
    return get_triage_system().should_allow_training(safety_level)
