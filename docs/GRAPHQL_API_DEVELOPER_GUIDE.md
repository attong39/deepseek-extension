# 📚 GraphQL API Developer Guide

## 🏗️ New Structure Overview

Sau khi migration, GraphQL API đã được tổ chức lại theo domain-driven design với cấu trúc rõ ràng và có thể mở rộng.

### 📁 Directory Structure

```
zeta_vn/app/api/graphql/
├── app.py                       # 🚀 Main GraphQL application setup
├── core/                        # 🏛️ Core infrastructure
│   ├── context.py              # GraphQL execution context
│   ├── middleware.py           # Custom middleware (future)
│   └── types.py                # Base/common types (future)
├── schema/                      # 📋 Schema definitions by domain
│   ├── base.py                 # Root schema composition
│   ├── simple.py               # SDL schema (legacy)
│   ├── agent.py                # Agent domain schema
│   ├── memory.py               # Memory/RAG domain schema
│   └── training.py             # Training domain schema
├── resolvers/                   # 🔧 Resolver implementations
│   ├── base_resolvers.py       # Main resolvers
│   ├── simple_resolvers.py     # Simple resolvers
│   ├── agent_resolvers.py      # Agent-specific resolvers
│   └── optimized_agent_resolvers.py
├── queries/                     # 📥 Query implementations (future)
├── mutations/                   # 📤 Mutation implementations (future)
├── subscriptions/               # 🔄 Real-time subscriptions
│   └── base_subscriptions.py   # WebSocket subscriptions
├── scalars/                     # 🔢 Custom scalar types (future)
└── directives/                  # 🎯 Custom directives (future)
```

## 🚀 Quick Start

### Using the New GraphQL API

```python
# Import the main GraphQL router
from zeta_vn.app.api.graphql import graphql_router

# Add to your FastAPI app
app.include_router(graphql_router, prefix="/api")

# GraphQL endpoint will be available at: /api/graphql
# GraphiQL interface at: /api/graphql (GET request)
```

### Creating New Domain Schemas

```python
# Example: Creating a new "user" domain schema
# File: zeta_vn/app/api/graphql/schema/user.py

import strawberry

@strawberry.type
class UserType:
    id: str
    name: str
    email: str

@strawberry.type
class UserQuery:
    @strawberry.field
    def get_user(self, user_id: str) -> UserType:
        # Implementation here
        return UserType(id=user_id, name="John", email="john@example.com")

@strawberry.type  
class UserMutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str) -> UserType:
        # Implementation here
        return UserType(id="new-id", name=name, email=email)
```

## 📋 Domain Organization

### 🤖 Agent Domain (`schema/agent.py`)
- Agent types and entities
- Agent queries (list, get, search)
- Agent mutations (create, update, delete)
- Agent-specific business logic

### 🧠 Memory Domain (`schema/memory.py`)  
- Memory and knowledge types
- RAG search queries
- Memory ingestion mutations
- Vector operations

### 🎯 Training Domain (`schema/training.py`)
- Training job types
- Model management queries
- Training pipeline mutations
- Progress subscriptions

## 🔧 Development Patterns

### Adding New Queries

```python
# In appropriate domain schema file
@strawberry.type
class YourDomainQuery:
    @strawberry.field
    def your_query(self, param: str) -> YourType:
        """Description of what this query does."""
        # Add authentication/authorization
        # Add input validation
        # Implement business logic
        # Return typed result
        pass
```

### Adding New Mutations

```python
@strawberry.type
class YourDomainMutation:
    @strawberry.mutation
    def your_mutation(self, input_data: YourInputType) -> YourResultType:
        """Description of what this mutation does."""
        # Add authentication/authorization
        # Validate input
        # Perform operation
        # Return result
        pass
```

### Adding Subscriptions

```python
# In subscriptions/your_domain_subscriptions.py
@strawberry.type
class YourDomainSubscription:
    @strawberry.subscription
    async def your_subscription(self) -> AsyncGenerator[YourType, None]:
        """Real-time updates for your domain."""
        # Implement subscription logic
        yield your_data
```

## 🔒 Security & Authentication

### Context-Based Auth

```python
# Use GraphQLContext for authentication
from zeta_vn.app.api.graphql.core.context import GraphQLContext

@strawberry.field
def protected_query(self, info: strawberry.Info) -> str:
    context: GraphQLContext = info.context
    
    # Check authentication
    if not context.security_context.user_id:
        raise strawberry.exceptions.GraphQLError("Authentication required")
    
    # Check permissions
    if not context.security_context.has_permission("read:data"):
        raise strawberry.exceptions.GraphQLError("Insufficient permissions")
    
    return "Protected data"
```

## 📈 Performance Best Practices

### 1. Use DataLoaders
```python
# Avoid N+1 queries with DataLoader pattern
@strawberry.field
async def related_data(self) -> List[RelatedType]:
    # Use batch loading
    pass
```

### 2. Implement Field-Level Caching
```python
# Add caching directives (future feature)
@strawberry.field
@cache(ttl=300)  # Cache for 5 minutes
def expensive_computation(self) -> ComplexType:
    pass
```

### 3. Limit Query Depth
```python
# Configure query complexity analysis
# Will be implemented in core/middleware.py
```

## 🧪 Testing Strategy

### Schema Testing
```python
# Test schema definitions
def test_user_schema():
    query = "{ getUser(userId: \"123\") { id name email } }"
    result = execute_query(query)
    assert result.data["getUser"]["id"] == "123"
```

### Resolver Testing
```python
# Test resolver logic independently
def test_user_resolver():
    resolver = UserQuery()
    result = resolver.get_user("123")
    assert result.id == "123"
```

## 🚢 Migration Guide

### For Existing Code

1. **Update Imports**:
   ```python
   # Old
   from zeta_vn.app.api.graphql.resolvers import some_resolver
   
   # New
   from zeta_vn.app.api.graphql.resolvers.base_resolvers import some_resolver
   ```

2. **Use New Schema Structure**:
   ```python
   # Old - everything in one file
   from zeta_vn.app.api.graphql.schema import AgentType
   
   # New - domain-specific
   from zeta_vn.app.api.graphql.schema.agent import AgentType
   ```

3. **Leverage New Context**:
   ```python
   # Use the new GraphQLContext for better type safety
   from zeta_vn.app.api.graphql.core.context import GraphQLContext
   ```

## 🎯 Future Enhancements

### Planned Features
- [ ] Custom scalar types (DateTime, UUID, JSON)
- [ ] Authentication directives (`@auth`, `@require_permission`)
- [ ] Caching directives (`@cache`, `@cache_key`)
- [ ] Rate limiting directives (`@rate_limit`)
- [ ] Query complexity analysis
- [ ] Automatic pagination
- [ ] Field-level subscriptions
- [ ] GraphQL Federation support

### Architecture Goals
- [ ] Complete domain separation
- [ ] Middleware pipeline
- [ ] Plugin architecture
- [ ] Performance monitoring
- [ ] Error tracking
- [ ] Schema versioning

## 📞 Support

### Getting Help
1. Check this guide first
2. Look at existing domain implementations
3. Check the migration report: `GRAPHQL_MIGRATION_REPORT.md`
4. Review GraphQL best practices
5. Ask team members familiar with the new structure

### Common Issues
- **Import errors**: Check new import paths
- **Schema conflicts**: Ensure proper domain separation
- **Context issues**: Use new GraphQLContext
- **Type errors**: Check strawberry decorators

This new structure provides a solid foundation for scalable GraphQL API development! 🚀