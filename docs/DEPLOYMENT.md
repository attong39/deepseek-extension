# 🚀 ZETA AI Server - Deployment Guide

- Prerequisites and required software
- Local development flow
- Docker images and Compose (dev/prod)
- Kubernetes deployment (namespace, DB/Redis, app, ingress)
- Terraform for infra, secrets, SSL, migrations job
- Health checks and smoke tests

## 🏠 Local Development

- Clone repo
- uv/venv setup
- .env configuration
- Start DB/Redis via compose
- Alembic migrations
- Run uvicorn, celery worker/beat

## 🐳 Docker Deployment

- Build app/worker images
- docker-compose.dev.yml and docker-compose.prod.yml
- Scaling workers

## ☸️ Kubernetes Deployment

- Helm pre-reqs
- Install PostgreSQL/Redis via Helm
- Apply manifests in deployment/kubernetes
- Ingress controller and rules

## 🌐 Production

- Terraform plan/apply
- Create K8s secrets (DATABASE_URL, REDIS_URL, SECRET_KEY, OPENAI_API_KEY)
- cert-manager for SSL
- Run migrations job
- Health checks: /api/v1/health, /api/v1/health/detailed

## 📈 Observability

- Prometheus/Grafana stack
- Metrics endpoint and sample queries
- ELK for logs
- Jaeger for tracing

## 🧰 Troubleshooting

- DB and Redis connectivity checks
- Worker logs and scaling
- Resource limits and kubectl top
- Performance tuning (DB, Redis, app)

## 💾 Backup & Recovery

- DB dump/restore
- File storage backup

## 📞 Support

- Docs, Issues, Discord, Email

Last updated: 2025-08-14
