# Deprecation Policy

We evolve without breaking existing users by following a clear deprecation policy.

- Signal: Mark old APIs with `@deprecated(reason=..., removal_version=..., alternative=...)`.
- Shim period: Keep deprecated paths for at least one minor release (or 30 days for internal users).
- Telemetry: Log and count usage of deprecated endpoints to track readiness to remove.
- Removal: Only remove after usage is negligible and the removal date has been communicated.

Example:
- Old: `core/events/event_bus.py` (legacy). New: `infrastructure/events/event_bus.py`.
  Keep the legacy as a thin adapter that warns and forwards to the infra bus.
