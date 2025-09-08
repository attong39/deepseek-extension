# 🤝 Contributing to ZETA AI Server

## 🎯 Welcome

Thank you for your interest in contributing to ZETA AI Server! This guide will help you get started with contributing to our AI-powered server platform.

## 🗂️ Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## 📝 Code of Conduct

This project adheres to a Code of Conduct. By participating, you agree to uphold this code. Please report unacceptable behavior to conduct@zeta-ai.com.

### Our Standards
- **Be respectful** and inclusive of all contributors
- **Be collaborative** and help others learn
- **Be constructive** in feedback and discussions
- **Be patient** with newcomers and questions

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Git
- Basic knowledge of FastAPI, SQLAlchemy, and Clean Architecture

### Setup Development Environment
```bash
# 1. Fork and clone the repository
git clone https://github.com/your-username/zeta-ai-server.git
cd zeta-ai-server

# 2. Set up development environment
./scripts/dev_setup.sh

# 3. Start development services
docker-compose -f docker-compose.dev.yml up -d

# 4. Run tests to verify setup
python -m pytest tests/ -v

# 5. Start the development server
python -m uvicorn app.main:app --reload
```

## 🔄 Development Workflow

### Branch Strategy
We use a simplified Git flow:
- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature development branches
- `hotfix/*` - Critical bug fixes

### Creating a Feature Branch
```bash
# Start from develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "feat: add your feature description"

# Push to your fork
git push origin feature/your-feature-name
```

### Commit Message Convention
We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(agents): add multi-agent orchestration
fix(chat): resolve message ordering issue
docs(api): update authentication examples
test(memory): add integration tests for storage
```

## 🧑‍💻 Coding Standards

### Python Code Style
We use **ruff** for linting and formatting:

```bash
# Check code style
ruff check .

# Format code
ruff format .

# Fix auto-fixable issues
ruff check --fix .
```

### Type Hints
- **100% type coverage** required
- Use `mypy --strict` for type checking
- Import types from `typing` for Python 3.11+

```python
from typing import List, Dict, Optional, Union
from uuid import UUID

def get_agent_by_id(agent_id: UUID) -> Optional[Agent]:
    """Get agent by ID with proper type hints."""
    pass
```

### Clean Architecture Rules
1. **Dependencies point inward**: `app` → `core` ← `data`
2. **No circular imports**: Use dependency injection
3. **Core layer is pure**: No external dependencies in `core/`
4. **Use interfaces**: Abstract repository interfaces in `core/interfaces/`

### Code Quality Checklist
- [ ] Follows Clean Architecture principles
- [ ] Has 100% type coverage (mypy --strict)
- [ ] Passes all linters (ruff)
- [ ] Has comprehensive tests (≥80% coverage)
- [ ] Includes docstrings for public APIs
- [ ] No hardcoded values (use config)
- [ ] Proper error handling
- [ ] Logging for important operations

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests with external dependencies
├── e2e/           # End-to-end user journey tests
├── performance/   # Load and stress tests
└── fixtures/      # Shared test data
```

### Writing Tests
```python
import pytest
from unittest.mock import Mock, patch

class TestAgentCreation:
    """Test agent creation functionality."""

    @pytest.fixture
    def mock_repository(self):
        """Mock agent repository."""
        return Mock()

    async def test_create_agent_success(self, mock_repository):
        """Test successful agent creation."""
        # Arrange
        agent_data = AgentCreate(name="Test Agent")
        mock_repository.create.return_value = Agent(id="123", name="Test Agent")

        # Act
        use_case = CreateAgent(mock_repository)
        result = await use_case.execute(agent_data)

        # Assert
        assert result.name == "Test Agent"
        mock_repository.create.assert_called_once_with(agent_data)
```

### Test Requirements
- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **E2E tests**: Test complete user workflows
- **Coverage**: Minimum 80% code coverage
- **Fast**: Unit tests should run in <1 second each

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/unit/test_agents.py

# Run with coverage
python -m pytest --cov=. --cov-report=html

# Run performance tests
python -m pytest tests/performance/ -m slow
```

## 📚 Documentation

### Documentation Types
1. **API Documentation**: Auto-generated from FastAPI
2. **Architecture Documentation**: High-level system design
3. **Code Documentation**: Docstrings and inline comments
4. **User Guides**: How-to guides for end users

### Docstring Style
We use **Google style** docstrings:

```python
def create_agent(name: str, config: AgentConfig) -> Agent:
    """Create a new AI agent.

    Args:
        name: The agent's display name
        config: Agent configuration parameters

    Returns:
        The newly created agent instance

    Raises:
        ValidationError: If the agent data is invalid
        DuplicateError: If an agent with this name exists

    Example:
        >>> config = AgentConfig(model="gpt-4")
        >>> agent = create_agent("Assistant", config)
        >>> print(agent.name)
        Assistant
    """
    pass
```

### Documentation Updates
- Update docs when adding new features
- Include examples for new APIs
- Update architecture diagrams if needed
- Add troubleshooting guides for common issues

## 🔄 Pull Request Process

### Before Submitting
1. **Rebase** your branch on latest `develop`
2. **Run all tests** and ensure they pass
3. **Check code quality** with ruff and mypy
4. **Update documentation** if needed
5. **Write descriptive commit messages**

### PR Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that breaks existing functionality)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass locally

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or properly documented)
```

### Review Process
1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Architecture review** for significant changes
4. **Testing verification** in staging environment
5. **Final approval** and merge by maintainer

## 🐛 Issue Reporting

### Bug Reports
Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.11.0]
- ZETA AI Server version: [e.g. 1.0.0]

**Additional context**
Any other context about the problem.
```

### Feature Requests
Use the feature request template:

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Any other context about the feature request.
```

## 🏅 Recognition

### Contributors
We recognize contributors in:
- README.md contributors section
- Release notes
- Annual contributor awards
- Community showcase

### Maintainer Nomination
Active contributors may be nominated as maintainers based on:
- Consistent high-quality contributions
- Understanding of project architecture
- Community involvement
- Code review participation

## 📞 Getting Help

### Communication Channels
- **Discord**: [https://discord.gg/zeta-ai](https://discord.gg/zeta-ai)
- **GitHub Discussions**: For technical discussions
- **Email**: developers@zeta-ai.com

### Mentorship
New contributors can request mentorship through:
- Discord mentorship channel
- GitHub discussions
- Direct message to maintainers

## 🗃️ Resources

### Learning Resources
- [Clean Architecture Guide](./ARCHITECTURE.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Development Tools
- [VS Code Extensions](../.vscode/extensions.json)
- [Pre-commit Hooks](../.pre-commit-config.yaml)
- [Docker Development](../docker-compose.dev.yml)

---

Thank you for contributing to ZETA AI Server! Your contributions help make AI more accessible and powerful for everyone. 🚀

*Last updated: 2025-08-14*
