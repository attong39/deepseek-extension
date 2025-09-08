# ZETA AI — E2E Blueprint (2025 Upgrade)

This blueprint consolidates the end-to-end architecture and upgrade path for the Desktop–Server AI assistant, aligned with the current repository structure (Clean Architecture: app/core/data) and ready for 2025 reliability, security, and scale.

---

## 1) System Overview & Scope

- Context: Desktop client (Electron/React) provides UI and an on-device Agent; apps/backend (FastAPI/Python) orchestrates LLM, memory, planning, learning, analytics.
- Architecture: Clean Architecture
  - app/: FastAPI routers (v1/v2), controllers (apps/desktop/mobile/voice), websockets, middleware (auth, rate-limit, logging, security), serializers/validators, exception handlers.
  - core/: entities, value objects, use_cases (agents/chat/memory/planning/learning/reflexion), services, specifications & policies.
  - data/: repositories, SQLAlchemy models, external clients (LLMs, Redis, S3, Vector DB), migrations.
- Realtime: WebSockets under `app/api/websockets` (e.g., `chat_router`).
- Datastores: PostgreSQL (primary), Redis (cache/broker), Vector DB (Chroma/Pinecone/Weaviate), S3-compatible storage.
- Current code highlights
  - Unified v1 API router: `app/api/v1/router.py` with `api_v1_router`, wired once in `app/main.py`.
  - Health endpoints: `/health` and `/api/v1/health` live and passing.
  - Settings: Pydantic v2 via `config/settings/base.py` (`get_settings()`), CORS applied.
  - DB compatibility: JSONB replaced with SQLAlchemy `JSON` in models for cross-dialect dev (SQLite) while keeping Postgres ready.
  - DI: `app/dependencies.py` centralizes auth, RBAC stub, service/repository factories.

Targets 2025
- Performance: p95 API < 200ms; chat streaming < 2s first-token; memory retrieval < 100ms.
- Scalability: 10k concurrent users, autoscale (HPA), zero-downtime deploys.
- Security: JWT + RBAC; content safety; audit trails; rate-limiting; secret management.
- Observability: Prometheus + Grafana; OpenTelemetry tracing; ELK logs.
- Direction: Modular by domain; normalized API surfaces v1/v2; microservice-ready hotspots (vector search, file ops, voice).

---

## 2) Reference Architecture (Logical & Deployment)

### 2.1 Logical View (Clean Architecture)
- UI/Desktop Client: React overlay + hotkeys; communicates over HTTPS/WebSocket; Desktop Agent executes approved plans (mouse/keyboard, OCR/ASR).
- Interface Layer (app/):
  - Routers: `app/api/v1` (aggregated), future `app/api/v2`.
  - Controllers: `app/controllers/*` (apps/desktop/mobile/voice/system/analytics/...)
  - WebSockets: `app/api/websockets` (e.g., chat streaming)
  - Middleware: `app/api/middleware` (security, logging, rate limit)
  - Validators/Serializers: `app/validators`, `app/serializers` (to standardize In/Out DTOs)
  - Exceptions: `app/exceptions.py` (registered in `app/main.py`)
- Domain Layer (core/):
  - Entities: Agent, Chat, Message, Memory, User, Task, ...
  - Value Objects: AgentConfig, ConversationContext, Embedding, ...
  - Use-Cases: agents/chat/memory/planning/learning/reflexion
  - Services: agent_orchestrator, memory_manager, workflow_engine
  - Policies/Specifications: safety and constraints
- Data Layer (data/):
  - Repositories: agent/chat/memory/user/vector/audit/analytics
  - Models: SQLAlchemy models with JSON where portable
  - External Clients: OpenAI/Anthropic/HF, Redis, S3, Pinecone/Weaviate/Chroma, ES/email
  - Migrations/Seeds

### 2.2 Deployment View
- Core app: FastAPI (uvicorn) + Celery workers/beat in containers.
- Datastores: Postgres (RDS/CloudSQL), Redis, Vector DB (managed/self-hosted), S3-compatible store (MinIO/AWS S3).
- Edge/Gateway: Nginx/Ingress terminates TLS; routes /api & /ws.
- Observability: Prometheus, Grafana, Jaeger/Tempo, ELK, Alertmanager.
- Autoscaling: K8s HPA (CPU/RAM/queue length), rolling updates.
- Strategy: Start monolith (modular), split microservices for vector/files/voice as load grows.

