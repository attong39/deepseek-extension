"""Performance Optimizer Service (Optimized)

- Pluggable MetricProviders (psutil, Prometheus, custom)
- Rule Engine: priority, cooldown, enable/disable, throttling, dry-run
- SLO/Error Budget awareness (latency / error-rate targets)
- Backpressure & autoscaling hints (queue depth, rps, connections)
- Optional Prometheus & OpenTelemetry instrumentation (soft dependency)
- Background collector + EMA trends, bounded history
- Safe re-entrancy guard; plan-only support

Public API preserved:
- collect_metrics()
- analyze_performance()
- optimize_system(force: bool = False, *, dry_run: bool = False, plan_only: bool = False)
- optimize_agent(agent_id: UUID)
"""

from __future__ import annotations

import logging
import threading
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Protocol, cast, runtime_checkable
import Exception
import abs
import agent
import agent_id
import agent_repository
import any
import applied
import auto_optimize
import b
import background_collect_interval
import bool
import bottlenecks
import changes
import curr
import current
import dict
import dry_run
import e
import enabled
import float
import force
import getattr
import history_limit
import int
import interval
import interval_sec
import isinstance
import len
import limit
import list
import max
import memory_repository
import min
import name
import old
import plan_only
import planned
import prev
import provider
import r
import rec
import recommendation
import recs
import result
import rule
import self
import sorted
import str
import sum
import tuple
import x

# Third-party (soft dependencies)
try:  # OpenTelemetry
    from opentelemetry import trace  # type: ignore
except Exception:  # pragma: no cover
    trace = None  # type: ignore[assignment]

try:  # Prometheus
    from prometheus_client import Gauge  # type: ignore
except Exception:  # pragma: no cover
    Gauge = None

# First-party
from apps.backend.core.exceptions.business_exceptions import (
    BusinessException,
    EntityNotFoundError,
)

if TYPE_CHECKING:  # pragma: no cover - for type checkers only
    from collections.abc import Callable, Iterator
    from uuid import UUID

    from apps.backend.core.domain.entities.agent import Agent
    from apps.backend.core.domain.entities.memory import Memory
    from apps.backend.core.interfaces.repositories import (
        AgentRepository,
        MemoryRepository,
    )


logger = logging.getLogger(__name__)

_tracer = trace.get_tracer(__name__) if trace is not None else None


# ========================= Models =========================


@dataclass
class SLOConfig:
    """Targets for reliability; used to compute severity & error budget."""

    latency_p95_ms: float = 2000.0
    latency_p99_ms: float = 5000.0
    error_rate_max: float = 0.01  # 1%
    cache_hit_min: float = 0.80
    cpu_max: float = 0.85
    mem_max: float = 0.85


@dataclass
class PerformanceMetrics:
    """Performance metrics snapshot."""

    response_time: float = 0.0  # seconds (avg)
    memory_usage: float = 0.0  # 0..1
    cpu_usage: float = 0.0  # 0..1
    throughput: float = 0.0  # req/s
    error_rate: float = 0.0  # 0..1
    latency_p95: float = 0.0  # seconds
    latency_p99: float = 0.0  # seconds
    cache_hit_rate: float = 0.0  # 0..1
    queue_depth: int = 0
    active_connections: int = 0

    # Derived
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    ema_weight: float = 0.25

    def apply_ema(self, prev: PerformanceMetrics | None) -> PerformanceMetrics:
        if not prev:
            return self

        def _ema(curr: float, old: float) -> float:
            w = self.ema_weight
            return (w * curr) + ((1 - w) * old)

        return PerformanceMetrics(
            response_time=_ema(self.response_time, prev.response_time),
            memory_usage=_ema(self.memory_usage, prev.memory_usage),
            cpu_usage=_ema(self.cpu_usage, prev.cpu_usage),
            throughput=_ema(self.throughput, prev.throughput),
            error_rate=_ema(self.error_rate, prev.error_rate),
            latency_p95=_ema(self.latency_p95, prev.latency_p95),
            latency_p99=_ema(self.latency_p99, prev.latency_p99),
            cache_hit_rate=_ema(self.cache_hit_rate, prev.cache_hit_rate),
            queue_depth=int(_ema(float(self.queue_depth), float(prev.queue_depth))),
            active_connections=int(
                _ema(float(self.active_connections), float(prev.active_connections))
            ),
            timestamp=self.timestamp,
            ema_weight=self.ema_weight,
        )

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class PerformanceReport:
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metrics: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    bottlenecks: list[dict[str, Any]] = field(default_factory=list)
    recommendations: list[dict[str, Any]] = field(default_factory=list)
    trends: dict[str, Any] = field(default_factory=dict)
    severity: str = "normal"  # normal | warning | critical
    error_budget_burn: float = 0.0


