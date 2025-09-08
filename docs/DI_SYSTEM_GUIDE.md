# ZETA AI Server - Advanced DI System Guide

## 🎯 Overview

The new ZETA AI Server features a comprehensive Dependency Injection (DI) system that provides:

- **Configuration-driven architecture** with environment-specific settings
- **Service lifecycle management** with startup, shutdown, and health checks
- **Request scoping** for efficient resource management
- **Type-safe dependency resolution** with FastAPI integration
- **Plugin architecture** for dynamic module loading
- **Enterprise-grade monitoring** and observability

## 🏗️ Architecture Components

### 1. Main Application (`app/main_v2.py`)
- **ZetaAIApplication**: Enterprise-grade FastAPI factory
- **AppConfig**: Configuration dataclass with environment support
- **PluginManager**: Dynamic module loading and health checks
- **HealthManager**: Comprehensive system monitoring

### 2. DI Container (`app/di_container.py`)
- **DIContainer**: Service registration and resolution
- **ServiceLifecycle**: Interface for managed services
- **ServiceScope**: Request-scoped service management
- **Factory patterns**: Singleton, transient, and scoped services

### 3. Enhanced Dependencies (`app/dependencies_v2.py`)
- **Type-safe FastAPI dependencies** with proper annotations
- **Authentication & authorization** helpers
- **Repository & service injection** with automatic resolution
- **Pagination & validation** utilities

### 4. Demo Router (`app/api/v1/demo_di.py`)
- **Complete demonstration** of DI patterns
- **Authentication examples** (required, optional, none)
- **Service injection patterns** with proper error handling
- **Health monitoring** and container status endpoints

## 🚀 Quick Start

### 1. Using the New Application Factory

```python
# Option 1: Use main_v2.py directly
uvicorn app.main_v2:app --reload

# Option 2: Integration with existing main.py
from app.main_v2 import ZetaAIApplication

app_instance = ZetaAIApplication()
app = await app_instance.create_app()
```

### 2. Testing the DI System

```bash
# Run the test script
python scripts/test_di_system.py

# Start the server
uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000

# Test demo endpoints
curl http://localhost:8000/demo/
curl http://localhost:8000/demo/health
curl -H "Authorization: Bearer test" http://localhost:8000/demo/auth/profile
```

### 3. Demo Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /demo/` | None | System overview and capabilities |
| `GET /demo/health` | None | DI services health check |
| `GET /demo/container/status` | None | DI container detailed status |
| `GET /demo/auth/profile` | Required | Authenticated user profile |
| `GET /demo/auth/optional` | Optional | Optional authentication demo |
| `GET /demo/agents` | Required | List user agents with pagination |
| `POST /demo/agents` | Required | Create new agent |
| `GET /demo/agents/{id}` | Required | Get specific agent with access control |

## 📝 Usage Patterns

### 1. Creating Endpoints with DI

```python
from app.dependencies_v2 import CurrentUserId, UserService, AgentService

@router.get("/users/profile")
async def get_profile(
    user_id: CurrentUserId,
    user_service: UserService
):
    """Get user profile with automatic DI."""
    user = await user_service.get_user(user_id)
    return {"user": user}

@router.get("/agents")
async def list_agents(
    user_id: CurrentUserId,
    agent_service: AgentService,
    pagination: PaginationParams
):
    """List agents with pagination and DI."""
    agents = await agent_service.list_user_agents(user_id)
    return paginate_results(agents, pagination)
```

### 2. Service Registration

```python
# In DI container setup
container.register_singleton("config", app_config)

container.register_factory(
    "user_service",
    create_user_service,
    dependencies=["user_repository"]
)

container.register_scoped(
    "db_session",
    lambda database_service: database_service.get_session(),
    dependencies=["database_service"]
)
```

### 3. Custom Service Lifecycle

```python
class MyService(ServiceLifecycle):
    async def startup(self):
        # Initialize resources
        pass

    async def shutdown(self):
        # Cleanup resources
        pass

    async def health_check(self):
        return {"status": "healthy", "connections": 10}
```

## 🔧 Configuration

### Environment-Specific Settings

```python
# config/settings/development.py
class DevelopmentConfig(BaseConfig):
    debug = True
    database_url = "sqlite:///dev.db"
    log_level = "DEBUG"

# config/settings/production.py
class ProductionConfig(BaseConfig):
    debug = False
    database_url = os.getenv("DATABASE_URL")
    log_level = "INFO"
```

### Plugin Configuration

```python
# Auto-discovery of routers
app_instance.plugin_manager.discover_plugins("app.api.v1")

# Manual plugin registration
app_instance.plugin_manager.register_plugin("demo_di", demo_router)
```

## 🏥 Health Monitoring

### Health Check Endpoints

- `/health` - Overall system health
- `/ready` - Readiness probe
- `/live` - Liveness probe
- `/demo/health` - DI services health

### Monitoring Integration

```python
# Prometheus metrics (if enabled)
from prometheus_client import Counter, Histogram

# Sentry error tracking (if enabled)
import sentry_sdk

# Structured logging
import structlog
logger = structlog.get_logger()
```

## 🧪 Testing

### Unit Tests

```python
@pytest.fixture
async def di_container():
    container = DIContainer(mock_config)
    # Register test services
    return container

async def test_service_resolution(di_container):
    service = await di_container.get("user_service")
    assert service is not None
```

### Integration Tests

```python
def test_fastapi_integration():
    with TestClient(app) as client:
        response = client.get("/demo/health")
        assert response.status_code == 200
```

## 🔄 Migration from Old System

### Step 1: Gradual Migration

```python
# Keep existing main.py, add new routes
from app.api.v1.demo_di import router as demo_router
app.include_router(demo_router)
```

### Step 2: Update Dependencies

```python
# Replace old dependencies
from app.dependencies_v2 import UserService, CurrentUserId

# Old way
async def endpoint(user_id: str = Depends(get_user_id)):
    pass

# New way
async def endpoint(user_id: CurrentUserId, user_service: UserService):
    pass
```

### Step 3: Full Transition

```python
# Replace main.py with main_v2.py
# Update all routers to use new dependencies
# Test thoroughly before production deployment
```

## 🎨 Benefits

1. **Type Safety**: Full type annotations with mypy support
2. **Testability**: Easy mocking and dependency injection
3. **Maintainability**: Clear separation of concerns
4. **Scalability**: Plugin architecture and service management
5. **Observability**: Built-in health checks and monitoring
6. **Flexibility**: Environment-specific configuration

## 📚 Next Steps

1. **Review**: Study the demo endpoints in `/demo/`
2. **Test**: Run the test script and try the API endpoints
3. **Integrate**: Gradually migrate existing endpoints
4. **Extend**: Add custom services and middleware
5. **Deploy**: Use the production-ready configuration

The new DI system provides a solid foundation for enterprise-grade FastAPI applications with proper dependency management, lifecycle control, and monitoring capabilities.
