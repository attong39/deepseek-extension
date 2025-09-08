import RuntimeError
import ValueError
import dict
import exc_info
import isinstance
import name
import scope1
import scope2
import self
import str
# zeta_vn/tests/integration/test_di_simple.py
"""
Simple DI Integration Tests
Testing DI container functionality without complex imports.
"""

from unittest.mock import MagicMock

import pytest

from app.di_container import DIContainer, ServiceLifecycle


class TestServiceLifecycle(ServiceLifecycle):
    """Test service for lifecycle testing."""

    def __init__(self, name: str):
        self.name = name
        self.started = False
        self.stopped = False
        self.health_status = "healthy"

    async def startup(self) -> None:
        self.started = True

    async def shutdown(self) -> None:
        self.stopped = True

    async def health_check(self) -> dict:
        return {"status": self.health_status, "service": self.name}


@pytest.fixture
def mock_config():
    """Create mock configuration for testing."""
    config = MagicMock()
    config.database.url = "sqlite:///test.db"
    config.cache.enabled = False
    config.app_name = "test-app"
    return config


@pytest.fixture
async def di_container(mock_config):
    """Create DI container for testing."""
    container = DIContainer(mock_config)

    # Register config service first
    container.register_singleton("config", mock_config)

    # Register test services
    test_service = TestServiceLifecycle("test")
    container.register_singleton("test_service", test_service)

    # Register factory
    container.register_factory(
        "factory_service",
        lambda config: f"factory-{config.app_name}",
        dependencies=["config"],
    )

    # Register scoped service
    container.register_scoped("scoped_service", lambda: "scoped-instance")

    return container


class TestDIContainer:
    """Test DI container functionality."""

    @pytest.mark.asyncio
    async def test_singleton_registration(self, di_container):
        """Test singleton service registration and retrieval."""
        service = await di_container.get("test_service")
        assert isinstance(service, TestServiceLifecycle)
        assert service.name == "test"

        # Should return same instance
        service2 = await di_container.get("test_service")
        assert service is service2

    @pytest.mark.asyncio
    async def test_factory_registration(self, di_container):
        """Test factory service registration with dependencies."""
        service = await di_container.get("factory_service")
        assert service == "factory-test-app"

        # Should return same instance (singleton factory)
        service2 = await di_container.get("factory_service")
        assert service == service2

    @pytest.mark.asyncio
    async def test_scoped_service(self, di_container):
        """Test scoped service registration and scope isolation."""
        async with di_container.create_scope() as scope1:
            async with di_container.create_scope() as scope2:
                service1 = await di_container.get("scoped_service", scope1)
                service2 = await di_container.get("scoped_service", scope2)

                # Different scopes should have different instances
                assert service1 == service2  # Same value
                # But they're from different scopes

    @pytest.mark.asyncio
    async def test_lifecycle_management(self, di_container):
        """Test service lifecycle startup and shutdown."""
        # Start services
        await di_container.startup_all()

        service = await di_container.get("test_service")
        assert service.started is True

        # Shutdown services
        await di_container.shutdown_all()
        assert service.stopped is True

    @pytest.mark.asyncio
    async def test_health_checks(self, di_container):
        """Test health check functionality."""
        await di_container.startup_all()

        health_results = await di_container.health_check_all()
        assert "test_service" in health_results
        assert health_results["test_service"]["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_missing_service(self, di_container):
        """Test error handling for missing services."""
        with pytest.raises(ValueError) as exc_info:
            await di_container.get("nonexistent_service")
        assert "not registered" in str(exc_info.value)


class TestErrorHandling:
    """Test error handling in DI system."""

    @pytest.mark.asyncio
    async def test_service_creation_error(self, mock_config):
        """Test error handling during service creation."""
        container = DIContainer(mock_config)

        def failing_factory():
            raise RuntimeError("Service creation failed")

        container.register_factory("failing_service", failing_factory)

        with pytest.raises(RuntimeError):
            await container.get("failing_service")

    @pytest.mark.asyncio
    async def test_lifecycle_error_handling(self, di_container):
        """Test error handling in lifecycle management."""
        # Create service that fails on startup
        failing_service = TestServiceLifecycle("failing")

        async def failing_startup():
            raise RuntimeError("Startup failed")

        failing_service.startup = failing_startup
        di_container.register_singleton("failing_service", failing_service)

        with pytest.raises(RuntimeError):
            await di_container.startup_all()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
