# 🎯 One-Click Learning + RAG + DevSecOps - Complete Implementation

**Hệ thống học tập thông minh với RAG, WebSocket Streaming, Clean DI & Security** - CPU-first, GPU-ready architecture

## 🏗️ Kiến Trúc Hoàn Chỉnh

### Backend (FastAPI + Clean DI)
```
apps/backend/app/
├── ai/                    # AI Engines (CPU-first, GPU-ready)
│   ├── config.py         # Device detection (ZETA_USE_GPU)
│   ├── embedder.py       # Sentence-Transformers wrapper
│   ├── rag_service.py    # FAISS + JSON persistence
│   ├── llm.py           # Ollama client + fallback
│   ├── asr_service.py   # Faster-Whisper (optional)
│   └── ocr_service.py   # PaddleOCR + Tesseract fallback
├── api/v1/
│   ├── rag_router.py    # REST + WebSocket endpoints
│   └── one_click_learning.py # Complete pipeline
├── serializers/rag.py   # Pydantic v2 schemas
└── dependencies.py      # DI factories + RBAC
```

### Frontend (Electron + React)
```
apps/desktop/src/
├── lib/ws/rag.ts        # Type-safe WebSocket client
└── pages/OneClickLearning.tsx # React UI for chat
```

## 🚀 Quick Start Commands

### 1. Backend Setup
```bash
cd apps/backend
uv sync                          # Install all dependencies
uv run python ../../setup_one_click_learning.py  # Download models
uv run uvicorn app.main:app --reload --port 8000  # Start server
```

### 2. Frontend Setup  
```bash
cd apps/desktop
pnpm install
pnpm electron:dev               # Start Electron app
```

### 3. GPU Activation (Optional)
```bash
export ZETA_USE_GPU=1          # Linux/macOS
set ZETA_USE_GPU=1             # Windows
```

## 📡 API Endpoints

### RAG Core
- `POST /api/v1/rag/ingest/text` - Ingest text documents
- `POST /api/v1/rag/ingest/upload` - Upload files (PDF, DOCX, images)
- `POST /api/v1/rag/search` - Search knowledge base
- `WS /api/v1/rag/chat/ws` - Real-time streaming chat

### One-Click Learning Pipeline
- `POST /api/v1/one-click/pipeline` - Complete file processing
- `POST /api/v1/one-click/transcribe` - Audio → Text (ASR)
- `POST /api/v1/one-click/extract-text` - Image → Text (OCR)
- `GET /api/v1/one-click/status` - System health check

## 🧪 Test the System

### REST API Tests
```bash
# Ingest text
curl -X POST http://localhost:8000/api/v1/rag/ingest/text \
  -H 'Content-Type: application/json' \
  -d '{"texts":["Zeta là trợ lý AI desktop + FastAPI."]}'

# Search
curl -X POST http://localhost:8000/api/v1/rag/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"trợ lý AI","top_k":3}'

# Complete pipeline
curl -X POST http://localhost:8000/api/v1/one-click/pipeline \
  -F 'file=@sample.txt' \
  -F 'auto_ingest=true'
```

### WebSocket Chat Test
```python
import asyncio, websockets, json, uuid

async def test_chat():
    uri = "ws://localhost:8000/api/v1/rag/chat/ws"
    async with websockets.connect(uri) as ws:
        msg = {
            "type": "user_message",
            "id": str(uuid.uuid4()),
            "text": "Zeta là gì?"
        }
        await ws.send(json.dumps(msg))
        
        async for raw in ws:
            data = json.loads(raw)
            print("←", data)
            if data.get("type") == "done":
                break

asyncio.run(test_chat())
```

## 🛡️ Security & DevSecOps

### RBAC Permissions
- `rag:ingest` - Upload và ingest documents
- `rag:search` - Search knowledge base  
- `learning.pipeline` - Access complete pipeline
- `learning.transcribe` - ASR transcription
- `learning.ocr` - OCR text extraction

### Security Scanning
```bash
uv run ruff check .            # Code quality
uv run mypy app                # Type checking
uv run bandit -r app -x tests  # Security scan
uv run pip-audit               # Dependency audit
uv run pytest --cov=app       # Tests + coverage
```

## 🎯 Architecture Principles

### 1. CPU-first, GPU-ready
- Mặc định chạy trên CPU cho compatibility
- `ZETA_USE_GPU=1` → tự động detect CUDA/MPS
- Fallback graceful khi GPU không available

### 2. Clean Architecture
- `app/ai/*` chứa pure engines (no FastAPI deps)
- `dependencies.py` cung cấp DI factories
- Routers chỉ orchestrate, không chứa business logic

