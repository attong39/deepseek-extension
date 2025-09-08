# DevEx & DevSecOps Checklist

Short checklist to enforce ruff/mypy/pytest/security tooling and CI/CD workflows.

1) Local dev (pre-commit)
- ruff --fix
- mypy --strict
- pytest -k "unit" (fast unit tests)
- bandit (security static checks)
- pip-audit (dependency vulnerabilities)

2) CI (GitHub Actions)
- Jobs: lint, typecheck, unit-tests, integration-tests (smoke), map-enforcer
- Build: containerized server & worker images; build apps/desktop (electron) artifact
- Security: run bandit and pip-audit; fail on high CVE

3) Releases
- Server: tagged docker image, Alembic migrations run automatically in deployment step
- Desktop: electron-builder artifacts + auto-update manifest

4) Infra (compose + orchestration)
- Compose file for dev: postgres + redis + qdrant + minio + server + worker
- Production: kubernetes manifests, secrets via Vault/KMS

5) Observability & Security
- Sentry for errors; Prometheus + Grafana for metrics; Jaeger for traces
- Audit events persisted to dedicated audit DB table; minimal PII retention

6) Quick run commands (dev)
```powershell
# create venv, install
python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -r requirements-dev.txt
# lint & tests
.venv\Scripts\ruff.exe check --fix .
.venv\Scripts\python.exe -m mypy zeta_vn
.venv\Scripts\pytest.exe -q tests/unit
```

---

Use this doc to seed CI jobs and pre-commit hooks.
