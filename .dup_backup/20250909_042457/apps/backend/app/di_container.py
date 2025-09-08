import Exception
import ImportError
import RuntimeError
import ValueError
import agent
import agent_data
import agent_id
import agent_repository
import bool
import call_next
import cfg_exc
import cleanup_func
import config
import data
import database_service
import db_session
import dep_name
import dict
import e
import email
import exc
import factory
import gemini_service
import getattr
import hasattr
import int
import isinstance
import key
import list
import memory_repository
import name
import owner_id
import param_name
import repository
import request
import self
import service
import service_name
import session
import status
import str
import svc_name
import telemetry_service
import type
import user
import user_id
import user_repository
import value
# zeta_vn/app/di_container.py


"""


Dependency Injection Container & Service Registry for ZETA AI Server


Author: Duy BG VN





🎯 COMPREHENSIVE DI SYSTEM:


- Service registration với lifecycle management


- Async service resolution với dependency graph


- Factory patterns cho complex services


- Scoped services cho request lifecycle


- Health check integration


- Configuration-driven service creation


"""

from __future__ import annotations

import asyncio
import inspect
import logging
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


T = TypeVar("T")

if TYPE_CHECKING:
    # Import interfaces only for typing; avoid runtime E402 issues
    from apps.backend.core.interfaces.repositories import (
        AgentRepository as AgentRepositoryInterface,
    )
    from apps.backend.core.interfaces.repositories import (
        UserRepository as UserRepositoryInterface,
    )


class ServiceLifecycle(ABC):
    """Service lifecycle management interface."""

    @abstractmethod
    async def startup(self) -> None:
        """Service startup logic."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Service cleanup logic."""

    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        """Service health check."""


class ServiceScope:
    """Service scope for request-scoped dependencies."""

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}
        # cleanup functions may be sync hoặc async; lưu trong danh sách
        self._cleanup_tasks: list[Callable[..., Any]] = []

    def set(self, key: str, value: Any) -> None:
        """Set a scoped service."""

        self._services[key] = value

    def get(self, key: str) -> Any:
        """Get a scoped service."""

        return self._services.get(key)

    def add_cleanup(self, cleanup_func: Callable[..., Any]) -> None:
        """Add cleanup function."""

        self._cleanup_tasks.append(cleanup_func)

    async def cleanup(self) -> None:
        """Cleanup all scoped services."""

        for cleanup_func in self._cleanup_tasks:
            try:
                if asyncio.iscoroutinefunction(cleanup_func):
                    await cleanup_func()

                else:
                    cleanup_func()

            except Exception as e:
                logger.error(f"Scope cleanup failed: {e}")


