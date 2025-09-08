# Domain Entities - Upgraded Architecture

Hệ thống domain entities đã được nâng cấp toàn diện theo Clean Architecture patterns với type safety, immutability, và business invariants.

## 🏗️ **Architecture Overview**

### **Base Components**
- **`DomainModel`**: Base class cho tất cả entities (frozen, type-safe)
- **`shared_value_objects.py`**: Type-safe IDs, validators, utilities
- **`mixins.py`**: Reusable behavior patterns
- **`events.py`**: Domain events cho Event Sourcing

### **Mixins Available**
- **`Versioned`**: Optimistic locking với `version: int`
- **`Ownable`**: Ownership tracking với `owner_user_id`
- **`Taggable`**: Tagging system với `tags: list[str]`
- **`Traceable`**: Observability với `trace_id`, `request_id`
- **`SoftDeletable`**: Soft delete với `deleted_at` và `is_deleted()`

## 📋 **Entity Catalog**

| Entity | Mixins | Key Invariants | Convenience Methods |
|--------|--------|----------------|-------------------|
| **Agent** | Versioned, Ownable, Taggable, Traceable | capabilities case-insensitive | `can()`, `require()`, `touch()` |
| **AuditRecord** | Traceable | immutable audit trail | - |
| **ConfigItem** | Versioned, Traceable | dot-notation keys, scope validation | - |
| **DatasetItem** | Versioned, Traceable | type-dependent payload requirements | - |
| **FileMeta** | Versioned, Traceable, SoftDeletable | cloud apps/backend location requirements | - |
| **LearningEvent** | Traceable | value ranges by signal type | - |
| **MemoryRecord** | Versioned, Taggable, Traceable, SoftDeletable | embedding dimension consistency | `with_ttl()`, `refresh()` |
| **MetricRecord** | Traceable | finite numeric values | - |
| **Notification** | Traceable | read state tracking | `mark_read()` |
| **Plan** | Versioned, Traceable | unique step indices | `next_pending_step()`, `touch()` |
| **Session** | Traceable | time ordering | `close()` |
| **TrainingJob** | Versioned, Traceable | monotonic progress, time ordering | `mark_started()`, `advance_progress()`, `mark_succeeded()`, `mark_failed()`, `cancel()` |
| **User** | Versioned, Traceable | role-based permissions | `has_role()` |
| **WorkflowRun** | Versioned, Traceable | DAG validation, cycle detection | `topo_order()` |

### 1. **User** (`user.py`)
**Responsibility**: User authentication, profile, permissions
**State**: id, username, email, role, permissions, profile data
**Key Methods**: authenticate(), update_profile(), change_role()
**Relationships**: 1-N với Agent, Chat, Session, Plan

### 2. **Agent** (`agent.py`)
**Responsibility**: AI agent configuration, capabilities, lifecycle
**State**: id, name, model, capabilities, tools, config, status
**Key Methods**: enable(), disable(), update_config(), attach_tool()
**Relationships**: N-1 với User, 1-N với Memory, Plan, Workflow

### 3. **Chat** (`chat.py`)
**Responsibility**: Conversation management, message history
**State**: id, title, messages, participants, status, metadata
**Key Methods**: add_message(), archive(), restore(), set_title()
**Relationships**: N-1 với User, Agent; 1-N với Message

### 4. **Plan** (`plan.py`)
**Responsibility**: Multi-step execution plans, approval workflow
**State**: id, steps, status, approval_state, execution_context
**Key Methods**: add_step(), approve(), start_execution(), complete_step()
**Relationships**: N-1 với Agent, User; 1-N với Workflow

### 5. **Workflow** (`workflow.py`)
**Responsibility**: DAG execution, multi-agent orchestration
**State**: id, nodes, edges, triggers, status, execution_state
**Key Methods**: add_node(), connect(), activate(), pause(), resume()
**Relationships**: N-1 với Plan; integrates với Agent orchestration