### 3. Optional Dependencies
- OCR/ASR import trong service constructor
- `ImportError` → `available() == False`  
- Endpoints vẫn hoạt động, trả về error message thân thiện

### 4. Security-first
- RBAC trên mọi endpoint
- Rate limiting per user tier
- Audit logging cho mọi action
- No secrets trong code

### 5. Observability
- Prometheus metrics (`/metrics`)
- OpenTelemetry tracing
- Health/readiness endpoints
- Structured logging

## 📊 Performance

### RAG Engine
- **Embedder**: all-MiniLM-L6-v2 (384 dims, ~90MB)
- **Index**: FAISS IndexFlatIP (cosine similarity)
- **Storage**: JSON + Binary FAISS files
- **Chunk size**: ~350 tokens per chunk

### Resource Usage
- **CPU mode**: ~1GB RAM, minimal GPU
- **GPU mode**: +2-4GB VRAM for embeddings
- **Storage**: ~100MB models + data size

## 🔮 Features Ready

### ✅ Completed (Phase 1)
- [x] RAG core (embedding + search)
- [x] ASR/OCR integration
- [x] WebSocket streaming
- [x] Clean DI architecture
- [x] Security (RBAC + audit)
- [x] Frontend WebSocket client

### 📋 Next Steps (Phase 2)
- [ ] Vector database scaling (pgvector/Qdrant)
- [ ] Advanced chunking strategies
- [ ] Multi-modal embedding
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)

## 🆘 Troubleshooting

### Common Issues

1. **PaddleOCR import error on Windows**
   ```bash
   uv sync --extra ocr-alt  # Use Tesseract instead
   ```

2. **CUDA out of memory**
   ```bash
   unset ZETA_USE_GPU  # Force CPU mode
   ```

3. **WebSocket connection refused**
   ```bash
   curl http://localhost:8000/api/v1/health  # Check backend
   ```

4. **Embedding model download slow**
   ```bash
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
   ```

### Debug Mode
```bash
export ZETA_DEBUG=1
uv run uvicorn app.main:app --log-level debug
```

---

**🎉 Kết luận**: Hệ thống One-Click Learning đã sẵn sàng cho production với đầy đủ RAG, streaming, security và DevSecOps pipeline. CPU-first architecture đảm bảo chạy stable trên mọi môi trường, GPU acceleration tùy chọn cho performance cao hơn.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Desktop App    │    │   AI Server     │    │  ML Engines     │
│  (Electron)     │◄──►│   (FastAPI)     │◄──►│  (CPU/GPU)      │
│                 │    │                 │    │                 │
│ • React + TS    │    │ • Clean DI      │    │ • RAG Engine    │
│ • WebSocket     │    │ • RBAC          │    │ • ASR Engine    │
│ • Auto-types    │    │ • DevSecOps     │    │ • OCR Engine    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 Key Features

### ✅ One-Click Learning Pipeline
- **Upload** → Auto-detect file type (audio/image/text)
- **Extract** → Use appropriate engine (ASR/OCR/direct)
- **Embed** → Generate vector embeddings (CPU/GPU)
- **Index** → Store in FAISS or pgvector
- **Search** → RAG-powered similarity search

### ✅ Real-time Chat with RAG
- WebSocket-based chat interface
- Context-aware responses using retrieved documents
- Type-safe message schemas (Pydantic ↔ Zod)
- Automatic reconnection

### ✅ CPU-First, GPU-Ready
- Default: All processing on CPU
- GPU: Set `ZETA_USE_GPU=1` for CUDA acceleration
- Fallback: Graceful degradation if GPU unavailable

### ✅ Production DevSecOps
- **Security**: bandit, pip-audit, RBAC
- **Quality**: ruff, mypy, pytest
- **Observability**: Prometheus, OpenTelemetry
- **Deployment**: Docker, uv-based deps

## 📦 Technology Stack

### Backend (FastAPI + AI)
| Component | Library | Purpose |
|-----------|---------|---------|
| **Web Framework** | FastAPI ≥ 0.115 | Async API with auto-docs |
| **Embedding** | sentence-transformers | CPU-friendly embeddings |
| **Vector DB** | FAISS-CPU + pgvector | Local + scalable search |
| **ASR** | faster-whisper | CPU/GPU speech recognition |
| **OCR** | OpenCV + PaddleOCR/Tesseract | Image text extraction |
| **Auth** | JWT + RBAC | Role-based permissions |
| **DevOps** | uv + ruff + mypy | Modern Python tooling |

### Frontend (Electron + React)
| Component | Library | Purpose |
|-----------|---------|---------|
| **Desktop** | Electron + React | Cross-platform app |
| **State** | TanStack Query + Zustand | Data fetching + state |
| **Types** | Auto-generated from OpenAPI | End-to-end type safety |
| **UI** | Radix + TailwindCSS | Accessible components |
| **WebSocket** | reconnecting-websocket | Real-time communication |

