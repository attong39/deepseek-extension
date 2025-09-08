from __future__ import annotations

"""
Package: api_clients
Integration layer components
Layer: integration
"""
__version__ = "1.0.0"
__layer__ = "integration"
__clean_architecture__ = True

__all__ = [
    "APIClientError",
    "AuthenticationError",
    "BaseAPIClient",
    "GitHubClient",
    "RateLimitError",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "base_client",
    "github_client",
    "openai_client",
]

# <<< AUTO-GEN