@dataclass
class OptimizationResult:
    rule_name: str
    actions: list[str]
    applied: bool
    estimated_improvement: str
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class OptimizationRule:
    name: str
    condition: Callable[[PerformanceMetrics, SLOConfig], bool]
    action: Callable[[PerformanceMetrics], OptimizationResult]
    priority: int = 10
    description: str = ""
    cooldown: float = 60.0
    enabled: bool = True
    last_applied: datetime | None = None
    apply_count: int = 0
    last_error: str | None = None

    def ready(self, now: datetime) -> bool:
        if not self.enabled:
            return False
        if self.last_applied is None:
            return True
        return (now - self.last_applied).total_seconds() >= self.cooldown


# ==================== Metric Providers ====================


@runtime_checkable
class MetricProvider(Protocol):
    def collect(self) -> PerformanceMetrics: ...


class PsutilMetricProvider:
    def __init__(self) -> None:
        try:
            import psutil  # type: ignore

            self._psutil = psutil
            self._ok = True
        except Exception:  # pragma: no cover
            self._psutil = None
            self._ok = False

    def collect(self) -> PerformanceMetrics:
        if not self._ok or self._psutil is None:
            # Fallback zeros, optimizer will blend with other providers if any
            return PerformanceMetrics()
        ps = cast("Any", self._psutil)
        vm = ps.virtual_memory()
        cpu = ps.cpu_percent(interval=0.0) / 100.0
        # We do not have RPS/latency from psutil; leave 0.0 to be supplied by app metrics
        return PerformanceMetrics(
            cpu_usage=cpu,
            memory_usage=vm.used / max(float(vm.total), 1.0),
        )


class DummyAppMetricProvider:
    """Example app-level provider (replace with real exporter/SDK)."""

    def collect(self) -> PerformanceMetrics:
        # Simulated metrics as a safe baseline
        return PerformanceMetrics(
            response_time=2.5,
            memory_usage=0.65,
            cpu_usage=0.45,
            throughput=150.0,
            error_rate=0.02,
            latency_p95=4.2,
            latency_p99=8.1,
            cache_hit_rate=0.85,
            queue_depth=12,
            active_connections=45,
        )


# ================== Performance Optimizer =================


