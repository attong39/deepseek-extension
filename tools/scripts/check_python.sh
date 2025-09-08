#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Ruff format (không tự sửa trong CI) và lint
python -m ruff format --check .
python -m ruff check .

# Mypy
MYPY_CFG=""
if [ -f "$ROOT_DIR/ci/mypy-temp.ini" ]; then
	MYPY_CFG="--config-file $ROOT_DIR/ci/mypy-temp.ini"
	echo "Using temporary mypy config: $ROOT_DIR/ci/mypy-temp.ini"
fi

# Allow limiting mypy to a small set of files during triage.
# If ci/mypy-files.txt exists, read it (ignoring comments) and use those paths.
FILES="zeta_vn"
if [ -f "$ROOT_DIR/ci/mypy-files.txt" ]; then
	FILES=$(sed -e '/^\s*#/d' "$ROOT_DIR/ci/mypy-files.txt" | xargs)
	echo "Mypy will check files: $FILES"
fi

python -m mypy --strict $MYPY_CFG $FILES

# Pytest với coverage
pytest --maxfail=1 -q --cov=zeta_vn --cov-report=term-missing

# Bandit security scan
bandit -r zeta_vn -q

# pip-audit
pip-audit -r requirements.txt

# Vulture (dead code)
vulture zeta_vn
