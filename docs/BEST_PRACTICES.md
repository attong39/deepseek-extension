# 🎯 Best Practices Guide - ZETA AI Server

Comprehensive best practices guide for developing, deploying, and maintaining ZETA AI Server applications. This guide covers architecture, security, performance, and operational excellence.

## 🏗️ Architecture Best Practices

### Clean Architecture Principles

**1. Dependency Inversion**
```python
# ✅ Good: Depend on abstractions
from abc import ABC, abstractmethod

class AgentRepository(ABC):
    @abstractmethod
    async def create(self, agent_data: dict) -> Agent:
        pass

class AgentService:
    def __init__(self, repository: AgentRepository):
        self.repository = repository  # Depends on abstraction

# ❌ Bad: Depend on concrete implementations
class AgentService:
    def __init__(self):
        self.repository = SQLAgentRepository()  # Tight coupling
```

**2. Single Responsibility Principle**
```python
# ✅ Good: Single responsibility
class AgentValidator:
    def validate_agent_config(self, config: dict) -> bool:
        return self._validate_model(config) and self._validate_temperature(config)

class AgentCreator:
    def create_agent(self, agent_data: dict) -> Agent:
        return Agent(**agent_data)

# ❌ Bad: Multiple responsibilities
class AgentManager:
    def validate_and_create_agent(self, agent_data: dict) -> Agent:
        # Validation logic
        # Creation logic
        # Notification logic
        pass
```

**3. Layered Architecture**
```
📱 Presentation Layer (FastAPI)     ← User interfaces, APIs
🎯 Application Layer (Use Cases)    ← Business workflows
🧠 Domain Layer (Entities)          ← Core business logic
📊 Data Layer (Repositories)        ← Data access
```

### Module Organization

**Project Structure:**
```
zeta_vn/
├── app/                    # Presentation layer
│   ├── api/               # REST API endpoints
│   ├── websockets/        # WebSocket handlers
│   ├── controllers/       # Request/response handling
│   └── validators/        # Input validation
├── core/                  # Domain layer
│   ├── entities/          # Business entities
│   ├── services/          # Domain services
│   ├── use_cases/         # Application use cases
│   └── interfaces/        # Abstract interfaces
├── data/                  # Data layer
│   ├── repositories/      # Data repositories
│   ├── models/            # SQLAlchemy models
│   └── dto/               # Data transfer objects
└── config/                # Configuration
```

**Import Guidelines:**
```python
# ✅ Good: Clear import structure
from core.entities.agent import Agent
from core.interfaces.repositories import AgentRepository
from data.repositories.agent_repository import SQLAgentRepository

# ❌ Bad: Circular imports, unclear structure
from ..models import Agent  # Relative imports across layers
from data import *          # Wildcard imports
```

---

## 🔒 Security Best Practices

### Authentication & Authorization

**1. JWT Token Management**
```python
# ✅ Good: Secure token handling
import secrets
from datetime import datetime, timedelta
from jose import jwt

class TokenManager:
    def __init__(self):
        self.secret_key = secrets.token_urlsafe(32)
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(minutes=30)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + self.access_token_expire
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except jwt.JWTError:
            raise InvalidTokenError()

# ❌ Bad: Insecure token handling
def create_token(user_id):
    return f"{user_id}:{datetime.now()}"  # Not encrypted, predictable
```

**2. Password Security**
```python
# ✅ Good: Secure password handling
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

# ❌ Bad: Insecure password handling
import hashlib

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is not secure
```

**3. API Key Management**
```python
# ✅ Good: Environment-based secrets
import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

    @classmethod
    def validate_secrets(cls):
        required_secrets = ["OPENAI_API_KEY", "SECRET_KEY", "DATABASE_URL"]
        missing = [key for key in required_secrets if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")

# ❌ Bad: Hardcoded secrets
OPENAI_API_KEY = "sk-proj-123456789"  # Never do this!
SECRET_KEY = "mysecretkey"           # Hardcoded in source
```

### Input Validation & Sanitization

**1. Pydantic Validation**
```python
# ✅ Good: Comprehensive validation
from pydantic import BaseModel, validator, EmailStr
from typing import Optional
import re

class CreateAgentRequest(BaseModel):
    name: str
    description: str
    config: AgentConfig
    tags: Optional[list[str]] = []

    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Name must be less than 100 characters")
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', v):
            raise ValueError("Name contains invalid characters")
        return v.strip()

    @validator('tags')
    def validate_tags(cls, v):
        if v and len(v) > 10:
            raise ValueError("Maximum 10 tags allowed")
        return [tag.strip().lower() for tag in v if tag.strip()]

# ❌ Bad: No validation
def create_agent(name, description, config):
    # Direct database insertion without validation
    return Agent(name=name, description=description, config=config)
```

**2. SQL Injection Prevention**
```python
# ✅ Good: Parameterized queries with SQLAlchemy
from sqlalchemy import text

async def get_agents_by_user(session: AsyncSession, user_id: int):
    query = text("SELECT * FROM agents WHERE user_id = :user_id")
    result = await session.execute(query, {"user_id": user_id})
    return result.fetchall()

# ❌ Bad: String concatenation
async def get_agents_by_user(session: AsyncSession, user_id: int):
    query = f"SELECT * FROM agents WHERE user_id = {user_id}"  # SQL injection risk
    result = await session.execute(text(query))
    return result.fetchall()
```

---

## 🚀 Performance Best Practices

### Database Optimization

... (content continues with caching, async patterns, testing, monitoring, DevOps, scalability, and code quality best practices) ...

---

## 🎉 Summary

Following these best practices will help you build:

- **🏗️ Maintainable Architecture** - Clean, testable, and extensible code
- **🔒 Secure Applications** - Protected against common vulnerabilities
- **🚀 High-Performance Systems** - Optimized for speed and efficiency
- **🧪 Reliable Software** - Well-tested and monitored
- **📈 Scalable Solutions** - Ready for growth and high loads

### Quick Checklist

- [ ] **Architecture**: Following Clean Architecture principles
- [ ] **Security**: JWT authentication, input validation, secrets management
- [ ] **Performance**: Database optimization, caching, async programming
- [ ] **Testing**: Unit tests, integration tests, proper mocking
- [ ] **Monitoring**: Structured logging, performance tracking, health checks
- [ ] **DevOps**: CI/CD pipeline, Docker optimization, deployment automation
- [ ] **Code Quality**: Clear naming, single responsibility, error handling

### Resources

- [API Reference](./API_REFERENCE.md)
- [Development Guide](./guides/development.md)
- [Troubleshooting Guide](./TROUBLESHOOTING.md)
- [Security Guidelines](./SECURITY.md)

---

Last updated: 2025-08-14