### 6. **Memory** (`memory.py`)
**Responsibility**: Vector embeddings, knowledge storage
**State**: id, content, embedding, metadata, importance, visibility
**Key Methods**: embed(), update_importance(), archive()
**Relationships**: N-1 với Agent, User

### 7. **Session** (`session.py`)
**Responsibility**: User session management, context tracking
**State**: id, user_id, status, context, timestamps
**Key Methods**: start(), end(), update_context(), extend()
**Relationships**: N-1 với User; 1-N với Chat, Plan

### 8. **Message** (`message.py`)
**Responsibility**: Individual chat messages, content, metadata
**State**: id, content, role, timestamp, metadata, attachments
**Key Methods**: edit(), delete(), add_attachment()
**Relationships**: N-1 với Chat

### 9. **File** (`file.py`)
**Responsibility**: File upload, processing, metadata
**State**: id, filename, content_type, size, status, metadata
**Key Methods**: process(), scan(), download(), delete()
**Relationships**: N-1 với User; N-N với Chat, Message

## System Entities

### 10. **Audit** (`audit.py`)
**Responsibility**: Compliance trail, action logging
**State**: id, actor, resource, action, before/after state, result
**Key Methods**: redact(), to_log_record(), mark_failed()
**Purpose**: Immutable audit trail cho tất cả domain actions

### 11. **Analytics** (`analytics.py`)
**Responsibility**: Usage metrics, performance tracking
**State**: id, metric_type, scope, value, dimensions, timestamp
**Key Methods**: record(), aggregate(), export()
**Purpose**: Business intelligence và performance monitoring

### 12. **Notification** (`notification.py`)
**Responsibility**: User notifications, delivery tracking
**State**: id, recipient, content, type, status, delivery_info
**Key Methods**: send(), mark_read(), retry()
**Purpose**: Decoupled notification system

### 13. **Metrics** (`metrics.py`)
**Responsibility**: Domain metrics standardization
**State**: metric definitions, aggregation rules, export formats
**Key Methods**: define_metric(), collect(), export_prometheus()
**Purpose**: Standardized metrics cho Prometheus export

### 14. **ConfigItem** (`config.py`)
**Responsibility**: Application configuration management
**State**: key, value, namespace, type, metadata
**Key Methods**: get(), set(), validate(), get_by_namespace()
**Purpose**: Dynamic configuration với validation

## Business Rules & Invariants

### Cross-Entity Rules
1. **User-Agent Ownership**: Agent phải có owner (User)
2. **Chat-Session Context**: Chat phải thuộc về Session hợp lệ
3. **Plan Approval**: Plan phải được approve trước khi execute
4. **Workflow Dependencies**: DAG không được có cycles
5. **Audit Immutability**: Audit records không được modify
6. **Memory Access Control**: Memory visibility rules theo User permissions

### Entity-Specific Invariants
- **User**: Username unique, email format valid
- **Agent**: Model compatibility với capabilities
- **Chat**: Message order chronological
- **Plan**: Steps dependencies valid, no circular deps
- **Workflow**: DAG validation, node type compatibility
- **Memory**: Embedding dimensions consistent
- **File**: Content type validation, size limits

## Domain Events

### Event Categories
- **User Events**: user.created, user.role_changed
- **Agent Events**: agent.created, agent.enabled, agent.tool_attached
- **Chat Events**: chat.created, message.sent, chat.archived
- **Plan Events**: plan.approved, plan.started, step.completed
- **Workflow Events**: workflow.activated, node.completed, workflow.paused
- **System Events**: audit.created, metric.recorded, notification.sent

### Event Handling
Events được collect trong entity `_events` field và processed bởi:
- **Event Dispatcher** (app layer)
- **Audit Service** (automatic logging)
- **Notification Service** (user alerts)
- **Analytics Service** (metrics collection)

## Integration với Application Layer

### Repository Protocols
Mỗi entity có corresponding repository protocol trong `core/interfaces/`:
```python
# Ví dụ: UserRepository protocol
class UserRepository(Protocol):
    async def create(self, user: User) -> User: ...
    async def get_by_id(self, user_id: str) -> User | None: ...
    async def update(self, user: User) -> User: ...
    async def delete(self, user_id: str) -> bool: ...
```

