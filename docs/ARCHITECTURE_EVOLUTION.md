# Architecture Evolution and Backward Compatibility

Goal: add features without breaking existing ones. Keep the project consistent while evolving.

Guidelines:
- Prefer additive changes. Do not remove or rename public APIs in-place. Add new modules and keep a shim.
- Mark old APIs with a deprecation decorator and clear docstring notes. Communicate removal timelines.
- Keep routers thin. When routing moves, keep the old path as a proxy to the new handler during a grace period.
- Separate contracts from implementations (interfaces in `core`, adapters in `app`/`infrastructure`).
- Version externally visible APIs (e.g., `/api/v1/...`), introduce `/api/v2/...` only when necessary.

Recipe:
1) Introduce new implementation under the stable contract.
2) Add deprecation shims that forward to the new code and warn once per process.
3) Update tests to cover both old and new entry points until the grace period ends.
4) Announce in CHANGELOG with migration snippets.

Tools:
- `zeta_vn.core.utils.deprecation.deprecated` for functions; `warn_deprecated_module` for modules.
- Focus Guard to prevent duplicate implementations diverging.
