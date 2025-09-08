from __future__ import annotations

import asyncio
import os
import time
from unittest.mock import Mock, patch

import psutil
import pytest
from apps.backend.core.common.base_classes import ConfigurationManager
from apps.backend.core.cost.guard import CostGuard
from apps.backend.core.observability.logging import get_logger
import Exception
import ValueError
import abs
import all
import dict
import float
import hasattr
import i
import int
import isinstance
import len
import mock_config
import mock_logger
import r
import range
import self

"""Unit tests for cost guard functionality.
This module contains comprehensive unit tests for the CostGuard class
and related cost management functionality.
"""


class TestCostGuard:
    """Test cases for CostGuard class."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.logger = get_logger(__name__)
        self.config_manager = Mock()
        self.cost_guard = CostGuard()

    def teardown_method(self) -> None:
        """Clean up after each test method."""

    @pytest.mark.asyncio
    async def test_initialization(self) -> None:
        """Test CostGuard initialization."""
        assert self.cost_guard is not None
        assert hasattr(self.cost_guard, "_config_manager")
        assert hasattr(self.cost_guard, "_logger")

    @pytest.mark.asyncio
    async def test_token_bucket_initialization(self) -> None:
        """Test token bucket initialization with default values."""
        tokens = await self.cost_guard._get_available_tokens("test_user")
        assert isinstance(tokens, (int, float))

    @pytest.mark.asyncio
    async def test_cost_calculation(self) -> None:
        """Test cost calculation for different operations."""
        cost = await self.cost_guard.calculate_cost("text_completion", {"tokens": 100})
        assert isinstance(cost, (int, float))
        assert cost >= 0

    @pytest.mark.asyncio
    async def test_rate_limiting(self) -> None:
        """Test rate limiting functionality."""
        user_id = "test_user"
        allowed1 = await self.cost_guard.check_rate_limit(user_id, "text_completion")
        assert allowed1 is True
        for _ in range(10):
            allowed = await self.cost_guard.check_rate_limit(user_id, "text_completion")
            if not allowed:
                break

    @pytest.mark.asyncio
    async def test_usage_tracking(self) -> None:
        """Test usage tracking and statistics."""
        user_id = "test_user"
        await self.cost_guard.track_usage(user_id, "text_completion", 0.1)
        stats = await self.cost_guard.get_usage_stats(user_id, days=1)
        assert isinstance(stats, dict)
        assert "total_cost" in stats
        assert "request_count" in stats

    @pytest.mark.asyncio
    async def test_budget_enforcement(self) -> None:
        """Test budget enforcement functionality."""
        user_id = "test_user"
        await self.cost_guard.set_budget(user_id, 0.01)
        allowed = await self.cost_guard.check_budget(user_id, 0.1)
        assert allowed is False

    @pytest.mark.asyncio
    async def test_cost_alerts(self) -> None:
        """Test cost alert functionality."""
        user_id = "test_user"
        await self.cost_guard.set_alert_threshold(user_id, 0.5)
        alert_triggered = await self.cost_guard.check_alert_threshold(user_id, 0.6)
        assert alert_triggered is True

    @pytest.mark.asyncio
    async def test_configuration_management(self) -> None:
        """Test configuration management."""
        new_config = {"default_budget": 10.0, "rate_limit_per_minute": 60}
        await self.cost_guard.configure(new_config)

    @pytest.mark.asyncio
    async def test_error_handling(self) -> None:
        """Test error handling in various scenarios."""
        with pytest.raises(ValueError):
            await self.cost_guard.calculate_cost("invalid_operation", {})
        with patch.object(self.cost_guard, "_config_manager") as mock_config:
            mock_config.get_config.side_effect = Exception("Config error")
            result = await self.cost_guard.get_usage_stats("test_user")
            assert result is not None

    @pytest.mark.asyncio
    async def test_concurrent_access(self) -> None:
        """Test concurrent access to cost guard."""
        user_id = "concurrent_user"

        async def concurrent_operation(task_id: int) -> float:
            cost = await self.cost_guard.calculate_cost(
                "text_completion", {"tokens": 10}
            )
            await self.cost_guard.track_usage(user_id, "text_completion", cost)
            return cost

        tasks = [concurrent_operation(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        assert len(results) == 10
        assert all(isinstance(r, (int, float)) for r in results)

    @pytest.mark.asyncio
    async def test_cleanup_and_reset(self) -> None:
        """Test cleanup and reset functionality."""
        user_id = "cleanup_user"
        await self.cost_guard.track_usage(user_id, "text_completion", 1.0)
        await self.cost_guard.reset_usage(user_id)
        stats = await self.cost_guard.get_usage_stats(user_id)
        assert abs(stats["total_cost"] - 0.0) < 1e-6

    @pytest.mark.asyncio
    async def test_persistence_simulation(self) -> None:
        """Test persistence simulation (in real implementation would use database)."""
        user_id = "persistent_user"
        await self.cost_guard.track_usage(user_id, "text_completion", 2.0)
        stats = await self.cost_guard.get_usage_stats(user_id)
        assert "total_cost" in stats
        assert stats["total_cost"] >= 2.0


class TestCostGuardIntegration:
    """Integration tests for CostGuard with other components."""

    @pytest.mark.asyncio
    async def test_with_configuration_manager(self) -> None:
        """Test integration with ConfigurationManager."""
        config_manager = ConfigurationManager()
        cost_guard = CostGuard()
        config = {"cost_guard": {"default_budget": 100.0, "alert_threshold": 80.0}}
        config_manager.merge_config(config)
        cost_guard.configure(config.get("cost_guard", {}))

    @pytest.mark.asyncio
    async def test_with_observability(self) -> None:
        """Test integration with observability/logging."""
        cost_guard = CostGuard()
        with patch("zeta_vn.core.observability.logging.get_logger") as mock_logger:
            await cost_guard.track_usage("test_user", "text_completion", 1.0)
            mock_logger.return_value.info.assert_called()


class TestCostGuardPerformance:
    """Performance tests for CostGuard."""

    @pytest.mark.asyncio
    async def test_high_concurrency_performance(self) -> None:
        """Test performance under high concurrency."""
        cost_guard = CostGuard()
        user_id = "perf_user"

        async def perf_operation() -> None:
            await cost_guard.check_rate_limit(user_id, "text_completion")
            await cost_guard.calculate_cost("text_completion", {"tokens": 50})

        start_time = time.time()
        tasks = [perf_operation() for _ in range(100)]
        await asyncio.gather(*tasks)
        end_time = time.time()
        duration = end_time - start_time
        assert duration < 5.0  # 5 seconds max

    @pytest.mark.asyncio
    async def test_memory_usage(self) -> None:
        """Test memory usage under load."""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        cost_guard = CostGuard()
        for i in range(1000):
            result = await cost_guard.track_usage(f"user_{i}", "text_completion", 0.01)
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        assert memory_increase < 50 * 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__])
__all__ = [
    "TestCostGuard",
    "TestCostGuardIntegration",
    "TestCostGuardPerformance",
    "alert_triggered",
    "allowed",
    "allowed1",
    "concurrent_operation",
    "config",
    "config_manager",
    "cost",
    "cost_guard",
    "duration",
    "end_time",
    "final_memory",
    "initial_memory",
    "memory_increase",
    "new_config",
    "perf_operation",
    "process",
    "result",
    "results",
    "setup_method",
    "start_time",
    "stats",
    "tasks",
    "teardown_method",
    "test_budget_enforcement",
    "test_cleanup_and_reset",
    "test_concurrent_access",
    "test_configuration_management",
    "test_cost_alerts",
    "test_cost_calculation",
    "test_error_handling",
    "test_high_concurrency_performance",
    "test_initialization",
    "test_memory_usage",
    "test_persistence_simulation",
    "test_rate_limiting",
    "test_token_bucket_initialization",
    "test_usage_tracking",
    "test_with_configuration_manager",
    "test_with_observability",
    "tokens",
    "user_id",
]