class DIContainer:
    """Advanced dependency injection container."""

    def __init__(self, config: Any):
        self.config = config

        # singleton instances and registered factory maps
        self._singletons: dict[str, Any] = {}
        self._factories: dict[str, Callable[..., Any]] = {}

        # transient and scoped factory registries
        self._transient_factories: dict[str, Callable[..., Any]] = {}
        self._scoped_factories: dict[str, Callable[..., Any]] = {}

        # lifecycle-managed services and dependency graph
        self._lifecycle_services: dict[str, ServiceLifecycle] = {}
        self._dependency_graph: dict[str, list[str]] = {}

    # ================================================================================

    # SERVICE REGISTRATION

    # ================================================================================

    def register_singleton(self, name: str, instance: Any) -> DIContainer:
        """Register a singleton service instance."""

        self._singletons[name] = instance

        if isinstance(instance, ServiceLifecycle):
            self._lifecycle_services[name] = instance

        logger.debug(f"Singleton registered: {name} ({type(instance).__name__})")

        return self

    def register_factory(
        self,
        name: str,
        factory: Callable[..., Any],
        dependencies: list[str] | None = None,
    ) -> DIContainer:
        """Register a factory function for singleton services."""

        self._factories[name] = factory

        self._dependency_graph[name] = dependencies or []

        logger.debug(f"Factory registered: {name}, dependencies: {dependencies}")

        return self

    def register_transient(
        self,
        name: str,
        factory: Callable[..., Any],
        dependencies: list[str] | None = None,
    ) -> DIContainer:
        """Register a transient service (new instance each time)."""

        self._transient_factories[name] = factory

        self._dependency_graph[name] = dependencies or []

        logger.debug(
            f"Transient factory registered: {name}, dependencies: {dependencies}"
        )

        return self

    def register_scoped(
        self,
        name: str,
        factory: Callable[..., Any],
        dependencies: list[str] | None = None,
    ) -> DIContainer:
        """Register a scoped service (one instance per request)."""

        self._scoped_factories[name] = factory

        self._dependency_graph[name] = dependencies or []

        logger.debug(f"Scoped factory registered: {name}, dependencies: {dependencies}")

        return self

    # ================================================================================

    # SERVICE RESOLUTION

    # ================================================================================

    async def get(self, name: str, scope: ServiceScope | None = None) -> Any:
        """Get a service instance with dependency resolution."""

        # Check singleton first

        if name in self._singletons:
            return self._singletons[name]

        # Check scoped services

        if scope and name in self._scoped_factories:
            scoped_instance = scope.get(name)

            if scoped_instance is not None:
                return scoped_instance

            # Create scoped instance

            instance = await self._create_instance(
                name, self._scoped_factories[name], scope
            )

            scope.set(name, instance)

            # Add cleanup if needed

            if hasattr(instance, "cleanup"):
                scope.add_cleanup(instance.cleanup)

            return instance

        # Check transient services

        if name in self._transient_factories:
            return await self._create_instance(
                name, self._transient_factories[name], scope
            )

        # Check singleton factories

        if name in self._factories:
            if name not in self._singletons:
                instance = await self._create_instance(
                    name, self._factories[name], scope
                )

                self._singletons[name] = instance

                if isinstance(instance, ServiceLifecycle):
                    self._lifecycle_services[name] = instance

            return self._singletons[name]

        raise ValueError(f"Service '{name}' not registered in DI container")

    def has(self, name: str) -> bool:
        """Return True if the service is registered or already instantiated."""
        return (
            name in self._singletons
            or name in self._factories
            or name in self._transient_factories
            or name in self._scoped_factories
        )

    def get_sync_if_ready(self, name: str) -> Any | None:
        """Return singleton instance if already created; do not instantiate.

        Useful for best-effort, non-blocking reads from the container.
        """
        return self._singletons.get(name)

    async def _create_instance(
        self,
        name: str,
        factory: Callable[..., Any],
        scope: ServiceScope | None = None,
    ) -> Any:
        """Create service instance with dependency injection."""

        try:
            # Resolve dependencies

            dependencies = self._dependency_graph.get(name, [])

            resolved_deps = {}

            for dep_name in dependencies:
                resolved_deps[dep_name] = await self.get(dep_name, scope)

            # Check if factory expects specific parameters

            sig = inspect.signature(factory)

            factory_args = {}

            for param_name in sig.parameters:
                if param_name in resolved_deps:
                    factory_args[param_name] = resolved_deps[param_name]

                elif param_name == "config":
                    factory_args["config"] = self.config

                elif param_name == "container":
                    factory_args["container"] = self

                elif param_name == "scope":
                    factory_args["scope"] = scope

            # Create instance

            if asyncio.iscoroutinefunction(factory):
                instance = await factory(**factory_args)

            else:
                instance = factory(**factory_args)

            logger.debug(
                f"Service instance created: {name} ({type(instance).__name__})"
            )

            return instance

        except Exception as e:
            logger.error(f"Failed to create service instance '{name}': {e}")

            raise

    # ================================================================================

    # LIFECYCLE MANAGEMENT

    # ================================================================================

    async def startup_all(self) -> None:
        """Start all lifecycle services."""
        # Eagerly instantiate all singleton factories so lifecycle hooks are available
        for svc_name in self._factories:
            try:
                await self.get(svc_name)
            except Exception as e:
                logger.warning(
                    "Service '%s' failed to initialize during startup: %s",
                    svc_name,
                    e,
                )

        for name, service in self._lifecycle_services.items():
            try:
                await service.startup()
                logger.info(f"Service started: {name}")
            except Exception as e:
                logger.error(f"Service startup failed '{name}': {e}")
                raise

    async def shutdown_all(self) -> None:
        """Shutdown all lifecycle services."""

        for name, service in self._lifecycle_services.items():
            try:
                await service.shutdown()

                logger.info(f"Service stopped: {name}")

            except Exception as e:
                logger.error(f"Service shutdown failed '{name}': {e}")

    async def health_check_all(self) -> dict[str, dict[str, Any]]:
        """Run health checks for all lifecycle services."""

        results = {}

        for name, service in self._lifecycle_services.items():
            try:
                results[name] = await service.health_check()

            except Exception as e:
                results[name] = {
                    "status": "unhealthy",
                    "error": str(e),
                }

        return results

    def get_database_service(self) -> Any | None:
        """Compatibility accessor for code paths expecting sync database service getter."""
        return self._singletons.get("database_service")

    # ================================================================================

    # SCOPE MANAGEMENT

    # ================================================================================

    @asynccontextmanager
    async def create_scope(self) -> AsyncGenerator[ServiceScope, None]:
        """Create a new service scope for request handling.

        Yields:
            ServiceScope: a new scope for request handling.
        """

        scope = ServiceScope()

        try:
            yield scope

        finally:
            await scope.cleanup()


