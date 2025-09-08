.PHONY: help install dev build test clean project-map qa smoke ws-bench test-all hooks

help:
	@echo "ZETA AI Monorepo Commands:"
	@echo "  install      Install all dependencies"
	@echo "  dev          Start development servers"
	@echo "  build        Build all projects"
	@echo "  test         Run all tests"
	@echo "  test-all     Run comprehensive test suite"
	@echo "  clean        Clean all build artifacts"
	@echo "  project-map  Generate PROJECT_MAP.md"
	@echo "  hooks        Setup git hooks for consistency guard"
	@echo ""
	@echo "Quality Gates:"
	@echo "  qa           Run all quality checks (lint, type, security, test)"
	@echo "  smoke        Quick smoke tests for core functionality"
	@echo "  ws-bench     WebSocket load testing and benchmarks"
	@echo ""
	@echo "Auto-Fix Turbo:"
	@echo "  fix-imports  Auto-fix imports with cache & lint-fix"
	@echo "  fast-fix     Quick fix: Only changed files + cache"
	@echo "  lint-fix     Run lint fixes (ruff + eslint)"
	@echo "  cleanup      Run repository cleanup"
	@echo ""
	@echo "Consistency Guard:"
	@echo "  guard        Run full consistency check with detailed report"
	@echo "  guard-fix    Auto-fix OpenAPI hash and re-run guard"
	@echo "  guard-status Quick hash status check"
	@echo "  prepush      Run pre-push consistency check (non-blocking)"

install:
@echo "Installing dependencies..."
npm install
cd apps/backend && poetry install

dev:
@echo "Starting development servers..."
npm run dev

build:
@echo "Building all projects..."
npm run build
cd apps/backend && poetry build

test:
@echo "Running all tests..."
npm run test

clean:
@echo "Cleaning build artifacts..."
rm -rf node_modules */node_modules */dist */out

project-map:
@echo "Generating PROJECT_MAP.md..."
python gen_project_map.py --depth 4 --respect-gitignore --out PROJECT_MAP.md
cd apps/backend && rm -rf dist .pytest_cache

# ==================== Quality Gates ====================

qa: lint type-check security-check test
@echo "✅ All quality gates passed!"

lint:
@echo "🔍 Running code linting..."
cd apps/backend && .venv/Scripts/python.exe -m ruff check --fix
cd apps/backend && .venv/Scripts/python.exe -m ruff format
@echo "✅ Linting completed"

type-check:
@echo "🔍 Running type checking..."
cd apps/backend && .venv/Scripts/python.exe -m mypy app/ --config-file=mypy.ini
@echo "✅ Type checking completed"

security-check:
@echo "🔒 Running security checks..."
cd apps/backend && .venv/Scripts/python.exe -m bandit -r app/ -f json -o bandit-report.json || true
cd apps/backend && .venv/Scripts/python.exe -m pip-audit --format=json --output=pip-audit-report.json || true
@echo "✅ Security scanning completed"

smoke:
@echo "💨 Running smoke tests..."
cd apps/backend && .venv/Scripts/python.exe -m pytest tests/unit/test_health.py -v --tb=short
cd apps/backend && .venv/Scripts/python.exe -m pytest tests/integration/test_agents_basic.py -v --tb=short
@echo "✅ Smoke tests passed"

ws-bench:
@echo "⚡ Running WebSocket benchmarks..."
cd tools/load && python ws_blast.py --clients=50 --duration=30 --target-mps=1000
@echo "✅ WebSocket benchmarks completed"

test-all:
@echo "🧪 Running comprehensive test suite..."
cd apps/backend && .venv/Scripts/python.exe -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=85
@echo "✅ Full test suite completed"

# ==================== Infrastructure ====================

start-ollama:
@echo "🚀 Starting Ollama server..."
ollama serve &

stop-ollama:
@echo "🛑 Stopping Ollama server..."
@powershell -Command "Get-Process ollama -ErrorAction SilentlyContinue | Stop-Process -Force"

restart-ollama: stop-ollama start-ollama
@echo "🔄 Ollama server restarted"

# ==================== Git Hooks ====================

hooks:
	@echo "🔧 Setting up git hooks for consistency guard..."
	git config core.hooksPath .githooks
	@powershell -Command "if (Test-Path '.githooks/pre-commit') { & icacls '.githooks/pre-commit' /grant Everyone:F | Out-Null }"
	@powershell -Command "if (Test-Path '.githooks/pre-push') { & icacls '.githooks/pre-push' /grant Everyone:F | Out-Null }"
	@echo "✅ Git hooks configured successfully"

# ==================== Consistency Guard ====================

.PHONY: guard guard-fix guard-status prepush
guard:
	@echo "🛡️ Running Consistency Guard..."
	uv run python tools/consistency/run_all.py
	@echo ""
	@echo "📊 Guard Report:"
	@type reports\\consistency\\result.md 2>nul || echo "No report generated"

guard-fix:
	@echo "🔧 Auto-fixing OpenAPI hash..."
	uv run python tools/consistency/openapi_hash.py --write
	@echo "🛡️ Re-running Guard..."
	$(MAKE) guard

guard-status:
	@echo "📊 Quick Guard Status:"
	@uv run python tools/consistency/openapi_hash.py --check || echo "Hash mismatch"
	@echo "Hash check completed"

prepush:
	@echo "🚀 Pre-push consistency check..."
	@powershell -ExecutionPolicy Bypass -File .githooks/pre-push.ps1

# ==================== Auto-Fix Turbo ====================

.PHONY: fix-imports fast-fix guard hooks cleanup lint-fix
fix-imports:
	@echo "🔧 Auto-fix missing imports & deps..."
	uv run python tools/auto_fix/cli.py all --use-cache --lint-fix && cat reports/auto_fix/report.md 2>/dev/null || echo "No report generated"

fast-fix:
	@echo "⚡ Quick fix: Only changed files + cache..."
	uv run python tools/auto_fix/cli.py all --changed-only --use-cache --lint-fix && cat reports/auto_fix/report.md 2>/dev/null || echo "No report generated"

lint-fix:
	@echo "🧹 Run lint fixes..."
	uv run ruff check --fix .
	@if command -v pnpm >/dev/null 2>&1; then pnpm -C apps/desktop eslint --ext .ts,.tsx --fix .; else npx --yes eslint --ext .ts,.tsx --fix apps/desktop/src; fi

cleanup:
	@echo "🗂️ Run repository cleanup..."
	uv run python tools/repo_maintenance/cleanup.py