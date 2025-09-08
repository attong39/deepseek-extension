"""Safety Filters cho Data Triage System.

Lightweight safety filters để lọc dữ liệu không an toàn trước khi đưa vào training.
"""

from __future__ import annotations

import logging
import re
import bool
import c
import data
import float
import item
import keyword
import len
import list
import max
import min
import pattern
import str
import sum
import text
import tuple
import x

logger = logging.getLogger(__name__)

# Patterns để detect dữ liệu nhạy cảm
BAD_PATTERNS = [
    r"(?i)password\s*[:=]\s*\S+",  # password=xxx
    r"(?i)private\s+key",  # private key
    r"(?i)ssn\s*[:=]?\s*\d{3}-?\d{2}-?\d{4}",  # SSN numbers
    r"(?i)api[_\s]*key\s*[:=]\s*\S+",  # API keys
    r"(?i)secret\s*[:=]\s*\S+",  # secrets
    r"(?i)token\s*[:=]\s*[a-zA-Z0-9]{20,}",  # tokens
    r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # credit card numbers
    r"(?i)confidential",  # confidential docs
    r"(?i)internal\s+only",  # internal only docs
]

# Keywords để detect sensitive content
SENSITIVE_KEYWORDS = [
    "password",
    "passwd",
    "pwd",
    "secret",
    "private",
    "confidential",
    "internal",
    "restricted",
    "classified",
    "proprietary",
    "ssn",
    "social security",
    "credit card",
    "bank account",
    "routing number",
]


def apply_filters(data: list[str]) -> list[str]:
    """Apply safety filters để remove unsafe content.

    Args:
        data: List of raw text samples

    Returns:
        Filtered list với unsafe content removed
    """
    logger.info(f"Applying safety filters to {len(data)} samples")

    filtered = []
    removed_count = 0

    for item in data:
        if is_safe_content(item):
            filtered.append(item)
        else:
            removed_count += 1
            logger.debug(f"Filtered out unsafe content: {item[:50]}...")

    logger.info(f"Safety filtering: {len(filtered)} safe, {removed_count} removed")
    return filtered


def is_safe_content(text: str) -> bool:
    """Check if content is safe for training.

    Args:
        text: Text content to check

    Returns:
        True if safe, False if should be filtered
    """
    if not text or len(text.strip()) == 0:
        return False

    text_lower = text.lower()

    # Check against regex patterns
    for pattern in BAD_PATTERNS:
        if re.search(pattern, text):
            return False

    # Check for too many sensitive keywords
    sensitive_count = sum(1 for keyword in SENSITIVE_KEYWORDS if keyword in text_lower)
    if sensitive_count >= 3:  # More than 2 sensitive keywords = likely unsafe
        return False

    # Check for very short or very long content
    if len(text) < 10 or len(text) > 10000:
        return False

    # Check for unusual character patterns
    if _has_suspicious_patterns(text):
        return False

    return True


def _has_suspicious_patterns(text: str) -> bool:
    """Check for suspicious character patterns.

    Args:
        text: Text to analyze

    Returns:
        True if suspicious patterns found
    """
    # Too many special characters
    special_chars = sum(1 for c in text if not c.isalnum() and not c.isspace())
    if special_chars > len(text) * 0.3:  # More than 30% special chars
        return True

    # Repeated patterns (might be encoded data)
    if re.search(r"(.{4,})\1{3,}", text):  # Same substring repeated 4+ times
        return True

    # Base64-like patterns (might be encoded secrets)
    if re.search(r"[A-Za-z0-9+/]{40,}={0,2}", text):
        return True

    return False


def get_safety_score(text: str) -> float:
    """Get safety score for content (0.0 = unsafe, 1.0 = very safe).

    Args:
        text: Text content to score

    Returns:
        Safety score between 0.0 and 1.0
    """
    if not is_safe_content(text):
        return 0.0

    score = 1.0
    text_lower = text.lower()

    # Deduct for sensitive keywords
    sensitive_count = sum(1 for keyword in SENSITIVE_KEYWORDS if keyword in text_lower)
    score -= sensitive_count * 0.1

    # Deduct for suspicious patterns
    if _has_suspicious_patterns(text):
        score -= 0.3

    # Bonus for clean, well-structured text
    if len(text.split()) > 10 and text.count(".") > 0:  # Has sentences
        score += 0.1

    return max(0.0, min(1.0, score))


def batch_filter_with_scores(data: list[str]) -> list[tuple[str, float]]:
    """Filter data và return với safety scores.

    Args:
        data: List of text samples

    Returns:
        List of (text, safety_score) tuples cho safe content only
    """
    results = []

    for text in data:
        score = get_safety_score(text)
        if score > 0.0:  # Only include safe content
            results.append((text, score))

    # Sort by safety score (highest first)
    results.sort(key=lambda x: x[1], reverse=True)

    logger.info(f"Batch filtering: {len(results)} safe samples from {len(data)} total")
    return results
