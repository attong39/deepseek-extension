# Import optimization across the monorepo

This repo includes helpers to clean up and organize imports for Python (backend) and TypeScript (extension, desktop).

## Python (backend)

- Tooling: Ruff (I) rules for import organization
- Check:
  - `npm run imports:py:check`
- Fix:
  - `npm run imports:py:fix`

Notes: Uses Poetry to run Ruff within `apps/backend`.

## TypeScript (extension, desktop)

- Tooling: ESLint with `plugin:import` rules
- Check:
  - `npm run imports:ts:check`
- Fix:
  - `npm run imports:ts:fix`

Rules applied:
- Remove duplicates, enforce first-imports, and consistent `import/order` with alphabetization and newlines between groups.

## Run all

`npm run imports:all`