class PerformanceOptimizer:
    """
    Service for optimizing system performance.

    Public API preserved:
      - collect_metrics()
      - analyze_performance()
      - optimize_system(force: bool = False)
      - optimize_agent(agent_id: UUID)
    """

    def __init__(
        self,
        agent_repository: AgentRepository,
        memory_repository: MemoryRepository,
        *,
        slo: SLOConfig | None = None,
        history_limit: int = 200,
        auto_optimize: bool = True,
        background_collect_interval: float | None = None,  # seconds
    ) -> None:
        self.agent_repository = agent_repository
        self.memory_repository = memory_repository

        self.slo = slo or SLOConfig()
        self.history_limit = max(10, history_limit)
        self.auto_optimize = auto_optimize

        self._rules: list[OptimizationRule] = []
        self._history: list[PerformanceReport] = []
        self._providers: list[MetricProvider] = [
            DummyAppMetricProvider(),
            PsutilMetricProvider(),
        ]
        self._lock = threading.RLock()
        self._collect_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._last_metrics: PerformanceMetrics | None = None

        # Prometheus gauges (if prometheus_client is installed)
        self._g = self._init_prometheus_gauges()

        # Default rules
        self._install_default_rules()

        # Background collector
        if background_collect_interval and background_collect_interval > 0:
            self.start_background_collector(background_collect_interval)

    # ---------- utils ----------
    def _now(self) -> datetime:
        return datetime.now(UTC)

    # ---------- providers ----------
    def add_metric_provider(self, provider: MetricProvider) -> None:
        self._providers.append(provider)

    # ---------- rules ----------
    def add_rule(self, rule: OptimizationRule) -> None:
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority)

    def enable_rule(self, name: str, enabled: bool = True) -> bool:
        for r in self._rules:
            if r.name == name:
                r.enabled = enabled
                return True
        return False

    # ---------- prometheus ----------
    def _init_prometheus_gauges(self) -> dict[str, Any] | None:
        if Gauge is None:
            return None
        try:
            return {
                "response_time": Gauge(
                    "zeta_response_time_seconds", "Average response time"
                ),
                "latency_p95": Gauge("zeta_latency_p95_seconds", "Latency p95"),
                "latency_p99": Gauge("zeta_latency_p99_seconds", "Latency p99"),
                "throughput": Gauge("zeta_throughput_rps", "Requests per second"),
                "error_rate": Gauge("zeta_error_rate_ratio", "Error rate"),
                "cpu": Gauge("zeta_cpu_usage_ratio", "CPU usage"),
                "mem": Gauge("zeta_memory_usage_ratio", "Memory usage"),
                "cache_hit": Gauge("zeta_cache_hit_ratio", "Cache hit rate"),
                "queue": Gauge("zeta_queue_depth", "Queue depth"),
                "conns": Gauge("zeta_active_connections", "Active connections"),
            }
        except Exception:  # pragma: no cover
            return None

    def _export_prometheus(self, m: PerformanceMetrics) -> None:
        g = self._g
        if not g:
            return
        try:
            g["response_time"].set(m.response_time)
            g["latency_p95"].set(m.latency_p95)
            g["latency_p99"].set(m.latency_p99)
            g["throughput"].set(m.throughput)
            g["error_rate"].set(m.error_rate)
            g["cpu"].set(m.cpu_usage)
            g["mem"].set(m.memory_usage)
            g["cache_hit"].set(m.cache_hit_rate)
            g["queue"].set(m.queue_depth)
            g["conns"].set(m.active_connections)
        except Exception as e:
            logger.debug("Prometheus export failed: %s", e)

    # ---------- background collector ----------
    def start_background_collector(self, interval_sec: float) -> None:
        """Spawn a daemon thread to collect metrics periodically."""
        if self._collect_thread and self._collect_thread.is_alive():
            return
        self._stop_event.clear()
        t = threading.Thread(
            target=self._collector_loop,
            args=(max(1.0, float(interval_sec)),),
            daemon=True,
            name="perf-collector",
        )
        t.start()
        self._collect_thread = t
        logger.info("Performance background collector started")

    def stop_background_collector(self) -> None:
        self._stop_event.set()
        if self._collect_thread:
            self._collect_thread.join(timeout=5.0)
            self._collect_thread = None
            logger.info("Performance background collector stopped")

    def _collector_loop(self, interval: float) -> None:
        while not self._stop_event.is_set():
            try:
                self.collect_metrics()
            except Exception as e:  # pragma: no cover
                logger.error("Background collect failed: %s", e)
            self._stop_event.wait(interval)

    # ---------- re-entrancy guard ----------
    @contextmanager
    def _guard(self, name: str) -> Iterator[None]:
        if not self._lock.acquire(blocking=False):
            raise BusinessException(f"Operation '{name}' is already running")
        try:
            yield
        finally:
            self._lock.release()

    # ---------- collect ----------
    def collect_metrics(self) -> PerformanceMetrics:
        """Collect current performance metrics via providers, blend with EMA."""
        with self._guard("collect_metrics"):
            if _tracer:
                with _tracer.start_as_current_span("perf.collect"):
                    m = self._collect_metrics_internal()
            else:
                m = self._collect_metrics_internal()

            # Prometheus export
            self._export_prometheus(m)
            return m

    def _collect_metrics_internal(self) -> PerformanceMetrics:
        combined = PerformanceMetrics()
        seen = 0
        for provider in self._providers:
            try:
                m = provider.collect()
                # combine using max for saturation and errors; keep max throughput
                combined.response_time = max(combined.response_time, m.response_time)
                combined.latency_p95 = max(combined.latency_p95, m.latency_p95)
                combined.latency_p99 = max(combined.latency_p99, m.latency_p99)
                combined.error_rate = max(combined.error_rate, m.error_rate)
                combined.cpu_usage = max(combined.cpu_usage, m.cpu_usage)
                combined.memory_usage = max(combined.memory_usage, m.memory_usage)
                combined.cache_hit_rate = max(combined.cache_hit_rate, m.cache_hit_rate)
                combined.queue_depth = max(combined.queue_depth, m.queue_depth)
                combined.active_connections = max(
                    combined.active_connections, m.active_connections
                )
                combined.throughput = max(combined.throughput, m.throughput)
                seen += 1
            except Exception as e:
                logger.warning(
                    "Metric provider %s failed: %s",
                    provider.__class__.__name__,
                    e,
                )
        if seen == 0:
            raise BusinessException("No metrics providers available")
        combined = combined.apply_ema(self._last_metrics)
        self._last_metrics = combined
        logger.debug("Collected metrics: %s", combined.to_dict())
        return combined

    # ---------- analyze ----------
    def analyze_performance(self) -> PerformanceReport:
        with self._guard("analyze_performance"):
            metrics = self.collect_metrics()
            report = PerformanceReport(metrics=metrics)
            report.bottlenecks = self._identify_bottlenecks(metrics)
            report.recommendations = self._generate_recommendations(
                metrics, report.bottlenecks
            )
            report.trends = self._calculate_trends(metrics)
            report.severity, report.error_budget_burn = self._calculate_severity(
                metrics, report.bottlenecks
            )
            self._append_history(report)
            logger.info("Performance analysis completed: severity=%s", report.severity)
            return report

    def _append_history(self, report: PerformanceReport) -> None:
        self._history.append(report)
        if len(self._history) > self.history_limit:
            self._history = self._history[-self.history_limit :]

    # ---------- optimize (system) ----------
    def optimize_system(
        self,
        force: bool = False,
        *,
        dry_run: bool = False,
        plan_only: bool = False,
    ) -> dict[str, Any]:
        with self._guard("optimize_system"):
            if not self.auto_optimize and not force:
                return {"optimizations_applied": 0, "reason": "auto_optimize_disabled"}

            report = self.analyze_performance()
            now = self._now()
            applied, planned = self._evaluate_rules(report, now, dry_run, plan_only)

            return {
                "optimizations_applied": 0 if (dry_run or plan_only) else len(applied),
                "optimizations_planned": len(planned),
                "applied": [asdict(x) for x in applied],
                "planned": [asdict(x) for x in planned],
                "performance_report": {
                    "severity": report.severity,
                    "bottlenecks": len(report.bottlenecks),
                    "recommendations": len(report.recommendations),
                },
                "timestamp": now.isoformat(),
            }

    def _evaluate_rules(
        self,
        report: PerformanceReport,
        now: datetime,
        dry_run: bool,
        plan_only: bool,
    ) -> tuple[list[OptimizationResult], list[OptimizationResult]]:
        applied: list[OptimizationResult] = []
        planned: list[OptimizationResult] = []
        for rule in sorted(self._rules, key=lambda r: r.priority):
            if not rule.enabled or not rule.ready(now):
                continue
            if not rule.condition(report.metrics, self.slo):
                continue
            try:
                _ = rule.action(report.metrics)
                result.rule_name = rule.name
                if dry_run or plan_only:
                    planned.append(result)
                else:
                    applied.append(result)
                    rule.last_applied = now
                    rule.apply_count += 1
                    logger.info("Applied optimization rule: %s", rule.name)
            except Exception as e:
                rule.last_error = str(e)
                logger.error("Rule %s failed: %s", rule.name, e)
        return applied, planned

    # ---------- optimize (agent) ----------
    async def optimize_agent(self, agent_id: UUID) -> dict[str, Any]:
        if _tracer:
            with _tracer.start_as_current_span("perf.optimize_agent"):
                return await self._optimize_agent_impl(agent_id)
        return await self._optimize_agent_impl(agent_id)

    async def _optimize_agent_impl(self, agent_id: UUID) -> dict[str, Any]:
        try:
            _ = await self.agent_repository.get_by_id(agent_id)
            if not agent:
                raise EntityNotFoundError(f"Agent not found: {agent_id}")

            memories = await self.memory_repository.get_by_agent(agent_id)
            agent_metrics = self._analyze_agent_performance(agent, memories)
            recommendations = self._generate_agent_recommendations(agent, agent_metrics)

            applied: list[dict[str, Any]] = []
            for rec in recommendations:
                if rec.get("auto_apply", False):
                    try:
                        _ = self._apply_agent_optimization(agent, rec)
                        applied.append(result)
                    except Exception as e:
                        logger.error("Failed to apply agent optimization: %s", e)

            if applied:
                await self.agent_repository.update(agent)

            return {
                "agent_id": str(agent_id),
                "metrics": agent_metrics,
                "recommendations": recommendations,
                "applied_optimizations": applied,
                "timestamp": self._now().isoformat(),
            }
        except Exception as e:
            logger.error("Failed to optimize agent: %s", e)
            raise BusinessException(f"Failed to optimize agent: {e!s}") from e

    # ---------- bottlenecks/recs/severity ----------
    def _identify_bottlenecks(self, m: PerformanceMetrics) -> list[dict[str, Any]]:
        b: list[dict[str, Any]] = []

        if m.response_time > 3.0:
            b.append(
                {
                    "type": "response_time",
                    "severity": "high" if m.response_time > 5.0 else "medium",
                    "value": m.response_time,
                    "threshold": 3.0,
                    "description": "Response time above acceptable threshold",
                }
            )

        if m.memory_usage > 0.75:
            b.append(
                {
                    "type": "memory_usage",
                    "severity": "high" if m.memory_usage > 0.90 else "medium",
                    "value": m.memory_usage,
                    "threshold": 0.75,
                    "description": "Memory usage approaching critical levels",
                }
            )

        if m.error_rate > 0.01:
            b.append(
                {
                    "type": "error_rate",
                    "severity": "high" if m.error_rate > 0.05 else "medium",
                    "value": m.error_rate,
                    "threshold": 0.01,
                    "description": "Error rate above acceptable threshold",
                }
            )

        if m.cache_hit_rate < 0.80:
            b.append(
                {
                    "type": "cache_efficiency",
                    "severity": "medium",
                    "value": m.cache_hit_rate,
                    "threshold": 0.80,
                    "description": "Cache hit rate below optimal",
                }
            )

        if m.cpu_usage > self.slo.cpu_max:
            b.append(
                {
                    "type": "cpu_usage",
                    "severity": "high" if m.cpu_usage > 0.95 else "medium",
                    "value": m.cpu_usage,
                    "threshold": self.slo.cpu_max,
                    "description": "CPU saturation",
                }
            )

        return b

    def _generate_recommendations(
        self,
        _metrics: PerformanceMetrics,
        bottlenecks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        recs: list[dict[str, Any]] = []
        for b in bottlenecks:
            t = b["type"]
            if t == "response_time":
                recs.append(
                    {
                        "type": "response_time_optimization",
                        "priority": "high",
                        "action": "optimize_model_parameters",
                        "description": "Reduce model complexity or enable/extend response cache; tune max_tokens.",
                        "estimated_impact": "20-30% response time reduction",
                        "auto_apply": True,
                    }
                )
            elif t == "memory_usage":
                recs.append(
                    {
                        "type": "memory_optimization",
                        "priority": "high",
                        "action": "cleanup_memory",
                        "description": "Prune unused embeddings/memories; compact session caches.",
                        "estimated_impact": "10-20% memory usage reduction",
                        "auto_apply": True,
                    }
                )
            elif t == "error_rate":
                recs.append(
                    {
                        "type": "error_handling_optimization",
                        "priority": "medium",
                        "action": "improve_error_handling",
                        "description": "Harden validation, retries with jitter, circuit breaker.",
                        "estimated_impact": "50-70% error rate reduction",
                        "auto_apply": True,
                    }
                )
            elif t == "cache_efficiency":
                recs.append(
                    {
                        "type": "cache_optimization",
                        "priority": "medium",
                        "action": "optimize_cache_strategy",
                        "description": "Adaptive TTL; LFU/LRU choice; warmup critical keys.",
                        "estimated_impact": "10-15% cache hit improvement",
                        "auto_apply": True,
                    }
                )
            elif t == "cpu_usage":
                recs.append(
                    {
                        "type": "autoscale_cpu",
                        "priority": "high",
                        "action": "scale_out_workers",
                        "description": "Increase workers or replicas; enable uvloop/httptools if not.",
                        "estimated_impact": "Reduce CPU saturation risk",
                        "auto_apply": False,
                    }
                )
        return recs

    def _calculate_trends(self, current: PerformanceMetrics) -> dict[str, Any]:
        if len(self._history) < 1:
            return {}
        last = self._history[-1].metrics

        def _trend(curr: float, prev: float) -> dict[str, Any]:
            delta = curr - prev
            if delta < 0:
                trend = "improving"
            elif delta > 0:
                trend = "degrading"
            else:
                trend = "flat"
            return {
                "change": delta,
                "trend": trend,
                "percentage": (abs(delta) / prev * 100.0) if prev > 0 else 0.0,
            }

        return {
            "response_time": _trend(current.response_time, last.response_time),
            "memory_usage": _trend(current.memory_usage, last.memory_usage),
            "error_rate": _trend(current.error_rate, last.error_rate),
            "latency_p95": _trend(current.latency_p95, last.latency_p95),
            "latency_p99": _trend(current.latency_p99, last.latency_p99),
        }

    def _calculate_severity(
        self,
        m: PerformanceMetrics,
        bottlenecks: list[dict[str, Any]],
    ) -> tuple[str, float]:
        """Compute severity + error budget burn (simple heuristic)."""
        if not bottlenecks:
            return "normal", 0.0

        slo = self.slo
        burn = 0.0
        # Additive burn components (normalized)
        if m.latency_p95 > (slo.latency_p95_ms / 1000.0):
            burn += (m.latency_p95 / (slo.latency_p95_ms / 1000.0)) - 1.0
        if m.latency_p99 > (slo.latency_p99_ms / 1000.0):
            burn += (m.latency_p99 / (slo.latency_p99_ms / 1000.0)) - 1.0
        if m.error_rate > slo.error_rate_max:
            burn += (m.error_rate / slo.error_rate_max) - 1.0
        if m.memory_usage > slo.mem_max:
            burn += (m.memory_usage / slo.mem_max) - 1.0
        if m.cpu_usage > slo.cpu_max:
            burn += (m.cpu_usage / slo.cpu_max) - 1.0

        if any(b.get("severity") == "high" for b in bottlenecks) or burn >= 1.0:
            return "critical", max(0.0, burn)
        if len(bottlenecks) > 2 or burn > 0.2:
            return "warning", max(0.0, burn)
        return "warning", max(0.0, burn)

    # ---------- default rules ----------
    def _install_default_rules(self) -> None:
        self.add_rule(
            OptimizationRule(
                name="high_response_time",
                priority=1,
                cooldown=60.0,
                description="Optimize when avg response time > 5s",
                condition=lambda m, _slo: m.response_time > 5.0,
                action=self._rule_optimize_response_time,
            )
        )
        self.add_rule(
            OptimizationRule(
                name="high_memory_usage",
                priority=1,
                cooldown=120.0,
                description="Optimize when memory usage > 80%",
                condition=lambda m, _slo: m.memory_usage > 0.80,
                action=self._rule_optimize_memory,
            )
        )
        self.add_rule(
            OptimizationRule(
                name="high_error_rate",
                priority=2,
                cooldown=90.0,
                description="Optimize when error rate > 5%",
                condition=lambda m, _slo: m.error_rate > 0.05,
                action=self._rule_optimize_error_handling,
            )
        )
        self.add_rule(
            OptimizationRule(
                name="low_cache_hit",
                priority=3,
                cooldown=90.0,
                description="Optimize when cache hit < 70%",
                condition=lambda m, _slo: m.cache_hit_rate < 0.70,
                action=self._rule_optimize_cache,
            )
        )
        self.add_rule(
            OptimizationRule(
                name="cpu_saturation",
                priority=2,
                cooldown=180.0,
                description="Scale out if CPU beyond SLO",
                condition=lambda m, slo: m.cpu_usage > slo.cpu_max,
                action=self._rule_scale_out_workers,
            )
        )

    def _rule_optimize_response_time(
        self, _m: PerformanceMetrics
    ) -> OptimizationResult:
        return OptimizationResult(
            rule_name="high_response_time",
            actions=[
                "enable_response_cache",
                "reduce_model_max_tokens",
                "optimize_query_planner",
            ],
            applied=True,
            estimated_improvement="~25% response time reduction",
            details={"hints": ["consider uvloop/httptools", "pre-warm cache"]},
        )

    def _rule_optimize_memory(self, _m: PerformanceMetrics) -> OptimizationResult:
        return OptimizationResult(
            rule_name="high_memory_usage",
            actions=[
                "prune_unused_memories",
                "shrink_embedding_cache",
                "enable_memory_compaction",
            ],
            applied=True,
            estimated_improvement="~15% memory usage reduction",
        )

    def _rule_optimize_error_handling(
        self, _m: PerformanceMetrics
    ) -> OptimizationResult:
        return OptimizationResult(
            rule_name="high_error_rate",
            actions=[
                "add_input_validation",
                "enable_circuit_breaker",
                "enable_retry_jitter",
            ],
            applied=True,
            estimated_improvement="~60% error rate reduction",
        )

    def _rule_optimize_cache(self, _m: PerformanceMetrics) -> OptimizationResult:
        return OptimizationResult(
            rule_name="low_cache_hit",
            actions=[
                "adjust_cache_ttl",
                "switch_eviction_policy_LFU",
                "cache_warmup_hot_keys",
            ],
            applied=True,
            estimated_improvement="~20% cache hit improvement",
        )

    def _rule_scale_out_workers(self, _m: PerformanceMetrics) -> OptimizationResult:
        return OptimizationResult(
            rule_name="cpu_saturation",
            actions=[
                "scale_out_workers_or_replicas",
                "enable_concurrency_tuning",
            ],
            applied=False,
            estimated_improvement="Reduce CPU saturation risk",
        )

    # ---------- agent-level ----------
    def _analyze_agent_performance(
        self, _agent: Agent, memories: list[Memory]
    ) -> dict[str, Any]:
        total = len(memories)
        if total == 0:
            return {
                "memory_count": 0,
                "recent_memory_count": 0,
                "avg_memory_accesses": 0.0,
                "memory_retention_rate": 0.0,
                "efficiency_score": 0.0,
            }
        recent = [m for m in memories if (datetime.now(UTC) - m.created_at).days <= 7]
        total_accesses = sum(getattr(m.metrics, "access_count", 0) for m in memories)
        avg_accesses = total_accesses / total if total > 0 else 0.0
        return {
            "memory_count": total,
            "recent_memory_count": len(recent),
            "avg_memory_accesses": avg_accesses,
            "memory_retention_rate": (len(recent) / total) if total > 0 else 0.0,
            "efficiency_score": min(avg_accesses / 10.0, 1.0),
        }

    def _generate_agent_recommendations(
        self, _agent: Agent, metrics: dict[str, Any]
    ) -> list[dict[str, Any]]:
        recs: list[dict[str, Any]] = []
        if metrics["memory_count"] > 1000:
            recs.append(
                {
                    "type": "memory_cleanup",
                    "priority": "medium",
                    "action": "cleanup_old_memories",
                    "description": "Archive or purge stale memories to reduce RAM.",
                    "auto_apply": False,
                }
            )
        if metrics["efficiency_score"] < 0.5:
            recs.append(
                {
                    "type": "model_optimization",
                    "priority": "high",
                    "action": "optimize_model_parameters",
                    "description": "Lower temperature/limits for better determinism and speed.",
                    "auto_apply": True,
                }
            )
        return recs

    def _apply_agent_optimization(
        self, agent: Agent, recommendation: dict[str, Any]
    ) -> dict[str, Any]:
        action = recommendation["action"]
        if action == "optimize_model_parameters":
            # guard for dict-like config
            cfg = getattr(agent, "config", None)
            if not isinstance(cfg, dict):
                return {
                    "action": action,
                    "changes": [],
                    "success": False,
                    "reason": "No dict config",
                }
            changes: list[str] = []
            try:
                # Safe clamps
                if float(cfg.get("temperature", 1.0)) > 0.8:
                    cfg["temperature"] = 0.7
                    changes.append("temperature")
                if int(cfg.get("max_tokens", 2000)) > 2000:
                    cfg["max_tokens"] = 1500
                    changes.append("max_tokens")
                return {"action": action, "changes": changes, "success": True}
            except Exception as e:
                return {
                    "action": action,
                    "changes": [],
                    "success": False,
                    "reason": str(e),
                }
        return {
            "action": action,
            "changes": [],
            "success": False,
            "reason": "Unknown action",
        }

    # ---------- public helpers ----------
    def get_performance_history(self, limit: int = 10) -> list[dict[str, Any]]:
        reports = self._history[-limit:] if self._history else []
        return [
            {
                "timestamp": r.timestamp.isoformat(),
                "severity": r.severity,
                "error_budget_burn": r.error_budget_burn,
                "metrics": r.metrics.to_dict(),
                "bottlenecks": len(r.bottlenecks),
                "recommendations": len(r.recommendations),
            }
            for r in reports
        ]

    def get_dashboard_payload(self) -> dict[str, Any]:
        """Compact JSON for a UI dashboard widget."""
        last = self._history[-1] if self._history else None
        return {
            "now": self._now().isoformat(),
            "severity": last.severity if last else "unknown",
            "metrics": last.metrics.to_dict() if last else {},
            "trends": last.trends if last else {},
        }
