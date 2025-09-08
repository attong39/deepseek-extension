# 📚 Frequently Asked Questions (FAQ) - ZETA AI Server

Comprehensive FAQ covering common questions about ZETA AI Server setup, usage, troubleshooting, and best practices. Find quick answers to the most frequently asked questions.

## 🚀 Getting Started

### Q: What is ZETA AI Server?
**A:** ZETA AI Server is a production-ready AI agent management platform built with FastAPI, SQLAlchemy, and Clean Architecture principles. It provides:

- **🤖 AI Agent Management** - Create, configure, and manage multiple AI agents
- **💬 Conversation Handling** - Real-time chat with memory and context
- **🧠 Memory System** - Long-term and short-term memory for agents
- **🔒 Enterprise Security** - JWT authentication, rate limiting, and data protection
- **📈 Analytics & Monitoring** - Performance tracking and usage analytics
- **🚀 Scalable Architecture** - Microservices-ready with horizontal scaling

### Q: What are the minimum system requirements?
**A:**
- **Development**: 4GB RAM, 2GB disk space, Python 3.11+
- **Production**: 8GB RAM, 20GB disk space, PostgreSQL, Redis
- **Docker**: 6GB RAM, 10GB disk space
- **Operating System**: Linux (Ubuntu 20.04+), macOS 10.15+, Windows 10+

### Q: How do I quickly get started?
**A:** Use our 30-second setup:

```bash
# Clone and setup
git clone https://github.com/your-org/zeta-ai-server.git
cd zeta-ai-server
docker-compose up -d

# Access the application
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

For detailed setup, see our [Quick Start Guide](./guides/quick_start.md).

---

## 🔧 Installation & Setup

### Q: Which installation method should I choose?

**A:** Choose based on your use case:

| Method | Best For | Complexity | Time |
|--------|----------|------------|------|
| **Docker Compose** | Development, Testing | ⭐ Easy | 2 minutes |
| **Manual Installation** | Customization | ⭐⭐ Medium | 10 minutes |
| **Kubernetes** | Production | ⭐⭐⭐ Advanced | 30 minutes |
| **Source Installation** | Development | ⭐⭐ Medium | 15 minutes |

### Q: How do I configure environment variables?
**A:** Create a `.env` file with required variables:

```bash
# Core Settings
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/zeta_ai
REDIS_URL=redis://localhost:6379/0

# AI Configuration
OPENAI_API_KEY=sk-proj-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Security
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Features
ENABLE_MEMORY_SYSTEM=true
ENABLE_ANALYTICS=true
ENABLE_RATE_LIMITING=true
```

### Q: What if I get database connection errors?
**A:** Common solutions:

1. **Check database is running**:
   ```bash
   # PostgreSQL
   sudo systemctl status postgresql

   # Docker
   docker ps | grep postgres
   ```

2. **Verify connection string**:
   ```bash
   # Test connection
   psql "postgresql://user:password@localhost:5432/zeta_ai"
   ```

3. **Check firewall/network**:
   ```bash
   # Test port connectivity
   telnet localhost 5432
   ```

4. **Reset database**:
   ```bash
   # Drop and recreate
   python scripts/setup_development.py --reset-db
   ```

### Q: How do I fix Redis connection issues?
**A:**

1. **Start Redis**:
   ```bash
   # Ubuntu/Debian
   sudo systemctl start redis-server

   # Docker
   docker run -d -p 6379:6379 redis:7
   ```

2. **Test connection**:
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

3. **Check configuration**:
   ```bash
   # Verify Redis config
   redis-cli config get "*"
   ```

---

## 🤖 AI Agents

### Q: How do I create my first AI agent?
**A:** Use the API or admin interface:

```python
import httpx

# Create agent via API
async def create_agent():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/agents",
            json={
                "name": "My First Agent",
                "description": "A helpful assistant",
                "config": {
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "system_prompt": "You are a helpful assistant."
                }
            },
            headers={"Authorization": "Bearer YOUR_TOKEN"}
        )
        return response.json()
