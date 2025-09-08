# Consolidation Checklist (Quick)

Use this short checklist when cleaning up duplicates and keeping imports consistent.

## 1) Update references (imports) from redundant → canonical

- Preview
  - `python scripts/update_references.py --plan reports/consolidation_plan/plan.json --root . --dry-run`

- Apply
  - `python scripts/update_references.py --plan reports/consolidation_plan/plan.json --root . --apply`

- Logs: `reports/reference_updates/<timestamp>/changes.json`

## 2) Apply consolidation plan (move redundant to trash, optional shims)

- Preview
  - `python scripts/apply_consolidation_plan.py --plan reports/consolidation_plan/plan.json --root . --dry-run`

- Apply
  - `python scripts/apply_consolidation_plan.py --plan reports/consolidation_plan/plan.json --root . --apply`

- Trash + log
  - `reports/consolidation_trash/<timestamp>/`
  - `.../apply_actions.log`

## 3) Audit (quick)

- `python scripts/consolidation_audit.py --root . --report-dir reports/quick_audit --no-near`
- Check reports under `reports/quick_audit/<timestamp>/`

## 4) Clean old reports (optional)

- Preview
  - `python scripts/cleanup_reports.py --days 14 --dry-run`

- Apply
  - `python scripts/cleanup_reports.py --days 14 --apply`

## 5) Optional tasks

- Backend tests
  - `python -m pytest backend/tests -q`

- Desktop build
  - `npm --prefix desktop ci`
  - `npm --prefix desktop run build`

---

Tip: You can enable a sample pre-commit hook to run a quick audit automatically:

```bash
git config core.hooksPath tools/git-hooks
```
