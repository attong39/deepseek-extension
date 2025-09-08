# LIBRARIES – ZETA_AI

## Tổng quan

Tài liệu này mô tả toàn bộ thư viện được sử dụng trong dự án ZETA_AI, bao gồm **AI Server (FastAPI)** và **Desktop App (Electron/React)**. Áp dụng nguyên tắc **Core tối giản + Extras mở rộng** để tối ưu hiệu suất và tránh bloat.

---

## 1) Core API (Python - Server)

### Web Framework & Runtime
- **fastapi**: Web framework hiện đại với async/await support
- **uvicorn[standard]**: ASGI server với performance cao (uvloop + httptools)
- **pydantic(v2)**: Validation & serialization với hiệu suất tối ưu
- **pydantic-settings**: Configuration management với environment variables
- **sqlmodel**: Type-safe ORM kết hợp SQLAlchemy + Pydantic
- **httpx**: HTTP client cho integration và testing
- **structlog + orjson**: Structured logging với JSON serialization nhanh
- **redis**: Cache và rate-limit apps/backend

### Core Architecture
```
zeta_vn/
├── application/     # API endpoints, middleware, dependencies
├── domain/         # Business entities, value objects, rules  
├── infrastructure/ # Database, external services, adapters
└── tests/         # Test suites với coverage ≥95%
```

---

## 2) Security

### Authentication & Authorization
- **python-jose[cryptography]**: JWT/OIDC token handling
- **passlib[bcrypt]**: Password hashing với bcrypt
- **argon2-cffi**: Modern password hashing (production-ready)
- **fastapi-limiter**: Rate limiting per endpoint qua Redis

### Best Practices
```python
# JWT với expire time ngắn + refresh token
# Rate limit: 100 req/min cho authenticated, 10 req/min cho anonymous
# PII masking trong logs
# Audit trail cho sensitive operations
```

---

## 3) RAG / AI Stack

### Vector Search & Embeddings
- **sentence-transformers**: Embeddings + cross-encoder (rerank)
- **faiss-cpu** / **pgvector**: Vector index (FAISS local hoặc Postgres+pgvector)
- **rank-bm25**: Lexical search bổ trợ
- **rapidfuzz**: Fuzzy string matching
- **numpy + scikit-learn**: ML utilities và metrics

### LLM Integration (Optional)
- **transformers**: Hugging Face models
- **accelerate**: Distributed training/inference
- **bitsandbytes**: Quantization (Linux only)
- **safetensors**: Safe model serialization

### RAG Pipeline
```
Documents → OCR/ASR → Chunking → Embeddings → Vector Store
Query → Embedding → Similarity Search → Rerank → LLM Generation
```

---

## 4) OCR/ASR (One-Click Learning)

### Automatic Speech Recognition
- **faster-whisper**: Optimized Whisper implementation
- **ffmpeg-python**: Audio processing
- **librosa + soundfile**: Audio analysis và I/O

### Optical Character Recognition  
- **pytesseract**: OCR engine (cần Tesseract binary)
- **opencv-python-headless**: Image preprocessing
- **Pillow**: Image manipulation
- **pdf2image**: PDF to image conversion (cần Poppler)

### Optional Heavy OCR
```toml
# Uncomment nếu cần OCR chất lượng cao
# "paddleocr>=2.7; platform_machine!='aarch64'"
# "easyocr>=1.7"
```

---

## 5) Observability

### Metrics & Monitoring
- **prometheus-fastapi-instrumentator**: `/metrics` endpoint
- **opentelemetry-sdk + instrumentation**: Distributed tracing
- **sentry-sdk**: Error reporting và performance monitoring

### Logging Structure
```json
{
  "timestamp": "2025-01-01T12:00:00Z",
  "level": "INFO", 
  "trace_id": "abc123",
  "user_id": "user_456",
  "event": "document_processed",
  "metadata": {"doc_size": 1024, "processing_time_ms": 250}
}
```

---

## 6) Task Queue/Orchestration

### Options (Chọn 1)
- **arq**: Async-native task queue (khuyến nghị cho FastAPI)
- **celery + redis**: Classic worker pattern (mature, nhiều features)

### Use Cases
```python
# Async tasks: document processing, model training, batch jobs
# Scheduled tasks: cleanup, health checks, report generation
# Long-running tasks: RAG indexing, vector updates
```

---

## 7) Cloud/Storage

### Object Storage
- **boto3**: AWS S3 integration
- **minio**: S3-compatible storage (self-hosted)
- **google-cloud-storage**: Google Cloud Storage

### File Types Supported
```
Documents: PDF, DOCX, TXT, MD
Images: PNG, JPG, WEBP, TIFF
Audio: WAV, MP3, M4A, FLAC  
Video: MP4, AVI, MOV (extract audio)
```

---

## 8) Serialization & Performance

### High-Performance Serialization
- **msgspec**: Fastest JSON/MessagePack encoder/decoder
- **orjson**: Fast JSON library (default for FastAPI)

### Linux Performance
- **uvloop**: Fast asyncio event loop
- **httptools**: Fast HTTP parsing

---

## 9) DevSecOps

