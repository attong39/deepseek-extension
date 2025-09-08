# Vault Integration (KV v2)

## Mount & Paths
- Mount: `kv/` (KV v2)
- Paths ví dụ:
  - `kv/zeta/prod/api`: `OPENAI_API_KEY`, `DATABASE_URL`, `JWT_SECRET`
  - `kv/zeta/prod/observability`: `SLACK_WEBHOOK`, `PAGERDUTY_ROUTING_KEY`

## Auth Methods
- Kubernetes Auth (prod): ServiceAccount `api-server` => Role `zeta-api`.
- Local/dev: `vault login` với token tạm.

## Policies (ví dụ)
```
path "kv/data/zeta/prod/api" {
  capabilities = ["read"]
}
path "kv/data/zeta/prod/observability" {
  capabilities = ["read"]
}
```

## Inject qua Vault Agent (K8s)
- Annotations cho Pod:
  - `vault.hashicorp.com/agent-inject: "true"`
  - `vault.hashicorp.com/role: "zeta-api"`
  - `vault.hashicorp.com/agent-inject-secret-env: "kv/data/zeta/prod/api"`
- Template env (ví dụ):
```
{{- with secret "kv/data/zeta/prod/api" -}}
OPENAI_API_KEY={{ .Data.data.OPENAI_API_KEY }}
DATABASE_URL={{ .Data.data.DATABASE_URL }}
JWT_SECRET={{ .Data.data.JWT_SECRET }}
{{- end }}
```

## Quy trình
1) Ops thêm secrets vào Vault theo path.
2) K8s Pod có annotations -> Vault Agent sidecar render file env hoặc set as env.
3) Ứng dụng đọc từ env/file đã inject (không còn cần `.env.production`).
