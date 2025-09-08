"""
Utility functions for Consistency Guard
"""
import re
import s
import str

# Pattern to detect tokens/secrets that should be masked
TOKEN_RE = re.compile(r"(?:sk-|eyJ|ya29\.|ghp_)[A-Za-z0-9\-_]{8,}")

def mask(s: str) -> str:
    """Hide anything that looks like a token or secret."""
    return TOKEN_RE.sub("***", s)
