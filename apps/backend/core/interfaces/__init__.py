"""Core interfaces package"""

from .repositories.agent_repository import AgentRepositoryInterface
from .repositories.user_repository import UserRepositoryInterface
from .services.ai_service import AIServiceInterface

__all__ = [
    "UserRepositoryInterface",
    "AgentRepositoryInterface",
    "AIServiceInterface",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "advanced_alerts",
    "alerts",
    "analytics_interfaces",
    "automation",
    "autonomy",
    "backup",
    "cache",
    "documentation",
    "external_services",
    "feature_toggles",
    "federated",
    "input_control",
    "llm_provider",
    "memory",
    "memory_backend",
    "metrics",
    "ml_interfaces",
    "mlops",
    "notification_interfaces",
    "observability",
    "perception",
    "security",
    "security_ai",
    "security_interfaces",
    "services",
    "storage_interfaces",
    "testing",
]

# <<< AUTO-GEN
