"""Test health monitor functionality."""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from apps.backend.core.services.health_monitor import (
    HealthMonitor,
    HealthState,
    ProbeResult,
    RealTimeHealthMonitor,
    Severity,
    build_default_monitor,
)


class TestHealthMonitor:
    """Test health monitoring functionality."""
import RuntimeError
import ValueError
import abs
import i
import isinstance
import len
import mock_gauge
import mock_heal
import mock_httpx
import range
import result

    def test_init_validation(self):
        """Test constructor validation."""
        with pytest.raises(ValueError, match="default_timeout_s must be > 0"):
            HealthMonitor(default_timeout_s=0)

        with pytest.raises(ValueError, match="cache_ttl_s must be >= 0"):
            HealthMonitor(cache_ttl_s=-1)

    async def test_no_probes_registered(self):
        """Test behavior when no probes are registered."""
        monitor = HealthMonitor()
        report = await monitor.probe_all()

        assert report.status == HealthState.UP
        assert len(report.results) == 1
        assert report.results[0].name == "_no_probes_"
        assert report.results[0].state == HealthState.UP
        assert report.results[0].detail == "no probes registered"

    async def test_probe_timeout(self):
        """Test probe timeout handling."""
        monitor = HealthMonitor(default_timeout_s=0.1)

        async def slow_probe() -> ProbeResult:
            await asyncio.sleep(0.2)  # Longer than timeout
            return ProbeResult(name="slow", state=HealthState.UP)

        monitor.register_custom("slow", slow_probe, timeout_s=0.1)

        report = await monitor.probe_all()
        assert report.status == HealthState.DOWN
        _ = report.results[0]
        assert result.name == "slow"
        assert result.state == HealthState.DOWN
        assert result.detail is not None


class TestRealTimeHealthMonitor:
    """Test real-time health monitoring with self-healing."""

    def test_init(self):
        """Test RealTimeHealthMonitor initialization."""
        metrics_mock = Mock()
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(
            metrics=metrics_mock,
            alerts=alerts_mock,
            heal_threshold=0.8,
            interval_sec=30,
        )

        assert monitor.metrics == metrics_mock
        assert monitor.alerts == alerts_mock
        assert abs(monitor.heal_threshold - 0.8) < 0.001
        assert monitor.interval_sec == 30
        assert not monitor._running

    def test_check_system_health_no_snapshot(self):
        """Test health check when metrics has no snapshot method."""
        metrics_mock = Mock()
        # Don't add snapshot method - should use fallback
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock)
        health = monitor.check_system_health()

        # Should return reasonable health score with default values
        assert 0.0 <= health <= 1.0
        assert len(monitor._health_history) == 1

    def test_check_system_health_with_metrics(self):
        """Test health check with actual metrics."""
        metrics_mock = Mock()
        metrics_mock.snapshot.return_value = {
            "latency_p95_ms": 500,
            "error_rate": 0.02,
            "memory_usage_percent": 60,
            "cpu_usage_percent": 40,
        }
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock)
        health = monitor.check_system_health()

        assert 0.0 <= health <= 1.0
        assert len(monitor._health_history) == 1

        # Check stored metrics
        stored = monitor._health_history[0]
        assert stored["latency"] == 500
        assert abs(stored["error_rate"] - 0.02) < 0.001

    def test_diagnose_issues(self):
        """Test issue diagnosis from metrics."""
        metrics_mock = Mock()
        metrics_mock.snapshot.return_value = {
            "latency_p95_ms": 3000,  # High latency
            "error_rate": 0.08,  # High error rate
            "memory_usage_percent": 85,  # High memory
            "cpu_usage_percent": 90,  # High CPU
        }
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock)
        monitor.check_system_health()  # Populate history

        issues = monitor._diagnose_issues()

        assert "high_latency" in issues
        assert "high_error_rate" in issues
        assert "memory_pressure" in issues
        assert "cpu_pressure" in issues

    def test_auto_heal_with_alerts(self):
        """Test auto-healing with working alerts."""
        metrics_mock = Mock()
        alerts_mock = Mock()
        alerts_mock.warn = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock)
        monitor._health_history.append(
            {"latency": 3000, "error_rate": 0.1, "memory": 90, "cpu": 95}
        )

        monitor.auto_heal()

        # Should have called alert
        alerts_mock.warn.assert_called_once()

    def test_auto_heal_without_alerts(self):
        """Test auto-healing when alerts don't have warn method."""
        metrics_mock = Mock()
        alerts_mock = Mock()
        # Don't add warn method

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock)
        monitor._health_history.append(
            {"latency": 3000, "error_rate": 0.1, "memory": 90, "cpu": 95}
        )

        # Should not raise exception
        monitor.auto_heal()

    def test_monitor_and_heal_below_threshold(self):
        """Test monitoring when health is below threshold."""
        metrics_mock = Mock()
        metrics_mock.snapshot.return_value = {
            "latency_p95_ms": 5000,  # Very high latency
            "error_rate": 0.2,  # Very high error rate
            "memory_usage_percent": 95,
            "cpu_usage_percent": 98,
        }
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock, heal_threshold=0.8)

        with patch.object(monitor, "auto_heal") as mock_heal:
            health = monitor.monitor_and_heal(once=True)

            assert health < 0.8
            mock_heal.assert_called_once()

    def test_monitor_and_heal_above_threshold(self):
        """Test monitoring when health is above threshold."""
        metrics_mock = Mock()
        metrics_mock.snapshot.return_value = {
            "latency_p95_ms": 100,
            "error_rate": 0.001,
            "memory_usage_percent": 30,
            "cpu_usage_percent": 20,
        }
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock, heal_threshold=0.8)

        with patch.object(monitor, "auto_heal") as mock_heal:
            health = monitor.monitor_and_heal(once=True)

            assert health >= 0.8
            mock_heal.assert_not_called()

    async def test_start_stop_monitoring(self):
        """Test starting and stopping monitoring loop."""
        metrics_mock = Mock()
        metrics_mock.snapshot.return_value = {}
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock, interval_sec=1)

        # Start monitoring in background
        task = asyncio.create_task(monitor.start_monitoring())

        # Let it run briefly
        await asyncio.sleep(0.05)

        # Stop monitoring
        monitor.stop_monitoring()

        # Wait for task to complete
        await asyncio.sleep(0.05)

        assert not monitor._running
        assert task.done()

    def test_get_health_trends_no_data(self):
        """Test health trends when no data available."""
        metrics_mock = Mock()
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock)
        trends = monitor.get_health_trends()

        assert trends["status"] == "no_data"

    def test_get_health_trends_with_data(self):
        """Test health trends with actual data."""
        metrics_mock = Mock()
        alerts_mock = Mock()

        monitor = RealTimeHealthMonitor(metrics_mock, alerts_mock, heal_threshold=0.8)

        # Add some health history
        for i in range(5):
            monitor._health_history.append(
                {
                    "score": 0.7 + i * 0.05,  # Improving trend
                    "latency": 1000 - i * 100,
                    "error_rate": 0.05 - i * 0.01,
                }
            )

        trends = monitor.get_health_trends()

        assert "current_health" in trends
        assert "avg_health_10m" in trends
        assert "trend" in trends
        assert "alerts_count" in trends
        assert trends["data_points"] == 5


