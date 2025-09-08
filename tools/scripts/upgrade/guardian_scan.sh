#!/usr/bin/env bash
set -euo pipefail
echo "▶ Guardian scan+fix"
uv run python -m deepseek.guardian.runner --scan --apply --json || true
echo "✔ Reports at .artifacts/guardian_report.{json,md}"
