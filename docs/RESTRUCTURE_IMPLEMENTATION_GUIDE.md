# 🏗️ HƯỚNG DẪN TÁI CẤU TRÚC DỰ ÁN ZETA AI - 2025

## 📋 Tổng quan

Tài liệu này hướng dẫn chi tiết cách tái cấu trúc toàn bộ dự án ZETA AI theo mô hình **Clean Architecture** và **Monorepo** hiện đại.

## 🎯 Mục tiêu tái cấu trúc

### 1. **Tách biệt rõ ràng các layer**


- **Domain Layer**: Logic nghiệp vụ thuần túy
- **Application Layer**: Use cases và orchestration
- **Infrastructure Layer**: External services, DB, APIs
- **Presentation Layer**: Controllers, DTOs, validation


### 2. **Monorepo tối ưu**

- **apps/**: Các ứng dụng độc lập (API server, apps/desktop, web)
- **packages/**: Shared packages có thể tái sử dụng
- **infrastructure/**: Infrastructure as Code
- **tools/**: Development tools và scripts


### 3. **Scalability và maintainability**

- Dễ dàng thêm mới applications
- Shared code được tối ưu
- CI/CD pipeline hiệu quả
- Documentation tập trung

## 🚀 Cách thực hiện

### Option 1: Sử dụng PowerShell Script (Khuyến nghị cho Windows)

```powershell
# 1. Backup dự án hiện tại
./restructure_zeta_ai.ps1 -Backup -DryRun

# 2. Preview quá trình restructure
./restructure_zeta_ai.ps1 -TargetDir "C:\Projects\zeta-ai-2025" -DryRun

# 3. Thực hiện restructure
./restructure_zeta_ai.ps1 -TargetDir "C:\Projects\zeta-ai-2025" -Backup
```

### Option 2: Sử dụng Python Script (Cross-platform)

```bash
# 1. Cài đặt dependencies
pip install tomli-w pyyaml

# 2. Chạy script
python restructure_zeta_ai.py
```

### Option 3: Manual Migration (Từng bước)

#### Step 1: Tạo cấu trúc thư mục mới

```powershell
# Tạo thư mục root
mkdir zeta-ai-2025
cd zeta-ai-2025

# Tạo cấu trúc chính
mkdir apps, packages, infrastructure, tools, docs, examples, tests, deployments, configs

# Apps structure
mkdir apps/api-server/src/{presentation,application,infrastructure}
mkdir apps/api-server/{tests,migrations}
mkdir apps/desktop-app/src/{main,renderer,shared,preload}
mkdir apps/web-dashboard/src

# Packages structure  
mkdir packages/core-domain/src/{entities,value-objects,aggregates,events,services,repositories}
mkdir packages/ai-engine/src/{llm,rag,agents,memory,training,evaluation}
mkdir packages/shared-types/{python/src/zeta_types,typescript/src,openapi}
mkdir packages/security/src/{auth,encryption,audit,compliance}
mkdir packages/observability/src/{metrics,tracing,logging,alerting}
mkdir packages/utilities/src/{validation,serialization,caching,helpers}

# Infrastructure structure
mkdir infrastructure/{docker,kubernetes,terraform,monitoring}
mkdir infrastructure/kubernetes/overlays/{development,staging,production}

# Tools structure
mkdir tools/{scripts,generators,linters,testing}

# Docs structure
mkdir docs/{architecture,development,user-guides,operations,assets}
```

#### Step 2: Migrate Core Domain

```powershell
# Copy domain entities
Copy-Item "zeta_vn/core/domain/entities/*" "packages/core-domain/src/entities/" -Recurse
Copy-Item "zeta_vn/core/domain/value_objects/*" "packages/core-domain/src/value-objects/" -Recurse
Copy-Item "zeta_vn/core/domain/aggregates/*" "packages/core-domain/src/aggregates/" -Recurse
Copy-Item "zeta_vn/core/services/*" "packages/core-domain/src/services/" -Recurse
```

#### Step 3: Migrate Applications

```powershell
# API Server
Copy-Item "zeta_vn/app/api/*" "apps/api-server/src/presentation/" -Recurse
Copy-Item "zeta_vn/app/services/*" "apps/api-server/src/application/" -Recurse
Copy-Item "zeta_vn/app/middleware/*" "apps/api-server/src/infrastructure/middleware/" -Recurse
Copy-Item "zeta_vn/data/*" "apps/api-server/src/infrastructure/data/" -Recurse

# Desktop App
Copy-Item "desktop_ai_zeta/*" "apps/desktop-app/" -Recurse
```

#### Step 4: Migrate AI Engine

```powershell
# AI Components
Copy-Item "zeta_vn/core/ai/*" "packages/ai-engine/src/llm/" -Recurse
Copy-Item "zeta_vn/core/rag/*" "packages/ai-engine/src/rag/" -Recurse
Copy-Item "zeta_vn/training/*" "packages/ai-engine/src/training/" -Recurse
Copy-Item "zeta_vn/evaluators/*" "packages/ai-engine/src/evaluation/" -Recurse
```

## ⚙️ Configuration Files

### Root pyproject.toml

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "zeta-ai-workspace"
version = "0.1.0"
description = "ZETA AI Workspace - Monorepo for AI Platform"
requires-python = ">=3.11"

[tool.uv]
workspace = true
members = [
    "packages/*",
    "apps/api-server"
]

[tool.ruff]
target-version = "py311"
line-length = 100
src = ["packages", "apps"]

[tool.ruff.lint]
select = ["E", "F", "I", "TID", "PLC", "PLE", "PLW"]
ignore = ["E203", "E501"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### Root package.json

```json
{
  "name": "zeta-ai-workspace",
  "version": "0.1.0",
  "private": true,
  "workspaces": [
    "apps/desktop-app",
    "apps/web-dashboard",
    "packages/shared-types/typescript"
  ],
  "scripts": {
    "dev:all": "concurrently \"npm run dev:api\" \"npm run dev:apps/desktop\"",
    "dev:api": "cd apps/api-server && uv run uvicorn src.main:app --reload",
    "dev:apps/desktop": "cd apps/desktop-app && npm run dev",
    "build:all": "npm run build:api && npm run build:apps/desktop",
    "test:all": "npm run test:api && npm run test:apps/desktop",
    "format": "ruff format . && prettier --write .",
    "lint": "ruff check . && eslint .",
    "typecheck": "mypy . && tsc --noEmit"
  },
  "devDependencies": {
    "concurrently": "^8.0.0",
    "prettier": "^3.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "typescript": "^5.0.0"
  }
}
```

### Package-specific pyproject.toml

#### packages/core-domain/pyproject.toml

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "zeta-core-domain"
version = "0.1.0"
description = "ZETA AI Core Domain - Business Logic & Entities"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.11.0,<3.0.0",
    "typing-extensions>=4.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0"
]
```

#### packages/ai-engine/pyproject.toml

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "zeta-ai-engine"
version = "0.1.0"
description = "ZETA AI Engine - LLM, RAG, Agents"
requires-python = ">=3.11"
dependencies = [
    "openai>=1.55.0,<2.0.0",
    "sentence-transformers>=2.7.0",
    "faiss-cpu>=1.8.0",
    "numpy>=1.26.4",
    "pydantic>=2.11.0,<3.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0"
]

gpu = [
    "faiss-gpu>=1.8.0"
]
```

#### apps/api-server/pyproject.toml

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "zeta-api-server"
version = "0.1.0"
description = "ZETA AI API Server"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0,<1.0.0",
    "uvicorn[standard]>=0.30.0,<1.0.0",
    "pydantic>=2.11.0,<3.0.0",
    "sqlalchemy>=2.0.35,<3.0.0",
    "alembic>=1.13.0,<2.0.0",
    "zeta-core-domain",
    "zeta-ai-engine",
    "zeta-security",
    "zeta-observability"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.28.0"
]
```

## 🐳 Infrastructure Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  api-server:
    build:
      context: ./apps/api-server
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/zeta
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    volumes:
      - ./apps/api-server:/app
    
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: zeta
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 🔧 Development Workflow

### Setup Development Environment

```powershell
# 1. Clone the restructured project
git clone <new-repository-url>
cd zeta-ai-2025

# 2. Install Python dependencies
uv sync --all-workspaces --dev

# 3. Install Node.js dependencies
pnpm install

# 4. Setup pre-commit hooks
uv run pre-commit install

# 5. Start development services
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# 6. Start all applications
pnpm run dev:all
```

### Development Commands

```powershell
# Start API server only
cd apps/api-server
uv run uvicorn src.main:app --reload

# Start apps/desktop app only
cd apps/desktop-app
npm run dev

# Run tests
pnpm run test:all

# Format code
pnpm run format

# Lint code
pnpm run lint

# Type check
pnpm run typecheck

# Build for production
pnpm run build:all
```

## 📊 Migration Checklist

### Pre-migration

- [ ] Backup current project
- [ ] Document current dependencies
- [ ] Test current functionality
- [ ] Plan database migration strategy

### During migration

- [ ] Create new directory structure
- [ ] Migrate core domain logic
- [ ] Migrate applications
- [ ] Update import statements
- [ ] Update configuration files
- [ ] Migrate tests
- [ ] Update documentation

### Post-migration

- [ ] Test all applications
- [ ] Verify database connections
- [ ] Check API functionality
- [ ] Test apps/desktop app
- [ ] Run full test suite
- [ ] Update CI/CD pipelines
- [ ] Train team on new structure

## 🔍 Testing Strategy

### Unit Tests

```powershell
# Test core domain
cd packages/core-domain
uv run pytest

# Test AI engine
cd packages/ai-engine
uv run pytest

# Test API server
cd apps/api-server
uv run pytest
```

### Integration Tests

```powershell
# Run integration tests
cd tests/integration
uv run pytest
```

### End-to-End Tests

```powershell
# Run E2E tests
cd tests/e2e
npm run test:e2e
```

## 🚀 Deployment Strategy

### Local Development

```powershell
# Start all services
pnpm run dev:all
```

### Staging

```powershell
# Build and deploy to staging
pnpm run build:all
pnpm run deploy:staging
```

### Production

```powershell
# Build and deploy to production
pnpm run build:all
pnpm run deploy:production
```

## 🤝 Team Collaboration

### Branch Strategy

```
main
├── develop
├── feature/core-domain-migration
├── feature/api-server-restructure
├── feature/desktop-app-update
└── hotfix/critical-fixes
```

### Pull Request Process

1. Create feature branch from `develop`
2. Make changes following new structure
3. Update tests
4. Update documentation
5. Create pull request
6. Code review
7. Merge to `develop`
8. Deploy to staging for testing
9. Merge to `main` for production

## 📚 Documentation Updates

### Architecture Documentation

- [ ] Update architecture diagrams
- [ ] Document new layer boundaries
- [ ] Update API documentation
- [ ] Create deployment guides

### User Documentation

- [ ] Update user guides
- [ ] Create migration guides
- [ ] Update troubleshooting docs
- [ ] Create video tutorials

## 🔧 Troubleshooting

### Common Issues

#### Import Errors

```python
# Old import
from zeta_vn.core.domain.entities import User

# New import
from zeta_core_domain.entities import User
```

#### Dependency Issues

```powershell
# Reinstall dependencies
uv sync --all-workspaces --dev --force-reinstall
pnpm install --force
```

#### Database Connection Issues

```powershell
# Check database status
docker-compose -f infrastructure/docker/docker-compose.yml ps

# Restart database
docker-compose -f infrastructure/docker/docker-compose.yml restart postgres
```

## 🎯 Success Metrics

### Technical Metrics

- [ ] Build time reduction: Target < 30% of original
- [ ] Test execution time: Target < 50% of original
- [ ] Code coverage: Maintain > 90%
- [ ] Static analysis: Zero critical issues

### Team Metrics

- [ ] Developer onboarding time: Target < 1 day
- [ ] Feature development velocity: Target +25%
- [ ] Bug resolution time: Target -30%
- [ ] Documentation completeness: 100%

## 🚀 Next Steps

1. **Review and approve** this restructure plan
2. **Execute migration** using provided scripts
3. **Test thoroughly** in development environment
4. **Train team** on new structure and workflows
5. **Deploy to staging** for validation
6. **Go live** with production deployment
7. **Monitor and optimize** based on usage patterns


---

*Tài liệu này sẽ được cập nhật liên tục trong quá trình thực hiện tái cấu trúc.*
