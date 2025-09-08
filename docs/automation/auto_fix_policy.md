# Auto-fix Policy & Automation

This document describes the `auto-fix` automation: what it does, when it creates PRs, and the safety policy.

Purpose
-------
Keep the repository tidy and reduce human overhead by automatically applying non-invasive fixes (formatting, import sorting, lint auto-fixes) and proposing them via Pull Requests. Avoid automatic logic-changing edits without human review.

Scope
-----
- Tools: `ruff` (format & fixes), `mypy` (typecheck), `pytest` (tests)
- Workflow: `.github/workflows/auto-fix.yml` runs daily or on-demand.

Rules
-----
1. The workflow runs `ruff --fix` and `ruff format` to apply auto-fixable lint changes.
2. After fixes, the workflow runs `mypy` and `pytest`.
3. If fixes produced file diffs and both `mypy` and `pytest` pass, the workflow opens a regular PR with the changes.
4. If fixes produced diffs but `mypy` or `pytest` fail, the workflow opens a draft PR for manual investigation.
5. The workflow never auto-merges changes. Maintainers review and merge explicitly.

Branch & Commit Conventions
--------------------------
- Branch: `auto/fixes/<run_id>`
- Commit message: `chore: apply auto-fixes (ruff/format)`
- PR title: `chore(auto-fix): apply lint/type fixes`

Low-risk vs High-risk
---------------------
- Low-risk (auto-fix and merge allowed after tests): formatting, import sorting, removing unused imports, trivial type annotations.
- High-risk (must be reviewed): refactors that change public API, barrel rewrites, changes to domain logic.

Rollout Plan
------------
1. Week 0: Enable workflow to create PRs only (no auto-merge). Monitor and triage.
2. Week 1: Tweak rules to reduce noise (whitelist/blacklist directories).
3. Week 2+: Optionally allow auto-merge for very low-risk cases after team agreement.

Troubleshooting
---------------
- If a PR by the bot contains unexpected changes: revert branch and investigate CI logs.
- If the workflow fails to run: check Actions permissions and `GITHUB_TOKEN` usage.

Contact
-------
For questions about automation policy, ping the `#devops` channel or open an issue in this repo with label `automation`.

Auto-barrel (regen `__all__`)
--------------------------------
To address barrel drift and PLE0605/TID252 issues, we run a separate workflow `auto-barrel.yml` that executes `tools/autobarrel_python.py` to regenerate `__all__` exports across packages.

Behavior
- Runs daily (03:00 UTC) and can be dispatched manually.
- After regeneration, the workflow formats files and inspects git diff.
- If there are no changes, the workflow exits.
- If changes exist and the total changed files <= threshold (default 30), the workflow creates a single PR containing all changes.
- If changes exceed the threshold, the workflow splits changes into multiple PRs grouped by top-level folder (one PR per folder).

Policy
- `auto-barrel` is PR-only (no auto-merge). Each PR includes a description of changed barrel files and requests a human review.
- The default threshold is 30 files; maintainers may tune via workflow inputs or CI config.

Testing locally
- Run `python tools/autobarrel_python.py` and inspect `git status`/`git diff` to see what would change.

Rollout notes
- Start with PR-only for at least one week to ensure exports are correct and avoid accidental public-API changes.
- If the pattern is stable, consider lowering the threshold or enabling auto-merge for trivial barrel-only changes after team agreement.
