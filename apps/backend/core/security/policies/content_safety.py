"""Content safety policies for filtering and monitoring content.





Provides policies and mechanisms for ensuring content safety,


including detection of harmful, inappropriate, or malicious content.


"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any
import bool
import bytes
import content
import dict
import domain
import enabled
import enumerate
import f
import filter_name
import float
import i
import isinstance
import len
import list
import min
import name
import pattern
import profanity_words
import self
import severity_threshold
import str
import sum
import super
import tld
import tuple
import violation
import word


class ContentRiskLevel(Enum):
    """Risk levels for content assessment."""

    SAFE = "safe"

    LOW_RISK = "low_risk"

    MEDIUM_RISK = "medium_risk"

    HIGH_RISK = "high_risk"

    DANGEROUS = "dangerous"


class ContentCategory(Enum):
    """Categories of content for classification."""

    TEXT = "text"

    CODE = "code"

    IMAGE = "image"

    AUDIO = "audio"

    VIDEO = "video"

    DOCUMENT = "document"

    URL = "url"

    JSON_DATA = "json_data"


@dataclass
class ContentItem:
    """Content to be evaluated for safety."""

    content: str | bytes

    category: ContentCategory

    source: str

    user_id: str | None = None

    session_id: str | None = None

    metadata: dict[str, Any] | None = None


@dataclass
class SafetyAssessment:
    """Result of content safety evaluation."""

    risk_level: ContentRiskLevel

    is_safe: bool

    violations: list[str]

    confidence: float

    details: dict[str, Any] | None = None

    recommended_action: str | None = None


class BaseSafetyFilter(ABC):
    """Abstract base class for content safety filters."""

    def __init__(self, name: str, enabled: bool = True):
        """Initialize safety filter.





        Args:


            name: Filter name


            enabled: Whether filter is enabled


        """

        self.name = name

        self.enabled = enabled

    @abstractmethod
    async def assess_content(self, content: ContentItem) -> SafetyAssessment:
        """Assess content for safety violations.





        Args:


            content: Content to assess





        Returns:


            Safety assessment result


        """

    @abstractmethod
    def applies_to(self, content: ContentItem) -> bool:
        """Check if this filter applies to the content.





        Args:


            content: Content to check





        Returns:


            True if filter should be applied


        """


class ProfanityFilter(BaseSafetyFilter):
    """Filter for detecting profanity and offensive language."""

    def __init__(
        self,
        profanity_words: list[str] | None = None,
        severity_threshold: float = 0.7,
    ):
        """Initialize profanity filter.





        Args:


            profanity_words: List of profane words to detect


            severity_threshold: Threshold for triggering violations


        """

        super().__init__("profanity_filter")

        self.profanity_words = profanity_words or [
            # Add common profanity words here
            "damn",
            "hell",
            "shit",
            "fuck",
            "bitch",
            "ass",
            "crap",
        ]

        self.severity_threshold = severity_threshold

    def applies_to(self, content: ContentItem) -> bool:
        """Apply to text content."""

        return content.category == ContentCategory.TEXT

    async def assess_content(self, content: ContentItem) -> SafetyAssessment:
        """Assess text for profanity."""

        if not isinstance(content.content, str):
            return SafetyAssessment(
                risk_level=ContentRiskLevel.SAFE,
                is_safe=True,
                violations=[],
                confidence=1.0,
            )

        text = content.content.lower()

        found_words = []

        for word in self.profanity_words:
            if word.lower() in text:
                found_words.append(word)

        if not found_words:
            return SafetyAssessment(
                risk_level=ContentRiskLevel.SAFE,
                is_safe=True,
                violations=[],
                confidence=1.0,
            )

        # Calculate severity based on number and type of violations

        severity = len(found_words) / len(text.split()) * 10

        if severity >= self.severity_threshold:
            risk_level = ContentRiskLevel.MEDIUM_RISK

            is_safe = False

            action = "Content contains profanity and should be reviewed"

        else:
            risk_level = ContentRiskLevel.LOW_RISK

            is_safe = True

            action = "Minor profanity detected but within acceptable limits"

        return SafetyAssessment(
            risk_level=risk_level,
            is_safe=is_safe,
            violations=[f"Profanity detected: {', '.join(found_words)}"],
            confidence=min(1.0, severity + 0.3),
            details={"found_words": found_words, "severity": severity},
            recommended_action=action,
        )


class CodeSafetyFilter(BaseSafetyFilter):
    """Filter for detecting dangerous code patterns."""

    def __init__(self):
        """Initialize code safety filter."""

        super().__init__("code_safety_filter")

        self.dangerous_patterns = [
            # System commands
            "os.system",
            "subprocess.call",
            "ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(",
            "# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed",
            # File operations
            "open(",
            "file(",
            "delete",
            "remove",
            "rmdir",
            # Network operations
            "urllib",
            "requests",
            "socket",
            "http",
            # Dangerous imports
            "import os",
            "import sys",
            "import subprocess",
            # Shell commands
            "bash",
            "sh",
            "cmd",
            "powershell",
        ]

        self.high_risk_patterns = [
            "__import__",
            "compile(",
            "globals()",
            "locals()",
            "getattr(",
            "setattr(",
            "delattr(",
        ]

    def applies_to(self, content: ContentItem) -> bool:
        """Apply to code content."""

        return content.category == ContentCategory.CODE

    async def assess_content(self, content: ContentItem) -> SafetyAssessment:
        """Assess code for dangerous patterns."""

        if not isinstance(content.content, str):
            return SafetyAssessment(
                risk_level=ContentRiskLevel.SAFE,
                is_safe=True,
                violations=[],
                confidence=1.0,
            )

        code = content.content

        violations = []

        risk_score = 0

        # Check for dangerous patterns

        for pattern in self.dangerous_patterns:
            if pattern in code:
                violations.append(f"Dangerous pattern detected: {pattern}")

                risk_score += 1

        # Check for high-risk patterns

        for pattern in self.high_risk_patterns:
            if pattern in code:
                violations.append(f"High-risk pattern detected: {pattern}")

                risk_score += 3

        # Determine risk level

        if risk_score == 0:
            risk_level = ContentRiskLevel.SAFE

            is_safe = True

            action = None

        elif risk_score <= 2:
            risk_level = ContentRiskLevel.LOW_RISK

            is_safe = True

            action = "Code contains potentially risky patterns but may be acceptable"

        elif risk_score <= 5:
            risk_level = ContentRiskLevel.MEDIUM_RISK

            is_safe = False

            action = "Code contains dangerous patterns and should be reviewed"

        else:
            risk_level = ContentRiskLevel.HIGH_RISK

            is_safe = False

            action = "Code contains highly dangerous patterns and should be blocked"

        return SafetyAssessment(
            risk_level=risk_level,
            is_safe=is_safe,
            violations=violations,
            confidence=min(1.0, risk_score / 10 + 0.5),
            details={"risk_score": risk_score, "patterns_found": len(violations)},
            recommended_action=action,
        )


class URLSafetyFilter(BaseSafetyFilter):
    """Filter for assessing URL safety."""

    def __init__(self):
        """Initialize URL safety filter."""

        super().__init__("url_safety_filter")

        self.suspicious_domains = [
            "bit.ly",
            "tinyurl.com",
            "t.co",
            "goo.gl",  # URL shorteners
            "tempmail",
            "10minutemail",
            "guerrillamail",  # Temp email
        ]

        self.malicious_tlds = [
            ".tk",
            ".ml",
            ".ga",
            ".cf",  # Free domains often used maliciously
        ]

    def applies_to(self, content: ContentItem) -> bool:
        """Apply to URL content."""

        return content.category == ContentCategory.URL

    async def assess_content(self, content: ContentItem) -> SafetyAssessment:
        """Assess URL for safety."""

        if not isinstance(content.content, str):
            return SafetyAssessment(
                risk_level=ContentRiskLevel.SAFE,
                is_safe=True,
                violations=[],
                confidence=1.0,
            )

        url = content.content.lower()

        violations = []

        risk_score = 0

        # Check for suspicious domains

        for domain in self.suspicious_domains:
            if domain in url:
                violations.append(f"Suspicious domain detected: {domain}")

                risk_score += 2

        # Check for malicious TLDs

        for tld in self.malicious_tlds:
            if url.endswith(tld) or f"{tld}/" in url:
                violations.append(f"Malicious TLD detected: {tld}")

                risk_score += 3

        # Check for IP addresses instead of domains

        import re

        ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

        if re.search(ip_pattern, url):
            violations.append("Direct IP address used instead of domain")

            risk_score += 2

        # Check for non-HTTPS

        if url.startswith("http://"):
            violations.append("Non-HTTPS URL detected")

            risk_score += 1

        # Determine risk level

        if risk_score == 0:
            risk_level = ContentRiskLevel.SAFE

            is_safe = True

            action = None

        elif risk_score <= 2:
            risk_level = ContentRiskLevel.LOW_RISK

            is_safe = True

            action = "URL has minor risk factors but may be acceptable"

        elif risk_score <= 5:
            risk_level = ContentRiskLevel.MEDIUM_RISK

            is_safe = False

            action = "URL has concerning risk factors and should be reviewed"

        else:
            risk_level = ContentRiskLevel.HIGH_RISK

            is_safe = False

            action = "URL appears highly suspicious and should be blocked"

        return SafetyAssessment(
            risk_level=risk_level,
            is_safe=is_safe,
            violations=violations,
            confidence=min(1.0, risk_score / 8 + 0.4),
            details={"risk_score": risk_score},
            recommended_action=action,
        )


class DataPrivacyFilter(BaseSafetyFilter):
    """Filter for detecting personal and sensitive data."""

    def __init__(self):
        """Initialize data privacy filter."""

        super().__init__("data_privacy_filter")

    def applies_to(self, content: ContentItem) -> bool:
        """Apply to all text-based content."""

        return content.category in [ContentCategory.TEXT, ContentCategory.JSON_DATA]

    async def assess_content(self, content: ContentItem) -> SafetyAssessment:
        """Assess content for personal data."""

        if not isinstance(content.content, str):
            return SafetyAssessment(
                risk_level=ContentRiskLevel.SAFE,
                is_safe=True,
                violations=[],
                confidence=1.0,
            )

        text = content.content

        violations = []

        risk_score = 0

        # Check for email addresses

        import re

        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        emails = re.findall(email_pattern, text)

        if emails:
            violations.append(f"Email addresses detected: {len(emails)} found")

            risk_score += len(emails)

        # Check for phone numbers

        phone_pattern = (
            r"\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b"
        )

        phones = re.findall(phone_pattern, text)

        if phones:
            violations.append(f"Phone numbers detected: {len(phones)} found")

            risk_score += len(phones) * 2

        # Check for credit card numbers (basic pattern)

        cc_pattern = r"\b(?:\d{4}[-\s]?){3}\d{4}\b"

        credit_cards = re.findall(cc_pattern, text)

        if credit_cards:
            violations.append(
                f"Potential credit card numbers detected: {len(credit_cards)} found"
            )

            risk_score += len(credit_cards) * 5

        # Check for SSN (US Social Security Numbers)

        ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"

        ssns = re.findall(ssn_pattern, text)

        if ssns:
            violations.append(f"Potential SSN detected: {len(ssns)} found")

            risk_score += len(ssns) * 10

        # Determine risk level

        if risk_score == 0:
            risk_level = ContentRiskLevel.SAFE

            is_safe = True

            action = None

        elif risk_score <= 3:
            risk_level = ContentRiskLevel.LOW_RISK

            is_safe = True

            action = "Minor personal data detected, consider data handling policies"

        elif risk_score <= 10:
            risk_level = ContentRiskLevel.MEDIUM_RISK

            is_safe = False

            action = "Personal data detected, ensure proper handling and consent"

        else:
            risk_level = ContentRiskLevel.HIGH_RISK

            is_safe = False

            action = "Sensitive personal data detected, requires immediate review"

        return SafetyAssessment(
            risk_level=risk_level,
            is_safe=is_safe,
            violations=violations,
            confidence=min(1.0, risk_score / 20 + 0.6),
            details={
                "risk_score": risk_score,
                "emails_found": len(emails),
                "phones_found": len(phones),
                "credit_cards_found": len(credit_cards),
                "ssns_found": len(ssns),
            },
            recommended_action=action,
        )


class ContentSafetyEngine:
    """Engine for evaluating content safety using multiple filters."""

    def __init__(self):
        """Initialize content safety engine."""

        self.filters: list[BaseSafetyFilter] = []

    def add_filter(self, filter_instance: BaseSafetyFilter) -> None:
        """Add a safety filter to the engine.





        Args:


            filter_instance: Filter to add


        """

        self.filters.append(filter_instance)

    def remove_filter(self, name: str) -> bool:
        """Remove a filter by name.





        Args:


            name: Name of filter to remove





        Returns:


            True if filter was removed


        """

        for i, filter_instance in enumerate(self.filters):
            if filter_instance.name == name:
                del self.filters[i]

                return True

        return False

    async def assess_content(self, content: ContentItem) -> SafetyAssessment:
        """Assess content using all applicable filters.





        Args:


            content: Content to assess





        Returns:


            Combined safety assessment


        """

        applicable_filters = [
            f for f in self.filters if f.enabled and f.applies_to(content)
        ]

        if not applicable_filters:
            # No filters apply - consider safe by default

            return SafetyAssessment(
                risk_level=ContentRiskLevel.SAFE,
                is_safe=True,
                violations=[],
                confidence=1.0,
                recommended_action="No safety filters applied",
            )

        # Evaluate all applicable filters

        assessments = []

        for filter_instance in applicable_filters:
            assessment = await filter_instance.assess_content(content)

            assessments.append((filter_instance.name, assessment))

        # Combine assessments

        return self._combine_assessments(assessments)

    def _combine_assessments(
        self,
        assessments: list[tuple[str, SafetyAssessment]],
    ) -> SafetyAssessment:
        """Combine multiple safety assessments.





        Args:


            assessments: List of (filter_name, assessment) tuples





        Returns:


            Combined assessment


        """

        # Risk level priority: DANGEROUS > HIGH_RISK > MEDIUM_RISK > LOW_RISK > SAFE

        risk_priority = {
            ContentRiskLevel.DANGEROUS: 5,
            ContentRiskLevel.HIGH_RISK: 4,
            ContentRiskLevel.MEDIUM_RISK: 3,
            ContentRiskLevel.LOW_RISK: 2,
            ContentRiskLevel.SAFE: 1,
        }

        # Find highest risk level

        highest_risk = ContentRiskLevel.SAFE

        all_violations = []

        combined_details = {}

        confidence_scores = []

        recommended_actions = []

        for filter_name, assessment in assessments:
            if risk_priority[assessment.risk_level] > risk_priority[highest_risk]:
                highest_risk = assessment.risk_level

            # Collect violations with filter names

            for violation in assessment.violations:
                all_violations.append(f"{filter_name}: {violation}")

            # Combine details

            if assessment.details:
                combined_details[filter_name] = assessment.details

            # Collect confidence scores

            confidence_scores.append(assessment.confidence)

            # Collect recommended actions

            if assessment.recommended_action:
                recommended_actions.append(
                    f"{filter_name}: {assessment.recommended_action}"
                )

        # Determine overall safety

        is_safe = highest_risk in [ContentRiskLevel.SAFE, ContentRiskLevel.LOW_RISK]

        # Calculate combined confidence (average)

        avg_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 1.0
        )

        return SafetyAssessment(
            risk_level=highest_risk,
            is_safe=is_safe,
            violations=all_violations,
            confidence=avg_confidence,
            details=combined_details if combined_details else None,
            recommended_action="; ".join(recommended_actions)
            if recommended_actions
            else None,
        )

    def get_filter_names(self) -> list[str]:
        """Get list of all filter names.





        Returns:


            List of filter names


        """

        return [f.name for f in self.filters]

    def get_filter_by_name(self, name: str) -> BaseSafetyFilter | None:
        """Get filter by name.





        Args:


            name: Filter name





        Returns:


            Filter instance or None if not found


        """

        for filter_instance in self.filters:
            if filter_instance.name == name:
                return filter_instance

        return None

    def enable_filter(self, name: str) -> bool:
        """Enable a filter by name.





        Args:


            name: Filter name





        Returns:


            True if filter was found and enabled


        """

        filter_instance = self.get_filter_by_name(name)

        if filter_instance:
            filter_instance.enabled = True

            return True

        return False

    def disable_filter(self, name: str) -> bool:
        """Disable a filter by name.





        Args:


            name: Filter name





        Returns:


            True if filter was found and disabled


        """

        filter_instance = self.get_filter_by_name(name)

        if filter_instance:
            filter_instance.enabled = False

            return True

        return False


def create_default_content_safety_engine() -> ContentSafetyEngine:
    """Create a content safety engine with default filters.





    Returns:


        Configured content safety engine


    """

    engine = ContentSafetyEngine()

    # Add default filters

    engine.add_filter(ProfanityFilter())

    engine.add_filter(CodeSafetyFilter())

    engine.add_filter(URLSafetyFilter())

    engine.add_filter(DataPrivacyFilter())

    return engine