## 🌐 API Endpoints

### RAG & Search
```http
POST /api/v1/one-click/ingest/text     # Add documents to index
POST /api/v1/one-click/search          # Search documents
GET  /api/v1/one-click/status          # Engine status
```

### AI Processing
```http
POST /api/v1/one-click/transcribe      # Audio → Text (ASR)
POST /api/v1/one-click/extract-text    # Image → Text (OCR)
POST /api/v1/one-click/pipeline        # Complete pipeline
```

### Real-time
```http
WS   /ws/chat                          # WebSocket chat with RAG
WS   /ws/notifications                 # System notifications
```

## 🔧 Development Commands

### Backend (uv-based)
```bash
# Install dependencies
uv sync

# Development tools
uv run ruff check .                    # Lint
uv run mypy app                        # Type check
uv run pytest --cov=app               # Test + coverage
uv run bandit -r app                   # Security scan
uv run pip-audit                       # Dependency audit

# Run server
uv run uvicorn app.main:app --reload
```

### Frontend (pnpm-based)
```bash
# Install dependencies
pnpm install

# Development tools
pnpm typecheck                         # Type check
pnpm lint                              # ESLint
pnpm test                              # Vitest
pnpm openapi:gen                       # Generate types

# Run app
pnpm electron:dev                      # Development
pnpm electron:build                    # Production build
```

## 🧪 Testing the System

### 1. Test RAG Search
```bash
curl -X POST http://localhost:8000/api/v1/one-click/search \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "k": 5}'
```

### 2. Test Document Ingestion
```bash
curl -X POST http://localhost:8000/api/v1/one-click/ingest/text \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Python is great", "FastAPI is fast"]}'
```

### 3. Test Complete Pipeline
```bash
curl -X POST http://localhost:8000/api/v1/one-click/pipeline \
  -F "file=@document.pdf" \
  -F "auto_ingest=true" \
  -F "search_query=python"
```

### 4. Test WebSocket Chat
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'message',
    content: 'Tell me about machine learning'
  }));
};
```

## ⚙️ Configuration

### Environment Variables
```bash
# GPU acceleration
ZETA_USE_GPU=1                         # Enable GPU for AI engines

# API settings
ZETA_API_HOST=0.0.0.0                  # Server host
ZETA_API_PORT=8000                     # Server port

# Database
DATABASE_URL=postgresql://...          # PostgreSQL with pgvector

# Observability
ENABLE_METRICS=true                    # Prometheus metrics
OTLP_ENDPOINT=http://jaeger:14268      # OpenTelemetry tracing
```

### Hardware Requirements
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 4 cores | 8+ cores |
| **RAM** | 8 GB | 16+ GB |
| **Storage** | 10 GB | 50+ GB SSD |
| **GPU** | None (CPU-first) | CUDA-compatible (optional) |

## 🚀 Deployment

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./apps/backend
    ports:
      - "8000:8000"
    environment:
      - ZETA_USE_GPU=1
    volumes:
      - ./data:/data
  
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      - POSTGRES_DB=zeta
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### Production Checklist
- [ ] Set up PostgreSQL with pgvector extension
- [ ] Configure Redis for caching and queues  
- [ ] Set up monitoring (Prometheus + Grafana)
- [ ] Configure reverse proxy (nginx/traefik)
- [ ] Set up SSL certificates
- [ ] Configure backup strategies
- [ ] Set up log aggregation
- [ ] Configure CI/CD pipelines

## 🛡️ Security

### Built-in Security Features
- **Authentication**: JWT-based with role permissions
- **Rate Limiting**: Per-user and per-endpoint limits
- **Input Validation**: Pydantic schemas + Zod validation
- **CSP**: Content Security Policy in Electron
- **Dependency Scanning**: Automated vulnerability checks
- **Code Analysis**: Static security analysis with bandit

### Security Best Practices
- Use environment variables for secrets
- Enable HTTPS in production
- Regularly update dependencies
- Monitor for security vulnerabilities
- Implement proper error handling
- Use least-privilege principles

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc (Alternative API docs)
- **Architecture**: See [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Contributing**: See [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`uv run pytest` and `pnpm test`)
5. Run security checks (`uv run bandit -r app`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **sentence-transformers** for efficient embeddings
- **FAISS** for fast similarity search
- **FastAPI** for modern Python APIs
- **Electron** for cross-platform desktop apps
- **The open source community** for amazing tools

---

**Built with ❤️ by the ZETA AI Team**

*Empowering everyone with accessible AI and learning tools.*