---

## 3) End-to-End Dataflows

### 3.1 Chat → Plan → Act
1) Desktop UI sends JWT-authenticated request via `/api/v1/chat` or `/ws/chat`.
2) app/: middleware adds request-id, rates limit; serializers/validators normalize input.
3) core/: Chat use-case invokes Agent Orchestrator → LLM Adapter + Memory Manager (RAG) to generate reply + plan (tool-calls).
4) policy & safety: SecurityManager/RuleEngine vet the plan (scope, permissions, risk score). Emit `plan.approved` if okay.
5) response streaming: stream tokens + plan to UI; Desktop Agent subscribes and executes steps; reports progress.
6) audit: all steps/logs persisted to AuditRepo + Analytics.

### 3.2 Memory/RAG Flow
- Ingest: files/URLs → split + embed → write VectorRepo + metadata in Postgres.
- Query: conversation context → retrieve top-k → context packer → LLM → answer; Redis caches for repeated queries/embeddings.

### 3.3 Continual Learning
- Feedback (thumbs up/down, step success/fail) → Analytics + training queue.
- Worker performs distillation/LoRA or prompt refinement; feature-flagged configs for canary rollout.

### 3.4 Observability Flow
- Each request: trace spans across gateway/router/use-case/repo; metrics (latency, RPS, errors); structured logs with correlation-id; alerts on SLO breaches.

---

## 4) Security & Compliance Model

- Identity & Access
  - AuthN: OAuth2/JWT (Bearer) + refresh; optional mTLS for internal.
  - AuthZ (RBAC): roles → permissions (agent CRUD, chat history, admin:*). Policies enforced in use-cases.
- Safety & Governance
  - Input safety: size/MIME limits, content filters.
  - Action safety: allow-list tools; scoped selectors; panic hotkey; human-in-the-loop for risky actions.
  - Audit: immutable audit log (who/when/what/result), PII redaction, retention policy.
- Data Protection
  - At-rest: DB TDE/pgcrypto; object-store SSE; secrets via KMS/Vault.
  - In-transit: TLS 1.2+; secure cookie for refresh; CSRF for forms.
  - Tenancy: org_id/user_id namespaces; row-level filters in repos.
- Platform Security
  - Rate limiting per user/endpoint; WAF; CORS/CSP headers; dependency audit; SBOM & supply-chain checks.

---

## 5) Agent Boundary & Contract

- Desktop Agent (On-device)
  - Capabilities: OCR/ASR local, screen read, mouse/keyboard, window control.
  - Trust boundary: execute only signed plan with HMAC + nonce/timestamp; timeboxed; revocable.
  - Telemetry: step results + (redacted) screenshots → server audit.
- Server Planner/Orchestrator
  - Emits Plan DSL (JSON schema): steps, selectors, preconditions, rollback, max_duration.
  - Policy check → sign → publish; map tools ↔ apps/desktop capabilities; idempotent steps.
- Handshake
  - Agent receives JWT/HMAC + TTL; verifies; executes; returns status/outputs. Server can re-plan on mismatch.

---

## 6) API Surface (v1/v2 — REST & WS)

- Versioning & Names follow current layout; v1 aggregated via `app/api/v1/router.py`.

### 6.1 Auth & Health
- POST /api/v1/auth/login → { email, password } → { access_token, refresh_token }
- POST /api/v1/auth/refresh → { refresh_token } → { access_token }
- GET  /api/v1/health → { status, version, components? }

### 6.2 Agents
- POST /api/v1/agents → create agent
- GET  /api/v1/agents/{id}
- PATCH /api/v1/agents/{id}
- DELETE /api/v1/agents/{id}

Request example
```json
{
  "name": "Desktop Helper",
  "model": "gpt-4o",
  "capabilities": ["chat", "planning", "vision"],
  "config": {"temperature": 0.4}
}
```

### 6.3 Chat & Planning
- POST /api/v1/chat → sync answer (or stream via /ws/chat)

Request example
```json
{
  "agent_id": "agt_123",
  "message": "Rename 10 files by pattern and upload to Drive",
  "context": {"window": "Explorer", "selection": ["*.png"]}
}
```

Response (simplified)
```json
{
  "reply": "I'll plan the steps and start.",
  "plan": {
    "id": "pln_abc",
    "steps": [
      {"tool": "find_files", "args": {"pattern": "*.png"}},
      {"tool": "rename_batch", "args": {"rule": "img_{n}.png"}},
      {"tool": "upload", "args": {"dest": "Drive:/Design/"}}
    ],
    "ttl_s": 120,
    "signature": "hmac..."
  }
}
```