# ================================================================================


# STANDARD SERVICE FACTORIES


# ================================================================================


class DatabaseService(ServiceLifecycle):
    """Database service with lifecycle management."""

    def __init__(self, config: Any):
        self.config = config

        self.session_maker = None

    async def startup(self) -> None:
        """Initialize database connection."""

        try:
            # Use standard SQLAlchemy async session from data.models.base

            try:
                from apps.backend.data.models.base import async_session_maker

            except ImportError:
                try:
                    # Try relative import if zeta_vn is not in path

                    from apps.backend.data.models.base import async_session_maker

                except ImportError:
                    logger.warning("Database models not available")

                    return

            self.session_maker = async_session_maker

            # Test connection by creating a session

            async with self.session_maker() as session:
                import sqlalchemy  # noqa: E402

                await session.execute(sqlalchemy.text("SELECT 1"))

            logger.info("Database service started with SQLAlchemy async session")

        except Exception as e:
            logger.error(f"Database startup failed: {e}")

            raise

    async def shutdown(self) -> None:
        """Close database connection."""

        if self.session_maker:
            # SQLAlchemy session maker doesn't need explicit cleanup

            logger.info("Database service stopped")

    async def health_check(self) -> dict[str, Any]:
        """Check database health."""

        if not self.session_maker:
            return {
                "status": "unhealthy",
                "message": "Database session maker not initialized",
            }

        try:
            import sqlalchemy

            async with self.session_maker() as session:
                await session.execute(sqlalchemy.text("SELECT 1"))

                return {"status": "healthy", "message": "Database connection OK"}

        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def get_session(self) -> AsyncSession:
        """Get database session."""

        if not self.session_maker:
            raise RuntimeError("Database session maker not initialized")

        return self.session_maker()


