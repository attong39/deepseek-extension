# ZETA AI - Developer Guide

## Table of Contents
- [Getting Started](#getting-started)
- [Architecture Overview](#architecture-overview)
- [Development Environment](#development-environment)
- [Code Organization](#code-organization)
- [Best Practices](#best-practices)
- [Testing](#testing)
- [Database](#database)
- [API Development](#api-development)
- [Frontend Development](#frontend-development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 13+ (or SQLite for development)
- Redis 6+ (for Celery)
- Node.js 18+ (for frontend development)
- Docker (for containerized deployment)

### Quick Setup
```bash
# Clone repository
git clone https://github.com/your-org/zeta-ai.git
cd zeta-ai

# Run automated setup
python scripts/setup_development.py

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Start development server
python -m uvicorn app.main:app --reload

# Start Celery worker (separate terminal)
python -m celery -A app.worker.celery_app worker -l info
```

### Manual Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Set up database
python scripts/setup_database.py

# Run migrations
alembic upgrade head

# Create superuser
python scripts/create_superuser.py
```

## Architecture Overview

ZETA AI follows Clean Architecture principles with clear separation of concerns:

```
zeta_vn/
├── app/                    # Application Layer
│   ├── api/               # API routes and endpoints
│   ├── controllers/       # Request/response handling
│   ├── middleware/        # HTTP middleware
│   ├── serializers/       # Data serialization
│   ├── validators/        # Input validation
│   └── websockets/        # WebSocket handlers
├── core/                  # Domain Layer
│   ├── domain/            # Domain entities
│   ├── interfaces/        # Abstract interfaces
│   ├── services/          # Business logic
│   ├── use_cases/         # Application use cases
│   └── value_objects/     # Value objects
├── data/                  # Data Layer
│   ├── models/            # Database models
│   ├── repositories/      # Data access
│   └── external/          # External services
└── config/                # Configuration
```

### Key Principles
1. **Dependency Inversion**: High-level modules don't depend on low-level modules
2. **Single Responsibility**: Each class has one reason to change
3. **Interface Segregation**: Clients depend only on interfaces they use
4. **Open/Closed**: Open for extension, closed for modification

## Development Environment

### VS Code Setup
Recommended extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Ruff (charliermarsh.ruff)
- Docker (ms-azuretools.vscode-docker)
- GitLens (eamodio.gitlens)

### Environment Variables
Create `.env` file with:
```env
# Environment
ENVIRONMENT=development
DEBUG=true

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=zeta_db
DB_USERNAME=postgres
DB_PASSWORD=your_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
JWT_SECRET_KEY=your-secret-key

# AI Services
OPENAI_API_KEY=your-openai-key
```

### Development Tools
```bash
# Code formatting
ruff format .

# Linting
ruff check .

# Type checking
mypy .

# Testing
pytest

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Code Organization

### Domain Layer (`core/`)
Contains business logic and domain models:

```python
# core/domain/entities/user.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: str
    email: str
    username: str
    full_name: str
    is_active: bool = True
    created_at: Optional[datetime] = None
```

### Use Cases (`core/use_cases/`)
Orchestrate business operations:

```python
# core/use_cases/create_user.py
from core.interfaces.repositories import UserRepositoryInterface
from core.domain.entities.user import User

class CreateUserUseCase:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    async def execute(self, user_data: dict) -> User:
        # Validate business rules
        existing_user = await self.user_repo.get_by_email(user_data["email"])
        if existing_user:
            raise ValueError("Email already exists")

        # Create user
        user = User(**user_data)
        return await self.user_repo.create(user)
```

### Controllers (`app/controllers/`)
Handle HTTP requests and responses:

```python
# app/controllers/user_controller.py
from fastapi import APIRouter, Depends
from app.serializers.user import UserCreateRequest, UserResponse
from core.use_cases.create_user import CreateUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    user = await use_case.execute(user_data.dict())
    return UserResponse.from_entity(user)
```

### Repositories (`data/repositories/`)
Handle data persistence:

```python
# data/repositories/user_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from core.interfaces.repositories import UserRepositoryInterface
from core.domain.entities.user import User
from data.models.user import UserModel

class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: User) -> User:
        user_model = UserModel(**user.__dict__)
        self.db.add(user_model)
        await self.db.commit()
        return user_model.to_entity()

    async def get_by_email(self, email: str) -> Optional[User]:
        user_model = await self.db.query(UserModel).filter(
            UserModel.email == email
        ).first()
        return user_model.to_entity() if user_model else None
```

## Best Practices

### Code Style
- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Write descriptive docstrings in Google style
- Keep functions small and focused
- Use meaningful variable and function names

### Error Handling
```python
from app.exceptions import BusinessException, ValidationException

class UserNotFoundError(BusinessException):
    def __init__(self, user_id: str):
        super().__init__(f"User {user_id} not found")

class InvalidEmailError(ValidationException):
    def __init__(self, email: str):
        super().__init__(f"Invalid email format: {email}")
```

### Logging
```python
import logging
from core.shared.logger import get_logger

logger = get_logger(__name__)

async def create_user(user_data: dict) -> User:
    logger.info(f"Creating user with email: {user_data['email']}")
    try:
        user = await self.user_repo.create(user_data)
        logger.info(f"User created successfully: {user.id}")
        return user
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise
```

### Dependency Injection
```python
# app/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from data.repositories.user_repository import UserRepository
from core.use_cases.create_user import CreateUserUseCase

def get_db() -> Session:
    # Database session dependency
    pass

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_create_user_use_case(
    user_repo: UserRepository = Depends(get_user_repository)
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo)
```

## Testing

### Unit Tests
```python
# tests/unit/test_create_user.py
import pytest
from unittest.mock import Mock
from core.use_cases.create_user import CreateUserUseCase
from core.domain.entities.user import User

@pytest.fixture
def mock_user_repo():
    return Mock()

@pytest.fixture
def create_user_use_case(mock_user_repo):
    return CreateUserUseCase(mock_user_repo)

@pytest.mark.asyncio
async def test_create_user_success(create_user_use_case, mock_user_repo):
    # Arrange
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User"
    }
    expected_user = User(id="123", **user_data)
    mock_user_repo.get_by_email.return_value = None
    mock_user_repo.create.return_value = expected_user

    # Act
    result = await create_user_use_case.execute(user_data)

    # Assert
    assert result == expected_user
    mock_user_repo.create.assert_called_once()
```

### Integration Tests
```python
# tests/integration/test_user_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_endpoint():
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "password123"
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

### Test Configuration
```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from data.models.base import Base

@pytest.fixture(scope="session")
def test_db():
    engine = create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    yield SessionLocal()

    Base.metadata.drop_all(engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        return test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
```

## Database

### Models
```python
# data/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from data.models.base import BaseModel
from core.domain.entities.user import User

class UserModel(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            username=self.username,
            full_name=self.full_name,
            is_active=self.is_active,
            created_at=self.created_at
        )
```

### Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Add user table"

# Review generated migration
# Edit alembic/versions/{revision}_add_user_table.py if needed

# Apply migration
alembic upgrade head

# Downgrade if needed
alembic downgrade -1
```

### Query Patterns
```python
# Repository query examples
async def get_active_users(self, limit: int = 10) -> List[User]:
    result = await self.db.execute(
        select(UserModel)
        .where(UserModel.is_active == True)
        .limit(limit)
    )
    return [user.to_entity() for user in result.scalars()]

async def search_users(self, query: str) -> List[User]:
    result = await self.db.execute(
        select(UserModel)
        .where(
            or_(
                UserModel.username.ilike(f"%{query}%"),
                UserModel.full_name.ilike(f"%{query}%")
            )
        )
    )
    return [user.to_entity() for user in result.scalars()]
```

## API Development

### Route Organization
```python
# app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1 import users, agents, chat

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users.router)
api_router.include_router(agents.router)
api_router.include_router(chat.router)
```

### Request/Response Models
```python
# app/serializers/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreateRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserResponse":
        return cls(**user.__dict__)
```

### Validation
```python
# app/validators/user.py
from pydantic import validator
import re

class UserValidator(BaseModel):
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v
```

### Authentication
```python
# app/middleware/auth.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from core.services.auth_service import AuthService

security = HTTPBearer()

async def get_current_user(
    token: str = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    try:
        user = await auth_service.validate_token(token.credentials)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Frontend Development

### React Components
```tsx
// frontend/src/components/UserProfile.tsx
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getUserProfile } from '../api/users';

interface UserProfileProps {
  userId: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => getUserProfile(userId)
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading user</div>;

  return (
    <div className="user-profile">
      <h2>{user.full_name}</h2>
      <p>{user.email}</p>
      <p>Joined: {new Date(user.created_at).toLocaleDateString()}</p>
    </div>
  );
};
```

### API Client
```typescript
// frontend/src/api/client.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 10000,
});

// Request interceptor for auth
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Deployment

### Docker
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - REDIS_HOST=redis
    depends_on:
      - db
      - redis

  worker:
    build: .
    command: celery -A app.worker.celery_app worker -l info
    environment:
      - DB_HOST=db
      - REDIS_HOST=redis
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: zeta_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

volumes:
  postgres_data:
```

### Kubernetes
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: zeta-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: zeta-ai
  template:
    metadata:
      labels:
        app: zeta-ai
    spec:
      containers:
      - name: app
        image: your-registry/zeta-ai:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          value: "postgres-service"
        - name: REDIS_HOST
          value: "redis-service"
```

## Troubleshooting

### Common Issues

#### Database Connection
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U postgres -d zeta_db

# Check logs
tail -f /var/log/postgresql/postgresql-13-main.log
```

#### Redis Connection
```bash
# Check Redis status
sudo systemctl status redis

# Test connection
redis-cli ping

# Monitor Redis
redis-cli monitor
```

#### Celery Issues
```bash
# Check Celery worker
celery -A app.worker.celery_app inspect active

# Purge tasks
celery -A app.worker.celery_app purge

# Monitor tasks
celery -A app.worker.celery_app events
```

### Debugging
```python
# Enable debug mode
import logging
logging.basicConfig(level=logging.DEBUG)

# Use debugger
import pdb; pdb.set_trace()

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()
```

### Performance Monitoring
```python
# Add timing middleware
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Logs Analysis
```bash
# View application logs
tail -f logs/app.log

# Filter error logs
grep ERROR logs/app.log

# Monitor real-time logs
tail -f logs/app.log | grep -E "(ERROR|WARNING)"
```

## Contributing

### Development Workflow
1. Create feature branch from `develop`
2. Implement feature with tests
3. Run quality checks: `ruff check . && mypy . && pytest`
4. Create pull request
5. Code review and merge

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Error handling is proper

### Release Process
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release tag
4. Deploy to staging
5. Run integration tests
6. Deploy to production

---

For more detailed information, refer to:
- [API Reference](API_REFERENCE.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)
