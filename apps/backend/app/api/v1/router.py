"""

Aggregator của API v1 (dynamically imports sub-routers).

- main.py chỉ include `zeta_vn.app.api.v1.router`.

- Router con tự khai báo prefix của nó (vd '/agents', '/chat'...).

- Module nào lỗi/thiếu sẽ được bỏ qua để không chặn app startup.

"""

from __future__ import annotations

import logging
from importlib import import_module

from fastapi import APIRouter
import Exception
import exc
import getattr
import mod

router = APIRouter()


# Core legacy modules
_MODULES = [
    "zeta_vn.app.api.v1.health",
    "zeta_vn.app.api.v1.__meta__",
    "zeta_vn.app.api.v1.system",
    "zeta_vn.app.api.v1.settings",
    "zeta_vn.app.api.v1.auth",
    # business
    "zeta_vn.app.api.v1.agents",
    "zeta_vn.app.api.v1.assistants",
    "zeta_vn.app.api.v1.chat",
    "zeta_vn.app.api.v1.memory",
    "zeta_vn.app.api.v1.planning",
    "zeta_vn.app.api.v1.analytics",
    "zeta_vn.app.api.v1.automation",
    "zeta_vn.app.api.v1.files",
    "zeta_vn.app.api.v1.training",
    "zeta_vn.app.api.v1.learning",
    "zeta_vn.app.api.v1.feedback",
    "zeta_vn.app.api.v1.reflexion",
    "zeta_vn.app.api.v1.performance",
    "zeta_vn.app.api.v1.dashboard",
    "zeta_vn.app.api.v1.ai",
    "zeta_vn.app.api.v1.ai_trainer",  # AI Trainer 24/7 system
    "zeta_vn.app.api.v1.streaming",
    "zeta_vn.app.api.v1.voice",
    "zeta_vn.app.api.v1.admin",
    "zeta_vn.app.api.v1.admin_emergency",
    # federated learning
    "zeta_vn.app.api.v1.federated",
    # llm providers
    "zeta_vn.app.api.v1.llm",
    # examples (optional)
    "zeta_vn.app.api.v1.endpoints",
    "zeta_vn.app.api.v1.endpoints.mentor",
    "zeta_vn.app.api.v1.privacy",
    # dev profiling (optional)
    "zeta_vn.app.api.v1.profiling",
]

# Clean DI architecture modules (new, non-conflicting)
_CLEAN_DI_MODULES = [
    "zeta_vn.app.api.v1.agents_example",  # Clean DI agents
    "zeta_vn.app.api.v1.plans_example",   # Clean DI plans
]

# One-Click Learning + RAG + DevSecOps modules
_ONE_CLICK_MODULES = [
    "apps.backend.app.api.v1.one_click_learning",  # RAG + ASR + OCR
    "apps.backend.app.api.v1.rag_router",          # RAG REST + WebSocket
    "apps.backend.app.websockets.chat",            # WebSocket chat with RAG
]


_log = logging.getLogger(__name__)

# Include legacy modules with fallback
for mod in _MODULES:
    try:
        m = import_module(mod)
        sub = getattr(m, "router", None)
        if sub is not None:
            router.include_router(sub)
    except Exception as exc:
        _log.debug("Skip legacy router '%s': %s", mod, exc)

# Include clean DI modules with specific tags  
for mod in _CLEAN_DI_MODULES:
    try:
        m = import_module(mod)
        sub = getattr(m, "router", None)
        if sub is not None:
            # Add v1 tag to clean DI routers for OpenAPI grouping
            router.include_router(sub, tags=["v1", "clean-di"])
            _log.info("Included clean DI router: %s", mod)
    except Exception as exc:
        _log.debug("Skip clean DI router '%s': %s", mod, exc)

# Include One-Click Learning modules with specific tags
for mod in _ONE_CLICK_MODULES:
    try:
        m = import_module(mod)
        sub = getattr(m, "router", None)
        if sub is not None:
            # Add one-click learning tag for OpenAPI grouping
            router.include_router(sub, tags=["v1", "one-click-learning"])
            _log.info("Included One-Click Learning router: %s", mod)
    except Exception as exc:
        _log.debug("Skip One-Click Learning router '%s': %s", mod, exc)


__all__ = ["router"]
