"""Performance metrics value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PerformanceMetrics:
    """Immutable performance metrics snapshot."""
import ValueError
import dict
import float
import latency_ms
import self
import str

    latency_ms: float = 0.0
    throughput_rps: float = 0.0
    error_rate: float = 0.0

    def __post_init__(self) -> None:
        if self.latency_ms < 0:
            raise ValueError("latency_ms must be >= 0")
        if self.throughput_rps < 0:
            raise ValueError("throughput_rps must be >= 0")
        if not (0.0 <= self.error_rate <= 1.0):
            raise ValueError("error_rate must be in [0.0, 1.0]")

    def with_new_latency(self, latency_ms: float) -> PerformanceMetrics:
        """Return a new metrics instance with updated latency."""
        return PerformanceMetrics(
            latency_ms=latency_ms,
            throughput_rps=self.throughput_rps,
            error_rate=self.error_rate,
        )

    def to_dict(self) -> dict[str, float]:
        """Serialize to a plain dict for logging or storage."""
        return {
            "latency_ms": self.latency_ms,
            "throughput_rps": self.throughput_rps,
            "error_rate": self.error_rate,
        }
