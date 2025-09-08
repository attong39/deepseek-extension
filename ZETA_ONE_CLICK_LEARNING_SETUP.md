# 🎯 "One‑Click Learning + RAG + DevSecOps" - Complete Setup Guide

## 📋 Overview

Bộ thư viện đầy đủ cho **Desktop (Electron + React) + AI‑Server (FastAPI)** với nguyên tắc:
- 🖥️ **CPU‑first, GPU‑ready** - Chạy CPU mặc định, bật GPU qua `ZETA_USE_GPU=1`
- 🔄 **Type‑safe** - OpenAPI → TypeScript, Pydantic v2
- 🛡️ **DevSecOps** - Tất cả qua `uv` thay thế Poetry
- 🔌 **Drop‑in ready** - Copy-paste và chạy ngay

## 🏗️ Architecture Overview

```
zeta-monorepo/
├── apps/backend/          # 🚀 FastAPI AI Server
│   ├── pyproject.toml     # uv dependencies
│   ├── app/
│   │   ├── rag/           # CPU-first RAG engine
│   │   ├── asr/           # Faster-Whisper ASR
│   │   ├── ocr/           # PaddleOCR
│   │   ├── websockets/    # Real-time chat
│   │   └── api/v1/        # Clean DI routers
│   └── tests/
├── apps/desktop/          # 💻 Electron + React
│   ├── package.json       # Node dependencies
│   ├── src/
│   │   ├── api/           # Auto-generated types
│   │   ├── components/    # React components
│   │   └── lib/           # WebSocket client
│   └── electron/
└── scripts/               # 🔧 Setup automation
```

## 🚀 Quick Start

```bash
# 1️⃣ Setup Backend (uv-based)
cd apps/backend
uv sync
uv run uvicorn app.main:app --reload

# 2️⃣ Setup Frontend (pnpm-based)
cd apps/desktop
pnpm install
pnpm openapi:gen  # Generate types from backend
pnpm electron:dev

# 3️⃣ Test GPU support (optional)
export ZETA_USE_GPU=1
uv run python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

---

## 📦 Dependencies & Tech Stack

### Backend (FastAPI + AI)
- **Core**: FastAPI ≥ 0.115, uvicorn, Pydantic v2
- **Database**: PostgreSQL + pgvector, SQLModel
- **RAG**: Sentence-Transformers + FAISS-CPU (+ Qdrant optional)
- **OCR/ASR**: PaddleOCR + Faster-Whisper (CPU-first)
- **Auth**: JWT + RBAC with slowapi rate-limiting
- **DevSecOps**: ruff, mypy, pytest, bandit, pip-audit

### Frontend (Electron + React)
- **Core**: Electron + React + Vite + TypeScript
- **State**: TanStack React Query + Zustand
- **Types**: Auto-generated from OpenAPI (openapi-typescript)
- **UI**: Radix UI + TailwindCSS + Lucide icons
- **WebSocket**: reconnecting-websocket with type safety

---

## 🎯 Key Features

### ✅ CPU-First, GPU-Ready
- All AI pipelines default to CPU
- GPU activation via `ZETA_USE_GPU=1` environment variable
- Automatic fallback if CUDA unavailable

### ✅ Type-Safe End-to-End
- Backend Pydantic models → Frontend TypeScript types
- WebSocket messages typed
- API responses fully typed

### ✅ Production-Ready DevSecOps
- Security scanning (bandit, pip-audit)
- Code quality (ruff, mypy)
- Testing (pytest with coverage)
- Observability (Prometheus + OpenTelemetry)

### ✅ Real-time RAG
- WebSocket-based chat
- Streaming responses
- Document ingestion pipeline
- Vector search with ranking

---

## 🔧 Implementation Status

Following the consolidation, I'll now implement the complete "One-Click Learning + RAG + DevSecOps" stack in the existing unified backend structure.

---

*This guide provides the complete blueprint for your unified learning + RAG system. Continue reading for detailed implementation...*