class CacheService(ServiceLifecycle):
    """Cache service with lifecycle management."""

    def __init__(self, config: Any):
        self.config = config
        # Backing client: CacheManager instance, dict fallback, or None
        self.client = None

    async def startup(self) -> None:
        """Initialize cache connection."""

        try:
            # Prefer centralized CacheManager from config.cache
            try:
                from apps.backend.config.cache import get_cache_manager, init_cache

                await init_cache()
                self.client = get_cache_manager()
                logger.info("Cache service started (CacheManager)")
                return
            except Exception as cfg_exc:
                logger.debug("CacheManager path unavailable: %s", cfg_exc)

            # Fallback cache implementation when optional client missing
            logger.warning("Cache client not available, using memory cache")
            self.client = {}  # Simple dict cache for development
        except Exception as e:
            logger.error(f"Cache startup failed: {e}")
            raise

    async def shutdown(self) -> None:
        """Close cache connection."""
        # Narrow types for static analysis and safe runtime
        if isinstance(self.client, dict):
            logger.info("Cache service stopped (memory cache)")
            return
        # Attempt to close via CacheManager when available
        try:
            from apps.backend.config.cache import close_cache

            await close_cache()
            logger.info("Cache service stopped")
            return
        except Exception:
            pass

    # No additional client-specific cleanup required

    async def health_check(self) -> dict[str, Any]:
        """Check cache health."""

        if not self.client:
            return {"status": "unhealthy", "message": "Cache client not initialized"}

        try:
            if isinstance(self.client, dict):
                # Memory cache is always healthy
                return {"status": "healthy", "message": "Memory cache OK"}
            # Prefer CacheManager.get_stats when available
            if hasattr(self.client, "get_stats"):
                try:
                    # type: ignore[call-arg]
                    stats = await self.client.get_stats()  # pyright: ignore[reportUnknownMemberType]
                    _ = stats  # mark used
                    return {"status": "healthy", "message": "Cache manager OK"}
                except Exception as exc:
                    return {"status": "unhealthy", "error": str(exc)}
            # No generic ping available
            return {"status": "unknown", "message": "Health check not implemented"}

        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# ================================================================================


# CONTAINER FACTORY & REGISTRATION


# ================================================================================


def create_di_container(config: Any) -> DIContainer:
    """Create and configure the DI container with all services."""

    container = DIContainer(config)

    # Register core services

    container.register_singleton("config", config)

    # Register database service

    container.register_factory(
        "database_service",
        lambda config: DatabaseService(config),
        dependencies=["config"],
    )

    # Register cache service

    container.register_factory(
        "cache_service", lambda config: CacheService(config), dependencies=["config"]
    )

    # Expose cache_manager as a singleton for fast access by components
    try:
        from apps.backend.config.cache import get_cache_manager

        container.register_singleton("cache_manager", get_cache_manager())
    except Exception as _:
        logger.debug("cache_manager not available at startup")

    # Register scoped database session

    container.register_scoped(
        "db_session",
        lambda database_service: database_service.get_session(),
        dependencies=["database_service"],
    )

    # Register repositories

    container.register_scoped(
        "user_repository", _create_user_repository, dependencies=["db_session"]
    )

    container.register_scoped(
        "agent_repository", _create_agent_repository, dependencies=["db_session"]
    )

    container.register_scoped(
        "memory_repository", _create_memory_repository, dependencies=["db_session"]
    )

    # Register services

    container.register_scoped(
        "user_service", _create_user_service, dependencies=["user_repository"]
    )

    container.register_scoped(
        "agent_service", _create_agent_service, dependencies=["agent_repository"]
    )

    container.register_scoped(
        "performance_optimizer",
        _create_performance_optimizer,
        dependencies=["agent_repository", "memory_repository"],
    )

    # Gemini LLM service (optional)
    container.register_factory(
        "gemini_service",
        lambda config: _create_gemini_service(config),
        dependencies=["config"],
    )

    # MoE Router (lightweight strategy selector)
    try:
        from apps.backend.core.services.moe_router import MoERouter  # type: ignore

        container.register_singleton("moe_router", MoERouter())
    except Exception as _:
        logger.debug("moe_router not available at startup")

    # Prompt Injection Guard (rule-based, optional use in services)
    try:
        from apps.backend.core.services.prompt_injection_guard import (
            PromptInjectionGuard,
        )

        container.register_singleton("prompt_injection_guard", PromptInjectionGuard())
    except Exception as _:
        logger.debug("prompt_injection_guard not available at startup")

    # Self-Learning (online bandit over MoE choices)
    try:
        from apps.backend.core.services.self_learning_service import SelfLearningService

        def _make_self_learning(_config):
            from apps.backend.core.services.moe_router import MoERouter

            r = container._singletons.get("moe_router")
            if not isinstance(r, MoERouter):
                r = MoERouter()
                container.register_singleton("moe_router", r)
            return SelfLearningService(router=r)

        container.register_factory(
            "self_learning", _make_self_learning, dependencies=["config"]
        )
    except Exception:
        logger.debug("self_learning not available at startup")

    # Register minimal telemetry service for training flows (dev-friendly)
    try:
        from apps.backend.core.services.telemetry import TelemetryService

        container.register_singleton("telemetry_service", TelemetryService())
    except Exception:
        logger.debug("telemetry service not available at startup")

    # Register RLHF store (in-memory dev implementation)
    try:
        from apps.backend.core.services.rlhf_store import InMemoryRLHFStore

        container.register_singleton("rlhf_store", InMemoryRLHFStore())
    except Exception:
        logger.debug("rlhf_store not available at startup")

    # Register a simple in-memory KnowledgeStore for dev (kb_store)
    try:

        class _InMemoryKB:
            def __init__(self):
                self._store = {}

            async def find_similar(self, q, *, threshold=0.9):
                # naive similarity: return empty (dev safe)
                await asyncio.sleep(0)
                return []

            async def upsert_artifact(self, key, data):
                self._store[key] = data
                return key

        container.register_singleton("kb_store", _InMemoryKB())
    except Exception:
        logger.debug("kb_store dev fallback not available at startup")

    # Trainer service factory: prefer configured gemini_service, fallback to stub LLM
    def _create_trainer_service(gemini_service=None, telemetry_service=None):
        try:
            from apps.backend.training.gpt4o_trainer import GPT4oTrainerService
        except Exception:
            raise

        # choose llm
        if (
            gemini_service is not None
            and getattr(gemini_service, "is_configured", lambda: False)()
        ):
            llm = gemini_service
        else:

            class _StubLLM:
                async def complete(self, *args, **kwargs):
                    return "STUB ARTIFACT: placeholder"

            llm = _StubLLM()

        # simple fetcher stub
        class _StubFetcher:
            def fetch(self, query, *, limit=5):
                return []

        fetcher = _StubFetcher()

        # concurrency limiter: small semaphore to avoid many parallel LLM calls
        sem_limit = (
            getattr(gemini_service, "concurrency_limit", None)
            if gemini_service is not None
            else None
        )
        sem = asyncio.Semaphore(int(sem_limit) if sem_limit else 3)

        return GPT4oTrainerService(
            llm=llm,
            fetcher=fetcher,
            telemetry=telemetry_service,
            concurrency_semaphore=sem,
        )

    container.register_factory(
        "trainer_service",
        _create_trainer_service,
        dependencies=["gemini_service", "telemetry_service"],
    )

    logger.info("DI Container configured with all services")

    return container


