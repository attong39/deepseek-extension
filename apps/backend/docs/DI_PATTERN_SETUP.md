# DI Pattern & RBAC Setup - ZETA AI Server

## Tổng quan

Hệ thống ZETA AI Server đã được chuẩn hóa theo **Dependency Injection (DI) Pattern** với **RBAC (Role-Based Access Control)** và **Audit Trail** tự động. Tài liệu này hướng dẫn cách scaffold endpoints mới và tích hợp với hệ thống hiện tại.

## 🏗️ Kiến trúc DI Pattern

### 1. Dependency Factory Structure

```
app/dependencies.py
├── get_db_session()              # Database session
├── get_current_user()            # Authentication
├── require_permissions(*scopes)  # RBAC enforcement
├── get_audit_context()           # Audit context
├── get_*_repository()            # Repository factories
├── get_*_uc()                    # Use Case factories
└── get_*_service()               # Service factories
```

### 2. Endpoint Pattern (Thin Controllers)

```python
# Mẫu endpoint chuẩn
@router.post(
    "",
    response_model=EntityOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("entity:create"))],
)
async def create_entity(
    payload: EntityCreateIn,
    use_case: CreateEntityUC,                           # Injected Use Case
    current_user: User = Depends(get_current_user),    # Auth context
    audit_context: AuditContextDep = Depends(),        # Audit context
) -> EntityOut:
    """Endpoint mỏng - chỉ parse input và gọi use case."""
    try:
        # 1. Convert input to value object
        entity_vo = payload.to_vo()
        entity_vo["owner_id"] = current_user.id

        # 2. Execute use case
        entity = await use_case.execute(entity_vo, audit_context)

        # 3. Return serialized response
        return EntityOut.from_entity(entity)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
```

## 🔐 RBAC & Security

### Permission Scopes

```python
# Standard permission format: "resource:action"
PERMISSIONS = {
    # Agent permissions
    "agent:create",    "agent:read",    "agent:update",    "agent:delete",    "agent:manage",

    # Chat permissions
    "chat:create",     "chat:read",     "chat:update",     "chat:delete",     "chat:moderate",

    # Plan permissions
    "plan:create",     "plan:read",     "plan:update",     "plan:delete",
    "plan:approve",    "plan:execute",

    # Workflow permissions
    "workflow:create", "workflow:read", "workflow:update", "workflow:delete",
    "workflow:execute", "workflow:manage",

    # Memory permissions
    "memory:create",   "memory:read",   "memory:update",   "memory:delete",   "memory:search",

    # Admin permissions
    "admin:users",     "admin:agents",  "admin:analytics", "admin:audit",     "admin:config",
}
```

### Role Definitions

```python
ROLES = {
    "user": [
        "agent:create", "agent:read", "agent:update", "agent:delete",
        "chat:create", "chat:read", "chat:update", "chat:delete",
        "plan:create", "plan:read", "plan:update", "plan:approve",
        "memory:create", "memory:read", "memory:update", "memory:delete", "memory:search",
    ],
    "premium": [
        "*user*",  # All user permissions plus:
        "workflow:create", "workflow:read", "workflow:execute",
        "plan:execute",
    ],
    "admin": [
        "*",  # All permissions
    ],
}
```

### Security Dependencies

```python
# Basic auth
current_user: User = Depends(get_current_user)

# Permission-based access
dependencies=[Depends(require_permissions("agent:create"))]

# Admin-only access
admin_user: User = Depends(require_admin)

# Resource ownership
dependencies=[Depends(require_agent_owner(agent_id))]
```

## 📊 Audit Trail

### Automatic Audit Logging

Mọi hành động quan trọng được tự động ghi audit:

```python
# Audit được trigger tự động trong use cases
audit_service.log_action(
    actor_id=current_user.id,
    action="agent_create",          # Action type
    resource_type="agent",          # Resource affected
    resource_id=agent.id,           # Resource ID
    context=audit_context,          # Request context (IP, UA, etc.)
    before_state={},                # State before change
    after_state=agent.to_dict(),    # State after change
)
```

### Audit Actions

```python
AUDIT_ACTIONS = {
    # User actions
    "login", "logout", "failed_login", "password_change", "profile_update",

    # Entity actions
    "agent_create", "agent_update", "agent_delete", "agent_enable", "agent_disable",
    "chat_create", "chat_update", "chat_delete", "message_send",
    "plan_create", "plan_approve", "plan_execute", "plan_step_add",
    "workflow_create", "workflow_activate", "workflow_pause",
    "memory_create", "memory_update", "memory_delete", "memory_access",

    # Admin actions
    "permission_change", "role_change", "access_grant", "access_revoke",
    "system_config", "data_export", "data_import",
}
```

## 🚀 Scaffold New Endpoint

### Step 1: Create Serializers

```python
# app/serializers/entity.py
from pydantic import BaseModel, Field

class EntityCreateIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field("", max_length=500)

    def to_vo(self) -> dict:
        return {"name": self.name, "description": self.description}

class EntityOut(BaseModel):
    id: str
    name: str
    description: str
    owner_id: str
    created_at: str

    @classmethod
    def from_entity(cls, entity) -> EntityOut:
        return cls(
            id=str(entity.id),
            name=entity.name,
            description=entity.description,
            owner_id=str(entity.owner_id),
            created_at=entity.created_at.isoformat(),
        )
```

### Step 2: Add Use Case Factory

