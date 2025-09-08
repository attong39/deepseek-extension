#!/usr/bin/env bash
set -euo pipefail

echo "🚀 ZETA_VN AI Self-Management Bootstrap"
echo "======================================"

# Check if we're on supported OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "❌ This script is for macOS/Linux. Use PowerShell setup for Windows."
    exit 1
fi

# 1. Install uv if not present
echo "📦 Installing uv package manager..."
if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# 2. Python setup
echo "🐍 Setting up Python environment..."
uv python install 3.11
uv sync

# 3. Database setup (optional)
echo "🗄️ Setting up database..."
if command -v docker >/dev/null 2>&1 && docker ps >/dev/null 2>&1; then
    echo "Starting PostgreSQL with pgvector..."
    docker run --rm -d --name zeta-pg \
        -e POSTGRES_PASSWORD=pass \
        -e POSTGRES_DB=zeta \
        -p 5432:5432 \
        pgvector/pgvector:pg16 || echo "⚠️  Database container already running or failed to start"
else
    echo "⚠️  Docker not available. Please set up PostgreSQL manually."
fi

# 4. Environment file
echo "⚙️ Creating .env file..."
if [ ! -f .env ]; then
    cat > .env <<'EOF'
# Database
DATABASE_URL=postgresql+asyncpg://postgres:pass@localhost:5432/zeta

# Outbox Pattern
OUTBOX_WORKERS=2
OUTBOX_BATCH_SIZE=200

# AI Self-Management (DEVELOPMENT ONLY)
ZETA_ALLOW_RUNTIME_INSTALL=1
ZETA_ALLOW_SELF_UPDATE=0
ZETA_SELF_SECURITY_AUTO_PATCH=0

# Security allowlist for auto-patching
ZETA_PATCH_ALLOW=requests,aiohttp,psutil

# Monitoring
ENABLE_METRICS=true
HEALTH_CHECK_INTERVAL=30

# Development
ZETA_DEV_MODE=1
LOG_LEVEL=DEBUG
EOF
    echo "✅ Created .env file with development settings"
else
    echo "✅ .env file already exists"
fi

# 5. Database migration
echo "🔄 Running database migrations..."
sleep 3  # Wait for DB container to be ready
uv run alembic upgrade head || echo "⚠️  Migration failed. Check database connection."

# 6. Desktop app setup
echo "🖥️ Setting up apps/desktop application..."
if [ -d "desktop_ai_zeta" ]; then
    pushd desktop_ai_zeta >/dev/null

    # Node version setup
    if command -v nvm >/dev/null 2>&1; then
        nvm use 20 || nvm install 20
    elif ! node --version | grep -q "v20"; then
        echo "⚠️  Please install Node.js 20+ manually"
    fi

    # Install dependencies
    echo "📦 Installing Node dependencies..."
    npm ci

    # Generate API types
    echo "🔄 Generating API types..."
    npm run codegen:api || npm run api:gen || echo "⚠️  API type generation failed"

    popd >/dev/null
else
    echo "⚠️  desktop_ai_zeta directory not found"
fi

# 7. Git hooks setup
echo "🪝 Setting up Git hooks..."
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit || echo "⚠️  Failed to set pre-commit executable"

# 8. Verify installation
echo "✅ Verifying installation..."

# Test Python environment
uv run python -c "
import sys
print(f'Python version: {sys.version}')

# Test AI Self-Management imports
try:
    from zeta_vn.core.self_improvement import AutoOptimizer, PerformanceKnobs
    from zeta_vn.core.security import security_sweep
    from zeta_vn.core.self_awareness import HealthMonitor
    from zeta_vn.core.utils import get_runtime_install_status
    print('✅ AI Self-Management modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')

# Test database connection (optional)
try:
    import asyncio
    import os
    from zeta_vn.data.database import test_connection
    if os.getenv('DATABASE_URL'):
        asyncio.run(test_connection())
        print('✅ Database connection successful')
except Exception as e:
    print(f'⚠️  Database test failed: {e}')
"

echo ""
echo "🎉 Bootstrap complete!"
echo ""
echo "📋 Next steps:"
echo "1. Open VS Code: code ."
echo "2. Run quality check: uv run python tools/master_quality_check.py"
echo "3. Start development server: uv run uvicorn zeta_vn.app.main_production:app --reload"
echo "4. Start apps/desktop app: cd desktop_ai_zeta && npm run dev"
echo ""
echo "📚 Useful VS Code tasks:"
echo "- Ctrl+Shift+P > 'Tasks: Run Task' > 'QA: Master Quality Check'"
echo "- Ctrl+Shift+P > 'Tasks: Run Task' > 'FastAPI: Uvicorn Dev'"
echo "- Ctrl+Shift+P > 'Tasks: Run Task' > 'Desktop: Contract Sync'"
echo ""
echo "🤖 AI Self-Management features are ready!"
echo "Check status: curl http://localhost:8000/admin/health/detailed"
