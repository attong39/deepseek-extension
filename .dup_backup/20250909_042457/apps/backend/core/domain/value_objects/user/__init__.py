# User Value Objects
from .auth import LoginRequest, RegisterRequest
from .permissions import ZetaAIPermission, ZetaAIRole
from .user_preferences import UserPreferences

__all__ = [
    "LoginRequest",
    "RegisterRequest",
    "ZetaAIPermission",
    "ZetaAIRole",
    "UserPreferences",
]
# >>> AUTO-GEN (ai_runner)
__all__ = [
    "auth",
    "permissions",
    "user_preferences",
]

# <<< AUTO-GEN
