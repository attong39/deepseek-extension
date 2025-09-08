# 🚀 Zeta AI Agent - Production Deployment Guide

> **Enterprise-ready VS Code extension với AI Agent tích hợp monitoring, alerting, và CI/CD hoàn chỉnh**

## 📋 Tổng quan

Zeta AI Agent là một VS Code extension mạnh mẽ tích hợp AI assistant với hệ thống monitoring và alerting production-ready. Extension cung cấp:

- ✅ **AI Assistant tích hợp** - Hỗ trợ tiếng Việt với quality scoring
- ✅ **Metrics & Monitoring** - Prometheus, Grafana, Alertmanager
- ✅ **Production Security** - CORS, CSP, health checks
- ✅ **CI/CD Pipeline** - GitHub Actions, Docker, Kubernetes
- ✅ **Enterprise Features** - Backup, logging, observability

## 🎯 Yêu cầu hệ thống

### Development Environment
```bash
# Runtime requirements
Node.js >= 18.0.0
Python >= 3.10
VS Code >= 1.80.0

# Package managers
npm >= 9.0.0
pip >= 23.0.0
```

### Production Environment
```bash
# Container runtime
Docker >= 20.10
Kubernetes >= 1.25 (optional)

# Monitoring stack
Prometheus >= 2.40
Alertmanager >= 0.25
Grafana >= 9.0 (optional)
```

## 🚀 Cài đặt nhanh (Development)

### 1. Clone và Setup
```bash
# Clone repository
git clone https://github.com/your-org/zeta-ai-agent.git
cd apps/zeta-ai-agent

# Install dependencies
npm install
pip install -r requirements.txt

# Build extension
npm run build
```

### 2. Khởi động Metrics Server
```bash
# Start FastAPI metrics server
uvicorn metrics_server:app --host 127.0.0.1 --port 9100 --reload

# Verify health
curl http://localhost:9100/health
# Expected: {"status":"healthy","timestamp":"..."}
```

### 3. Install Extension trong VS Code
```bash
# Package extension
npx vsce package

# Install locally
code --install-extension zeta-ai-agent-*.vsix
```

### 4. Sử dụng Extension
1. Mở VS Code
2. Nhấn `Ctrl+Shift+P` → tìm "Zeta: Ask AI"
3. Gõ câu hỏi tiếng Việt hoặc tiếng Anh
4. Xem kết quả trong webview panel

## 🔒 Cấu hình Production Security

### CORS Configuration
```python
# metrics_server.py - Production CORS setup
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", 
    "https://your-domain.com,https://api.your-domain.com"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=86400,  # Cache preflight 24h
)
```

### Content Security Policy (CSP)
```html
<!-- src/webview/index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self'; 
               style-src 'self' 'unsafe-inline'; 
               img-src data: https:; 
               connect-src https://api.your-domain.com;
               object-src 'none'; 
               base-uri 'none';
               frame-ancestors 'none';">
```

### Environment Variables (Production)
```bash
# .env.production
ALLOWED_ORIGINS=https://app.yourcompany.com
METRICS_HOST=0.0.0.0
METRICS_PORT=9100
SMTP_PASSWORD=your-smtp-password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

## 📊 Monitoring & Alerting

### Prometheus Metrics
Zeta AI Agent expose các metrics sau trên endpoint `/metrics`:

```prometheus
# Request metrics
zeta_requests_total{model="gpt-4",status="success"} 1523
zeta_request_duration_seconds_bucket{model="gpt-4",le="1"} 1200
zeta_request_duration_seconds_sum{model="gpt-4"} 892.5

# Quality metrics
zeta_vietnamese_quality_score{model="gpt-4"} 8.5
zeta_feedback_total 1523
zeta_errors_total 12

# System metrics  
zeta_model_usage_total{model="gpt-4"} 1523
```

### Kiểm tra nhanh Monitoring
```bash
# 1. Test metrics endpoint
curl http://localhost:9100/metrics | grep zeta_

# 2. Test health checks
curl http://localhost:9100/health
curl http://localhost:9100/ready

# 3. Test alerting (Mock high latency)
curl -X POST http://localhost:9100/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "test",
    "prompt": "Test prompt", 
    "response": "Test response",
    "rating": 8,
    "latency": 5.5,
    "vietnamese_quality": 9,
    "session_id": "test-session"
  }'
