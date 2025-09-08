from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from apps.backend.core.services.security_ai_service import SecurityAiService
import callable
import dict
import event
import float
import getattr
import kind
import max
import min
import self
import str
import v

logger = logging.getLogger(__name__)


@dataclass
class SecurityAiAgent:
    """Tác nhân tự trị điều chỉnh ngưỡng UEBA/Phishing theo phản hồi vận hành.

    - Theo dõi tỷ lệ alert và phản hồi FP/FN để điều chỉnh threshold nhỏ dần/lớn dần.
    - Không can thiệp mô hình, chỉ thay đổi tham số ngưỡng runtime (an toàn, nhanh).
    """

    service: SecurityAiService
    step: float = 0.02
    min_threshold: float = 0.5
    max_threshold: float = 0.99
    stats: dict[str, Any] = field(
        default_factory=lambda: {
            "alerts": 0,
            "events": 0,
            "fp": 0,
            "fn": 0,
        }
    )

    def _clamp(self, v: float) -> float:
        return max(self.min_threshold, min(self.max_threshold, v))

    def feedback(self, kind: str) -> None:
        """Ghi nhận phản hồi: 'fp' hoặc 'fn'."""
        if kind == "fp":
            self.stats["fp"] += 1
        elif kind == "fn":
            self.stats["fn"] += 1

    async def observe_event(self, event: dict[str, Any]) -> None:
        """Ghi nhận sự kiện và thích nghi ngưỡng nếu cần."""
        self.stats["events"] += 1
        res = await self.service.score_event(event)
        if res.label == "anomaly":
            self.stats["alerts"] += 1

    def adapt(self) -> dict[str, float]:
        """Thích nghi ngưỡng dựa trên thống kê gần nhất.

        Chiến lược đơn giản:
        - Tỷ lệ FP cao -> tăng threshold (giảm alert)
        - Tỷ lệ FN cao -> giảm threshold (tăng nhạy)
        - Nếu alert rate cao vượt 10% traffic -> tăng nhẹ threshold
        """
        # Lấy threshold hiện tại nếu có API, nếu không bỏ qua
        thr_ueba = getattr(self.service.ueba, "get_threshold", lambda: 0.85)()
        thr_phish = getattr(self.service.phishing, "get_threshold", lambda: 0.7)()

        alerts = float(self.stats.get("alerts", 0))
        events = float(self.stats.get("events", 1))
        fp = float(self.stats.get("fp", 0))
        fn = float(self.stats.get("fn", 0))

        # Tỷ lệ
        alert_rate = alerts / max(events, 1.0)
        fp_bias = fp - fn

        # Điều chỉnh theo bias
        if fp_bias > 0.5:
            thr_ueba = self._clamp(thr_ueba + self.step)
            thr_phish = self._clamp(thr_phish + self.step)
        elif fp_bias < -0.5:
            thr_ueba = self._clamp(thr_ueba - self.step)
            thr_phish = self._clamp(thr_phish - self.step)

        # Điều chỉnh theo alert rate tổng
        if alert_rate > 0.10:
            thr_ueba = self._clamp(thr_ueba + self.step / 2)

        # Áp dụng nếu có setter
        set_thr_ueba = getattr(self.service.ueba, "set_threshold", None)
        set_thr_phish = getattr(self.service.phishing, "set_threshold", None)
        if callable(set_thr_ueba):
            set_thr_ueba(thr_ueba)
        if callable(set_thr_phish):
            set_thr_phish(thr_phish)

        logger.debug(
            "SecurityAiAgent adapt: ueba=%.3f phishing=%.3f", thr_ueba, thr_phish
        )
        return {
            "ueba_threshold": float(thr_ueba),
            "phishing_threshold": float(thr_phish),
        }
