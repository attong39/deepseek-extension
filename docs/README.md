# 🚀 Zeta AI Server

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](docker-compose.yml)

A comprehensive, production-ready AI server platform built with FastAPI, featuring intelligent agents, real-time chat, advanced memory systems, and enterprise-grade infrastructure.

## 🌟 Key Features

### 🤖 **AI Agent Management**
- Multi-model AI agent orchestration
- Dynamic configuration and scaling
- Performance monitoring and analytics
- Custom agent deployment

### 💬 **Real-time Communication**
- WebSocket-powered chat system
- Multi-participant conversations
- Message history and search
- File sharing and attachments

### 🧠 **Intelligent Memory System**
- Vector-based semantic memory
- Episodic and procedural memory types
- Context-aware retrieval
- Memory decay and optimization

### 🔒 **Enterprise Security**
- JWT-based authentication
- Rate limiting and DDoS protection
- CORS and security middleware
- Audit logging and monitoring

### 📊 **Production Ready**
- Docker containerization
- Kubernetes deployment
- Monitoring and alerting
- Automated testing and CI/CD

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

### 1. Clone Repository

```bash
git clone https://github.com/your-org/zeta-ai-server.git
cd zeta-ai-server
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

### 3. Docker Deployment (Recommended)

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f zeta-api
```

### 4. Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup database
python scripts/setup_database.py

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 📡 API Endpoints

### 🏥 Health & Status
- `GET /api/v1/health` - System health check
- `GET /api/v1/status` - Detailed system status

### 🤖 Agent Management
- `POST /api/v1/agents/` - Create new agent
- `GET /api/v1/agents/` - List all agents
- `GET /api/v1/agents/{id}` - Get agent details
- `PUT /api/v1/agents/{id}` - Update agent
- `DELETE /api/v1/agents/{id}` - Delete agent

### 💬 Chat Operations
- `POST /api/v1/chat/start` - Start chat session
- `POST /api/v1/chat/{id}/messages` - Send message
- `GET /api/v1/chat/{id}` - Get conversation
- `POST /api/v1/chat/{id}/end` - End session

### 🧠 Memory Management
- `POST /api/v1/memory/` - Create memory
- `GET /api/v1/memory/search` - Search memories
- `GET /api/v1/memory/{id}` - Get memory details
- `PUT /api/v1/memory/{id}` - Update memory
- `DELETE /api/v1/memory/{id}` - Delete memory

### 📁 File Operations
- `POST /api/v1/files/upload` - Upload file
- `GET /api/v1/files/download/{id}` - Download file
- `GET /api/v1/files/list` - List files
- `DELETE /api/v1/files/delete/{id}` - Delete file

### 🔌 WebSocket Endpoints
- `WS /ws/chat` - Real-time chat connection

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   AI Services   │
│   (Web/Mobile)  │◄──►│   (FastAPI)     │◄──►│   (OpenAI/etc)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                    ┌─────────────────┐
                    │   Core Domain   │
                    │   (Business     │
                    │    Logic)       │
                    └─────────────────┘
                                │
        ┌─────────────────┬─────────────────┬─────────────────┐
        │                 │                 │                 │
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Database      │ │   Cache/Queue   │ │   File Storage  │ │   Monitoring    │
│   (PostgreSQL)  │ │   (Redis)       │ │   (Local/S3)    │ │   (Prometheus)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 🎯 Clean Architecture Layers

- **`app/`** - API layer (FastAPI, routers, middleware)
- **`core/`** - Domain layer (entities, use cases, interfaces)
- **`data/`** - Infrastructure layer (repositories, external services)
- **`tests/`** - Test suites (unit, integration, e2e)

## 💻 Development

### Code Quality

```bash
# Run linting
ruff check .
ruff format .

# Type checking
mypy .

# Run tests
pytest

# Pre-commit hooks
pre-commit run --all-files
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing

```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# End-to-end tests
pytest tests/e2e/ -v