```python
# app/dependencies.py
def get_create_entity_uc(
    entity_repo: EntityRepository = Depends(get_entity_repository),
    session: AsyncSession = Depends(get_db_session),
) -> object:
    from core.use_cases.entity.create_entity import CreateEntityUseCase
    return CreateEntityUseCase(entity_repo=entity_repo, session=session)

# Type alias
CreateEntityUC = Annotated[object, Depends(get_create_entity_uc)]
```

### Step 3: Create Endpoint

```python
# app/api/v1/endpoints/entities.py
@router.post(
    "",
    response_model=EntityOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions("entity:create"))],
)
async def create_entity(
    payload: EntityCreateIn,
    use_case: CreateEntityUC,
    current_user: User = Depends(get_current_user),
    audit_context: AuditContextDep = Depends(),
) -> EntityOut:
    try:
        entity_vo = payload.to_vo()
        entity_vo["owner_id"] = current_user.id
        entity = await use_case.execute(entity_vo, audit_context)
        return EntityOut.from_entity(entity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
```

### Step 4: Register Router

```python
# app/api/v1/router.py
from .endpoints import entities

api_router.include_router(entities.router)
```

## 📝 Use Case Implementation

### Standard Use Case Structure

```python
# core/use_cases/entity/create_entity.py
from dataclasses import dataclass
from typing import Any

@dataclass
class CreateEntityUseCase:
    entity_repo: EntityRepository
    session: AsyncSession

    async def execute(self, entity_data: dict[str, Any], audit_context: dict) -> Entity:
        # 1. Validate business rules
        self._validate_input(entity_data)

        # 2. Create domain entity
        entity = Entity(**entity_data)

        # 3. Persist via repository
        saved_entity = await self.entity_repo.create(entity)

        # 4. Log audit
        await self._log_audit(saved_entity, audit_context)

        # 5. Process domain events
        await self._process_events(saved_entity)

        return saved_entity

    def _validate_input(self, data: dict) -> None:
        # Business validation logic
        pass

    async def _log_audit(self, entity: Entity, context: dict) -> None:
        # Audit logging
        pass

    async def _process_events(self, entity: Entity) -> None:
        # Domain event processing
        pass
```

## 🔄 Repository Pattern

### Repository Protocol

```python
# core/interfaces/repository_protocols.py
from typing import Protocol

class EntityRepository(Protocol):
    async def create(self, entity: Entity) -> Entity: ...
    async def get_by_id(self, entity_id: str) -> Entity | None: ...
    async def update(self, entity: Entity) -> Entity: ...
    async def delete(self, entity_id: str) -> bool: ...
    async def list_by_owner(self, owner_id: str, skip: int = 0, limit: int = 100) -> list[Entity]: ...
```

### Repository Implementation

```python
# data/repositories/entity_repository.py
class EntityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: Entity) -> Entity:
        db_entity = EntityModel.from_domain(entity)
        self.session.add(db_entity)
        await self.session.commit()
        await self.session.refresh(db_entity)
        return db_entity.to_domain()
```

## 🛡️ Rate Limiting & Monitoring

### Redis Rate Limiting

```python
# For sensitive endpoints
@router.post("/sensitive-action", dependencies=[
    Depends(require_permissions("admin:critical")),
    Depends(rate_limit(calls=5, period=60)),  # 5 calls per minute
])
async def sensitive_action(...): ...
```

### Health & Metrics Endpoints

```python
# app/api/v1/endpoints/monitoring.py
@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@router.get("/metrics")
async def prometheus_metrics() -> Response:
    # Return Prometheus format metrics
    pass
```

## 🔧 Development Guidelines

### 1. Entity First
- Tạo Domain Entity trước
- Định nghĩa business rules và invariants
- Implement domain events

### 2. Repository Protocol
- Define interface trong `core/interfaces/`
- Implement trong `data/repositories/`

### 3. Use Cases
- Implement business logic trong `core/use_cases/`
- Inject dependencies via constructor
- Handle domain events

### 4. Endpoints
- Thin controllers - chỉ parse và delegate
- Use DI pattern cho tất cả dependencies
- Implement proper error handling

### 5. Security
- Luôn check permissions
- Log audit cho sensitive actions
- Validate input với Pydantic

### 6. Testing
- Unit test cho entities và use cases
- Integration test cho repositories
- E2E test cho endpoints

## 📋 Checklist Scaffold Endpoint

- [ ] Domain Entity created và tested
- [ ] Repository Protocol defined
- [ ] Repository Implementation created
- [ ] Use Case implemented
- [ ] Serializers created (Input/Output schemas)
- [ ] Use Case Factory added to dependencies.py
- [ ] Endpoint implemented với RBAC
- [ ] Router registered
- [ ] Permissions added to RBAC matrix
- [ ] Audit actions defined
- [ ] Tests written
- [ ] Documentation updated

## 🎯 Advanced Features

### WebSocket Support
```python
# app/websockets/entity_events.py
@websocket_router.websocket("/entities/{entity_id}/events")
async def entity_events_ws(websocket: WebSocket, entity_id: str):
    # Real-time updates
    pass
```

### Background Tasks
```python
# app/worker/tasks.py
@celery_app.task
def process_entity_async(entity_id: str):
    # Background processing
    pass
```

### Caching
```python
# Redis caching for expensive operations
@cached(ttl=300)  # 5 minutes
async def get_entity_stats(entity_id: str) -> dict:
    pass
```

---

**Kết luận**: Pattern này đảm bảo endpoint mỏng, separation of concerns, automatic audit, RBAC enforcement, và maintainability cao. Mọi endpoint mới chỉ cần follow pattern này để có đầy đủ tính năng security và compliance.
