#!/usr/bin/env bash
set -euo pipefail

echo "🔒 [Phase3] Security Hardening - Zero-Trust và bảo mật"
echo "======================================================"

echo "🛡️ [Phase3] Running security hardening checks..."

echo "🔍 Security code analysis (bandit)..."
uv run bandit -q -r zeta_vn || {
    echo "⚠️ Security issues detected"
}

echo "📋 Dependency vulnerability audit..."
uv run pip-audit || {
    echo "⚠️ Vulnerable dependencies found"
}

echo "🔐 Checking for secrets in code..."
if command -v git >/dev/null 2>&1; then
    git secrets --scan || {
        echo "💡 Install git-secrets for better secret scanning"
    }
fi

echo "✅ Security baseline checks completed!"
echo ""
echo "🚀 Manual security hardening tasks:"
echo "  - Enable JWT authentication in main_production.py"
echo "  - Configure Zero-Trust middleware"
echo "  - Set up rate limiting"
echo "  - Enable audit logging for WebSocket connections"
echo "  - Configure CORS policies"
echo ""
echo "Next: Run 'bash scripts/impl/phase4_deploy.sh' for production deployment"