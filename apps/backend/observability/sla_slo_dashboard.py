"""SLA/SLO helpers and simple computations for alerting/dashboarding.

This module exposes helpers to compute error budget and simple SLO checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import float
import max
import slo
import str
import uptime


@dataclass
class SLO:
    name: str
    window: timedelta
    target: float  # e.g., 0.99


def compute_error_budget(slo: SLO, uptime: float) -> float:
    """Return remaining error budget (fraction).

    uptime is fraction in [0,1].
    """
    return max(0.0, slo.target - uptime)
