# HƯỚNG DẪN MIGRATION ZETA_VN → ZETA_VN_RESTRUCTURED

## 📋 Tổng quan
Đây là hướng dẫn chi tiết để di chuyển từ cấu trúc cũ `zeta_vn` sang cấu trúc mới `zeta_vn_restructured` theo Clean Architecture.

## 🏗️ Cấu trúc mới đã tạo

### 1. Application Layer (`app/`)
```
app/
├── api/                 # API Routes & Endpoints
│   ├── v1/endpoints/   # API v1
│   └── v2/endpoints/   # API v2
├── auth/               # Authentication & Authorization
├── config/             # App configuration
├── controllers/        # Request controllers
├── dependencies/       # FastAPI dependencies
├── exceptions/         # Custom exceptions
├── middleware/         # Custom middleware
├── models/             # Pydantic models
├── schemas/            # Request/Response schemas
├── services/           # Application services
└── utils/              # App utilities
```

### 2. Core Domain Layer (`core/`)
```
core/
├── ai/                 # AI-specific domain logic
├── application/        # Application Use Cases
├── domain/             # Domain Layer
└── infrastructure/     # Infrastructure Layer
```

### 3. Supporting Directories
```
tests/                  # Test Suite
docs/                   # Documentation
scripts/                # Utility scripts
deployment/             # Deployment configurations
monitoring/             # Monitoring
```

## 🚀 Kế hoạch Migration

### Phase 1: Core Domain Migration
1. **Domain Entities**
   - `zeta_vn/core/domain/` → `zeta_vn_restructured/core/domain/entities/`
   - `zeta_vn/core/value_objects/` → `zeta_vn_restructured/core/domain/value_objects/`

2. **Use Cases**
   - `zeta_vn/core/use_cases/` → `zeta_vn_restructured/core/application/use_cases/`

3. **Interfaces**
   - `zeta_vn/core/interfaces/` → `zeta_vn_restructured/core/application/interfaces/`

### Phase 2: Infrastructure Migration
1. **Repositories**
   - `zeta_vn/core/implementations/` → `zeta_vn_restructured/core/infrastructure/repositories/`

2. **Database**
   - `zeta_vn/storage/` → `zeta_vn_restructured/core/infrastructure/database/`

3. **External Services**
   - `zeta_vn/core/llm/` → `zeta_vn_restructured/core/ai/llm/`
   - External APIs → `zeta_vn_restructured/core/infrastructure/external/`

### Phase 3: Application Layer Migration
1. **API Routes**
   - `zeta_vn/app/api/` → `zeta_vn_restructured/app/api/`

2. **Auth System**
   - `zeta_vn/app/auth/` → `zeta_vn_restructured/app/auth/`

3. **Services**
   - `zeta_vn/app/services/` → `zeta_vn_restructured/app/services/`

## 📋 Checklist Migration

### ✅ Đã hoàn thành
- [x] Tạo cấu trúc thư mục đầy đủ
- [x] Thiết lập Clean Architecture layers
- [x] Tạo các thư mục con chi tiết

### 🔄 Cần thực hiện
- [ ] Di chuyển Domain Entities
- [ ] Di chuyển Value Objects
- [ ] Di chuyển Use Cases
- [ ] Di chuyển Repository Interfaces
- [ ] Di chuyển Repository Implementations
- [ ] Di chuyển API Routes
- [ ] Di chuyển Auth System
- [ ] Di chuyển Services
- [ ] Cập nhật imports
- [ ] Viết tests cho cấu trúc mới
- [ ] Cập nhật documentation

## 🎯 Lợi ích của cấu trúc mới

1. **Clean Architecture**
   - Tách biệt rõ ràng giữa business logic và infrastructure
   - Dependency Inversion principle

2. **Domain-Driven Design**
   - Domain entities và business rules ở trung tâm
   - Value objects được tổ chức rõ ràng

3. **Scalability**
   - Dễ dàng thêm features mới
   - API versioning hỗ trợ

4. **Testability**
   - Unit tests, Integration tests, E2E tests tách biệt
   - Mock dependencies dễ dàng

5. **Maintainability**
   - Code organization rõ ràng
   - Single Responsibility Principle

## 🚨 Lưu ý quan trọng

1. **Dependencies Direction**
   - Core không phụ thuộc vào App layer
   - Infrastructure implement interfaces từ Core
   - App layer sử dụng Core thông qua interfaces

2. **Import Rules**
   ```python
   # ✅ Đúng
   from zeta_vn_restructured.core.domain.entities import User
   from zeta_vn_restructured.core.application.interfaces import UserRepository
   
   # ❌ Sai - Core không được import App
   # from zeta_vn_restructured.app.services import SomeService
   ```

3. **Testing Strategy**
   - Unit tests: Test domain logic isolated
   - Integration tests: Test with real infrastructure
   - E2E tests: Test complete user flows

## 📞 Tiếp theo

Sau khi hoàn thành cấu trúc thư mục, chúng ta có thể:
1. Bắt đầu migrate từng module một cách có hệ thống
2. Thiết lập CI/CD cho cấu trúc mới
3. Viết documentation chi tiết cho từng layer

Cấu trúc đã sẵn sàng! 🎉