```

### Q: Which AI models are supported?
**A:** Currently supported models:

| Provider | Models | Best For |
|----------|--------|----------|
| **OpenAI** | GPT-4, GPT-3.5-turbo | General purpose, complex reasoning |
| **Anthropic** | Claude-3, Claude-2 | Long conversations, analysis |
| **Local** | Ollama models | Privacy, cost control |
| **Custom** | API-compatible | Specialized models |

### Q: How do I configure agent memory?
**A:** Memory is automatically enabled. Configure via agent settings:

```python
agent_config = {
    "memory": {
        "enabled": True,
        "max_memories": 1000,
        "memory_types": ["user_preferences", "conversation_context", "facts"],
        "retention_days": 30
    }
}
```

### Q: Can agents access external tools?
**A:** Yes! Configure tools in agent settings:

```python
agent_config = {
    "tools": [
        {
            "name": "web_search",
            "type": "function",
            "config": {
                "search_engine": "google",
                "max_results": 5
            }
        },
        {
            "name": "calculator",
            "type": "function",
            "config": {
                "precision": 10
            }
        }
    ]
}
```

### Q: How do I handle rate limiting for AI APIs?
**A:** Built-in rate limiting with configuration:

```python
# In your settings
RATE_LIMITS = {
    "openai": {
        "requests_per_minute": 60,
        "tokens_per_minute": 40000
    },
    "anthropic": {
        "requests_per_minute": 30,
        "tokens_per_minute": 20000
    }
}
```

---

## 💬 Conversations

### Q: How do I start a conversation?
**A:** Create a conversation via API:

```python
# Start conversation
response = await client.post(
    "http://localhost:8000/api/v1/conversations",
    json={
        "agent_id": "agent-uuid",
        "title": "My Conversation"
    }
)

conversation_id = response.json()["id"]

# Send message
await client.post(
    f"http://localhost:8000/api/v1/conversations/{conversation_id}/messages",
    json={
        "content": "Hello! How can you help me today?",
        "role": "user"
    }
)
```

### Q: Does the system support real-time chat?
**A:** Yes! Use WebSocket connections:

```javascript
// JavaScript WebSocket client
const ws = new WebSocket('ws://localhost:8000/ws/conversations/CONVERSATION_ID');

ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log('New message:', message);
};

ws.send(JSON.stringify({
    type: 'message',
    content: 'Hello via WebSocket!'
}));
```

### Q: How does conversation memory work?
**A:** The system maintains multiple memory types:

- **Short-term Memory**: Recent conversation context (last 10-20 messages)
- **Long-term Memory**: Important facts, preferences, and patterns
- **Episodic Memory**: Specific conversation events and outcomes
- **Semantic Memory**: General knowledge learned from interactions

### Q: Can I export conversation history?
**A:** Yes, multiple export formats:

```python
# Export conversation
response = await client.get(
    f"http://localhost:8000/api/v1/conversations/{conversation_id}/export",
    params={"format": "json"}  # json, csv, txt
)
```

---

## 🔐 Security & Authentication

### Q: How do I get an API token?
**A:** Authenticate to receive a JWT token:

```python
# Login to get token
response = await client.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "user@example.com",
        "password": "your-password"
    }
)

token = response.json()["access_token"]

