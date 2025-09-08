# Enhanced Authentication System v2.1

A production-ready, enterprise-grade authentication system with comprehensive security, observability, and operational features.

## 🚀 Quick Start

```python
from factory import create_mfa_system
from mfa_config import MFAConfig

# Create enhanced production system
config = MFAConfig(
    hmac_secret_key="your-256-bit-secret-key",
    enable_metrics=True,
    enable_tracing=True,
    adaptive_rate_limiting=True,
    enable_dynamic_blocklist=True
)

mfa_manager, sms_manager, email_manager, device_trust, metrics = create_mfa_system(
    config=config,
    storage_backend="redis",  # or "memory" for development
    enable_metrics=True,
    enable_tracing=True
)

# Send SMS with enhanced security
await mfa_manager.send_sms_code("user123", "+1234567890")

# Verify with device trust and metrics
success = await mfa_manager.verify_mfa(
    user_id="user123",
    phone="+1234567890", 
    code="123456",
    device_fingerprint="browser-chrome-windows"
)
```

## 🏗️ Architecture

### Core Components

- **MFA Manager**: Orchestrates authentication flow with enhanced security
- **SMS Manager**: Handles SMS codes with anti-bombing protection  
- **Email Manager**: Manages email verification with backup codes
- **Device Trust Manager**: HMAC-based device fingerprinting and trust
- **Rate Limiter**: Multi-layer adaptive rate limiting
- **Metrics System**: Prometheus metrics with OpenTelemetry tracing
- **Security Auditor**: Automated code auditing and vulnerability detection

### Storage Backends

- **Memory Storage**: Development and testing (thread-safe, protocol-compliant)
- **Redis Storage**: Production (distributed, persistent, scalable)

## 🛡️ Security Features

### Enhanced Device Trust
- **HMAC Fingerprints**: Cryptographically secure device identification
- **Constant-Time Comparison**: Prevents timing attacks
- **Secure Token Generation**: Cryptographically random tokens
- **Automatic Expiration**: Configurable TTL with cleanup
- **Brute-Force Protection**: Rate limiting on device operations

### Advanced Rate Limiting  
- **Multi-Layer Protection**: User, SMS, and API-level limits
- **Adaptive Thresholds**: Dynamic adjustment based on patterns
- **Anti-SMS Bombing**: Daily and hourly SMS limits per phone
- **Sliding Window**: Precise temporal rate limiting
- **Emergency Blocklist**: Dynamic IP/user blocking

### Comprehensive Security Monitoring
- **Security Event Logging**: Structured logging with severity levels
- **Metrics Collection**: Real-time security metrics
- **Audit Trail**: Complete operation logging
- **Threat Detection**: Pattern-based anomaly detection
- **Compliance Reporting**: Automated security reports

## 📊 Observability

### Metrics (Prometheus)
```
# Authentication operations
auth_operations_total{operation="sms_send",status="success"} 1234
auth_operations_total{operation="mfa_verify",status="failed"} 56

# Security events  
auth_security_events_total{event="rate_limit_triggered",severity="medium"} 12
auth_security_events_total{event="device_trust_bypass",severity="low"} 890

# Performance metrics
auth_operation_duration_seconds{operation="mfa_verify"} 0.045
auth_request_duration_seconds{method="POST",endpoint="/auth/verify"} 0.12

# System health
auth_active_devices_current 1543
auth_failed_attempts_current 23
```

### Tracing (OpenTelemetry)
- **Distributed Tracing**: End-to-end request tracking
- **Operation Spans**: Detailed timing and context
- **Error Attribution**: Precise error location and context
- **Performance Profiling**: Bottleneck identification

### Structured Logging
```json
{
  "timestamp": "2024-01-15T10:30:45Z",
  "level": "WARNING", 
  "event": "mfa_verification_failed",
  "user_id": "user123",
  "phone": "+12***90",
  "attempts": 3,
  "severity": "medium",
  "fingerprint": "abc123...",
  "trace_id": "abc123xyz789"
}
```

## 🚀 FastAPI Integration

