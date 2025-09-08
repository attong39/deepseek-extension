# zeta_vn/data/instrumentation/latency_timer.py
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any
import Exception
import float
import getattr
import property
import round
import self
import str
import type


@dataclass
class Timer:
    name: str
    start: float | None = None

    def __enter__(self) -> Timer:
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type: type | None, exc: Exception | None, tb: Any) -> None:
        self.duration = time.perf_counter() - (self.start or time.perf_counter())

    @property
    def ms(self) -> float:
        return round(getattr(self, "duration", 0.0) * 1000.0, 3)