### 6.4 Memory (RAG)
- POST /api/v1/memory/store → ingest documents { source, text|file }
- POST /api/v1/memory/search → { query, k, filters } → { matches: [{chunk, score, source}] }
- DELETE /api/v1/memory/{id}

### 6.5 Files
- POST /api/v1/files (multipart) → upload; returns file_id + checksum + mime
- GET  /api/v1/files/{id} → download (scoped; signed URLs)

### 6.6 Analytics & Audit
- GET /api/v1/analytics/usage?from=&to=
- GET /api/v1/admin/audit?actor=&resource=&from=&to=

### 6.7 WebSockets
- /ws/chat → stream tokens & tool-calls
- /ws/agent/{agent_id} → push plan progress, receive step_receipts

Schemas: Prefer Pydantic v2; separate `*_In` (request) and `*_Out` (response) in `app/serializers`; domain Value Objects in `core/value_objects`.

---

## 7) Non‑Functional Requirements (SLOs & Quality Gates)

- Performance: p50 < 80ms; p95 < 200ms; streaming TTFB < 500ms; vector query < 80ms.
- Reliability: 99.9% uptime; RTO < 5m; backups daily; circuit breaker & retries.
- Security: no secrets in code; SBOM; weekly deps audit; quarterly pentest.
- Quality: ruff + mypy strict; unit+integration+e2e ≥ 80% (core ≥ 90%); style & ADR updated.
- Observability: golden signals + business KPIs; SLO alerts & error budgets.

---

## 8) Upgrade Plan (fit current project)

- Phase A — Foundation (week 1–2)
  - Standardize serializers/validators/exceptions; enable ruff+mypy; OpenTelemetry middleware; WS chat streaming.
- Phase B — RAG & Caching (week 3–4)
  - Solid ingest pipeline; Redis caching for embeddings/search; HMAC plan signing + nonce.
- Phase C — Security Hardening (week 5–6)
  - RBAC policies, role-based rate limits; content safety filter; complete audit log; secrets via Vault/KMS.
- Phase D — Scale & Observability (week 7–8)
  - K8s manifests (HPA, probes); dashboards & alert rules; canary rollout for model/config.

Deliverables: OpenAPI spec, system/deployment/dataflow diagrams, runbooks (incident, backup/restore), CI/CD gates (lint/type/test/sec).

---

## 9) Concrete To‑Dos (next 2 sprints)

- API: finalize `/api/v1/chat` streaming and `/api/v1/memory/search` filters; add `/api/v1/admin/audit`.
- Security: implement RBAC matrix; role-based rate limiting; HMAC plan signing.
- Observability: add request-id propagation; trace use-cases & repos; baseline SLOs.
- Desktop Agent: implement Plan DSL executor + panic hotkey; step receipts protocol.
- Docs: publish OpenAPI; sequence diagrams; ADRs for Plan DSL & safety gates.

---

## Appendix — Code Pointers (current repo)

- Entrypoint: `zeta_vn/app/main.py` — includes `api_v1_router`, sets CORS and health.
- V1 Aggregator: `zeta_vn/app/api/v1/router.py` — bundles routers: auth, health, agents, assistants, chat, memory, planning, reflexion, learning, files, analytics, admin, system, voice.
- Health: `zeta_vn/app/api/v1/health.py` and top-level `/health` in `app/main.py`.
- DI: `zeta_vn/app/dependencies.py` — central auth (HTTPBearer), RBAC stub, service/repo factories, lazy DB session.
- Settings: `zeta_vn/config/settings/base.py` — Pydantic v2 settings (`get_settings()`, `get_cors_config()`).
- WebSockets: `zeta_vn/app/api/websockets/` (e.g., `chat_router`).
- Controllers: `zeta_vn/app/controllers/` — apps/desktop, mobile, voice, system, analytics, stream, webhook, etc.
- Models: `zeta_vn/data/models/*` — use `JSON` for portable columns; tables created successfully in dev.
- Core: `zeta_vn/core/*` — domain entities, services, use_cases, repository interfaces.

> Note: Keep endpoints thin; push business logic into `core/use_cases` and `core/services`. Use DI from `app/dependencies.py` to wire repositories and services into routes.
