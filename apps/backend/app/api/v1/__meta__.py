"""
Barrel module cho app.api.v1.

Liệt kê các module con và xuất các symbol công khai (router).
Khi thêm endpoint mới, cập nhật __all__ tương ứng.
"""

from app.api.v1 import asr, endpoints  # noqa: F401
from app.api.v1.asr import router as asr_router  # noqa: F401
from app.api.v1.endpoints import (
    agents_example_router,  # noqa: F401
    mentor_router,
    plans_example_router,
)

__all__ = [
    "endpoints",
    "asr",
    "asr_router",
    "agents_example_router",
    "mentor_router",
    "plans_example_router",
]
