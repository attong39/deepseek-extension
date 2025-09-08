# Adopting Root Configs Gradually

Subprojects can extend root configs when convenient. No mandatory changes required.

## TypeScript
- In `apps/desktop/tsconfig.json` and `extension/tsconfig.json`:
```jsonc
{
  "extends": "../tsconfig.base.json",
  // ...existing options...
}
```
- In `.eslintrc.*` for apps/desktop/extension:
```js
module.exports = {
  extends: ["../.eslintrc.base.cjs"],
  // ...existing rules...
};
```

## Python (apps/backend)
- Use `pyproject.base.toml` as reference; align line-length and targets
- Keep backend-specific tooling in `apps/backend/pyproject.toml`

## Formatting
- `.prettierrc.json` at root is the baseline; project overrides allowed

## CI
- Root CI (`ci-root.yml`) is additive and won’t replace existing workflows

## Rollback
- These changes are config-only. If any issue arises, simply stop extending the base and revert the config edits in the subproject.
