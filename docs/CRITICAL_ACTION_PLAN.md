# CRITICAL ACTION PLAN - ZETA_AI REFACTOR

## 🚨 URGENT ISSUES DETECTED

### Quality Issues (20 files scanned)
- ✅ Pass (≥70): **2 files** 
- ❌ Fail (<70): **18 files**
- 🔧 Main issues: **mypy type errors**, **ruff formatting**

### Missing Infrastructure
- ❌ No PROJECT_MAP.md mapping available
- ❌ No structured refactor guidance

## 🎯 IMMEDIATE ACTIONS (Next 24h)

### 1. Create PROJECT_MAP.md
```bash
# Generate current project structure
uv run python .github/prompts/update_project_map.py
```

### 2. Fix Critical Quality Issues
```bash
# Auto-fix formatting
uv run ruff format .

# Check remaining issues
uv run ruff check .
uv run mypy . --show-error-codes
```

### 3. Setup Clean Architecture Foundation
```bash
# Create standard directory structure
mkdir -p zeta_vn/{app,core,data,config,tests}
mkdir -p zeta_vn/app/{api,websockets,controllers}
mkdir -p zeta_vn/core/{domain,use_cases,services,interfaces}
mkdir -p zeta_vn/data/{models,repositories,database,external}
```

## 🔥 HIGH PRIORITY FIXES

### Files with Multiple Issues (ruff + mypy):
1. `careful_init_fixer.py` - Score: 30
2. `conftest.py` - Score: 30  
3. `fix_all_init_files.py` - Score: 30

### Files with Type Issues Only:
- Most demo/fix scripts have mypy errors
- Need proper type annotations

## 📊 QUALITY METRICS TARGET

| Metric        | Current | Target | Action                     |
| ------------- | ------- | ------ | -------------------------- |
| Pass Rate     | 10%     | 90%    | Fix type annotations       |
| Ruff Clean    | ~60%    | 100%   | Auto-format + manual fixes |
| Mypy Clean    | ~10%    | 95%    | Add type hints             |
| Test Coverage | Unknown | 80%    | Add pytest coverage        |

## 🛠️ IMPLEMENTATION STRATEGY

### Phase 1: Emergency Stabilization (Week 1)
1. **Fix all ruff issues** (auto-format + manual)
2. **Add basic type hints** for critical paths
3. **Create PROJECT_MAP.md** with current structure
4. **Setup quality gates** in CI

### Phase 2: Structural Reform (Week 2-3)
1. **Implement Clean Architecture** structure
2. **Move files to correct layers** (app/core/data)
3. **Create interface contracts** (protocols)
4. **Add comprehensive tests**

### Phase 3: Feature Enhancement (Week 4+)
1. **RAG pipeline implementation**
2. **WebSocket real-time features**
3. **Desktop app modernization**
4. **Security hardening**

## ⚡ QUICK WINS (Today)

```bash
# 1. Format all Python files
uv run ruff format .

# 2. Run quality check
uv run python -m pytest --version || uv add pytest

# 3. Create basic PROJECT_MAP
echo "# Project Structure Map" > .github/prompts/PROJECT_MAP.md

# 4. Setup quality task
code .vscode/tasks.json
```

## 🎯 SUCCESS CRITERIA

- [ ] All files pass ruff formatting
- [ ] 90%+ files pass mypy type checking  
- [ ] PROJECT_MAP.md exists and is accurate
- [ ] CI pipeline with quality gates
- [ ] Clean Architecture structure in place
- [ ] Basic RAG pipeline functional

## 🚀 NEXT STEPS

1. **Run emergency fixes** (ruff format, basic types)
2. **Create PROJECT_MAP.md** based on actual structure
3. **Setup CI quality gates** to prevent regression
4. **Plan gradual migration** to Clean Architecture
5. **Implement RAG core** with proper testing

---

*This is a critical path to project health. Focus on stabilization first, then systematic improvement.*
