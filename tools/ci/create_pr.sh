#!/usr/bin/env bash
set -euo pipefail
TITLE="CI Gates v2 – Finalize & Protect"
BODY=$'This PR enables the final CI gates and branch protection.\n\n- CI Doctor\n- Consistency Guard\n- Auto-Fix dry-run\n- QA (ruff/mypy/bandit/pip-audit)\n- Coverage ≥85%\n- Docker build + Trivy\n- E2E WS/API smoke\n- Contract snapshot\n'
gh pr create -B main -H ci/gates-v2 -t "$TITLE" -b "$BODY" || true
gh pr view --web || true
