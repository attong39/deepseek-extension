"""Tests for Self-Improvement modules."""

from unittest.mock import Mock

import pytest
from apps.backend.core.self_improvement.auto_updater import (
    IntelligentUpdater,
    UpdatePlan,
    UpdatePriority,
    UpdateStatus,
)
from apps.backend.core.services.health_monitor import (
    HealthMetrics,
    RealTimeHealthMonitor,
)


class TestIntelligentUpdater:
    """Test cases for intelligent updater."""

    def setup_method(self):
        """Set up test instance."""
        self.updater = IntelligentUpdater()

    def test_security_impact_analysis(self):
        """Test security impact analysis."""
        # High security impact
        high_security_meta = {
            "changelog": "Critical security vulnerability fix - CVE-2023-1234 patch",
            "features": ["security_patch"],
        }

        score = self.updater._analyze_security_impact(high_security_meta)
        assert score >= 7.0  # Should be high security score

        # Low security impact
        low_security_meta = {
            "changelog": "Minor UI improvements and bug fixes",
            "features": ["ui_update"],
        }

        score = self.updater._analyze_security_impact(low_security_meta)
        assert score < 3.0  # Should be low security score

    def test_business_impact_analysis(self):
        """Test business impact analysis."""
        # High business impact
        high_impact_meta = {
            "features": ["new_dashboard", "user_analytics", "performance_boost"],
            "performance": True,
        }

        impact = self.updater._analyze_business_impact(high_impact_meta)
        assert impact > 0.7  # Should be high impact

        # Low business impact
        low_impact_meta = {"features": [], "performance": False}

        impact = self.updater._analyze_business_impact(low_impact_meta)
        assert impact < 0.3  # Should be low impact

    def test_breaking_changes_detection(self):
        """Test breaking changes detection."""
        # Version-based breaking change
        breaking_version_meta = {
            "version": "2.0.0",  # Major version bump
            "changelog": "Major API overhaul",
        }

        self.updater.current_version = "1.5.0"
        has_breaking = self.updater._analyze_breaking_changes(breaking_version_meta)
        assert has_breaking is True

        # Keyword-based breaking change
        breaking_keyword_meta = {
            "version": "1.6.0",
            "changelog": "Deprecated old API, removed legacy endpoints",
        }

        has_breaking = self.updater._analyze_breaking_changes(breaking_keyword_meta)
        assert has_breaking is True

        # No breaking changes
        safe_meta = {
            "version": "1.5.1",
            "changelog": "Bug fixes and minor improvements",
        }

        has_breaking = self.updater._analyze_breaking_changes(safe_meta)
        assert has_breaking is False

    def test_priority_assessment(self):
        """Test update priority assessment."""
        # Critical security update
        critical_meta = {
            "changelog": "Critical security vulnerability patch - immediate action required",
            "features": ["security_fix"],
            "performance": False,
        }

        priority = self.updater.assess_update_priority(critical_meta)
        assert priority == UpdatePriority.CRITICAL

        # Important update with breaking changes
        important_meta = {
            "changelog": "Major feature release with breaking API changes",
            "features": ["new_api", "performance_improvements"],
            "performance": True,
        }

        priority = self.updater.assess_update_priority(important_meta)
        assert priority == UpdatePriority.IMPORTANT

        # Optional update
        optional_meta = {
            "changelog": "Minor bug fixes and documentation updates",
            "features": ["doc_update"],
            "performance": False,
        }

        priority = self.updater.assess_update_priority(optional_meta)
        assert priority == UpdatePriority.OPTIONAL

    def test_update_plan_creation(self):
        """Test update plan creation."""
        release_meta = {
            "version": "1.6.0",
            "changelog": "Security improvements and performance optimizations",
            "features": ["enhanced_auth", "caching_improvements"],
            "performance": True,
        }

        plan = self.updater.create_update_plan(release_meta)

        assert isinstance(plan, UpdatePlan)
        assert plan.priority in UpdatePriority
        assert plan.estimated_downtime_seconds > 0
        assert len(plan.safety_checks) > 0
        assert "security_score" in plan.impact_assessment
        assert "business_impact" in plan.impact_assessment

    def test_immediate_update_execution(self):
        """Test immediate update execution."""
        _ = self.updater.immediate_update()

        assert result["status"] == UpdateStatus.COMPLETED
        assert "execution_time_seconds" in result
        assert "actions_taken" in result
        assert result["rollback_available"] is True
        assert len(self.updater.update_history) == 1

    def test_scheduled_update(self):
        """Test scheduled update."""
        _ = self.updater.scheduled_update()

        assert result["status"] == UpdateStatus.PENDING
        assert "scheduled_time" in result
        assert "preparation_steps" in result

    def test_user_approved_update(self):
        """Test user approved update."""
        _ = self.updater.user_approved_update()

        assert result["status"] == UpdateStatus.PENDING
        assert result["approval_required"] is True
        assert "approval_deadline" in result
        assert "approval_methods" in result

    def test_check_and_update_with_metadata(self):
        """Test main update orchestration."""
        release_meta = {
            "version": "1.1.0",
            "changelog": "Security improvements and performance optimizations",
            "features": ["enhanced_auth"],
            "performance": True,
        }

        _ = self.updater.check_and_update(release_meta)

        assert "status" in result
        assert "plan" in result
        assert result["plan"]["priority"] in [p.value for p in UpdatePriority]

    def test_update_status_retriast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval(self):
        """Test getting update status."""
        status = self.updater.get_update_status()

        assert status["current_version"] == "1.0.0"
        assert "last_check" in status
        assert "available_strategies" in status
        assert status["status"] == "operational"