### Testing
- **pytest + pytest-asyncio + pytest-cov**: Test framework với async support
- **respx**: HTTP mocking cho tests

### Code Quality
- **ruff**: Fast linter + formatter (thay thế black, isort, flake8)
- **mypy**: Static type checking
- **bandit**: Security linting
- **pip-audit**: Supply chain security
- **vulture**: Dead code detection
- **pre-commit**: Git hooks automation

### Quality Gates
```bash
# CI pipeline cần pass tất cả:
pytest --cov=zeta_vn --cov-fail-under=95
ruff check . && ruff format --check .
mypy zeta_vn
bandit -r zeta_vn  
pip-audit
```

---

## 10) Desktop App (Electron/React)

### Core Framework
- **electron**: Cross-platform apps/desktop app
- **react + react-dom**: UI library
- **typescript**: Type safety
- **vite + vite-plugin-electron**: Build tool với HMR

### UI Components
- **tailwindcss**: Utility-first CSS
- **@radix-ui/***: Headless UI components  
- **lucide-react**: Icon library
- **framer-motion**: Animations
- **sonner**: Toast notifications
- **class-variance-authority + tailwind-merge**: Dynamic styling

### State & Data
- **@tanstack/react-query**: Server state management
- **zustand**: Client state management  
- **ky**: Modern HTTP client
- **idb**: IndexedDB wrapper
- **zod + ajv**: Runtime validation

### Routing & I18n
- **react-router-dom**: Routing với **HashRouter** (Electron compatibility)
- **i18next + react-i18next**: Internationalization
- **react-dropzone**: File upload handling

### Development
- **vitest**: Fast unit testing
- **@testing-library/react + @testing-library/jest-dom**: Component testing
- **msw**: API mocking
- **eslint + @typescript-eslint/***: Linting
- **prettier**: Code formatting

### Build & Distribution
- **electron-builder**: Package và distribute
- **electron-updater**: Auto-update mechanism
- **electron-log**: Logging trong Electron

---

## 11) Installation Commands

### Server (Python)
```bash
# Core + tất cả extras phổ biến
uv pip install -e ".[dev,db,security,rag,asr,ocr,obs,cloud,perf]"

# Hoặc selective install
uv pip install -e ".[dev,db,security,rag]"  # RAG-focused
uv pip install -e ".[dev,db,security,ocr,asr]"  # Document processing

# Chạy server
uv run uvicorn zeta_vn.application.api.main:app --reload --port 8000
```

### Desktop (Node)
```bash
cd desktop_ai_zeta

# Install dependencies (khuyến nghị pnpm)
pnpm install

# Development
pnpm run dev

# Build & package
pnpm run build
pnpm run dist

# Testing & linting
pnpm run test
pnpm run lint
```

---

## 12) Architecture Decisions

### Why FastAPI?
- Native async/await support
- Automatic OpenAPI generation  
- High performance (so sánh với Django/Flask)
- Type hints integration với Pydantic

### Why Electron + React?
- Cross-platform compatibility
- Reuse web technologies
- Rich ecosystem
- Easy integration với apps/backend APIs

### Why HashRouter?
- Electron không support browser history API
- Đơn giản hóa routing trong apps/desktop app
- Tránh conflicts với file:// protocol

### Why uv over pip?
- Faster dependency resolution
- Better lock file management
- Improved security với hash verification
- Compatible với existing pip workflows

---

## 13) Roadmap & Future Considerations

### Planned Additions
- **WebRTC**: Real-time communication
- **WebAssembly**: High-performance client-side processing
- **Kubernetes**: Container orchestration
- **Apache Kafka**: Event streaming

### Performance Targets
- API response time: <100ms (p95)
- Desktop app startup: <3s
- Document processing: <5s per MB
- Memory usage: <500MB baseline

### Security Roadmap
- OAuth2/OIDC integration
- E2E encryption cho sensitive data
- Zero-trust architecture
- Compliance với GDPR/SOC2

---

## 14) Known Limitations & Workarounds

### Platform-specific Issues
- **faiss-cpu**: Không support ARM64 (dùng pgvector thay thế)
- **bitsandbytes**: Chỉ Linux (GPU quantization)
- **paddleocr**: Nặng, có thể fail trên Windows (dùng pytesseract)

### External Dependencies
- **Tesseract**: Cần cài binary cho OCR
- **Poppler**: Cần cho PDF processing
- **FFmpeg**: Cần cho audio processing

### Memory Considerations
- **sentence-transformers**: Models ~500MB RAM
- **FAISS**: Vector index scale với data size
- **Whisper**: ~1GB VRAM cho large model

---

## 15) Troubleshooting

### Common Issues
```bash
# ModuleNotFoundError
uv pip install -e ".[dev]"

# MyPy type errors  
mypy --install-types

# FAISS installation fails
pip install faiss-cpu --no-cache-dir

# Electron build fails
rm -rf node_modules && pnpm install

# OCR not working
sudo apt-get install tesseract-ocr  # Ubuntu
brew install tesseract  # macOS
```

### Debug Mode
```bash
# Server debug
DEBUG=1 uv run uvicorn zeta_vn.application.api.main:app --reload

# Desktop debug  
pnpm run dev  # Opens DevTools automatically
```
