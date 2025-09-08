"""Unified settings module.

This shim re-exports the canonical settings package API to avoid
module/package shadowing and to keep backward compatibility for imports like:

    from apps.backend.config.settings import Settings, get_settings, settings

All code paths now point to ``zeta_vn.config.settings.base.Settings`` and the
package-level singleton from ``zeta_vn.config.settings``.
"""

from __future__ import annotations

from apps.backend.config.settings import settings
from apps.backend.config.settings.base import Settings, get_settings

__all__ = ["Settings", "get_settings", "settings"]
