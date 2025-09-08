# P1 PR Checklist: Auto-update, Desktop Cache, Restart Policies

Use this checklist when preparing PRs for the P1 work (Electron auto-update, server auto-updater, apps/desktop cache, restart policies, Dependabot).

Files to add or update
- `desktop_ai_zeta/electron/main.js` — integrate `electron-updater` check on app ready and expose update UI.
- `desktop_ai_zeta/src/services/cache.ts` — implement SQLite-backed store (this repo contains `MemoryCache` skeleton already).
- `zeta_vn/core/self_improvement/auto_updater.py` — implement check & plan functions; wire Celery task in `app/worker/celery_app`.
- `.github/workflows/release-electron.yml` — release workflow (skeleton exists).
- `docker-compose.yml` / k8s manifests — add `restart: always` / liveness probes to reference `/api/v1/health`.
- `.github/dependabot.yml` — enable dependency updates for Python & Node.

PR Content
- Summary of change and why.
- List of files changed (short) and short description for each.
- How to test locally (commands / expected results).
- Acceptance: automation runs, update check works, cache hit/miss tests, container restart policy validated.

Testing Notes
- Desktop auto-update: test with a draft release / version bump in a controlled environment.
- Cache: write unit tests for `MemoryCache` and SQLite-backed store (TTL, LRU eviction).
- Auto-updater: test check_for_new_release() with a mocked index and ensure plan returned.

Security & Safety
- Ensure updates are signed & verify signature on client (electron-updater supports code signing).
- Server auto-updater should prefer operator approval or orchestrator-driven deployments.