# ================================================================================


# REPOSITORY & SERVICE FACTORIES


# ================================================================================


def _create_user_repository(db_session: AsyncSession):
    """Create user repository."""

    try:
        try:
            from apps.backend.data.repositories.sqlalchemy_user_repository import (
                SQLAlchemyUserRepository,
            )

        except ImportError:
            from apps.backend.data.repositories.sqlalchemy_user_repository import (
                SQLAlchemyUserRepository,
            )

        return SQLAlchemyUserRepository(db_session)

    except ImportError:
        logger.warning("SQLAlchemy user repository not available")

        # Lightweight interface-conforming mock for development
        class MockUserRepository(UserRepositoryInterface):
            def __init__(self) -> None:
                pass

            async def create(self, user) -> Any:  # type: ignore[no-untyped-def]
                return user

            async def get_by_id(self, user_id: str) -> Any:  # type: ignore[no-untyped-def]
                _ = user_id
                return None

            async def get_by_email(self, email: str) -> Any:  # type: ignore[no-untyped-def]
                _ = email
                return None

            async def update(self, user) -> Any:  # type: ignore[no-untyped-def]
                return user

            async def delete(self, user_id: str) -> bool:  # type: ignore[no-untyped-def]
                _ = user_id
                return True

        return MockUserRepository()


