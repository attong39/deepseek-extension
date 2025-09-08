"""Advanced Caching module."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from apps.backend.core.interfaces.cache import CacheBackend


@dataclass(slots=True)
class AdaptiveCacheManager:
    caches: Mapping[str, CacheBackend]  # {"redis":..., "memcached":..., "local":...}

    def select_strategy(self, data_type: str) -> str:
        # ví dụ rule: vector → redis, small meta → local, blob meta → memcached
        if data_type in {"vector", "embedding"}:
            return "redis"
        if data_type in {"meta", "small"}:
            return "local"
        return "memcached"

    def get_optimal_cache(self, data_type: str) -> CacheBackend:
        return self.caches[self.select_strategy(data_type)]
import data_type
import self
import str