class TestRealTimeHealthMonitor:
    """Test cases for health monitor."""

    def setup_method(self):
        """Set up test dependencies."""
        self.mock_metrics = Mock()
        self.mock_alerts = Mock()

        # Configure metrics mock
        self.mock_metrics.snapshot.return_value = {
            "cpu_usage_percent": 45.0,
            "memory_usage_percent": 60.0,
            "latency_p95_ms": 150.0,
            "error_rate_percent": 1.0,
        }

        self.monitor = RealTimeHealthMonitor(
            metrics=self.mock_metrics,
            alerts=self.mock_alerts,
            heal_threshold=0.7,
            interval_sec=10,
        )

    def test_health_metrics_collection(self):
        """Test health metrics collection."""
        metrics = self.monitor.collect_health_metrics()

        assert isinstance(metrics, HealthMetrics)
        assert metrics.cpu_usage_percent == 45.0
        assert metrics.memory_usage_percent == 60.0
        assert metrics.latency_p95_ms == 150.0
        assert metrics.error_rate_percent == 1.0

    def test_health_score_calculation(self):
        """Test health score calculation."""
        metrics = HealthMetrics(
            cpu_usage_percent=20.0,
            memory_usage_percent=30.0,
            latency_p95_ms=100.0,
            error_rate_percent=0.5,
        )

        score = self.monitor.calculate_health_score(metrics)

        assert 0.0 <= score <= 1.0
        assert score > 0.7  # Should be healthy with these metrics

    def test_unhealthy_score_calculation(self):
        """Test health score with unhealthy metrics."""
        unhealthy_metrics = HealthMetrics(
            cpu_usage_percent=95.0,
            memory_usage_percent=90.0,
            latency_p95_ms=2000.0,
            error_rate_percent=10.0,
        )

        score = self.monitor.calculate_health_score(unhealthy_metrics)

        assert 0.0 <= score <= 1.0
        assert score < 0.3  # Should be unhealthy

    def test_system_health_check(self):
        """Test system health check."""
        health_score = self.monitor.check_system_health()

        assert 0.0 <= health_score <= 1.0
        self.mock_metrics.snapshot.assert_called_once()

    def test_auto_heal_execution(self):
        """Test auto healing execution."""
        self.monitor.auto_heal()

        # Should have called alerts
        self.mock_alerts.warn.assert_called_once()

    @pytest.mark.asyncio
    async def test_monitor_and_heal_once(self):
        """Test monitoring loop with once=True."""
        health_score = await self.monitor.monitor_and_heal(once=True)

        assert 0.0 <= health_score <= 1.0
        assert self.monitor.is_monitoring is False

    def test_health_summary(self):
        """Test health summary generation."""
        summary = self.monitor.get_health_summary()

        assert "current_health" in summary
        assert "monitoring_status" in summary
        assert "score" in summary["current_health"]
        assert "status" in summary["current_health"]

    def test_metrics_collection_error_handling(self):
        """Test error handling in metrics collection."""
        # Make metrics.snapshot raise an exception
        self.mock_metrics.snapshot.side_effect = Exception("Metrics unavailable")

        metrics = self.monitor.collect_health_metrics()

        # Should return default HealthMetrics on error
        assert isinstance(metrics, HealthMetrics)
        assert metrics.cpu_usage_percent == 0.0

    def test_health_calculation_error_handling(self):
        """Test error handling in health calculation."""
        # Create invalid metrics that might cause calculation errors
        invalid_metrics = HealthMetrics(
            cpu_usage_percent=-10.0,  # Invalid value
            memory_usage_percent=float("inf"),  # Invalid value
            latency_p95_ms=float("nan"),  # Invalid value
            error_rate_percent=-5.0,  # Invalid value
        )

        score = self.monitor.calculate_health_score(invalid_metrics)

        # Should handle errors gracefully
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0


