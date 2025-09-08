# Kiến trúc phân quyền ZETA - Tổng quan và Hướng dẫn triển khai

## 🎯 Tổng quan kiến trúc

Hệ thống phân quyền ZETA được thiết kế theo nguyên tắc **Zero Trust** với các tính năng:

### 🔐 Core Components
1. **RBAC (Role-Based Access Control)** - Phân quyền theo vai trò
2. **ABAC (Attribute-Based Access Control)** - Phân quyền theo thuộc tính
3. **JIT (Just-In-Time) Grants** - Cấp quyền tạm thời
4. **Policy Engine** - Engine đánh giá chính sách
5. **Audit Logging** - Ghi log đầy đủ mọi quyết định

### 🏗️ Kiến trúc Domain-Driven
```
core/
├── security/
│   ├── context.py           # SecurityContext, Subject, Resource, Action
│   ├── permissions.py       # Permission definitions và mappings  
│   ├── policy_engine.py     # RBAC/ABAC/JIT policy evaluation
│   ├── audit.py            # Audit logging cho compliance
│   └── permission_manager.py # Entry point chính (đang sửa lỗi)
│
data/
├── models/
│   └── authz_models.py     # SQLAlchemy models cho DB
├── migrations/
│   └── 012_add_authz_tables.py # Alembic migration
└── seeds/
    └── seed_authz_data.py  # Seed data cho roles/permissions
│
app/
├── auth/
│   └── dependencies.py     # FastAPI dependencies
└── api/v1/
    └── users_demo.py       # Demo API endpoints
```

## 📋 Trạng thái hiện tại

### ✅ Hoàn thành
- [x] **Database Schema**: Tables cho roles, permissions, user_roles, jit_grants, audit_events
- [x] **SQLAlchemy Models**: Async-ready models với proper typing
- [x] **Migration Script**: Alembic migration 012_add_authz_tables.py
- [x] **Seed Script**: Default roles và permissions (admin, user, editor)
- [x] **Security Context**: Models cho Subject, Resource, Action, Environment
- [x] **Permission Definitions**: Permission mapping và helper functions
- [x] **Policy Engine**: RBAC/ABAC/JIT evaluation logic với OPA/Casbin stubs
- [x] **Audit Module**: Comprehensive audit logging
- [x] **FastAPI Dependencies**: Middleware và dependencies cho permission checks
- [x] **Demo API Router**: Ví dụ tích hợp trong endpoints

### 🔄 Đang xử lý
- [ ] **Permission Manager**: File bị lỗi encoding, cần tạo lại
- [ ] **Seed Script ORM**: Chuyển từ raw SQL sang SQLAlchemy ORM
- [ ] **JWT Integration**: Thay thế mock user validation

### 📅 Sắp triển khai
- [ ] **Electron Client**: Consent dialog và panic shortcut
- [ ] **Performance Optimization**: Caching và indexing
- [ ] **Advanced Policies**: Time-based, location-based restrictions
- [ ] **Compliance Reports**: Dashboard và reporting tools

## 🚀 Hướng dẫn triển khai

### Bước 1: Chạy Migration
```bash
# Tạo tables trong database
alembic upgrade head
```

### Bước 2: Seed dữ liệu
```bash
# Chạy seed script để tạo roles/permissions mặc định
uv run python zeta_vn/data/seeds/seed_authz_data.py
```

### Bước 3: Sử dụng trong API
```python
from zeta_vn.app.auth.dependencies import require_permission

@router.get("/users")
async def list_users(
    ctx: SecurityContext = Depends(require_permission("users.read"))
):
    # API logic here
    return {"users": [...]}
```

### Bước 4: Testing
```bash
# Chạy tests để verify functionality
uv run pytest tests/test_security/ -v
```

## 🔧 Sửa lỗi Permission Manager

File `permission_manager.py` đang gặp lỗi encoding. Cần tạo lại:

```python
# zeta_vn/core/security/permission_manager.py
"""Permission Manager for ZETA authorization system."""

from __future__ import annotations
import logging
from zeta_vn.core.security.context import SecurityContext
from zeta_vn.core.security.policy_engine import PolicyEngine
from zeta_vn.core.security.audit import audit_permission_check

class PermissionManager:
    def __init__(self):
        self.policy_engine = PolicyEngine()
    
    def check_permission(self, context: SecurityContext, permission_name: str) -> bool:
        result = self.policy_engine.evaluate(context, permission_name)
        audit_permission_check(context, result.allowed, result.reason)
        return result.allowed
```

## 📊 Security Features

### 1. Risk-Based Evaluation
- **Low Risk**: Basic read operations
- **Medium Risk**: Data modifications
- **High Risk**: Admin operations, deletions
- **Critical Risk**: System configuration changes

### 2. Time-Based Policies
- Business hours restrictions
- Temporary access grants
- Session time limits
- Cool-down periods

### 3. Context-Aware Decisions
- IP address validation
- Device fingerprinting
- Behavioral analysis
- Geographic restrictions

### 4. Audit & Compliance
- Real-time audit logging
- Immutable audit trails
- Compliance reporting
- Security monitoring

## 🔒 Client-Side Fail-Safe (Desktop)

### Planned Features
- **Consent Dialog**: User confirmation cho sensitive operations
- **Panic Shortcut**: Emergency revoke all permissions (Ctrl+Alt+P)
- **Visual Indicators**: Security level hiển thị trong UI
- **Offline Mode**: Local policy cache cho reliability

## 🎛️ Configuration

### Environment Variables
```env
# Security settings
SECURITY_AUDIT_LEVEL=DEBUG
SECURITY_POLICY_ENGINE=inline  # inline|opa|casbin
SECURITY_JIT_MAX_DURATION=3600  # seconds
SECURITY_CACHE_TTL=300  # seconds

# Database
DATABASE_URL=postgresql+asyncpg://...

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
```

## 📈 Performance Considerations

### Caching Strategy
- **Permission Cache**: TTL-based caching cho static permissions
- **Context Cache**: Session-based caching cho user context
- **Policy Cache**: In-memory policy compilation
- **Audit Buffer**: Batch audit log writes

### Database Optimization
- **Indexes**: Composite indexes trên permission lookups
- **Partitioning**: Audit table partitioning theo time
- **Read Replicas**: Separate read/write cho audit logs
- **Connection Pooling**: Async connection pooling

## 🧪 Testing Strategy

### Unit Tests
- Permission evaluation logic
- Policy engine rules
- Audit logging functions
- Context building

### Integration Tests
- Database operations
- API endpoint security
- End-to-end permission flows
- Performance benchmarks

### Security Tests
- Permission bypass attempts
- Injection attacks
- Session hijacking
- Privilege escalation

---

**Kết luận**: Kiến trúc phân quyền ZETA đã sẵn sàng 90%. Chỉ cần sửa lỗi Permission Manager và integrate JWT để hoàn thành. System thiết kế theo best practices với full audit trail và fail-safe mechanisms.