def _create_agent_repository(db_session: AsyncSession):
    """Create agent repository."""

    try:
        try:
            from apps.backend.data.repositories.sqlalchemy_agent_repository import (
                SQLAlchemyAgentRepository,
            )

        except ImportError:
            from apps.backend.data.repositories.sqlalchemy_agent_repository import (
                SQLAlchemyAgentRepository,
            )

        return SQLAlchemyAgentRepository(db_session)

    except ImportError:
        logger.warning("SQLAlchemy agent repository not available")

        # Lightweight interface-conforming mock for development
        class MockAgentRepository(AgentRepositoryInterface):
            async def create(self, agent):  # type: ignore[no-untyped-def]
                return agent

            async def get_by_id(self, agent_id):  # type: ignore[no-untyped-def]
                _ = agent_id
                return None

            async def get_by_owner(self, owner_id):  # type: ignore[no-untyped-def]
                _ = owner_id
                return []

            async def update(self, agent):  # type: ignore[no-untyped-def]
                return agent

            async def delete(self, agent_id):  # type: ignore[no-untyped-def]
                _ = agent_id
                return True

            async def list_by_status(self, status):  # type: ignore[no-untyped-def]
                _ = status
                return []

        return MockAgentRepository()


def _create_memory_repository(db_session: AsyncSession):
    """Create memory repository."""

    try:
        try:
            from apps.backend.data.repositories.sqlalchemy_memory_repository import (
                SQLAlchemyMemoryRepository,
            )

        except ImportError:
            from apps.backend.data.repositories.sqlalchemy_memory_repository import (
                SQLAlchemyMemoryRepository,
            )

        return SQLAlchemyMemoryRepository(db_session)

    except ImportError:
        logger.warning("SQLAlchemy memory repository not available")

        # Return simple mock for development
        class MockMemoryRepository:
            def __init__(self, session):
                self._ = session

            async def get_by_agent(self, agent_id):  # type: ignore[no-untyped-def]
                _ = agent_id  # mark used
                await asyncio.sleep(0)
                return []

        return MockMemoryRepository(db_session)


# Public wrappers for building repositories/services per session (for dependencies.py)


def create_agent_repository_for_session(
    db_session: AsyncSession,
) -> AgentRepositoryInterface:
    """Create an AgentRepository bound to the given session.

    Kept in di_container so that data-layer imports remain whitelisted.
    """
    return _create_agent_repository(db_session)


def create_user_repository_for_session(
    db_session: AsyncSession,
) -> UserRepositoryInterface:
    """Create a UserRepository bound to the given session.

    Kept in di_container so that data-layer imports remain whitelisted.
    """
    return _create_user_repository(db_session)


def create_training_service_for_session(db_session: AsyncSession):
    """Create TrainingService with real SQLAlchemy repositories bound to session."""
    try:
        from apps.backend.core.services.training_service import TrainingService
        from apps.backend.data.repositories.dataset_item_repository import (
            DatasetItemRepository,
        )
        from apps.backend.data.repositories.training_job_repository import (
            TrainingJobRepository,
        )

        training_job_repo = TrainingJobRepository(db_session)
        dataset_item_repo = DatasetItemRepository(db_session)

        return TrainingService(
            training_job_repository=training_job_repo,
            dataset_item_repository=dataset_item_repo,
        )
    except Exception as exc:  # pragma: no cover - optional path
        logger.warning("TrainingService creation failed: %s", exc)
        raise


def _create_performance_optimizer(agent_repository: Any, memory_repository: Any):
    """Factory for PerformanceOptimizer bound to scoped repositories.

    Returns a request-scoped optimizer without background threads.
    """
    try:
        from apps.backend.core.services.performance_optimizer import (
            PerformanceOptimizer,
        )

        return PerformanceOptimizer(
            agent_repository=agent_repository,
            memory_repository=memory_repository,
            auto_optimize=True,
            background_collect_interval=None,
        )
    except Exception as exc:  # pragma: no cover - optional dep path
        logger.warning("PerformanceOptimizer unavailable: %s", exc)

        class _Stub:
            async def optimize_agent(self, _agent_id):  # type: ignore[no-untyped-def]
                await asyncio.sleep(0)
                return {"status": "unavailable"}

        return _Stub()