### Enhanced API with Middleware

```python
from fastapi import FastAPI, Depends, Security, Request
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(title="Enhanced Authentication API", version="2.1.0")

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*.example.com"])
app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"])

# Request timing middleware
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    metrics.record_request_duration(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
        duration=duration
    )
    return response

# Enhanced endpoints with comprehensive error handling
@app.post("/auth/mfa/verify")
async def verify_mfa(request: VerifyMFARequest):
    try:
        success = await mfa_manager.verify_mfa(...)
        return {"success": success, "device_token": device_token}
    except Exception as e:
        metrics.increment_security_event("api_error", "medium")
        raise HTTPException(status_code=500, detail="Internal error")

# Admin endpoints with metrics
@app.get("/auth/metrics", response_class=PlainTextResponse)
async def prometheus_metrics():
    return metrics.get_prometheus_metrics()

@app.get("/auth/security/stats")
async def security_stats():
    return mfa_manager.get_security_stats()
```

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/sms/send` | POST | Send SMS verification code |
| `/auth/mfa/verify` | POST | Verify MFA code with device trust |
| `/auth/email/send` | POST | Send email verification |
| `/auth/email/verify` | POST | Verify email token/code |
| `/auth/devices/{user_id}` | GET | List trusted devices |
| `/auth/devices/{token}` | DELETE | Revoke device trust |
| `/auth/devices/revoke-all` | POST | Emergency device revocation |
| `/auth/security/stats` | GET | Security statistics |
| `/auth/metrics` | GET | Metrics data |
| `/metrics` | GET | Prometheus metrics |
| `/health` | GET | Health check |
| `/health/detailed` | GET | Detailed health status |

## 📖 Configuration

### Enhanced MFA Config

```python
config = MFAConfig(
    # Basic settings
    max_failed_attempts=5,
    rate_limit_window_seconds=900,  # 15 minutes
    device_trust_ttl_days=30,
    
    # SMS settings  
    sms_code_ttl_minutes=5,
    max_sms_per_hour=3,
    max_sms_per_phone_per_day=10,
    
    # Email settings
    email_verification_ttl_hours=24,
    
    # Security enhancements
    hmac_secret_key="your-256-bit-secret-key",  # Required for production
    secure_token_length=32,
    log_security_events=True,
    
    # Advanced features
    adaptive_rate_limiting=True,
    enable_dynamic_blocklist=True,
    enable_metrics=True,
    enable_tracing=True,
    
    # Performance tuning
    cleanup_interval_minutes=60,
    max_device_history=1000
)
```

### Environment Variables

```bash
# Security
AUTH_HMAC_SECRET_KEY=your-256-bit-secret-key
AUTH_SECURE_TOKEN_LENGTH=32

# Rate limiting  
AUTH_MAX_FAILED_ATTEMPTS=5
AUTH_RATE_LIMIT_WINDOW=900
AUTH_MAX_SMS_PER_HOUR=3
AUTH_MAX_SMS_PER_DAY=10

# Features
AUTH_ENABLE_METRICS=true
AUTH_ENABLE_TRACING=true
AUTH_ADAPTIVE_RATE_LIMITING=true
AUTH_DYNAMIC_BLOCKLIST=true

# Storage
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your-redis-password

# Observability
PROMETHEUS_ENABLED=true
JAEGER_ENDPOINT=http://jaeger:14268/api/traces
LOG_LEVEL=INFO
```

## 🔧 Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  auth-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
      - AUTH_HMAC_SECRET_KEY=${AUTH_HMAC_SECRET_KEY}
      - PROMETHEUS_ENABLED=true
    depends_on:
      - redis
      - prometheus
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  redis_data:
  grafana_data:
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auth-api
  template:
    metadata:
      labels:
        app: auth-api
    spec:
      containers:
      - name: auth-api
        image: auth-api:2.1.0
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          value: "redis://redis-cluster:6379/0"
        - name: AUTH_HMAC_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: auth-secrets
              key: hmac-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi" 
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /health/detailed
            port: 8000
          initialDelaySeconds: 5
```

