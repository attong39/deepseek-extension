# Code Standards

This document supplements the Vietnamese proposal with practical rules and examples.

## Conventional Commits
- Types: feat, fix, docs, style, refactor, test, chore, ci, perf, revert
- Examples:
  - feat(apps/desktop): add memory analytics dashboard
  - fix(apps/backend): handle None in embeddings pipeline
  - docs: update setup guide for Windows

## TypeScript
- TS strict mode on (extend tsconfig.base.json)
- ESLint extends from .eslintrc.base.cjs; fix autofixables
- Prefer zod for runtime validation; avoid any; use unknown + narrow

## Python
- Ruff check, Black format, type hints for public functions
- mypy for core modules when practical
- Prefer Pydantic v2 for models and settings

## PowerShell
- Windows PowerShell 5.1 compatible
- Comment-based help and clear exit codes

## Testing
- Aim for increasing coverage over time (60 → 70 → 80%)
- Unit for logic; integration for cross-layer flows; perf regularly

## Docs
- Docs-as-code; update alongside changes
- Keep runbooks, troubleshooting, and C4 diagrams versioned

See also: `docs/ZETA_CONSISTENCY_PROPOSAL_VN.md`.