def _create_user_service(user_repository):
    """Create user service."""
    try:
        from importlib import import_module

        user_mod = import_module("zeta_vn.core.services.user_service")
        user_service_cls = user_mod.UserService  # type: ignore[attr-defined]
        return user_service_cls(user_repository)  # type: ignore[call-arg]

    except Exception:
        logger.warning("User service not available")

        # Return simple mock for development
        class MockUserService:
            def __init__(self, repository):
                self.repository = repository

            def get_user(self, user_id: str):
                return {"id": user_id, "name": f"User {user_id}", "status": "active"}

        return MockUserService(user_repository)


def _create_agent_service(agent_repository):
    """Create agent service."""
    try:
        from importlib import import_module

        # Use canonical import path to avoid legacy shim and reduce depth
        agent_mod = import_module("zeta_vn.core.services.agent.service")
        agent_service_cls = agent_mod.AgentService  # type: ignore[attr-defined]
        # AgentService inherits from BaseService which takes no arguments
        logger.info("Using canonical AgentService (unified orchestrator)")
        return agent_service_cls()  # type: ignore[call-arg]

    except Exception:
        logger.warning("Agent service not available")

        # Return simple mock for development
        class MockAgentService:
            def __init__(self, repository):
                self.repository = repository

            def create_agent(self, agent_data: dict):
                return {
                    "id": "mock_agent",
                    "name": agent_data.get("name", "Mock Agent"),
                }

            def get_agent(self, agent_id: str):
                return {"id": agent_id, "name": f"Agent {agent_id}", "status": "active"}

        return MockAgentService(agent_repository)


def _create_gemini_service(config: Any):
    """Create Gemini service if configured; return a safe stub otherwise."""
    try:
        from apps.backend.app.services.gemini_service import GeminiService

        def _client_provider():
            # Importing data-layer client here is allowed by import-linter exclusions
            from apps.backend.data.external.llm.gemini_client import GeminiClient

            return GeminiClient(
                api_key=str(getattr(config, "GEMINI_API_KEY", "")),
                model=str(getattr(config, "GEMINI_MODEL", "")),
                api_endpoint=str(getattr(config, "GEMINI_API_ENDPOINT", "")),
                request_timeout=int(getattr(config, "GEMINI_REQUEST_TIME_SECONDS", 30)),
            )

        return GeminiService(config, client_provider=_client_provider)
    except Exception as exc:  # pragma: no cover - optional dep
        logger.warning("GeminiService unavailable: %s", exc)

    class Stub:
        def is_configured(self) -> bool:
            return False

        def ping(self) -> dict[str, Any]:
            return {"status": "unavailable", "reason": "gemini service not available"}

    return Stub()


# ================================================================================


# FASTAPI INTEGRATION


# ================================================================================


class DIMiddleware:
    """FastAPI middleware for dependency injection."""

    def __init__(self, container: DIContainer):
        self.container = container

    async def __call__(self, request, call_next):
        """Process request with DI scope."""

        async with self.container.create_scope() as scope:
            request.state.di_scope = scope

            response = await call_next(request)

            return response


def get_di_container() -> DIContainer | None:
    """FastAPI dependency to get DI container."""

    # This will be set by the application factory

    return getattr(get_di_container, "_container", None)


def get_service(service_name: str):
    """FastAPI dependency factory for services."""

    async def _get_service(request):
        container = get_di_container()

        if container is None:
            # Fallback: fetch from FastAPI app state
            container = getattr(getattr(request, "app", None), "state", None)
            container = getattr(container, "di_container", None)
            if container is None:
                raise RuntimeError("DI container not initialized")

        scope = getattr(request.state, "di_scope", None)

        return await container.get(service_name, scope)

    return _get_service


# ================================================================================


# DEPENDENCY SHORTCUTS


# ================================================================================


# Common dependency shortcuts for FastAPI endpoints


GetUserService = get_service("user_service")


GetAgentService = get_service("agent_service")


GetUserRepository = get_service("user_repository")


GetAgentRepository = get_service("agent_repository")


GetDatabaseSession = get_service("db_session")

# Additional shortcuts
GetMemoryRepository = get_service("memory_repository")
GetPerformanceOptimizer = get_service("performance_optimizer")
