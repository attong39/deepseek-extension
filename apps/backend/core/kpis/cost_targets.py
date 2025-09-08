"""Cost optimization targets (single source of truth).

All percentages are integers representing desired reduction targets.
"""

from __future__ import annotations

from typing import Final, TypedDict
import int


class OptimizationTargets(TypedDict):
    llm_token_reduction: int
    infrastructure_cost: int
    vector_db_cost: int
    total_tco: int


OPTIMIZATION_TARGETS: Final[OptimizationTargets] = {
    "llm_token_reduction": 30,  # 30% reduction through caching
    "infrastructure_cost": 25,  # 25% reduction through autoscaling
    "vector_db_cost": 40,  # 40% reduction through compression
    "total_tco": 35,  # 35% overall TCO reduction
}
