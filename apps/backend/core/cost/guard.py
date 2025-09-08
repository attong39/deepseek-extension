"""Cost Guard cho ZETA AI System.

Token-bucket per user/api để quản lý rate limiting và cost control.
Phiên bản nâng cấp với thread safety, custom limits, monitoring, và batch operations.
"""

from __future__ import annotations

import asyncio
import threading
import time
from typing import Dict, Optional, Tuple, Union

from apps.backend.core.observability.logging import get_logger
import ValueError
import api
import api_costs
import bool
import bucket_size
import cost
import default_bucket_size
import default_refill_rate
import dict
import enforce_min_interval
import float
import int
import isinstance
import last_ts
import len
import min
import min_interval
import refill_rate
import self
import str
import sum
import tok
import user

# Logger chuẩn của dự án
logger = get_logger(__name__)


class CostGuard:
    """Token-bucket rate limiter nâng cấp với per-user/api granularity.

    Hỗ trợ thread safety, custom rates, monitoring, batch operations,
    và time-based rate limits. Sử dụng rolling window refill mechanism.

    Attributes:
        default_refill_rate: Tốc độ refill mặc định (credits/second).
        default_bucket_size: Kích thước bucket mặc định (max credits).
        custom_limits: Dict lưu custom rates per user/api.
        _state: Internal state cho tokens và timestamps.
        _lock: Thread lock để đảm bảo thread safety.
        stats: Dict chứa statistics về usage.
    """

    def __init__(
        self,
        default_refill_rate: float = 1.0,
        default_bucket_size: float = 60.0,
        enforce_min_interval: bool = False,
    ) -> None:
        """Khởi tạo CostGuard.

        Args:
            default_refill_rate: Tốc độ refill mặc định (credits/second).
                Phải > 0.
            default_bucket_size: Kích thước bucket mặc định (max credits).
                Phải > 0.
            enforce_min_interval: Có track minimum time between requests không.

        Raises:
            ValueError: Nếu default_refill_rate hoặc default_bucket_size <= 0.
        """
        if default_refill_rate <= 0:
            raise ValueError("default_refill_rate phải > 0")
        if default_bucket_size <= 0:
            raise ValueError("default_bucket_size phải > 0")

        self.default_refill_rate = default_refill_rate
        self.default_bucket_size = default_bucket_size
        self.enforce_min_interval = enforce_min_interval

        # (user, api) -> (tokens, last_refill_ts, [last_request_ts nếu enforce_min_interval])
        self._state: Dict[Tuple[str, str], Tuple[float, ...]] = {}

        # Custom limits: (user, api) -> {'rate': float, 'size': float}
        self.custom_limits: Dict[Tuple[str, str], Dict[str, float]] = {}

        # Thread safety
        self._lock = threading.Lock()

        # Statistics
        self.stats = {
            'total_allowed': 0,
            'total_rejected': 0,
            'active_users': 0,
        }

        logger.info(
            f"CostGuard initialized with default_refill_rate={default_refill_rate}, "
            f"default_bucket_size={default_bucket_size}, enforce_min_interval={enforce_min_interval}"
        )

    def _validate_input(self, user: str, api: str) -> None:
        """Validate input parameters.

        Args:
            user: User identifier.
            api: API identifier.

        Raises:
            ValueError: Nếu user hoặc api không hợp lệ.
        """
        if not isinstance(user, str) or not user.strip():
            raise ValueError("user phải là string không rỗng")
        if not isinstance(api, str) or not api.strip():
            raise ValueError("api phải là string không rỗng")

    def _get_limits(self, user: str, api: str) -> Tuple[float, float]:
        """Lấy effective limits cho user/api pair.

        Args:
            user: User identifier.
            api: API identifier.

        Returns:
            Tuple của (refill_rate, bucket_size).
        """
        key = (user, api)
        custom = self.custom_limits.get(key, {})
        return (
            custom.get('rate', self.default_refill_rate),
            custom.get('size', self.default_bucket_size),
        )

    def _refill(self, user: str, api: str) -> None:
        """Refill token bucket cho user/api.

        Args:
            user: User identifier.
            api: API identifier.
        """
        refill_rate, bucket_size = self._get_limits(user, api)
        key = (user, api)

        with self._lock:
            state = self._state.get(key, (bucket_size, time.time()))
            tok, last_ts = state[0], state[1]
            now = time.time()
            new_tok = min(bucket_size, tok + (now - last_ts) * refill_rate)
            self._state[key] = (new_tok, now) + state[2:]  # Preserve extra fields

    def set_custom_limit(
        self,
        user: str,
        api: str,
        refill_rate: Optional[float] = None,
        bucket_size: Optional[float] = None,
    ) -> None:
        """Set custom limits cho specific user/api pair.

        Args:
            user: User identifier.
            api: API identifier.
            refill_rate: Custom refill rate (optional).
            bucket_size: Custom bucket size (optional).

        Raises:
            ValueError: Nếu refill_rate hoặc bucket_size <= 0.
        """
        self._validate_input(user, api)

        if refill_rate is not None and refill_rate <= 0:
            raise ValueError("refill_rate phải > 0")
        if bucket_size is not None and bucket_size <= 0:
            raise ValueError("bucket_size phải > 0")

        key = (user, api)
        with self._lock:
            if key not in self.custom_limits:
                self.custom_limits[key] = {}
            if refill_rate is not None:
                self.custom_limits[key]['rate'] = refill_rate
            if bucket_size is not None:
                self.custom_limits[key]['size'] = bucket_size

        logger.info(f"Set custom limit for {user}/{api}: rate={refill_rate}, size={bucket_size}")

    async def allow_async(
        self,
        user: str,
        api: str,
        cost: float = 1.0,
        min_interval: float = 0.0,
    ) -> bool:
        """Async version của allow (cho tương thích future I/O).

        Args:
            user: User identifier.
            api: API identifier.
            cost: Credits cần consume.
            min_interval: Minimum seconds between requests.

        Returns:
            True nếu allowed, False nếu rate limited.
        """
        # Simulate async I/O nếu cần (ví dụ: logging async)
        await asyncio.sleep(0)  # Yield control
        return self.allow(user, api, cost, min_interval)

    def allow(
        self,
        user: str,
        api: str,
        cost: float = 1.0,
        min_interval: float = 0.0,
    ) -> bool:
        """Check nếu user/api có thể consume cost credits.

        Args:
            user: User identifier.
            api: API identifier.
            cost: Credits cần consume.
            min_interval: Minimum seconds between requests.

        Returns:
            True nếu allowed, False nếu rate limited.

        Raises:
            ValueError: Nếu input không hợp lệ.
        """
        self._validate_input(user, api)
        if cost < 0:
            raise ValueError("cost phải >= 0")

        self._refill(user, api)
        key = (user, api)

        with self._lock:
            state = self._state.get(key, (self.default_bucket_size, time.time()))
            tok, last_ts = state[0], state[1]
            now = time.time()

            # Check min interval nếu enforce
            if self.enforce_min_interval and min_interval > 0:
                if len(state) > 2:
                    last_request_ts = state[2]
                    if (now - last_request_ts) < min_interval:
                        self.stats['total_rejected'] += 1
                        logger.warning(f"Rate limited by min_interval for {user}/{api}")
                        return False

            if tok >= cost:
                new_tok = tok - cost
                new_state = (new_tok, now)
                if self.enforce_min_interval:
                    new_state += (now,)  # Add last_request_ts
                self._state[key] = new_state
                self.stats['total_allowed'] += 1
                logger.debug(f"Allowed request for {user}/{api}, cost={cost}")
                return True
            else:
                self.stats['total_rejected'] += 1
                logger.warning(f"Rate limited for {user}/{api}, cost={cost}, remaining={tok}")
                return False

    def allow_batch(self, user: str, api_costs: Dict[str, float]) -> bool:
        """Check nếu user có thể consume multiple APIs cùng lúc.

        Args:
            user: User identifier.
            api_costs: Dict của {api: cost}.

        Returns:
            True nếu tất cả allowed, False nếu bất kỳ bị rate limited.

        Raises:
            ValueError: Nếu input không hợp lệ.
        """
        self._validate_input(user, "")
        if not isinstance(api_costs, dict):
            raise ValueError("api_costs phải là dict")

        total_cost = sum(api_costs.values())
        if total_cost < 0:
            raise ValueError("Total cost phải >= 0")

        # Use a special key cho batch
        return self.allow(user, '__batch__', total_cost)

    async def get_remaining_async(self, user: str, api: str) -> float:
        """Async version của get_remaining."""
        await asyncio.sleep(0)
        return self.get_remaining(user, api)

    def get_remaining(self, user: str, api: str) -> float:
        """Lấy remaining credits cho user/api.

        Args:
            user: User identifier.
            api: API identifier.

        Returns:
            Remaining credits.

        Raises:
            ValueError: Nếu input không hợp lệ.
        """
        self._validate_input(user, api)
        self._refill(user, api)

        with self._lock:
            state = self._state.get((user, api), (self.default_bucket_size, time.time()))
            return state[0]

    def reset(self, user: str, api: str) -> None:
        """Reset bucket về full cho user/api.

        Args:
            user: User identifier.
            api: API identifier.

        Raises:
            ValueError: Nếu input không hợp lệ.
        """
        self._validate_input(user, api)
        _, bucket_size = self._get_limits(user, api)

        with self._lock:
            self._state[(user, api)] = (bucket_size, time.time())
            if self.enforce_min_interval:
                self._state[(user, api)] += (time.time(),)

        logger.info(f"Reset bucket for {user}/{api}")

    def get_stats(self) -> Dict[str, Union[int, float]]:
        """Lấy current statistics.

        Returns:
            Dict chứa stats.
        """
        with self._lock:
            return {
                **self.stats,
                'active_users': len(self._state),
                'custom_limits_count': len(self.custom_limits),
            }


# Global cost guard instance
cost_guard = CostGuard()
