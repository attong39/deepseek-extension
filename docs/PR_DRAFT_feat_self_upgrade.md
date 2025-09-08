# PR draft: feat/self-upgrade

Short description
-----------------
Introduce a safe, minimal skeleton for server self-upgrade orchestration and supporting artifacts. This PR adds a Celery-task-friendly runner, a small k8s client wrapper (stub), a release record model + migration stub, a CLI for manual dry-run/apply, unit test skeleton and documentation. The intent is to provide a safe feature branch (`feat/self-upgrade`) that contains the scaffolding required to implement a production-grade self-upgrade flow.

Why
---
- Enable automated, auditable, safe server upgrades (rolling updates with health checks and rollback).
- Provide a staging area for building CI workflows and apps/desktop update publishing (paired with electron-updater).

What changed (high level)
-------------------------
- `zeta_vn/app/worker/self_upgrade.py` — self-upgrade task runner (dry-run default).
- `zeta_vn/app/utils/k8s_client.py` — minimal k8s wrapper (stubs to be expanded to real k8s client).
- `zeta_vn/data/models/release_model.py` — dataclass model for release audit.
- `zeta_vn/data/migrations/011_release_table.py` — migration stub.
- `zeta_vn/tests/unit/test_self_upgrade.py` — simple unit test (dry-run).
- `tools/self_upgrade/cli.py` — CLI to manual-run dry-run/apply.
- `docs/SELF_UPGRADE.md` — usage and notes.

Files to review (suggested commit breakdown)
------------------------------------------
1. feat(self-upgrade): add task skeleton and docs
   - `zeta_vn/app/worker/self_upgrade.py`
   - `docs/SELF_UPGRADE.md`

2. feat(self-upgrade): add k8s client wrapper and CLI
   - `zeta_vn/app/utils/k8s_client.py`
   - `tools/self_upgrade/cli.py`

3. feat(self-upgrade): add release model + migration + tests
   - `zeta_vn/data/models/release_model.py`
   - `zeta_vn/data/migrations/011_release_table.py`
   - `zeta_vn/tests/unit/test_self_upgrade.py`

Testing
-------
- Unit tests: `pytest -q e:\zeta\zeta_vn\tests\unit\test_self_upgrade.py` (already included and passing locally for dry-run).
- Lint: run `ruff check zeta_vn` in your environment.
- Integration: (manual) draft workflow added as next step to run in a test k8s cluster (kind/k3s) to validate rollout/rollback.

CI / Workflows (proposed)
-------------------------
1. `.github/workflows/self-upgrade-integration.yml` (manual_dispatch)
   - Build test image, push to test registry.
   - Run a job that invokes `tools/self_upgrade/cli.py` in dry-run mode, then in apply mode against a kind/k3s cluster (or mocked k8s via pytest).
2. Update `publish-desktop.yml` to emit `release.json` containing `{version, assets, sha256}` as release metadata (used by self-upgrade and apps/desktop auto-update tests).

Operator safety & checklist (must pass before enabling in production)
-----------------------------------------------------------------
- [ ] Replace `k8s_client` stubs with production-grade `kubernetes` python client implementation.
- [ ] Add DB migration to persist `release_records` and wire into audit tables.
- [ ] Add RBAC checks + operator approval gates for upgrades that include DB migrations.
- [ ] Add CI integration tests that run in a disposable k8s cluster (kind/k3d) and validate rollout/rollback behavior.
- [ ] Add logging/metrics for upgrade progress and failures (Prometheus counters + traces).
- [ ] Create GitHub Release publishing pipeline for apps/desktop artifacts and release metadata.

Requirements coverage
---------------------
- Self-updater skeleton: Done (scaffold + CLI + docs).
- Production k8s integration: Deferred (requires `kubernetes` client + infra).
- CI integration: Draft/proposed (not yet implemented).

How to review
-------------
1. Checkout a feature branch and apply these changes: create branch `feat/self-upgrade` and commit the files.
2. Run linter: `ruff check zeta_vn` and fix any environment-specific issues.
3. Run unit tests: `python -m pytest -q e:\zeta\zeta_vn\tests\unit\test_self_upgrade.py`.
4. Inspect `zeta_vn/app/utils/k8s_client.py` and replace stubs with a real client implementation in a follow-up PR.

Notes
-----
- This PR intentionally provides a safe, minimal foundation. The real rollout/rollback logic and CI deployment must be implemented in a follow-up once the k8s client and operator safety checks are in place.

Prepared-by: automated PR draft generator
