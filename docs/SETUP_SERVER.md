Server setup (editable install, minimal guidance)

Goal: allow developers to do an editable install and run the server as a module
without changing repository layout.

Recommended (preferred): use the repository root pyproject and run editable install
from the repo root (no PYTHONPATH hacks):

# create venv and activate (Windows PowerShell)
python -m venv .venv; . .venv\Scripts\Activate.ps1

# install editable dev environment
.venv\Scripts\python.exe -m pip install -U pip
.venv\Scripts\python.exe -m pip install -e .[dev]

# run the server (module mode)
.venv\Scripts\python.exe -m uvicorn zeta_vn.app.main:app --reload --host 127.0.0.1 --port 8000

Notes and tips
- Do NOT set PYTHONPATH globally. Use editable install (-e) so imports are absolute.
- If you prefer a separate package root named `zeta_server/`, create it as a thin wrapper
  that references the same source. This repo already exposes `zeta_vn` at top-level; moving
  files is a larger change.
- Use the provided `pyproject.toml` for dependency groups (dev/test/production).
- Run code checks before PR: `ruff check .`, `mypy`, `pytest -q`.

Import-linter
- We added `importlinter.ini` with layered contract. Run locally with:

.venv\Scripts\python.exe -m import_linter.check_imports importlinter.ini

FE generator (OpenAPI -> TypeScript types)
- Desktop client can generate typed client using openapi-typescript (installed in apps/desktop dev deps):

pnpm --filter zeta_desktop run gen:api

This document is intentionally minimal. For full bootstrap see CONTRIBUTING.md and docs/INSTALLATION.md.
