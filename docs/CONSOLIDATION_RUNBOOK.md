# Monorepo Consolidation Runbook (Windows)

Safe steps to consolidate apps/zeta-ai-agent, apps/desktop, apps/backend under apps/ without disrupting current work.

## 1) Create a copy for dry run
```powershell
robocopy E:\zeta-monorepo E:\zeta-monorepo-dryrun /MIR `
  /XD .git node_modules .venv apps/backend\.benchmarks apps/backend\.ruff_cache `
  apps/zeta-ai-agent\node_modules apps/desktop\node_modules `
  apps/zeta-ai-agent\out apps/desktop\dist `
  /XF *.vsix *.db
```

## 2) Dry run and review plan
```powershell
Set-Location E:\zeta-monorepo-dryrun
# PowerShell dry-run (move mode)
powershell -NoProfile -ExecutionPolicy Bypass -File .\consolidate_monorepo.ps1 -DryRun | Tee-Object -FilePath .\consolidation_plan.txt

# Python dry-run (copy-swap with defaults)
python .\consolidate_monorepo.py --dry-run --mode copy-swap --report consolidation_plan.json

# Python dry-run with extra excludes
python .\consolidate_monorepo.py --dry-run --mode copy-swap --exclude .cache --exclude coverage --report consolidation_plan_excludes.json
```

Review both `consolidation_plan.txt` and `consolidation_plan.json`.

## 3) Apply in the copy and smoke test
```powershell
# Apply with PowerShell copy-swap and extra excludes
powershell -NoProfile -ExecutionPolicy Bypass -File .\consolidate_monorepo.ps1 -Force -CopySwap -Exclude .cache,coverage | Tee-Object -FilePath .\consolidation_apply.log

# Or apply with Python script in copy-swap mode
python .\consolidate_monorepo.py --mode copy-swap --exclude .cache --exclude coverage --report consolidation_apply.json

# Then update references
python .\tools\reference_updater.py              # dry-run
python .\tools\reference_updater.py --apply     # apply updates
```

Quick checks:
- `tree /A /F > post_consolidation_tree.txt`
- Node: `npm install` then build apps/desktop/agent workspaces
- Backend: create venv, run pytest if available

## 4) Initialize git in the copy and commit
```powershell
Set-Location E:\zeta-monorepo-dryrun
git init
git config core.longpaths true
git add .
git commit -m "chore: baseline before monorepo consolidation"
git checkout -b feat/monorepo-consolidation
git add .
git commit -m "feat: consolidate monorepo into apps/* + packages/shared"
```

Push and open a PR when ready.