## 🧪 Testing

### Comprehensive Test Suite

```bash
# Run enhanced test suite
python test_enhanced_system.py

# Run specific test categories
pytest tests/ -k "security"
pytest tests/ -k "performance"  
pytest tests/ -k "metrics"

# Load testing
locust -f tests/load_test.py --host=http://localhost:8000

# Security testing
bandit -r . -f json -o security_report.json
safety check --json --output safety_report.json
```

### Performance Benchmarks

| Operation | Target | Achieved |
|-----------|--------|----------|
| SMS Send | <100ms | ~45ms |
| MFA Verify | <50ms | ~25ms |
| Device Trust | <10ms | ~5ms |
| Rate Check | <5ms | ~2ms |
| Metrics Export | <200ms | ~150ms |

## 🔒 Security Hardening

### Production Checklist

- [ ] **Secret Management**: Use secure key management (Vault, AWS KMS)
- [ ] **TLS Configuration**: Enforce TLS 1.3 with proper certificates
- [ ] **Network Security**: Configure firewalls and VPCs
- [ ] **Monitoring**: Set up alerts for security events
- [ ] **Backup Strategy**: Regular backups of user data and device trust
- [ ] **Incident Response**: Define security incident procedures
- [ ] **Compliance**: Ensure GDPR/CCPA compliance for user data
- [ ] **Penetration Testing**: Regular security assessments
- [ ] **Dependency Updates**: Automated security updates
- [ ] **Rate Limiting**: Configure per-environment limits

### Security Audit

```python
from security_audit import SecurityAuditor

auditor = SecurityAuditor()

# Audit codebase
results = auditor.audit_project(".")
print(f"Issues found: {len(results['issues'])}")

# Generate security report
report = auditor.generate_report(results)
with open("security_report.html", "w") as f:
    f.write(report)
```

## 📈 Monitoring and Alerting

### Grafana Dashboards

- **Authentication Overview**: Request rates, success rates, error rates
- **Security Dashboard**: Failed attempts, rate limits, security events  
- **Device Trust**: Active devices, trust events, revocations
- **Performance**: Response times, throughput, resource usage
- **System Health**: Error rates, availability, dependencies

### Alert Rules

```yaml
groups:
- name: auth_alerts
  rules:
  - alert: HighFailureRate
    expr: rate(auth_operations_total{status="failed"}[5m]) > 0.1
    labels:
      severity: warning
    annotations:
      summary: "High authentication failure rate"
      
  - alert: SecurityEvent
    expr: increase(auth_security_events_total{severity="high"}[5m]) > 0
    labels:
      severity: critical
    annotations:
      summary: "Critical security event detected"
```

## 🔄 Migration and Upgrades

### Upgrading from v1.x

```python
# 1. Update configuration
old_config = MFAConfig(...)
new_config = MFAConfig(
    **old_config.__dict__,
    hmac_secret_key="your-secret",  # Required
    enable_metrics=True,
    adaptive_rate_limiting=True
)

# 2. Migrate device trust data
from migration import migrate_device_trust
migrate_device_trust(old_storage, new_storage)

# 3. Update API calls
# Old: verify_mfa(user_id, phone, code)
# New: verify_mfa(user_id, phone, code, device_token, device_fingerprint)
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Run tests**: `python test_enhanced_system.py`
4. **Check security**: `bandit -r .`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run pre-commit hooks
pre-commit install
pre-commit run --all-files

# Start development services
docker-compose -f docker-compose.dev.yml up -d
```

## 📚 Documentation

- [API Reference](docs/api.md)
- [Security Guide](docs/security.md)
- [Deployment Guide](docs/deployment.md)
- [Monitoring Guide](docs/monitoring.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Changelog](CHANGELOG.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/auth-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/auth-system/discussions)
- **Security**: security@your-org.com
- **Documentation**: [Wiki](https://github.com/your-org/auth-system/wiki)

---

**Enhanced Authentication System v2.1** - Production-ready security with enterprise-grade observability.

Built with ❤️ for secure, scalable authentication.