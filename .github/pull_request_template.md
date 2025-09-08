## PR Checklist

- [ ] Conventional Commit title (feat|fix|docs|style|refactor|test|chore): scope - summary
- [ ] Linked issue or context
- [ ] Lint passes locally
  - [ ] Backend: `poetry run ruff check .` and `black --check .`
  - [ ] Extension: `npm run lint` in `extension/`
  - [ ] Desktop: `npm run lint` in `apps/desktop/`
- [ ] Tests pass locally
  - [ ] Backend: `pytest -q`
  - [ ] Extension: `npm test`
  - [ ] Desktop: `npm test`
- [ ] Documentation updated (if applicable)
- [ ] Security considerations reviewed (secrets, deps, network)

## What does this PR change?

<!-- Describe changes concisely -->

## How was it tested?

<!-- Brief test notes, screenshots, or logs -->

## Additional Notes

<!-- Risks, rollbacks, follow-ups -->