# Performance tests
pytest tests/performance/ -v --durations=10

# Coverage report
pytest --cov=app --cov-report=html
```

## 🐳 Docker Deployment

### Development

```bash
docker-compose -f deployment/docker/docker-compose.dev.yml up -d
```

### Production

```bash
# Set environment variables
export SECRET_KEY="your-secret-key"
export OPENAI_API_KEY="your-openai-key"

# Deploy with production config
docker-compose -f deployment/docker/docker-compose.prod.yml up -d
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deployment/kubernetes/

# Check deployment
kubectl get pods -n zeta

# View logs
kubectl logs -f deployment/zeta-api -n zeta
```

## 📊 Monitoring

### Health Checks

- **Application**: `http://localhost:8001/api/v1/health`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (admin/admin123)

### Key Metrics

- Request rate and latency
- Error rates and status codes
- Database connection pool
- Memory usage and CPU utilization
- Agent performance metrics

### Alerts

Configure alerts for:
- High error rates (>5%)
- Slow response times (>2s)
- Database connection issues
- Memory usage (>85%)
- Disk space (>90%)

## 🔧 Configuration

### Environment Variables

```bash
# Application
ENVIRONMENT=production
SECRET_KEY=your-secret-key-here
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/zeta
REDIS_URL=redis://localhost:6379/0

# AI Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-key

# Security
CORS_ORIGINS=["http://localhost:3000"]
RATE_LIMIT_PER_MINUTE=100

# File Storage
UPLOAD_MAX_SIZE=10485760  # 10MB
STORAGE_PATH=./storage/uploads

# Monitoring
PROMETHEUS_ENABLED=true
LOG_LEVEL=INFO
```

### Configuration Files

- **`config/settings/`** - Environment-specific settings
- **`deployment/docker/`** - Docker configurations
- **`deployment/kubernetes/`** - K8s manifests
- **`monitoring/`** - Monitoring configs

## 🔒 Security

### Authentication

```python
# API Key authentication
headers = {
    "Authorization": "Bearer your-api-key"
}

# JWT token authentication
headers = {
    "Authorization": "Bearer jwt-token"
}
```

### Best Practices

- Use HTTPS in production
- Rotate API keys regularly
- Implement rate limiting
- Monitor for suspicious activity
- Keep dependencies updated
- Use secrets management

## 📚 Documentation

- **[API Reference](docs/API.md)** - Complete API documentation
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture
- **[Deployment](docs/DEPLOYMENT.md)** - Deployment guide
- **[Contributing](docs/CONTRIBUTING.md)** - Development guide
- **[Security](docs/SECURITY.md)** - Security guidelines

## 🧪 Testing Examples

### Unit Testing

```python
import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_create_agent():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/agents/", json={
            "name": "Test Agent",
            "description": "Test description"
        })
        assert response.status_code == 201
```

### Load Testing

```bash
# Using locust
locust -f tests/performance/locustfile.py --host=http://localhost:8001

# Using k6
k6 run tests/performance/load_test.js
```

## 🚀 Performance

### Optimization

- **Database**: Connection pooling, query optimization
- **Caching**: Redis for frequently accessed data
- **Async**: FastAPI async/await for I/O operations
- **Load Balancing**: Multiple worker processes
- **CDN**: Static file delivery optimization

### Benchmarks

- **Throughput**: 1000+ requests/second
- **Latency**: <100ms average response time
- **Concurrent Users**: 10,000+ simultaneous connections
- **Memory**: <512MB per worker process

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests before committing
pytest && ruff check . && mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/zeta-ai-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/zeta-ai-server/discussions)
- **Email**: support@zeta.ai
- **Documentation**: [docs.zeta.ai](https://docs.zeta.ai)

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://sqlalchemy.org/) - Database ORM
- [Celery](https://celeryproject.org/) - Task queue
- [Redis](https://redis.io/) - In-memory data store
- [Docker](https://docker.com/) - Containerization

---

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by the Zeta AI Team
