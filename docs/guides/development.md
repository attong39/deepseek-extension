# 🏗️ Development Guide - ZETA AI Server

Complete guide for developing, testing, and contributing to ZETA AI Server. This guide covers everything from setting up your development environment to advanced debugging techniques.

## 🚀 Development Environment Setup

### Prerequisites
- **Python 3.11+** (required for modern async features)
- **Docker Desktop** (for database and Redis)
- **Git** (latest version recommended)
- **IDE**: VS Code with Python extension (recommended)
- **Node.js 18+** (for frontend development, if applicable)

### 1. Project Structure Overview

```
zeta_ai_server/
├── zeta_vn/                    # Main application package
│   ├── app/                    # FastAPI application layer
│   │   ├── api/                # API routes and endpoints
│   │   ├── controllers/        # Request/response handlers
│   │   ├── serializers/        # Pydantic models for serialization
│   │   ├── validators/         # Input validation logic
│   │   ├── websockets/         # WebSocket handlers
│   │   └── worker/             # Celery background tasks
│   ├── core/                   # Domain layer (business logic)
│   │   ├── entities/           # Domain entities
│   │   ├── services/           # Business services
│   │   ├── use_cases/          # Application use cases
│   │   └── interfaces/         # Abstract interfaces
│   ├── data/                   # Data access layer
│   │   ├── repositories/       # Data repositories
│   │   ├── models/             # SQLAlchemy models
│   │   ├── dto/                # Data transfer objects
│   │   └── migrations/         # Database migrations
│   ├── config/                 # Configuration management
│   ├── tests/                  # Test suites
│   └── docs/                   # Documentation
├── scripts/                    # Development and deployment scripts
├── deployment/                 # Deployment configurations
├── tools/                      # Development tools and utilities
└── requirements/               # Python dependencies
```

### 2. Initial Setup

```bash
# Clone the repository
git clone https://github.com/your-org/zeta-ai-server.git
cd zeta-ai-server

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Install development dependencies
pip install -r requirements/development.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env.development

# Edit development environment
nano .env.development
```

**Essential development settings:**
```env
# Development Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/zeta_ai_dev
DATABASE_ECHO=true

# Redis
REDIS_URL=redis://localhost:6379/0

# Security (use weak keys for development)
SECRET_KEY=dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI Services (get your own keys)
OPENAI_API_KEY=sk-your-development-key
ANTHROPIC_API_KEY=sk-ant-your-key

# CORS (allow all for development)
CORS_ORIGINS=["*"]

# Email (use console apps/backend for development)
EMAIL_BACKEND=console
EMAIL_HOST=localhost
EMAIL_PORT=1025

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

### 4. Database Setup

```bash
# Start development services
docker-compose -f docker-compose.dev.yml up -d

# Verify services are running
docker-compose -f docker-compose.dev.yml ps

# Run database migrations
cd zeta_vn
python -m alembic upgrade head

# Load sample data (optional)
python scripts/load_sample_data.py
```

### 5. Development Server

```bash
# Terminal 1: Start FastAPI server
cd zeta_vn
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Celery worker
python -m celery -A app.worker.celery_app worker -l debug

# Terminal 3: Start Celery beat (for scheduled tasks)
python -m celery -A app.worker.celery_app beat -l debug

# Terminal 4: Start Celery flower (task monitoring)
python -m celery -A app.worker.celery_app flower --port=5555
```

**Verify setup:**
- API: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health
- Flower: http://localhost:5555

## 🧪 Testing Strategy

... (full testing strategy and examples as in source docs) ...

## 🐞 Debugging Guide

... (logging configuration, debugging tools, scenarios) ...

## 🛠️ Code Quality Tools

... (pre-commit, ruff, mypy, bandit, radon) ...

## 📈 Performance Monitoring

... (SQL monitoring, middleware, memory profiling) ...

## 🚀 Development Workflow

... (git workflow, CI guidance) ...

## 📚 Advanced Topics

... (custom middleware, exception handlers, background tasks) ...

## 🔎 Troubleshooting

... (common issues and fixes) ...

---

**Happy Coding! 🎉**

*This development guide is continuously updated. Last revision: 2025-08-14*
