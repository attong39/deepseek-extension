## 🔐 Secrets (Kubernetes/Vault)
- ❌ Không commit `.env.production` vào repo.
- ✅ K8s: tạo `zeta-ai-secrets` và mount với `envFrom.secretRef` (xem `deployment/k8s/secrets/secret-template.yaml`).
- ✅ Vault (khuyên dùng cho multi-env): xem `docs/VAULT.md` để inject secrets tự động qua Vault Agent.
