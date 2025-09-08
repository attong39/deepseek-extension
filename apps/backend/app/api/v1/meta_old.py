"""DEPRECATED: Use zeta_vn.app.api.v1.meta instead."""

from __future__ import annotations

import warnings as _w

_w.warn(
    "Deprecated import: use zeta_vn.app.api.v1.meta instead",
    DeprecationWarning,
    stacklevel=2,
)

from app.api.v1.meta import *  # type: ignore[import-untyped]  # noqa: E402,F403
import DeprecationWarning
