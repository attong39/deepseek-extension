# 🛠 Troubleshooting Guide - ZETA AI Server

Comprehensive troubleshooting guide for ZETA AI Server. This document covers common issues, debugging techniques, error resolution, and best practices for maintaining a healthy system.

## 🎯 Quick Issue Resolution

### Most Common Issues (90% of problems)

| Issue | Quick Fix | Time |
|-------|----------|------|
| Authentication Error | Refresh token or check API key format | 2 min |
| Rate Limit Exceeded | Wait and retry or upgrade plan | 5 min |
| Agent Not Responding | Check model status and reduce complexity | 3 min |
| Database Connection | Restart containers or check config | 5 min |
| Memory Not Working | Verify agent memory settings enabled | 2 min |

### Emergency Contacts

- Critical Issues: emergency@zeta-ai.com
- Status Updates: https://status.zeta-ai.com
- Live Chat: Available 24/7 for Enterprise customers

---

## 🔎 Diagnostic Tools

### Health Check Commands

```bash
# Check API health
curl -X GET "https://api.zeta-ai.com/api/v1/health"

# Check authentication
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.zeta-ai.com/api/v1/users/me"

# Test agent creation
curl -X POST "https://api.zeta-ai.com/api/v1/agents" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Agent", "description": "Test"}'
```

### System Status Verification

```bash
# Check all services
curl -X GET "https://api.zeta-ai.com/api/v1/system/status" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Response example:
{
  "status": "healthy",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "celery": "healthy",
    "ai_services": {
      "openai": "healthy",
      "anthropic": "degraded"
    }
  }
}
```

### Log Analysis Tools

```bash
# Get application logs (Admin only)
curl -X GET "https://api.zeta-ai.com/api/v1/admin/logs?level=error&limit=100" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Local development logs
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f redis
```

---

## 🔐 Authentication Issues

### Invalid Token Errors

Symptoms:
- HTTP 401 Unauthorized
- "Invalid token" or "Token expired" messages
- Authentication required errors

Diagnosis:
```bash
# Check token format (should be JWT)
echo "YOUR_TOKEN" | cut -d'.' -f2 | base64 -d

# Verify token hasn't expired
python3 -c "
import jwt
import datetime
token = 'YOUR_TOKEN'
try:
    payload = jwt.decode(token, options={'verify_signature': False})
    exp = datetime.datetime.fromtimestamp(payload['exp'])
    print(f'Token expires: {exp}')
    print(f'Current time: {datetime.datetime.now()}')
    print(f'Valid: {exp > datetime.datetime.now()}')
except Exception as e:
    print(f'Error: {e}')
"
```

Solutions:

1) Refresh Access Token:
```bash
curl -X POST "https://api.zeta-ai.com/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
```

2) Re-login:
```bash
curl -X POST "https://api.zeta-ai.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

3) Check Token Storage (browser/local):
```javascript
localStorage.getItem('access_token')
localStorage.getItem('refresh_token')
```

### Permission Denied Errors (403)

Diagnosis:
```bash
curl -X GET "https://api.zeta-ai.com/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Solutions:
- Request elevated permissions
- Use an account with correct role
- Check endpoint requirements

### Login Issues

Diagnosis:
```bash
curl -X POST "https://api.zeta-ai.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test"}' \
  -w "Response Time: %{time_total}s\n"
```

Solutions:
- Reset password
- Verify account status
- Check network/endpoint

---

## 🤖 Agent Issues

### Agent Not Responding

Diagnosis:
```bash
curl -X GET "https://api.zeta-ai.com/api/v1/agents/AGENT_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Solutions:
- Check model availability
- Reduce max_tokens
- Simplify system prompt
- Check upstream status (OpenAI/Anthropic)

### Memory Not Working

Diagnosis:
```bash
curl -X GET "https://api.zeta-ai.com/api/v1/memory?agent_id=AGENT_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Solutions:
- Enable memory in agent config
- Test storing a memory
- Verify conversation settings

### Agent Configuration Errors

Common issues: temperature range, model name, token limits. Use validation endpoint before creating.

---

## 💬 Conversation Issues

- Messages not sending: check rate limits; implement retry with backoff
- Streaming issues: verify SSE/WebSocket handling; network timeouts; server logs

---

## 📄 Database Issues

- Connection problems: restart DB, verify URL, pool settings
- Migration issues: alembic current/history; upgrade head; regenerate migrations
- Performance: indexes, eager loading, maintenance (VACUUM/ANALYZE)

---

## ⚡ Performance Issues

- High response times: caching, pagination, async tasks
- Memory issues: profiling, generators, connection cleanup, container memory limits

---

## 🌀 Background Task Issues

- Celery workers: inspect active/stats; restart workers; purge queue; monitor with Flower
- Redis: test connectivity; check memory and config; connection pools

---

## 🌐 Network/Connectivity

- DNS/SSL: nslookup/curl/openssl checks; update cert store
- Firewall: open required ports; check Docker networks

---

## 📊 Monitoring & Logging

- Log locations: app, DB, Redis, Nginx
- Add monitoring middleware; scheduled health checks

---

## 🧪 Dev Environment Issues

- Docker: container status, logs, resource usage; prune unused artifacts
- Environment variables: verify .env; docker-compose env_file

---

## 🆘 Emergency Procedures

- Service recovery: restart stack; verify health; inspect logs
- Database recovery: backup/restore
- Data export: admin export endpoints

---

## 📣 Getting Help

- Documentation: https://docs.zeta-ai.com
- Status: https://status.zeta-ai.com
- Community: https://community.zeta-ai.com
- GitHub Issues: https://github.com/zeta-ai/issues

Include when contacting support: account ID, errors, steps, expected vs actual, client info, time.

Enterprise support: dedicated team, phone, custom SLAs, priority.

---

## ✅ Prevention & Best Practices

- Proactive monitoring, maintenance schedule, performance settings

Keep this guide handy.

Last updated: 2025-08-14