# Use token in requests
headers = {"Authorization": f"Bearer {token}"}
```

### Q: How long do tokens last?
**A:** Token lifetimes (configurable):

- **Access Token**: 30 minutes (default)
- **Refresh Token**: 7 days (default)
- **API Key**: Never expires (until revoked)

### Q: How do I secure my installation?
**A:** Follow security checklist:

1. **Environment Variables**: Never hardcode secrets
2. **HTTPS**: Use SSL certificates in production
3. **Firewall**: Restrict database/Redis access
4. **Rate Limiting**: Enable API rate limits
5. **CORS**: Configure allowed origins
6. **Updates**: Keep dependencies updated

```bash
# Security audit
python scripts/security_audit.py
```

### Q: How do I manage user permissions?
**A:** Role-based access control:

```python
# User roles
ROLES = {
    "admin": ["*"],  # All permissions
    "user": ["agents:read", "conversations:create"],
    "viewer": ["agents:read", "conversations:read"]
}
```

---

## 📈 Monitoring & Analytics

### Q: How do I monitor system health?
**A:** Use built-in health checks:

```bash
# Health check endpoint
curl http://localhost:8000/api/v1/health

# Detailed system status
curl http://localhost:8000/api/v1/status
```

### Q: What metrics are collected?
**A:** Key metrics include:

- **Performance**: Response times, throughput, error rates
- **Usage**: API calls, active users, conversation counts
- **Resources**: CPU, memory, database connections
- **AI**: Token usage, model performance, cost tracking

### Q: How do I access analytics dashboard?
**A:** Available at multiple endpoints:

- **Web Dashboard**: `http://localhost:8000/admin/analytics`
- **API Metrics**: `http://localhost:8000/api/v1/metrics`
- **Prometheus**: `http://localhost:8000/metrics` (if enabled)

### Q: Can I integrate with external monitoring?
**A:** Yes, supports popular tools:

```yaml
# Prometheus configuration
prometheus:
  enabled: true
  port: 9090

grafana:
  enabled: true
  dashboard_url: "http://localhost:3000"

datadog:
  enabled: false
  api_key: "your-datadog-key"
```

---

## 🚀 Performance & Scaling

### Q: How many requests can the system handle?
**A:** Performance benchmarks:

- **Single Instance**: 1,000-2,000 req/sec
- **With Redis Cache**: 3,000-5,000 req/sec
- **Horizontal Scale**: 10,000+ req/sec (multiple instances)
- **Database**: 50,000+ queries/sec (with read replicas)

### Q: How do I improve performance?
**A:** Optimization strategies:

1. **Enable Caching**: Redis for frequently accessed data
2. **Database Optimization**: Connection pooling, indexes
3. **Load Balancing**: Multiple application instances
4. **CDN**: Static assets and API responses
5. **Async Processing**: Background tasks with Celery

```python
# Performance configuration
PERFORMANCE_SETTINGS = {
    "database_pool_size": 20,
    "redis_max_connections": 100,
    "async_workers": 4,
    "cache_ttl": 300
}
```

### Q: How do I scale horizontally?
**A:** Deploy multiple instances:

```yaml
# Docker Compose scaling
version: '3.8'
services:
  app:
    image: zeta-ai-server
    scale: 3  # Run 3 instances

  nginx:
    image: nginx
    # Load balancer configuration
```

### Q: What about database scaling?
**A:** Database scaling options:

1. **Read Replicas**: Separate read/write operations
2. **Connection Pooling**: Optimize connection usage
3. **Partitioning**: Split large tables
4. **Caching**: Reduce database load

---

## 🛠️ Development

### Q: How do I contribute to the project?
**A:** Follow our contribution guide:

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/new-feature`
3. **Make** changes with tests
4. **Run** quality checks: `ruff check . && pytest`
5. **Submit** pull request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

### Q: How do I run tests?
**A:** Comprehensive testing:

```bash
# Run all tests
pytest

# With coverage
pytest --cov=zeta_vn --cov-report=html

# Specific test types
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/e2e/          # End-to-end tests

