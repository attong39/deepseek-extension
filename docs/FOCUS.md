# Focus Guardrails and Cut-list Policy

This repo tracks a Focus Index and flags anti-patterns to support the "tập trung–cắt gọn–tự động hoá" strategy.

What it does
- Computes a Focus Index (0–100) based on layer coverage and penalties
- Detects cut-list targets: `*manager.py`, duplicate models (e.g., `agent.py` vs `agent_model.py`), duplicate event bus (`core/events/event_bus.py` vs infra bus)
- Reports repository implementation preferences (prefer `sqlalchemy_*_repository.py`)

How to run locally
- python tools/focus_guard.py
- JSON output: python tools/focus_guard.py --json

CI behavior
- Workflow `.github/workflows/focus-guard.yml` runs the script in report-only mode for now.
- To enforce thresholds in CI, set env vars in the job:
  - FOCUS_ENFORCE=1
  - MAX_FILES=304 (example)
  - MAX_MANAGERS=0 (example)

Next consolidation steps
- Fold manager modules into service façades with deprecation shims.
- Merge legacy dashboard service into `AnalyticsService` (shim retained).
- Use infrastructure `infrastructure/events/event_bus.py` and deprecate `core/events` bus.
- Normalize data models to `*_model.py` and update imports.
- Prefer `sqlalchemy_*_repository.py` implementations; deprecate legacy duplicates.
