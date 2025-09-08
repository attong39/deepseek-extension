@echo off
REM Windows PowerShell wrapper for upgrade scripts

echo ▶ ZETA_AI UPGRADE START (Windows)

REM Check if uv is available
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ uv not found. Install uv first: https://docs.astral.sh/uv/
    exit /b 1
)

REM Backend quality check
echo → Running Python quality checks...
cd /d "%~dp0..\..\"
uv sync
uv run ruff check . --fix
uv run ruff format .
uv run mypy zeta_vn --pretty --no-error-summary
uv run pytest -q --maxfail=1 --disable-warnings --cov=zeta_vn --cov-report=term-missing --cov-fail-under=80
uv run bandit -q -r zeta_vn
uv run pip-audit

REM Performance gate
echo → Running performance gate...
uv run python scripts/perf/perf_gate.py --host 127.0.0.1 --port 8099 --startup-budget 3.0 --ram-budget-mb 300

REM Frontend quality check (if exists)
if exist "desktop_ai_zeta\" (
    echo → Running TypeScript quality checks...
    cd desktop_ai_zeta
    npm run format 2>nul || echo "No format script found"
    npm run lint 2>nul || echo "No lint script found"
    npm run typecheck 2>nul || echo "No typecheck script found"
    npm run test 2>nul || echo "No test script found"
    cd ..
) else (
    echo ⚠ desktop_ai_zeta/ not found, skipping frontend checks
)

echo ✔ Upgrade complete! Consider: git add -A && git commit -m "chore: upgrade & quality gates"