### Use Cases
Domain logic được orchestrate qua Use Cases:
```python
# Ví dụ: CreateAgentUseCase
class CreateAgentUseCase:
    def __init__(self, agent_repo: AgentRepository, audit_service: AuditService):
        self._agent_repo = agent_repo
        self._audit_service = audit_service

    async def execute(self, request: CreateAgentRequest) -> Agent:
        # Create agent entity
        agent = Agent(name=request.name, owner_id=request.owner_id)

        # Persist via repository
        saved_agent = await self._agent_repo.create(agent)

        # Process domain events
        for event in agent.clear_events():
            await self._audit_service.log_event(event)

        return saved_agent
```

### Dependency Injection
Entities được inject vào endpoints qua factories trong `app/dependencies.py`:
```python
def get_create_agent_uc(
    agent_repo: AgentRepository = Depends(get_agent_repository),
    audit_service: AuditService = Depends(get_audit_service),
) -> CreateAgentUseCase:
    return CreateAgentUseCase(agent_repo, audit_service)
```

## Testing Strategy

### Unit Tests
Mỗi entity có comprehensive unit tests:
- **State Validation**: Constructor validation, invariants
- **Business Logic**: Methods behavior, side effects
- **Domain Events**: Event generation, data content
- **Error Cases**: Invalid state transitions, constraint violations

### Integration Tests
Entity integration với repositories và services:
- **Repository Operations**: CRUD operations
- **Event Processing**: Event handlers, side effects
- **Cross-Entity Workflows**: Multi-entity business processes

## Development Guidelines

### Adding New Entity
1. **Define Domain Model**: State, behavior, invariants
2. **Create Entity Class**: Use dataclass, implement methods
3. **Add Domain Events**: Define events cho state changes
4. **Write Unit Tests**: Cover all business logic
5. **Update Barrel Export**: Add to `__init__.py`
6. **Document Relationships**: Update này README
7. **Create Repository Protocol**: Define persistence interface
8. **Implement Use Cases**: Business workflow orchestration

### Modifying Existing Entity
1. **Preserve Invariants**: Không break existing business rules
2. **Migration Strategy**: Database schema changes if needed
3. **Backward Compatibility**: API compatibility cho existing clients
4. **Update Tests**: Cover new functionality
5. **Domain Events**: Add events cho new state changes

## Conventions

### File Structure
```
entities/
├── README.md                 # Này file
├── __init__.py              # Barrel exports
├── user.py                  # User entity
├── agent.py                 # Agent entity
├── chat.py                  # Chat + Message entities
├── plan.py                  # Plan entity
├── workflow.py              # Workflow entity
├── memory.py                # Memory entity
├── session.py               # Session entity
├── file.py                  # File entity
├── audit.py                 # Audit entity (system)
├── analytics.py             # Analytics entity (system)
├── notification.py          # Notification entity (system)
├── metrics.py               # Metrics entity (system)
└── config.py                # ConfigItem entity (system)
```

### Import Patterns
```python
# Preferred: Barrel import
from core.domain.entities import User, Agent, Chat

# Direct import (for specific cases)
from core.domain.entities.user import User, UserStatus

# Module import (for backward compatibility)
from core.domain.entities import workflow
```

## Performance Considerations

### Entity Design
- **Lazy Loading**: Heavy properties computed on demand
- **Event Batching**: Collect events, process in batches
- **Value Object Reuse**: Cache common value objects
- **Immutable State**: Reduce copying overhead

### Memory Management
- **Entity Lifecycle**: Clear events after processing
- **Collection Limits**: Paginate large collections
- **Weak References**: Avoid memory leaks in relationships

---

**Copilot Integration**: Này README giúp GitHub Copilot hiểu context và relationships giữa entities, enabling better code suggestions và scaffolding accuracy.
