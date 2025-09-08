"""Compatibility shim: re-export canonical ChatService from subpackage.

DEPRECATED: Use zeta_vn.core.services.chat.service.ChatService instead.
"""

from __future__ import annotations

from apps.backend.core.services.chat.service import ChatService

__all__ = ["ChatService"]
