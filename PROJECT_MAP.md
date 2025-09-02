# Project Architecture Map

## Overview
This project implements a DeepSeek AI Extension for VS Code with Python backend services for AI model distillation and training workflows.

## Architecture Principles

### Coding Rules
1. **Type Safety**: All Python code must pass `mypy --strict`
2. **Code Quality**: All code must pass `ruff` linting
3. **Testing**: All code must have comprehensive test coverage and pass `pytest`
4. **Backward Compatibility**: Maintain API stability and backward compatibility
5. **Async-First**: Use async/await patterns for I/O operations
6. **Error Handling**: Implement comprehensive error handling with exponential backoff
7. **Observability**: Include metrics and logging for production monitoring

### Directory Structure

```
├── src/                          # TypeScript VS Code extension
├── python_backend/               # Python backend services
│   ├── core/
│   │   ├── domain/
│   │   │   ├── entities.py       # Core entities (TeacherLabel, DistillationDatapoint)
│   │   │   └── interfaces.py     # Abstract interfaces/ports
│   │   ├── services/
│   │   │   ├── enhanced_service.py   # Core distillation service
│   │   │   ├── cache_service.py      # Caching logic
│   │   │   └── metrics_service.py    # Observability
│   │   └── use_cases/
│   │       └── distillation/
│   │           ├── orchestrator.py   # Main orchestration logic
│   │           └── student_training.py
│   ├── app/
│   │   └── api/
│   │       └── v1/
│   │           └── distillation/
│   │               ├── __init__.py
│   │               ├── endpoints.py  # REST API endpoints
│   │               └── models.py     # Pydantic request/response models
│   ├── infrastructure/
│   │   ├── repositories/         # Data access layer
│   │   │   ├── __init__.py
│   │   │   └── distillation_repository.py
│   │   └── external/
│   │       ├── teacher_model_client.py
│   │       └── cache_client.py
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── test_enhanced_service.py
│   ├── requirements.txt
│   └── pyproject.toml
```

## Core Components

### Primary Components (High Impact)
- **core/domain/entities.py**: Core business entities
- **core/services/enhanced_service.py**: Main distillation service with optimizations
- **core/use_cases/distillation/orchestrator.py**: Workflow orchestration

### Secondary Components (Medium Impact)
- **app/api/v1/distillation/**: REST API layer
- **infrastructure/repositories/**: Data persistence
- **tests/**: Test infrastructure

## Quality Gates

### Required Checks
1. `mypy --strict python_backend/` - Type checking
2. `ruff check python_backend/` - Linting
3. `ruff format python_backend/` - Formatting
4. `pytest python_backend/tests/` - Testing

### Performance Requirements
- API response time < 200ms for cached requests
- Support for concurrent processing with configurable limits
- Batch processing for datasets > 1000 items
- Circuit breaker activation at 5 consecutive failures

### Security Requirements
- Input sanitization for all external inputs
- Rate limiting on API endpoints
- No secrets in code (use environment variables)
- SQL injection prevention in repository layer

## Invariants
1. **API Stability**: Public interfaces must maintain backward compatibility
2. **Error Propagation**: All errors must be properly handled and logged
3. **Resource Management**: All async resources must be properly cleaned up
4. **Testing**: New features require corresponding tests
5. **Documentation**: Public methods require docstrings with examples

## Integration Points
- VS Code Extension (TypeScript) ↔ Python Backend (REST API)
- Teacher Model APIs (external) ↔ Enhanced Service
- Cache Layer (Redis/Memory) ↔ Services
- Metrics Collection ↔ Prometheus/Grafana