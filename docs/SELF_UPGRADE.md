Self-upgrade feature (skeleton)
=================================

This document describes the self-upgrade capability scaffold added under
`feat/self-upgrade` branch. It contains a minimal safe implementation to
orchestrate server rolling updates and a CLI for manual testing.

Quick start
-----------

1. Prepare a metadata JSON for a release, for example:

```json
{
  "release_id": "r1",
  "image": "myrepo/zeta-server:1.2.3",
  "checksum": "sha256:..."
}
```

2. Dry run:

```powershell
python -m zeta_vn.app.worker.self_upgrade release.json
```

3. Apply:

```powershell
python -m zeta_vn.app.worker.self_upgrade release.json --apply
```

Notes
-----
- This is intentionally a skeleton. Replace `k8s_client` stubs with a real
  implementation (official `kubernetes` python package) before enabling in prod.
- Add migrations to persist release audit history and integrate with RBAC.
