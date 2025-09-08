# Kế Hoạch Thực Thi Tái Cấu Trúc ZETA_AI

## Phase 1: Foundation Setup (Week 1-2)

### 1.1 Audit & Mapping Current State
```bash
# Chạy script audit hiện trạng
uv run python tools/refactor/copilot_refactor.py --dry-run

# Cập nhật PROJECT_MAP.md
uv run python .github/prompts/update_project_map.py
```

### 1.2 Clean Architecture Foundation
- [ ] Tạo cấu trúc thư mục chuẩn:
  - `zeta_vn/app/` (interfaces)
  - `zeta_vn/core/` (domain/use_cases)
  - `zeta_vn/data/` (repositories/infrastructure)
  - `zeta_vn/config/` & `zeta_vn/tests/`

### 1.3 Quality Gates Setup
```bash
# Setup quality tools
uv add --dev ruff mypy pytest bandit pip-audit vulture

# Configure CI/CD
cp .github/workflows/ci.yml.template .github/workflows/ci.yml
```

## Phase 2: Core RAG Implementation (Week 3-4)

### 2.1 RAG Pipeline Core
- [ ] `core/use_cases/rag.py` - One-Click Learning pipeline
- [ ] `core/interfaces/repositories.py` - Document repository protocol
- [ ] `data/repositories/vector_store.py` - Vector DB implementation

### 2.2 API Layer
- [ ] `app/api/v1/rag.py` - REST endpoints
- [ ] `app/websockets/training.py` - Real-time progress streaming
- [ ] Middleware: PII masking, rate limiting

## Phase 3: Frontend Modernization (Week 5-6)

### 3.1 Desktop App Structure
```
desktop_ai_zeta/
├── src/
│   ├── components/
│   │   ├── ChatPanel.tsx
│   │   ├── TrainingPanel.tsx
│   │   └── ControlPanel.tsx
│   ├── services/
│   │   ├── apiClient.ts
│   │   └── wsClient.ts
│   └── App.tsx
```

### 3.2 Integration Features
- [ ] HashRouter navigation
- [ ] WebSocket training progress
- [ ] File upload with progress
- [ ] Real-time chat interface

## Phase 4: DevSecOps & Automation (Week 7-8)

### 4.1 Security Hardening
- [ ] PII masking middleware
- [ ] Permission management
- [ ] Audit logging
- [ ] Secret scanning

### 4.2 Copilot Enhancement
- [ ] Auto-refactor scripts
- [ ] Code quality scoring
- [ ] Intelligent file mapping
- [ ] Stub generation

## Critical Success Factors

### ✅ Must-Have Features
1. **Zero Data Loss**: Backup before refactor
2. **Backward Compatibility**: API versioning
3. **Quality Gates**: 100% lint/type pass, 80%+ coverage
4. **Security**: PII masking, rate limiting, audit logs

### 🎯 Performance Targets
- API response time: < 200ms (P95)
- Test coverage: ≥ 80%
- Code quality: ruff + mypy clean
- Security: bandit + pip-audit pass

### 🔧 Tools & Commands

```bash
# Development workflow
uv run uvicorn zeta_vn.app.main:app --reload
cd desktop_ai_zeta && pnpm dev

# Quality checks
uv run ruff check . && uv run mypy . && uv run pytest -q

# Security scans
uv run bandit -r zeta_vn && uv run pip-audit

# Copilot refactor
uv run python tools/refactor/copilot_refactor.py --dry-run
```

## Risk Mitigation

### 🚨 High Risk Areas
1. **Database Migration**: Careful schema changes
2. **API Breaking Changes**: Maintain v1 compatibility
3. **File Movement**: Ensure imports update correctly
4. **Dependencies**: Version conflicts between old/new

### 🛡️ Mitigation Strategies
- Feature flags for gradual rollout
- Comprehensive test coverage
- Rollback procedures
- Documentation updates

## Next Steps

1. **Immediate (Today)**: Run audit script, review current state
2. **This Week**: Setup Clean Architecture foundation
3. **Next Week**: Implement RAG pipeline core
4. **Month 1**: Complete frontend modernization
5. **Month 2**: Full DevSecOps integration

## Success Metrics

- [ ] All quality gates passing
- [ ] RAG pipeline functional end-to-end
- [ ] Desktop app modernized with React/TypeScript
- [ ] Copilot integration enhanced
- [ ] Documentation updated and comprehensive