```

### Alert Rules đã cấu hình

| Alert | Trigger | Severity | Mô tả |
|-------|---------|----------|-------|
| `ZetaHighLatency` | Latency > 2s for 2m | Warning | Response time cao |
| `ZetaServiceDown` | Service unreachable 1m | Critical | Service không hoạt động |
| `ZetaHighErrorRate` | Error rate > 0.1/s for 3m | Warning | Tỷ lệ lỗi cao |
| `ZetaLowVietnameseQuality` | VN quality < 6 for 5m | Warning | Chất lượng tiếng Việt thấp |
| `ZetaNoFeedback` | No feedback 1h | Info | Không có feedback |

## 🐳 Production Deployment với Docker

### Dockerfile (Multi-stage build)
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage  
FROM python:3.11-slim
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built assets
COPY --from=builder /app/dist ./static
COPY metrics_server.py .
COPY config/ ./config/

# Security: Non-root user
RUN adduser --disabled-password --gecos '' zeta
USER zeta

EXPOSE 9100
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:9100/health || exit 1

ENV ALLOWED_ORIGINS="https://your-production-domain.com"
CMD ["uvicorn", "metrics_server:app", "--host", "0.0.0.0", "--port", "9100"]
```

### Docker Compose (Development + Monitoring)
```yaml
version: '3.8'

services:
  zeta-api:
    build: .
    ports:
      - "9100:9100"
    environment:
      - ALLOWED_ORIGINS=http://localhost:3000
    volumes:
      - ./feedback.db:/app/feedback.db
    networks:
      - zeta-network
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus:/etc/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    networks:
      - zeta-network
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./config/alertmanager:/etc/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    networks:
      - zeta-network
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
    networks:
      - zeta-network
    restart: unless-stopped

networks:
  zeta-network:
    driver: bridge

volumes:
  grafana-storage:
```

### Khởi chạy Production Stack
```bash
# Build và start tất cả services
docker-compose up -d

# Verify services
docker-compose ps
curl http://localhost:9100/health
curl http://localhost:9090/targets
curl http://localhost:9093/#/alerts

# View logs
docker-compose logs -f zeta-api
```

## ☸️ Kubernetes Deployment

### Kustomize Base
```yaml
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: apps/zeta-ai-agent
  labels:
    app: apps/zeta-ai-agent
spec:
  replicas: 2
  selector:
    matchLabels:
      app: apps/zeta-ai-agent
  template:
    metadata:
      labels:
        app: apps/zeta-ai-agent
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9100"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: zeta-api
        image: your-registry.io/apps/zeta-ai-agent:latest
        ports:
        - containerPort: 9100
        env:
        - name: ALLOWED_ORIGINS
          value: "https://zeta.yourcompany.com"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi" 
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /ready
            port: 9100
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /health
            port: 9100
          initialDelaySeconds: 15
          periodSeconds: 20
        securityContext:
          runAsNonRoot: true
          runAsUser: 1000
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false
```

### Helm Deployment
```bash
# Install Helm chart
helm upgrade --install apps/zeta-ai-agent ./helm/apps/zeta-ai-agent \
  --namespace zeta-system \
  --create-namespace \
  --set image.tag=v1.0.0 \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=zeta.yourcompany.com \
  --set resources.limits.memory=512Mi

# Verify deployment
kubectl get pods -n zeta-system
kubectl logs -n zeta-system deployment/apps/zeta-ai-agent
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          npm ci
          pip install -r requirements.txt
          
      - name: Lint TypeScript
        run: npm run lint
        
      - name: Lint Python
        run: |
          flake8 metrics_server.py
          mypy metrics_server.py
          
      - name: Run tests
        run: |
          npm test
          pytest tests/
          
      - name: Security scan
        run: |
          npm audit --audit-level high
          bandit -r . -f json -o bandit-report.json

  build-and-package:
    needs: lint-and-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build extension
        run: |
          npm ci
          npm run build
          
      - name: Package VSIX
        run: npx vsce package --out zeta-ai-agent.vsix
        
      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: apps/zeta-ai-agent:${{ github.sha }}
          
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: |
            zeta-ai-agent.vsix
            Dockerfile

  deploy-staging:
    needs: build-and-package
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying to staging environment"
          # kubectl apply -f k8s/staging/
          
  deploy-production:
    needs: build-and-package
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Publish to VS Code Marketplace
        env:
          VSCE_PAT: ${{ secrets.VSCE_PAT }}
        run: |
          npx vsce publish --packagePath zeta-ai-agent.vsix
          
      - name: Deploy to production
        run: |
          echo "Deploying to production"
          # helm upgrade apps/zeta-ai-agent ./helm/apps/zeta-ai-agent
```

## 📖 API Documentation

### Metrics Server Endpoints

#### `GET /health` - Health Check
```bash
curl http://localhost:9100/health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "zeta-ai-metrics",
  "version": "1.0.0"
}
```

