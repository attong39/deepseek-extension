# SAFE_PHASE3_ROADMAP.md
**Phase 3: Data Layer & Infrastructure - Zero Code Loss Strategy**  
*Nguyên tắc: Scaffold → Test → Migrate → Validate*

---

## 🎯 **Objectives & Principles**

### **Core Goals**:
1. **Zero Code Loss**: Không phá vỡ kiến trúc đang chạy
2. **Scaffold-First**: Mọi file mới nằm ở `_scaffold/_templates`
3. **Type-Safe Contracts**: UoW/Repository interface-driven
4. **CI Integration**: Postgres + Redis automated testing
5. **Migration Health**: Alembic zero multiple heads

### **Non-Goals**:
- ❌ Thay đổi cây thư mục hiện tại
- ❌ Auto-import scaffold vào app chính
- ❌ Breaking changes đến services đang chạy
- ❌ Forced migration từ current implementation

---

## 📁 **Architecture Overview**

```
zeta_vn/
├── infrastructure/
│   ├── _scaffold/          # Safe templates (không auto-import)
│   │   ├── repository_base.py
│   │   ├── uow.py
│   │   └── contracts.py
│   ├── _templates/         # Implementation examples
│   │   ├── cache_redis.py
│   │   ├── vector_pgvector.py
│   │   └── db_postgres.py
│   └── adapters/          # Current implementations (unchanged)
│
tests/
├── infrastructure/
│   ├── persistence/       # DB integration tests
│   │   ├── test_uow_contract.py
│   │   └── test_repository_contract.py
│   └── integration/       # End-to-end tests
│
scripts/
├── db/
│   ├── check_migration_health.py
│   └── setup_test_db.py
└── safe/
    └── generate_phase3_work_orders.py
```

---

## 🏗️ **Implementation Strategy**

### **Phase 3A: Contracts & Scaffold (Week 1)**
- ✅ Create repository base interfaces - **COMPLETED**
- ✅ UnitOfWork protocol with context manager - **COMPLETED** 
- ✅ Database health check scripts - **COMPLETED**
- ✅ CI workflow for DB integration - **READY**
- ✅ Initial smoke tests - **COMPLETED**

## 🎯 **Current Status: Phase 3A COMPLETED** ✅

### **Achievements:**
1. **Repository Contracts** - Full protocol with generic types, error handling, validation
2. **Unit of Work Pattern** - Transaction management with async context manager
3. **Health Check System** - Database connection & migration status monitoring  
4. **Test Coverage** - Complete test suite for all scaffold components
5. **Quality Validation** - All files pass ruff + mypy strict checking

### **Ready for Phase 3B:**

### **Phase 3B: Implementation Templates (Week 2)**
- 🔄 Redis cache adapter (optional dependency)
- 🔄 PgVector integration template
- 🔄 Postgres connection pooling
- 🔄 Migration health automation
- 🔄 Integration test expansion

### **Phase 3C: Gradual Migration (Week 3)**
- 🔄 Wiring scaffold to existing services
- 🔄 A/B testing old vs new implementations
- 🔄 Performance benchmarking
- 🔄 Production readiness validation

---

## 🛡️ **Safety Guards**

### **Migration Health Checks**:
```python
# scripts/db/check_migration_health.py
def check_alembic_health():
    """Ensure no multiple heads, DB at head."""
    heads = get_alembic_heads()
    if len(heads) > 1:
        raise Exception(f"Multiple heads detected: {heads}")
    
    current = get_current_revision()
    latest = get_latest_revision()
    if current != latest:
        raise Exception(f"DB not at head: {current} != {latest}")
```

### **Contract Compliance Tests**:
```python
# tests/infrastructure/persistence/test_uow_contract.py
@pytest.mark.integration_db
class TestUnitOfWorkContract:
    """Ensure all UoW implementations comply with contract."""
    
    async def test_context_manager_protocol(self):
        async with uow:
            # Transaction should be active
            assert uow.in_transaction()
        # Transaction should be committed/rolled back
```

### **Optional Dependencies**:
```python
# zeta_vn/infrastructure/_templates/cache_redis.py
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    
class RedisCache:
    def __init__(self):
        if not REDIS_AVAILABLE:
            raise ImportError("redis not installed: pip install redis")
```

---

## 🧪 **Testing Strategy**

### **Test Markers**:
- `@pytest.mark.unit` - Unit tests (no external deps)
- `@pytest.mark.integration_db` - DB integration tests
- `@pytest.mark.integration_cache` - Cache integration tests
- `@pytest.mark.e2e` - End-to-end tests

### **CI Workflow**:
```yaml
# .github/workflows/db-integration.yml
name: DB Integration Tests
on: [push, pull_request]

jobs:
  test-db:
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install uv
          uv sync --all-extras
      
      - name: Check migration health
        run: |
          uv run alembic upgrade head
          uv run python scripts/db/check_migration_health.py
      
      - name: Run integration tests
        run: |
          uv run pytest -m integration_db -v
          uv run pytest -m integration_cache -v
      
      - name: Quality gates
        run: |
          uv run ruff check .
          uv run mypy zeta_vn
          uv run pytest -q
```

---

## 📋 **Work Orders Priority**

### **HIGH Priority (Week 1)**:
1. **WO-301**: Infrastructure contracts (Repository, UoW)
2. **WO-302**: Database health check system
3. **WO-303**: CI workflow setup
4. **WO-304**: Basic integration tests

### **MEDIUM Priority (Week 2)**:
5. **WO-305**: Redis cache adapter template
6. **WO-306**: PgVector integration scaffold
7. **WO-307**: Connection pooling optimization
8. **WO-308**: Performance benchmarking

### **LOW Priority (Week 3)**:
9. **WO-309**: Service wiring automation
10. **WO-310**: Production monitoring setup

---

## 🚦 **Success Criteria**

### **Phase 3A Complete When**:
- ✅ All contracts defined and tested
- ✅ Migration health checks pass
- ✅ CI workflow running green
- ✅ Zero breaking changes to existing code
- ✅ Test coverage ≥80% for new code

### **Phase 3B Complete When**:
- ✅ Redis/PgVector templates functional
- ✅ Optional dependencies handled gracefully
- ✅ Performance meets/exceeds current implementation
- ✅ Integration tests comprehensive

### **Phase 3C Complete When**:
- ✅ Services can use new or old implementation
- ✅ A/B testing shows equivalent functionality
- ✅ Production deployment validated
- ✅ Documentation and migration guide complete

---

## 🔄 **Rollback Strategy**

**If Phase 3 Issues Detected**:
1. **Immediate**: Disable scaffold imports
2. **Short-term**: Revert to Phase 2 stable state  
3. **Analysis**: Review what went wrong
4. **Retry**: Fix issues and re-attempt

**Rollback Commands**:
```bash
# Quick rollback to Phase 2
git checkout HEAD~1 -- zeta_vn/infrastructure/_scaffold/
git checkout HEAD~1 -- zeta_vn/infrastructure/_templates/
uv run pytest -q  # Ensure Phase 2 still works
```

---

## 📊 **Monitoring & Metrics**

### **Health Metrics**:
- 🟢 Migration health: 0 multiple heads
- 🟢 Test coverage: ≥80% new code
- 🟢 Performance: ≤10% regression
- 🟢 CI success rate: ≥95%

### **Quality Gates**:
- 🟢 Ruff: 0 errors in scaffold code
- 🟢 MyPy: 0 errors in contracts
- 🟢 Pytest: All integration tests pass
- 🟢 Coverage: No coverage decrease

**Ready to begin Phase 3A implementation! 🚀**
