#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to run quality check
quality_check() {
    local command="$1"
    local description="$2"
    local strict_mode="${3:-true}"
    
    echo -e "${YELLOW}🔍 $description...${NC}"
    
    if [ "$strict_mode" = "true" ]; then
        if eval "$command"; then
            echo -e "${GREEN}✅ $description passed${NC}"
        else
            echo -e "${RED}❌ $description failed${NC}"
            exit 1
        fi
    else
        if eval "$command"; then
            echo -e "${GREEN}✅ $description passed${NC}"
        else
            echo -e "${YELLOW}⚠️  $description warnings detected${NC}"
        fi
    fi
}

echo -e "${CYAN}== ZETA_AI :: QUALITY GATES ==${NC}"

# Main quality checks
quality_check "uv run ruff check ." "Ruff linting"
quality_check "uv run ruff format --check ." "Ruff formatting"
quality_check "uv run mypy zeta_vn zeta_vn_restructured --show-column-numbers --hide-error-context" "MyPy type checking"
quality_check "uv run pytest tests zeta_vn_restructured/tests -q -k 'not slow' --maxfail=1" "Pytest quick tests"

# Optional security & supply chain checks (non-strict)
quality_check "uv run bandit -q -r zeta_vn zeta_vn_restructured" "Bandit security scan" false
quality_check "uv run pip-audit" "Pip-audit supply chain check" false

echo -e "\n${GREEN}== ✅ ALL QUALITY GATES PASSED (dev mode) ==${NC}"
echo -e "${CYAN}🚀 Code is ready for development and deployment!${NC}"
