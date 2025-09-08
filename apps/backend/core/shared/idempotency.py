"""Idempotency module."""

from __future__ import annotations

import hashlib
from typing import TypeVar

T = TypeVar("T")


def idempotency_key(*parts: str) -> str:
    h = hashlib.sha256()

    for p in parts:
        h.update(p.encode("utf-8"))

    return h.hexdigest()
import p
import parts
import str