# Performance tests
pytest tests/performance/ --benchmark-only
```

### Q: How do I debug issues?
**A:** Debugging tools:

1. **Logs**: Check application logs
   ```bash
   tail -f logs/app.log
   ```

2. **Debug Mode**: Enable detailed logging
   ```python
   ENVIRONMENT=development
   LOG_LEVEL=DEBUG
   ```

3. **Database Queries**: Monitor SQL
   ```python
   SQLALCHEMY_ECHO=true
   ```

4. **Profiling**: Use built-in profiler
   ```bash
   python -m cProfile -o profile.stats scripts/profile_app.py
   ```

### Q: How do I add new features?
**A:** Follow Clean Architecture:

1. **Domain Layer**: Add entities and business logic
2. **Application Layer**: Create use cases
3. **Infrastructure Layer**: Implement repositories
4. **Presentation Layer**: Add API endpoints
5. **Tests**: Write comprehensive tests

---

## 🐛 Troubleshooting

### Q: The application won't start. What should I check?

**A:** Common startup issues:

1. **Check environment variables**:
   ```bash
   python -c "from zeta_vn.config.settings import get_settings; print(get_settings())"
   ```

2. **Verify dependencies**:
   ```bash
   pip check
   ```

3. **Test database connection**:
   ```bash
   python scripts/check_database.py
   ```

4. **Check ports**:
   ```bash
   lsof -i :8000  # Check if port is in use
   ```

### Q: AI responses are slow. How can I fix this?

**A:** Performance tuning:

1. **Check AI API latency**:
   ```bash
   curl -w "%{time_total}" -s -o /dev/null "https://api.openai.com/v1/models"
   ```

2. **Enable response streaming**:
   ```python
   agent_config = {
       "streaming": True,
       "max_tokens": 1000  # Limit response length
   }
   ```

3. **Use faster models**:
   ```python
   # Use GPT-3.5-turbo instead of GPT-4 for faster responses
   "model": "gpt-3.5-turbo"
   ```

4. **Implement caching**:
   ```python
   # Cache similar requests
   ENABLE_RESPONSE_CACHE = True
   CACHE_TTL = 300  # 5 minutes
   ```

### Q: Getting memory errors with large conversations?

**A:** Memory optimization:

1. **Limit conversation history**:
   ```python
   CONVERSATION_SETTINGS = {
       "max_messages": 100,
       "auto_summarize": True,
       "summarize_threshold": 50
   }
   ```

2. **Enable message pagination**:
   ```python
   # Load messages in chunks
   messages = await get_messages(
       conversation_id=conv_id,
       limit=20,
       offset=0
   )
   ```

3. **Configure memory management**:
   ```python
   MEMORY_SETTINGS = {
       "max_memory_items": 1000,
       "cleanup_interval": 3600,  # 1 hour
       "compression_enabled": True
   }
   ```

### Q: Database is running out of space?

**A:** Database maintenance:

1. **Check disk usage**:
   ```sql
   SELECT
       schemaname,
       tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
   FROM pg_tables
   ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
   ```

2. **Clean old data**:
   ```bash
   python scripts/cleanup_old_data.py --days=30
   ```

3. **Archive conversations**:
   ```bash
   python scripts/archive_conversations.py --older-than=90d
   ```

4. **Optimize database**:
   ```sql
   VACUUM ANALYZE;
   REINDEX DATABASE zeta_ai;
   ```

---

## 📈 Deployment & Production

### Q: How do I deploy to production?

**A:** Production deployment options:

1. **Docker (Recommended)**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Kubernetes**:
   ```bash
   kubectl apply -f deployment/kubernetes/
   ```

3. **Traditional Server**:
   ```bash
   python scripts/deploy_production.py
   ```

### Q: What environment variables do I need for production?

**A:** Essential production variables:

```bash
# Security
SECRET_KEY=your-256-bit-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=["https://yourdomain.com"]

# Database
DATABASE_URL=postgresql://user:pass@db:5432/zeta_ai
REDIS_URL=redis://redis:6379/0

# AI Services
OPENAI_API_KEY=sk-proj-your-key
ANTHROPIC_API_KEY=sk-ant-your-key

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=INFO
ENABLE_METRICS=true

