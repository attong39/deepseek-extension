# Quick Start - ZETA_AI Libraries

Hướng dẫn **cài đặt và chạy nhanh** dự án ZETA_AI với bộ thư viện tối ưu.

---

## 🚀 Server (Python) - FastAPI + RAG

### 1. Cài đặt Dependencies

```bash
# Core + các extras thông dụng
uv pip install -e ".[dev,db,security,rag,asr,ocr,obs,cloud,perf]"

# Hoặc cài theo nhu cầu cụ thể
uv pip install -e ".[dev,db,security,rag]"        # RAG-focused
uv pip install -e ".[dev,db,security,ocr,asr]"    # Document processing
uv pip install -e ".[dev,db,security,obs]"        # Production monitoring
```

### 2. External Dependencies (Required)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr poppler-utils ffmpeg

# macOS
brew install tesseract poppler ffmpeg

# Windows (Chocolatey)
choco install tesseract poppler ffmpeg
```

### 3. Database Setup

```bash
# PostgreSQL với pgvector (recommended)
docker run -d --name zeta-postgres \
  -e POSTGRES_DB=zeta_ai \
  -e POSTGRES_USER=zeta \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Redis cho cache và rate limiting
docker run -d --name zeta-redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 4. Environment Setup

```bash
# .env file
cp .env.example .env

# Cấu hình cơ bản
DATABASE_URL=postgresql://zeta:your_password@localhost:5432/zeta_ai
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_super_secret_key_here
DEBUG=True
```

### 5. Run Server

```bash
# Migration (first time)
uv run alembic upgrade head

# Development server với auto-reload
uv run uvicorn zeta_vn.application.api.main:app --reload --port 8000

# Production server
uv run uvicorn zeta_vn.application.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6. Health Check

```bash
# API health
curl http://localhost:8000/api/v1/health

# Metrics
curl http://localhost:8000/metrics

# OpenAPI docs
open http://localhost:8000/docs
```

---

## 💻 Desktop (Electron + React)

### 1. Prerequisites

```bash
# Install Node.js 18+ và pnpm (recommended)
npm install -g pnpm

# hoặc sử dụng npm/yarn
npm --version  # should be >=9.0
```

### 2. Install Dependencies

```bash
cd desktop_ai_zeta

# Install với pnpm (fastest)
pnpm install

# hoặc npm
npm install
```

### 3. API Codegen (Optional)

```bash
# Generate TypeScript types từ server OpenAPI
pnpm run codegen:api

# Sync WebSocket schemas
pnpm run ws:sync
```

### 4. Development

```bash
# Dev server với HMR
pnpm run dev

# Type checking
pnpm run type-check

# Linting
pnpm run lint
pnpm run lint:fix
```

### 5. Build & Package

```bash
# Build for development
pnpm run build

# Package cho distribution
pnpm run dist         # Auto-detect platform
pnpm run dist:win     # Windows
pnpm run dist:mac     # macOS
pnpm run dist:linux   # Linux
```

### 6. Testing

```bash
# Unit tests
pnpm run test

# Watch mode
pnpm run test:watch

# UI test runner  
pnpm run test:ui
```

---

## 🔧 Development Workflow

### Quality Gates (Server)

```bash
# Chạy tất cả quality checks
uv run pytest -q --cov=zeta_vn --cov-fail-under=95
uv run ruff check . && ruff format --check .
uv run mypy zeta_vn
uv run bandit -r zeta_vn
uv run pip-audit
```

### Quality Gates (Desktop)

```bash
cd desktop_ai_zeta

# Chạy tất cả checks
pnpm run test
pnpm run type-check  
pnpm run lint
```

### End-to-End Test

```bash
# 1. Start server
uv run uvicorn zeta_vn.application.api.main:app --port 8000 &

# 2. Start apps/desktop app
cd desktop_ai_zeta && pnpm run dev &

# 3. Test integration
curl -X POST http://localhost:8000/api/v1/documents \
  -H "Content-Type: application/json" \
  -d '{"content": "Test document", "metadata": {}}'
