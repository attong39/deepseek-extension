# 🧩 Installation Guide - ZETA AI Server

Set up and run ZETA AI Server locally or in the cloud.

## 📦 Requirements

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js 18+ (if using frontend)
- Git, Docker (optional), Make (optional)

## 🔧 Local Setup (Without Docker)

1) Clone and create virtualenv
2) Install dependencies
3) Configure environment
4) Initialize database
5) Start services

### 1) Create Virtualenv

Windows (PowerShell):

- py -3.11 -m venv .venv
- .venv\Scripts\Activate.ps1

### 2) Install Dependencies

- pip install -U pip wheel
- pip install -r requirements.txt

### 3) Environment

Create .env file with:

- DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/zeta
- REDIS_URL=redis://localhost:6379/0
- SECRET_KEY=change_me
- OPENAI_API_KEY=sk-...

### 4) Database

- Create DB user and database
- Run migrations (alembic upgrade head)

### 5) Run Services

- API: uvicorn app.main:app --reload --port 8000
- Worker: celery -A app.worker.celery_app worker -l info
- Beat: celery -A app.worker.celery_app beat -l info

Verify: http://localhost:8000/api/v1/health

## 🐳 Docker Setup

- docker-compose up -d
- docker compose -f deployment/docker/docker-compose.prod.yml up -d

## ☸️ Kubernetes (Advanced)

- kubectl apply -f deployment/kubernetes/

## 🔗 References

- API Reference: ./API_REFERENCE.md
- OpenAPI Spec: ./api/openapi.yaml
- Troubleshooting: ./TROUBLESHOOTING.md

Last updated: 2025-08-14