# Performance
WORKERS=4
MAX_CONNECTIONS=100
CACHE_TTL=300
```

### Q: How do I handle SSL certificates?

**A:** SSL setup options:

1. **Let's Encrypt (Free)**:
   ```bash
   certbot --nginx -d api.yourdomain.com
   ```

2. **Load Balancer SSL**: Use cloud provider SSL termination

3. **Reverse Proxy**: Configure Nginx/Apache with SSL

### Q: How do I backup the database?

**A:** Automated backup strategy:

```bash
# Daily backup script
python scripts/backup_database.py --format=sql --compress=true

# Backup to S3
python scripts/backup_database.py --storage=s3 --bucket=your-backups

# Restore from backup
python scripts/restore_database.py --file=backup_2024_01_15.sql.gz
```

---

## 💡 Best Practices

### Q: What are the recommended coding standards?

**A:** Follow our style guide:

- **Code Style**: Use Black formatter and Ruff linter
- **Type Hints**: Always use type annotations
- **Documentation**: Docstrings for all public functions
- **Testing**: Minimum 80% code coverage
- **Architecture**: Follow Clean Architecture principles

### Q: How should I structure agent prompts?

**A:** Effective prompt structure:

```python
system_prompt = """
You are {agent_role}, an AI assistant specialized in {domain}.

## Your Capabilities:
- {capability_1}
- {capability_2}
- {capability_3}

## Guidelines:
1. Always be helpful and accurate
2. If unsure, say so rather than guessing
3. Use {tone} tone in responses
4. Keep responses {length_preference}

## Context:
{context_information}
"""
```

### Q: How do I optimize costs for AI API usage?

**A:** Cost optimization strategies:

1. **Model Selection**: Use appropriate models for tasks
2. **Token Management**: Implement token counting and limits
3. **Caching**: Cache similar responses
4. **Batch Processing**: Group similar requests
5. **Usage Monitoring**: Track and alert on costs

```python
COST_OPTIMIZATION = {
    "max_tokens_per_request": 1000,
    "enable_response_caching": True,
    "use_cheaper_models_for_simple_tasks": True,
    "daily_cost_limit": 100  # USD
}
```

---

## 🆘 Getting Help

### Q: Where can I get support?

**A:** Support channels:

- **📖 Documentation**: [docs/](./README.md)
- **🐛 Issues**: [GitHub Issues](https://github.com/your-org/zeta-ai-server/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/your-org/zeta-ai-server/discussions)
- **✉️ Email**: support@zeta-ai.com
- **💬 Discord**: [Community Server](https://discord.gg/zeta-ai)

### Q: How do I report a bug?

**A:** Bug report template:

1. **Environment**: OS, Python version, installation method
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Logs**: Relevant error messages
6. **Configuration**: Relevant settings (sanitized)

### Q: How do I request a feature?

**A:** Feature request process:

1. **Check Existing**: Search existing issues/discussions
2. **Use Template**: Follow feature request template
3. **Provide Context**: Use case and justification
4. **Community Input**: Engage with community feedback

---

## 📝 Additional Resources

### Quick Links

- [🚀 Quick Start Guide](./guides/quick_start.md)
- [🔧 Installation Guide](./INSTALLATION.md)
- [📖 API Documentation](./API_REFERENCE.md)
- [🏗️ Architecture Guide](./ARCHITECTURE.md)
- [🔒 Security Guide](./SECURITY.md)
- [🛠️ Development Guide](./guides/development.md)
- [🐛 Troubleshooting](./TROUBLESHOOTING.md)

### Video Tutorials

- [📹 Getting Started (5 min)](https://youtube.com/watch?v=example)
- [📹 Creating Your First Agent (10 min)](https://youtube.com/watch?v=example)
- [📹 Production Deployment (15 min)](https://youtube.com/watch?v=example)

---

**❓ Still have questions?**

Check our [GitHub Discussions](https://github.com/your-org/zeta-ai-server/discussions) or [open an issue](https://github.com/your-org/zeta-ai-server/issues/new).

*Last updated: 2025-08-14*