```

---

## 📋 Feature Matrix

### Available Extras

| Extra | Dependencies | Use Case |
|-------|-------------|----------|
| `dev` | pytest, ruff, mypy | Development tooling |
| `db` | psycopg, alembic | Database với migrations |
| `security` | jose, passlib, limiter | Auth + rate limiting |
| `rag` | faiss, sentence-transformers | Vector search + embeddings |
| `llm` | transformers, accelerate | Local LLM inference |
| `asr` | faster-whisper, librosa | Speech recognition |
| `ocr` | pytesseract, opencv | Document OCR |
| `obs` | opentelemetry, sentry | Monitoring + tracing |
| `cloud` | boto3, minio, gcs | Object storage |
| `queue_arq` | arq | Async task queue |
| `queue_celery` | celery, redis | Classic task queue |
| `serialize` | msgspec, orjson | High-performance serialization |
| `perf` | uvloop, httptools | Linux performance |

### Platform Considerations

```bash
# macOS ARM64 - skip faiss-cpu, use pgvector
uv pip install -e ".[dev,db,security,rag]" --no-deps
uv pip install sentence-transformers pgvector

# Windows - lightweight OCR setup
uv pip install -e ".[dev,db,security,rag,obs]"
# Manual: install Tesseract from GitHub releases

# Linux - full stack with GPU support
uv pip install -e ".[dev,db,security,rag,llm,asr,ocr,obs,perf]"
# GPU: pip install torch --index-url https://download.pytorch.org/whl/cu124
```

---

## 🐳 Docker Quickstart

### Server Container

```dockerfile
# Dockerfile.server
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml ./
RUN pip install uv && uv pip install -e ".[db,security,rag,obs,perf]"

COPY . .
EXPOSE 8000

CMD ["uvicorn", "zeta_vn.application.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  zeta-server:
    build:
      context: .
      dockerfile: Dockerfile.server
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://zeta:password@postgres:5432/zeta_ai
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  postgres:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_DB=zeta_ai
      - POSTGRES_USER=zeta
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

```bash
# Run với Docker
docker-compose up -d

# Health check
curl http://localhost:8000/api/v1/health
```

---

## 🚨 Troubleshooting

### Common Issues

1. **`ModuleNotFoundError: No module named 'xxx'`**
   ```bash
   uv pip install -e ".[dev]"  # Reinstall dependencies
   ```

2. **FAISS installation fails on ARM64**
   ```bash
   # Use pgvector instead
   uv pip install pgvector
   ```

3. **OCR not working**
   ```bash
   # Install Tesseract system package first
   which tesseract  # Should return path
   tesseract --version  # Should show version
   ```

4. **Desktop app won't start**
   ```bash
   cd desktop_ai_zeta
   rm -rf node_modules package-lock.json
   pnpm install
   ```

5. **Permission denied (Linux)**
   ```bash
   sudo chown -R $USER:$USER ~/.cache/uv
   ```

### Debug Mode

```bash
# Server debug với detailed logs
DEBUG=1 LOG_LEVEL=DEBUG uv run uvicorn zeta_vn.application.api.main:app --reload

# Desktop debug với DevTools
cd desktop_ai_zeta
NODE_ENV=development pnpm run dev
```

### Performance Tuning

```bash
# Server - enable production optimizations
uvloop=1 httptools=1 uvicorn zeta_vn.application.api.main:app --workers 4

# Desktop - disable unused features
# Edit electron/main.js: webSecurity: false, devTools: false
```

---

## 📈 Next Steps

1. **Thêm authentication**: Implement JWT + RBAC
2. **Enhanced RAG**: Multi-modal embeddings + reranking
3. **Real-time features**: WebSocket + push notifications
4. **CI/CD**: GitHub Actions với quality gates
5. **Monitoring**: Grafana + Prometheus dashboards
6. **Security**: SAST/DAST + dependency scanning

---

**🎯 Goal**: Cài đặt và chạy được trong **< 5 phút** cho development, **< 15 phút** cho production setup.
