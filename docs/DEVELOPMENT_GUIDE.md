# ZETA AI Server - Development Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Node.js 18+ (for tools)

### Installation

1. **Clone Repository**
```bash
git clone https://github.com/your-org/zeta-ai-server.git
cd zeta-ai-server
```

2. **Setup Python Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Database Setup**
```bash
# Create database
createdb zeta_ai

# Run migrations
alembic upgrade head
```

5. **Start Development Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Architecture Overview

ZETA AI Server follows Clean Architecture principles with 8 distinct layers:

### Layer Structure
```
app/     - Interface Layer (FastAPI, controllers, API endpoints)
core/    - Domain Layer (business logic, entities, use cases)
data/    - Data Layer (repositories, models, external clients)
config/  - Configuration Layer (settings, feature flags)
tests/   - Testing Layer (unit, integration, e2e tests)
docs/    - Documentation Layer (API docs, guides)
scripts/ - DevOps Layer (deployment, monitoring scripts)
storage/ - Storage Layer (file management, cache)
```

### Key Principles
- **Dependency Inversion**: Core domain never depends on external layers
- **Single Responsibility**: Each layer has one clear responsibility
- **Interface Segregation**: Use protocols/interfaces for decoupling
- **Clean Separation**: No circular dependencies between layers

## 📝 Development Workflow

### Code Style
- **Formatting**: Use `ruff format` for consistent code style
- **Linting**: Use `ruff check` for code quality
- **Type Checking**: Use `mypy --strict` for type safety
- **Testing**: Maintain >80% test coverage

### Git Workflow
1. Create feature branch from `main`
2. Make changes following Clean Architecture
3. Write tests for new functionality
4. Run quality checks: `ruff check && mypy . && pytest`
5. Create pull request with clear description
6. Review and merge after CI passes

### Code Quality Commands
```bash
# Format code
ruff format .

# Check linting
ruff check .

# Type checking
mypy app core data

# Run tests
pytest --cov=app --cov=core --cov=data --cov-report=html

# Security scan
bandit -r app core data
```

## 🧪 Testing Strategy

### Test Types
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user workflows
- **Performance Tests**: Test system performance and limits

### Test Organization
```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for component interactions
├── e2e/           # End-to-end workflow tests
├── performance/   # Performance and load tests
├── fixtures/      # Test data and fixtures
└── mocks/         # Mock objects for testing
```

### Writing Tests
```python
# Unit test example
def test_agent_creation():
    agent = Agent(name="Test Agent")
    assert agent.name == "Test Agent"
    assert agent.status == AgentStatus.INACTIVE

# Integration test example
@pytest.mark.asyncio
async def test_create_agent_endpoint(client, db_session):
    response = await client.post("/api/v1/agents", json={
        "name": "Test Agent",
        "description": "Test Description"
    })
    assert response.status_code == 201
```

## 🔧 Configuration Management

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/zeta_ai
REDIS_URL=redis://localhost:6379

# AI Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-key

# Application
DEBUG=false
LOG_LEVEL=info
SECRET_KEY=your-secret-key
```

### Feature Flags
```python
# In code
from config.settings import settings

if settings.enable_advanced_memory:
    # Advanced memory features
    pass
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t zeta-ai-server .

# Run container
docker run -p 8000:8000 -e DATABASE_URL=... zeta-ai-server
```

### Kubernetes Deployment
```bash
# Apply configurations
kubectl apply -f deployment/kubernetes/

# Check status
kubectl get pods -l app=zeta-ai-server
```

### Environment-Specific Configs
- **Development**: Local PostgreSQL + Redis
- **Staging**: Cloud databases with test data
- **Production**: Highly available setup with monitoring

## 📊 Monitoring & Observability

### Health Checks
- `/health` - Basic application health
- `/health/detailed` - Detailed component health
- `/metrics` - Prometheus metrics endpoint

### Logging
```python
import logging
from app.core.logging import get_logger

logger = get_logger(__name__)
logger.info("Processing request", extra={"request_id": request_id})
```

### Metrics
- Request latency and throughput
- Database connection pool status
- AI service response times
- Memory usage and performance

## 🔒 Security Guidelines

### Authentication & Authorization
- JWT tokens for API authentication
- Role-based access control (RBAC)
- API key management for external services

### Data Protection
- Encrypt sensitive data at rest
- Use HTTPS for all communications
- Sanitize user inputs
- Audit logging for sensitive operations

### Security Scanning
```bash
# Dependency vulnerabilities
pip-audit

# Code security issues
bandit -r app core data

# Container scanning
docker scan zeta-ai-server:latest
```

## 📚 API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Versioning
- v1: Stable API with backward compatibility
- v2: New features and improvements
- GraphQL: Flexible query interface

### Authentication
```bash
# Get access token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Use token in requests
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/v1/agents"
```

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database status
pg_isready -h localhost -p 5432

# Reset database
dropdb zeta_ai && createdb zeta_ai
alembic upgrade head
```

#### Redis Connection Issues
```bash
# Check Redis status
redis-cli ping

# Restart Redis
sudo systemctl restart redis
```

#### Import Errors
```bash
# Check Python path
echo $PYTHONPATH

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=debug
export DEBUG=true

# Run with debugger
python -m debugpy --listen 5678 --wait-for-client -m uvicorn app.main:app
```

## 🤝 Contributing

### Pull Request Process
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes following coding standards
4. Add tests for new functionality
5. Ensure all tests pass: `pytest`
6. Update documentation if needed
7. Submit pull request with clear description

### Code Review Guidelines
- Review for Clean Architecture compliance
- Check test coverage and quality
- Verify security implications
- Ensure documentation is updated
- Performance impact assessment

## 📞 Support

### Getting Help
- **Documentation**: Check this guide and API docs
- **Issues**: Create GitHub issue with detailed description
- **Discussions**: Use GitHub Discussions for questions
- **Emergency**: Contact team lead for critical issues

### Useful Links
- [Project Repository](https://github.com/your-org/zeta-ai-server)
- [API Documentation](http://localhost:8000/docs)
- [Architecture Guide](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)

## Monorepo Consistency (Addendum)

- See `docs/ZETA_CONSISTENCY_PROPOSAL_VN.md` for repo-wide standards (coding, QA, deployment, security).
- See `docs/CONSISTENCY_IMPLEMENTATION_ROADMAP.md` for the 3-phase rollout.
- Root CI: `.github/workflows/ci-root.yml` runs lint/test without replacing existing project workflows.
- Base configs at root for gradual adoption: `tsconfig.base.json`, `.eslintrc.base.cjs`, `.prettierrc.json`, `pyproject.base.toml`.