#### `GET /ready` - Readiness Check  
```bash
curl http://localhost:9100/ready
```
Response:
```json
{
  "status": "ready",
  "timestamp": "2024-01-15T10:30:00Z",
  "dependencies": {
    "database": "connected",
    "metrics_storage": "available"
  },
  "metrics_count": 5,
  "feedback_count": 1523
}
```

#### `POST /feedback` - Submit Feedback
```bash
curl -X POST http://localhost:9100/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "gpt-4",
    "prompt": "Viết code Python tính fibonacci",
    "response": "def fibonacci(n): ...",
    "rating": 9,
    "latency": 1.2,
    "vietnamese_quality": 8,
    "session_id": "session-123"
  }'
```

#### `GET /stats` - Comprehensive Statistics
```bash
curl http://localhost:9100/stats
```

### VS Code Extension Commands

| Command | Mô tả | Shortcut |
|---------|-------|----------|
| `zeta.askAI` | Mở AI assistant dialog | `Ctrl+Shift+A` |
| `zeta.showMetrics` | Hiển thị metrics dashboard | `Ctrl+Shift+M` |
| `zeta.exportFeedback` | Export feedback data | - |
| `zeta.configure` | Mở settings | - |

## 🚨 Troubleshooting

### Common Issues

#### 1. CORS Error trong VS Code
```bash
# Kiểm tra CORS setting
curl -I -H "Origin: vscode-file://vscode-app" http://localhost:9100/metrics

# Fix: Update allowed origins
export ALLOWED_ORIGINS="vscode-file://*,http://localhost:*"
```

#### 2. Metrics không hiện trong Prometheus
```bash
# Kiểm tra target status
curl http://localhost:9090/api/v1/targets

# Kiểm tra metrics endpoint
curl http://localhost:9100/metrics | grep zeta_

# Fix: Restart Prometheus
docker-compose restart prometheus
```

#### 3. Alert không trigger
```bash
# Test alert expression
curl -G 'http://localhost:9090/api/v1/query' \
  --data-urlencode 'query=rate(zeta_request_duration_seconds_sum[1m])'

# Check Alertmanager config
curl http://localhost:9093/api/v1/alerts
```

#### 4. High Memory Usage
```bash
# Check container stats
docker stats apps/zeta-ai-agent

# Optimize Python memory
export PYTHONHASHSEED=0
export MALLOC_ARENA_MAX=2
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
uvicorn metrics_server:app --host 0.0.0.0 --port 9100 --log-level debug

# VS Code extension debug
# 1. Open workspace in VS Code
# 2. Press F5 to launch Extension Development Host
# 3. Check Debug Console for logs
```

## 📋 Production Checklist

### Security ✅
- [ ] CORS properly configured với whitelist domains
- [ ] CSP headers implemented
- [ ] No `unsafe-inline` or `unsafe-eval` in CSP
- [ ] Service runs as non-root user
- [ ] Read-only filesystem where possible
- [ ] Secrets managed via environment variables
- [ ] TLS/HTTPS enabled in production

### Monitoring ✅  
- [ ] Health check endpoint returns 200
- [ ] Readiness check validates all dependencies
- [ ] Prometheus metrics exposed and scraped
- [ ] Alert rules configured and tested
- [ ] Alertmanager receivers configured (Slack/Email)
- [ ] Grafana dashboards imported
- [ ] Log aggregation setup (ELK/Loki)

### Performance ✅
- [ ] Resource limits set in Kubernetes
- [ ] Horizontal Pod Autoscaler configured
- [ ] Database connection pooling
- [ ] Metrics retention policy set
- [ ] CORS preflight caching enabled
- [ ] Load testing completed

### Reliability ✅
- [ ] Multiple replicas running
- [ ] Rolling deployment strategy
- [ ] Database backup scheduled
- [ ] Disaster recovery plan documented
- [ ] Circuit breaker implemented for external APIs
- [ ] Graceful shutdown handling

### CI/CD ✅
- [ ] Automated testing pipeline
- [ ] Security scanning (npm audit, bandit)
- [ ] Docker image scanning
- [ ] Staging environment deployed
- [ ] Production deployment automated
- [ ] Rollback procedure tested

## 🔗 Useful Links

- [VS Code Extension API](https://code.visualstudio.com/api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Charts](https://helm.sh/docs/)

## 👥 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🆘 Support

- 📧 Email: support@zeta.ai
- 💬 Slack: [#zeta-support](https://yourcompany.slack.com/channels/zeta-support)
- 🐛 Issues: [GitHub Issues](https://github.com/your-org/apps/zeta-ai-agent/issues)
- 📖 Documentation: [docs.zeta.ai](https://docs.zeta.ai)

---

**Happy coding with Zeta AI Agent! 🚀**