class TestBuildDefaultMonitor:
    """Test default monitor builder."""

    def test_build_minimal(self):
        """Test building monitor with minimal config."""
        monitor = build_default_monitor()

        assert isinstance(monitor, HealthMonitor)
        assert monitor._version is None

    def test_build_with_all_options(self):
        """Test building monitor with all options."""
        monitor = build_default_monitor(
            version="1.0.0",
            redis_url="redis://localhost:6379",
            pg_dsn="postgresql://user:pass@localhost/db",
            http_endpoints={"api": "http://localhost:8000/health"},
            temporal_target="localhost:7233",
            cache_ttl_s=2.0,
            default_timeout_s=3.0,
        )

        assert isinstance(monitor, HealthMonitor)
        assert monitor._version == "1.0.0"
        assert abs(monitor._cache_ttl_s - 2.0) < 0.001
        assert abs(monitor._default_timeout_s - 3.0) < 0.001
        assert len(monitor._probes) == 4  # redis, postgres, http, temporal

    async def test_cache_ttl_behavior(self):
        """Test cache TTL functionality."""
        monitor = HealthMonitor(cache_ttl_s=0.1)
        call_count = 0

        async def counting_probe() -> ProbeResult:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.001)  # Minimal async work
            return ProbeResult(
                name="counter", state=HealthState.UP, detail=f"call_{call_count}"
            )

        monitor.register_custom("counter", counting_probe)

        # First call
        report1 = await monitor.probe_all()
        assert report1.results[0].detail == "call_1"
        assert call_count == 1

        # Second call within TTL - should use cache
        report2 = await monitor.probe_all()
        assert report2.results[0].detail == "call_1"  # Same as before
        assert call_count == 1  # Function not called again

    async def test_status_aggregation_critical_down(self):
        """Test that CRITICAL/HIGH DOWN probes make overall status DOWN."""
        monitor = HealthMonitor()

        async def critical_down() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(
                name="db", state=HealthState.DOWN, severity=Severity.CRITICAL
            )

        async def medium_up() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(
                name="cache", state=HealthState.UP, severity=Severity.MEDIUM
            )

        monitor.register_custom("critical_down", critical_down)
        monitor.register_custom("medium_up", medium_up)

        report = await monitor.probe_all()
        assert report.status == HealthState.DOWN

    async def test_status_aggregation_degraded(self):
        """Test that DEGRADED probes make overall status DEGRADED (if no critical DOWN)."""
        monitor = HealthMonitor()

        async def low_degraded() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(
                name="service", state=HealthState.DEGRADED, severity=Severity.LOW
            )

        async def medium_up() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(
                name="cache", state=HealthState.UP, severity=Severity.MEDIUM
            )

        monitor.register_custom("low_degraded", low_degraded)
        monitor.register_custom("medium_up", medium_up)

        report = await monitor.probe_all()
        assert report.status == HealthState.DEGRADED

    async def test_status_aggregation_all_up(self):
        """Test that all UP probes result in overall UP status."""
        monitor = HealthMonitor()

        async def up_probe() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(
                name="service", state=HealthState.UP, severity=Severity.MEDIUM
            )

        monitor.register_custom("up_probe", up_probe)

        report = await monitor.probe_all()
        assert report.status == HealthState.UP

    @patch("zeta_vn.core.services.health_monitor.aioredis", None)
    async def test_redis_probe_missing_library(self):
        """Test Redis probe when aioredis is not installed."""
        monitor = HealthMonitor()
        monitor.register_redis("redis", url="redis://localhost:6379")

        report = await monitor.probe_all()
        _ = report.results[0]
        assert result.name == "redis"
        assert result.state == HealthState.DEGRADED
        assert result.detail is not None
        assert "aioredis not installed" in result.detail

    @patch("zeta_vn.core.services.health_monitor.asyncpg", None)
    async def test_postgres_probe_missing_library(self):
        """Test Postgres probe when asyncpg is not installed."""
        monitor = HealthMonitor()
        monitor.register_postgres("postgres", dsn="postgresql://localhost:5432/test")

        report = await monitor.probe_all()
        _ = report.results[0]
        assert result.name == "postgres"
        assert result.state == HealthState.DEGRADED
        assert result.detail is not None
        assert "asyncpg not installed" in result.detail

    @patch("zeta_vn.core.services.health_monitor.httpx", None)
    async def test_http_probe_missing_library(self):
        """Test HTTP probe when httpx is not installed."""
        monitor = HealthMonitor()
        monitor.register_http("api", url="http://localhost:8080/health")

        report = await monitor.probe_all()
        _ = report.results[0]
        assert result.name == "api"
        assert result.state == HealthState.DEGRADED
        assert result.detail is not None
        assert "httpx not installed" in result.detail

    @patch("zeta_vn.core.services.health_monitor.httpx")
    async def test_http_probe_status_codes(self, mock_httpx):
        """Test HTTP probe with different status codes."""
        monitor = HealthMonitor()

        # Mock HTTP client
        mock_client = AsyncMock()
        mock_httpx.AsyncClient.return_value.__aenter__.return_value = mock_client

        # Test expected status (200) => UP
        mock_response = Mock()
        mock_response.status_code = 200
        mock_client.request.return_value = mock_response

        monitor.register_http("api_200", url="http://test.com", expected_status=200)
        report = await monitor.probe_all()
        assert report.results[0].state == HealthState.UP

    def test_prometheus_metrics_disabled(self):
        """Test that Prometheus metrics can be disabled."""
        monitor = HealthMonitor(enable_prom_metrics=False)
        assert monitor._g_status is None
        assert monitor._g_latency is None

    @patch("zeta_vn.core.services.health_monitor.Gauge")
    def test_prometheus_metrics_enabled(self, mock_gauge):
        """Test Prometheus metrics when enabled and available."""
        HealthMonitor(enable_prom_metrics=True)

        # Should create gauges
        assert mock_gauge.call_count == 2

    def test_build_default_monitor(self):
        """Test the default monitor builder utility."""
        monitor = build_default_monitor(
            version="1.0.0",
            redis_url="redis://localhost:6379",
            pg_dsn="postgresql://localhost:5432/test",
            http_endpoints={"api": "http://localhost:8080"},
            temporal_target="localhost:7233",
            cache_ttl_s=2.0,
            default_timeout_s=3.0,
        )

        assert monitor._version == "1.0.0"
        assert abs(monitor._cache_ttl_s - 2.0) < 0.001
        assert abs(monitor._default_timeout_s - 3.0) < 0.001
        assert len(monitor._probes) == 4  # redis, postgres, api, temporal

    async def test_probe_exception_handling(self):
        """Test that probe exceptions are handled gracefully."""
        monitor = HealthMonitor()

        async def failing_probe() -> ProbeResult:
            await asyncio.sleep(0.001)
            raise RuntimeError("Simulated failure")

        monitor.register_custom("failing", failing_probe)

        report = await monitor.probe_all()
        _ = report.results[0]
        assert result.name == "failing"
        assert result.state == HealthState.DOWN
        assert result.detail is not None
        assert "RuntimeError" in result.detail

    async def test_report_counts(self):
        """Test that report counts are accurate."""
        monitor = HealthMonitor()

        async def up_probe() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(name="up", state=HealthState.UP)

        async def degraded_probe() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(name="degraded", state=HealthState.DEGRADED)

        async def down_probe() -> ProbeResult:
            await asyncio.sleep(0.001)
            return ProbeResult(
                name="down", state=HealthState.DOWN, severity=Severity.LOW
            )

        monitor.register_custom("up", up_probe)
        monitor.register_custom("degraded", degraded_probe)
        monitor.register_custom("down", down_probe)

        report = await monitor.probe_all()

        assert report.counts[HealthState.UP] == 1
        assert report.counts[HealthState.DEGRADED] == 1
        assert report.counts[HealthState.DOWN] == 1
