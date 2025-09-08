# AI Server Design (summary)

Mục tiêu: server FastAPI an toàn, audit-ready, serve plans cho apps/desktop client.

Core components

- FastAPI (HTTPS)
- Auth: OAuth2 + JWT for API requests (all endpoints protected)
- Core AI: wrapper over LLM provider(s) (OpenAI, Anthropic, HF)
- Rule Engine + Permission Manager: guard ở server trước khi sign plan
- SafetyEngine (optional): external safety checks (LLM-assisted or rules)
- DB: PostgreSQL + SQLAlchemy 2.0 + Alembic
- Background: Celery + Redis
- Cache / Rate limit: Redis
- Vector DB: Qdrant or pgvector
- Storage: MinIO / S3
- Observability: structlog + OpenTelemetry + Prometheus/Grafana
- Secrets: env + KMS (recommend HashiCorp/Vault in production)

Data flow

1. Client sends chat + context (screenshots/text summary/OCR result)
2. Server LLM generates reply + candidate plan (Plan DSL)
3. Server runs Rule Engine + permission checks
4. If safe, sign plan (HMAC) and return -> client executes
5. Actions & outcomes are audited and stored (for RL/fine-tune)

Encryption & PII

- Sensitive payloads (full screenshots, PII) should not be stored in plaintext.
- Use envelope encryption: generate per-object encryption key, encrypt with KMS-managed key.
- Transport: TLS; additionally encrypt large media before upload to object storage.

Recommendations for deployment

- Use separate machines for AI model calls (GPU) and API server.
- Use autoscaling groups and horizontal scaling behind LB.
- Enable tracing and sampling for sensitive endpoints.

Quick start (dev)

- Python 3.11
- Create venv + install requirements
- Start PostgreSQL + Redis (docker-compose)
- uvicorn app.main:app --reload
