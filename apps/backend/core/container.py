"""
Dependency Injection Container for Core Services.

Wiring các dependencies theo ports/adapters pattern với clean architecture.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

# Imports from project structure (adjust paths if needed)
from zeta_monorepo.core.logger import get_logger  # Assumed standard logger
import Exception
import RuntimeError
import all
import bool
import dict
import e
import factory
import isinstance
import k
import len
import name
import self
import status
import str
import sum
import v
import validation_results

# Global logger instance
logger = get_logger(__name__)


@dataclass(slots=True)
class Container:
    """
    DI Container for core services dependencies.

    This class manages dependencies for various core components, ensuring
    proper injection and validation.

    Attributes:
        metrics (Any): MetricsCollector implementation.
        detector (Any): BottleneckDetector implementation.
        alerts (Any): AlertSystem implementation.
        threat_db (Any): ThreatIntelDatabase implementation.
        bae (Any): BehaviorAnalyticsEngine implementation.
        sec_feed (Any): SecurityEventFeed implementation.
        caches (Dict[str, Any]): CacheBackend implementations by type.
        registry (Any): ModelRegistry implementation.
        deployer (Any): DeploymentStrategy implementation.
        evaluator (Any): EvalService implementation.
        tester_gen (Any): TestCaseGenerator implementation.
        tester_runner (Any): TestRunner implementation.
        tester_reporter (Any): QualityReporter implementation.
    """

    # Metrics & Monitoring
    metrics: Any  # MetricsCollector implementation
    detector: Any  # BottleneckDetector implementation

    # Alerting
    alerts: Any  # AlertSystem implementation

    # Security
    threat_db: Any  # ThreatIntelDatabase implementation
    bae: Any  # BehaviorAnalyticsEngine implementation
    sec_feed: Any  # SecurityEventFeed implementation

    # Caching
    caches: Dict[str, Any]  # CacheBackend implementations by type

    # MLOps
    registry: Any  # ModelRegistry implementation
    deployer: Any  # DeploymentStrategy implementation
    evaluator: Any  # EvalService implementation

    # Testing
    tester_gen: Any  # TestCaseGenerator implementation
    tester_runner: Any  # TestRunner implementation
    tester_reporter: Any  # QualityReporter implementation

    def validate_dependencies(self) -> Dict[str, bool]:
        """
        Validate that all required dependencies are available.

        Returns:
            Dict[str, bool]: Validation results for each dependency.

        Raises:
            ValueError: If validation fails due to invalid input types.
        """
        try:
            validation_results: Dict[str, bool] = {}

            # Check metrics dependencies
            validation_results["metrics"] = self.metrics is not None
            validation_results["detector"] = self.detector is not None

            # Check alerting
            validation_results["alerts"] = self.alerts is not None

            # Check security dependencies
            validation_results["threat_db"] = self.threat_db is not None
            validation_results["bae"] = self.bae is not None
            validation_results["sec_feed"] = self.sec_feed is not None

            # Check caching
            validation_results["caches"] = (
                isinstance(self.caches, dict) and len(self.caches) > 0
            )

            # Check MLOps dependencies
            validation_results["registry"] = self.registry is not None
            validation_results["deployer"] = self.deployer is not None
            validation_results["evaluator"] = self.evaluator is not None

            # Check testing dependencies
            validation_results["tester_gen"] = self.tester_gen is not None
            validation_results["tester_runner"] = self.tester_runner is not None
            validation_results["tester_reporter"] = self.tester_reporter is not None

            all_valid = all(validation_results.values())
            logger.info(
                f"Dependency validation: {sum(validation_results.values())}/{len(validation_results)} dependencies valid"
            )

            if not all_valid:
                missing = [k for k, v in validation_results.items() if not v]
                logger.warning(f"Missing dependencies: {missing}")

            return validation_results

        except Exception as e:
            logger.error(f"Error validating dependencies: {e}")
            return {"validation_error": False}

    async def get_performance_optimizer(self) -> Optional[Any]:
        """
        Get configured performance optimizer.

        Returns:
            Optional[Any]: Performance optimizer instance or None if failed.

        Raises:
            RuntimeError: If optimizer creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.performance.optimizer import (
                AdaptivePerformanceOptimizer,
            )

            # Create optimizer with injected dependencies
            optimizer = AdaptivePerformanceOptimizer(
                monitoring_interval=30.0,
                optimization_cooldown=300.0,
                enable_auto_optimization=True,
            )

            # Note: In real implementation, would inject metrics and detector
            logger.debug("Created performance optimizer with injected dependencies")
            return optimizer

        except Exception as e:
            logger.error(f"Error creating performance optimizer: {e}")
            raise RuntimeError(f"Failed to create performance optimizer: {e}") from e

    async def get_security_monitor(self) -> Optional[Any]:
        """
        Get configured security monitor.

        Returns:
            Optional[Any]: Security monitor instance or None if failed.

        Raises:
            RuntimeError: If monitor creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.security.advanced_monitoring import AISecurityMonitor

            monitor = AISecurityMonitor(
                intel=self.threat_db,
                bae=self.bae,
                feed=self.sec_feed,
                alerts=self.alerts,
            )

            logger.debug("Created security monitor with injected dependencies")
            return monitor

        except Exception as e:
            logger.error(f"Error creating security monitor: {e}")
            raise RuntimeError(f"Failed to create security monitor: {e}") from e

    async def get_memory_manager(self) -> Optional[Any]:
        """
        Get configured memory manager.

        Returns:
            Optional[Any]: Memory manager instance or None if failed.

        Raises:
            RuntimeError: If manager creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.memory.advanced_manager import AdaptiveMemoryManager

            manager = AdaptiveMemoryManager()

            logger.debug("Created memory manager")
            return manager

        except Exception as e:
            logger.error(f"Error creating memory manager: {e}")
            raise RuntimeError(f"Failed to create memory manager: {e}") from e

    async def get_cache_manager(self) -> Optional[Any]:
        """
        Get configured cache manager.

        Returns:
            Optional[Any]: Cache manager instance or None if failed.

        Raises:
            RuntimeError: If manager creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.performance.advanced_caching import (
                AdaptiveCacheManager,
            )

            manager = AdaptiveCacheManager()

            logger.debug("Created cache manager")
            return manager

        except Exception as e:
            logger.error(f"Error creating cache manager: {e}")
            raise RuntimeError(f"Failed to create cache manager: {e}") from e

    async def get_mlops_manager(self) -> Optional[Any]:
        """
        Get configured MLOps manager.

        Returns:
            Optional[Any]: MLOps manager instance or None if failed.

        Raises:
            RuntimeError: If manager creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.learning.ml_integration import MLOpsManager

            manager = MLOpsManager(
                registry=self.registry, deployer=self.deployer, evaluator=self.evaluator
            )

            logger.debug("Created MLOps manager with injected dependencies")
            return manager

        except Exception as e:
            logger.error(f"Error creating MLOps manager: {e}")
            raise RuntimeError(f"Failed to create MLOps manager: {e}") from e

    async def get_automated_tester(self) -> Optional[Any]:
        """
        Get configured automated tester.

        Returns:
            Optional[Any]: Automated tester instance or None if failed.

        Raises:
            RuntimeError: If tester creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.quality.auto_testing import AIPoweredTester

            tester = AIPoweredTester(
                generator=self.tester_gen,
                runner=self.tester_runner,
                reporter=self.tester_reporter,
            )

            logger.debug("Created automated tester with injected dependencies")
            return tester

        except Exception as e:
            logger.error(f"Error creating automated tester: {e}")
            raise RuntimeError(f"Failed to create automated tester: {e}") from e

    async def intelligent_updater(self) -> Optional[Any]:
        """
        Get configured auto updater (v1).

        Returns:
            Optional[Any]: Auto updater instance or None if failed.

        Raises:
            RuntimeError: If updater creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.self_improvement.auto_updater import (
                AsyncShellRunner,
                AutoUpdater,
                LocalFSRepoAdapter,
            )

            repo = LocalFSRepoAdapter(".")
            runner = AsyncShellRunner()
            updater = AutoUpdater(repo, runner)

            logger.debug("Created auto updater (v1) with repo and runner")
            return updater

        except Exception as e:
            logger.error(f"Error creating auto updater: {e}")
            raise RuntimeError(f"Failed to create auto updater: {e}") from e

    async def intelligent_updater_v2(self) -> Optional[Any]:
        """
        Get configured auto updater (v2) with orchestration.

        Returns:
            Optional[Any]: Auto updater v2 instance or None if failed.

        Raises:
            RuntimeError: If updater v2 creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.self_improvement.auto_updater_v2 import (
                AutoUpdaterV2,
                Policy,
            )

            v1_updater = await self.intelligent_updater()
            if not v1_updater:
                return None

            policy = Policy(
                max_changed_files=20,  # Conservative for safety
                allow_globs=("zeta_vn/**", "tests/**", "*.md", "pyproject.toml"),
                deny_globs=("**/.env*", "**/secrets.*", "**/*.key", "**/*.pem"),
            )

            updater_v2 = AutoUpdaterV2(
                v1_updater, policy=policy, history_path="logs/self_improvement.jsonl"
            )

            logger.debug("Created auto updater (v2) with orchestration")
            return updater_v2

        except Exception as e:
            logger.error(f"Error creating auto updater v2: {e}")
            raise RuntimeError(f"Failed to create auto updater v2: {e}") from e

    async def feature_engine(self) -> Optional[Any]:
        """
        Get configured feature rollout engine.

        Returns:
            Optional[Any]: Feature engine instance or None if failed.

        Raises:
            RuntimeError: If engine creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.self_improvement.feature_rollout import FeatureEngine

            engine = FeatureEngine()

            logger.debug("Created feature rollout engine")
            return engine

        except Exception as e:
            logger.error(f"Error creating feature engine: {e}")
            raise RuntimeError(f"Failed to create feature engine: {e}") from e

    async def health_monitor(self) -> Optional[Any]:
        """
        Get configured health monitor.

        Returns:
            Optional[Any]: Health monitor instance or None if failed.

        Raises:
            RuntimeError: If monitor creation fails.
        """
        try:
            from zeta_monorepo.apps.backend.core.services.health_monitor import RealTimeHealthMonitor

            monitor = RealTimeHealthMonitor(
                metrics=self.metrics,
                alerts=self.alerts,
                heal_threshold=0.7,
                interval_sec=60,
            )

            logger.debug("Created health monitor with injected dependencies")
            return monitor

        except Exception as e:
            logger.error(f"Error creating health monitor: {e}")
            raise RuntimeError(f"Failed to create health monitor: {e}") from e

    async def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status from all components.

        Returns:
            Dict[str, Any]: System status dictionary.

        Raises:
            RuntimeError: If status retrieval fails.
        """
        try:
            status: Dict[str, Any] = {
                "container": "operational",
                "dependencies": self.validate_dependencies(),
                "components": {},
            }

            # Check each component
            components = [
                ("performance_optimizer", self.get_performance_optimizer),
                ("security_monitor", self.get_security_monitor),
                ("memory_manager", self.get_memory_manager),
                ("cache_manager", self.get_cache_manager),
                ("mlops_manager", self.get_mlops_manager),
                ("automated_tester", self.get_automated_tester),
                ("intelligent_updater", self.intelligent_updater),
                ("intelligent_updater_v2", self.intelligent_updater_v2),
                ("feature_engine", self.feature_engine),
                ("health_monitor", self.health_monitor),
            ]

            for name, factory in components:
                try:
                    component = await factory()
                    status["components"][name] = "available" if component else "failed"
                except Exception as e:
                    status["components"][name] = f"error: {e}"

            available_count = sum(
                1 for v in status["components"].values() if v == "available"
            )
            status["health_score"] = available_count / len(components)

            logger.info(
                f"System status: {available_count}/{len(components)} components available"
            )
            return status

        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            raise RuntimeError(f"Failed to get system status: {e}") from e


__all__ = ["Container"]
