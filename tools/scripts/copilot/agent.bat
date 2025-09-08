@echo off
REM Windows batch wrapper for Copilot Coding Agent

echo 🤖 COPILOT CODING AGENT - Windows Edition

REM Check dependencies
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ uv not found. Install from: https://docs.astral.sh/uv/
    exit /b 1
)

where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Node.js not found. Install from: https://nodejs.org/
    exit /b 1
)

REM Setup directories
if not exist ".artifacts" mkdir .artifacts

REM Set variables
set TIMESTAMP=%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set LOG_FILE=.artifacts\copilot_agent_%TIMESTAMP%.log

echo ▶ Copilot Coding Agent started @ %TIMESTAMP% > %LOG_FILE%

REM 1) Build Copilot context
echo 📖 Building Copilot context... | tee -a %LOG_FILE%
uv run python scripts\copilot\build_context.py >> %LOG_FILE% 2>&1

REM 2) Backend quality
echo 🐍 Running Python quality checks... | tee -a %LOG_FILE%
uv sync >> %LOG_FILE% 2>&1
uv run ruff check . --fix >> %LOG_FILE% 2>&1
uv run ruff format . >> %LOG_FILE% 2>&1
uv run mypy zeta_vn --pretty --no-error-summary >> %LOG_FILE% 2>&1
uv run pytest -q --maxfail=1 --disable-warnings --cov=zeta_vn --cov-report=term-missing --cov-fail-under=80 >> %LOG_FILE% 2>&1
uv run bandit -q -r zeta_vn >> %LOG_FILE% 2>&1
uv run pip-audit >> %LOG_FILE% 2>&1

REM 3) Frontend quality (if exists)
if exist "desktop_ai_zeta\" (
    echo 📘 Running TypeScript quality checks... | tee -a %LOG_FILE%
    cd desktop_ai_zeta
    npm ci >> ..\%LOG_FILE% 2>&1
    npx prettier "src/**/*.{ts,tsx,css,md}" --write >> ..\%LOG_FILE% 2>&1
    npx eslint "src/**/*.{ts,tsx}" --fix >> ..\%LOG_FILE% 2>&1
    npx tsc --noEmit >> ..\%LOG_FILE% 2>&1
    if exist "vitest.config.ts" npx vitest run --coverage >> ..\%LOG_FILE% 2>&1
    npx depcheck >> ..\%LOG_FILE% 2>&1
    npx ts-prune > ..\.artifacts\deadcode\ts-prune.txt 2>&1
    cd ..
)

REM 4) Code analysis
echo 🔍 Running code duplication analysis... | tee -a %LOG_FILE%
if not exist ".artifacts\jscpd-report" mkdir .artifacts\jscpd-report
npx jscpd --reporters html --output .artifacts\jscpd-report --threshold 2 --pattern "**/*.{ts,tsx,js,py}" . >> %LOG_FILE% 2>&1

echo 💀 Running dead code analysis... | tee -a %LOG_FILE%
if not exist ".artifacts\deadcode" mkdir .artifacts\deadcode
uvx vulture zeta_vn --min-confidence 80 > .artifacts\deadcode\vulture.txt 2>&1

REM 5) Performance gate
echo ⚡ Running performance gate... | tee -a %LOG_FILE%
uv run python scripts\perf\perf_gate.py --startup-budget 3.0 --ram-budget-mb 300 >> %LOG_FILE% 2>&1

REM 6) Summary
echo. >> %LOG_FILE%
echo === SUMMARY ARTIFACTS === >> %LOG_FILE%
if exist ".artifacts\jscpd-report\jscpd-report.html" (echo • .artifacts\jscpd-report\jscpd-report.html (OK)) else (echo • .artifacts\jscpd-report\jscpd-report.html (missing)) >> %LOG_FILE%
if exist ".artifacts\deadcode\vulture.txt" (echo • .artifacts\deadcode\vulture.txt (OK)) else (echo • .artifacts\deadcode\vulture.txt (missing)) >> %LOG_FILE%
if exist ".artifacts\deadcode\ts-prune.txt" (echo • .artifacts\deadcode\ts-prune.txt (OK)) else (echo • .artifacts\deadcode\ts-prune.txt (missing)) >> %LOG_FILE%
if exist "COPILOT_CONTEXT.md" (echo • COPILOT_CONTEXT.md (OK)) else (echo • COPILOT_CONTEXT.md (missing)) >> %LOG_FILE%

echo ✔ Done. Log: %LOG_FILE%
echo 👉 Gợi ý commit: git add -A ^&^& git commit -m "chore: copilot agent – format, imports, dedupe, deadcode, perf-gate"

pause