class TestSelfImprovementIntegration:
    """Integration tests for self-improvement components."""

    def setup_method(self):
        """Set up integration test dependencies."""
        self.mock_metrics = Mock()
        self.mock_alerts = Mock()

        self.mock_metrics.snapshot.return_value = {
            "cpu_usage_percent": 50.0,
            "memory_usage_percent": 65.0,
            "latency_p95_ms": 200.0,
            "error_rate_percent": 2.0,
        }

        self.updater = IntelligentUpdater()
        self.health_monitor = RealTimeHealthMonitor(
            metrics=self.mock_metrics, alerts=self.mock_alerts
        )

    def test_health_triggered_update_scenario(self):
        """Test scenario where poor health triggers update check."""
        # Simulate poor health
        self.mock_metrics.snapshot.return_value = {
            "cpu_usage_percent": 95.0,
            "memory_usage_percent": 90.0,
            "latency_p95_ms": 2000.0,
            "error_rate_percent": 15.0,
        }

        # Check health
        health_score = self.health_monitor.check_system_health()
        assert health_score < 0.5  # Poor health

        # Simulate update check triggered by poor health
        release_meta = {
            "version": "1.1.0",
            "changelog": "Critical performance fixes and memory optimizations",
            "features": ["performance_fix", "memory_optimization"],
            "performance": True,
        }

        # Should prioritize this update due to performance issues
        priority = self.updater.assess_update_priority(release_meta)
        assert priority in [UpdatePriority.IMPORTANT, UpdatePriority.CRITICAL]

    def test_update_status_tracking(self):
        """Test update status tracking across multiple operations."""
        # Execute multiple update operations
        self.updater.immediate_update()
        self.updater.scheduled_update()

        status = self.updater.get_update_status()

        assert status["update_history_count"] >= 1
        assert len(status["recent_updates"]) >= 1

    def test_system_status_aggregation(self):
        """Test aggregated system status from both components."""
        # Health status
        health_summary = self.health_monitor.get_health_summary()

        # Update status
        update_status = self.updater.get_update_status()

        # Both should be operational
        assert update_status["status"] == "operational"
        assert "error" not in health_summary
