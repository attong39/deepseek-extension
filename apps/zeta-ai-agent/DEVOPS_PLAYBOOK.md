# Zeta AI Agent - DevOps Playbook 🔧

> Comprehensive operational guide for production deployment and maintenance

## 📋 Table of Contents

1. [Production Deployment](#-production-deployment)
2. [Infrastructure Management](#-infrastructure-management)
3. [Monitoring & Observability](#-monitoring--observability)
4. [Performance Optimization](#-performance-optimization)
5. [Security Operations](#-security-operations)
6. [Backup & Recovery](#-backup--recovery)
7. [Troubleshooting Runbook](#-troubleshooting-runbook)
8. [Maintenance Procedures](#-maintenance-procedures)

## 🚀 Production Deployment

### Pre-Deployment Checklist

```bash
# ✅ Environment Verification
□ Ollama 0.11.8+ installed and running
□ VS Code 1.74.0+ with extension support
□ Node.js 18.0+ available
□ Network connectivity to localhost:11434
□ Sufficient storage (10GB+ for models)
□ RAM requirements met (8GB minimum, 16GB recommended)

# ✅ Model Validation
□ attong39/zeta model deployed and functional
□ Supporting models (starcoder, codellama) available
□ Model checksums verified
□ Performance baseline established

# ✅ Security Validation  
□ No hardcoded API keys in codebase
□ Secure storage implementation verified
□ Network ports properly configured
□ TLS/SSL certificates valid

# ✅ Extension Verification
□ TypeScript compilation successful
□ VSIX package created and tested
□ Local installation verified
□ Command palette integration working
```

### Deployment Commands

```bash
# 1. Environment Setup
cd /path/to/apps/zeta-ai-agent

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Run tests
npm test

# 2. Model Deployment
ollama serve &
ollama pull attong39/zeta
ollama pull starcoder  
ollama pull codellama:13b-instruct
ollama pull deepseek-coder

# Verify models
ollama list | grep -E "(attong39/zeta|starcoder|codellama|deepseek)"

# 3. Extension Packaging
npm run package

# Verify VSIX
ls -la *.vsix
# Expected: zeta-ai-agent-1.0.0.vsix (>1MB)

# 4. Local Testing
code --install-extension zeta-ai-agent-1.0.0.vsix
code --list-extensions | grep zeta
```

### Production Configuration

```json
// .vscode/settings.json (Production)
{
  "zeta.production": {
    "enabled": true,
    "loggingLevel": "info",
    "metricsEnabled": true,
    "telemetryEnabled": false
  },
  "zeta.models": {
    "primary": "attong39/zeta",
    "fallback": "starcoder", 
    "timeout": 30000,
    "retryAttempts": 3
  },
  "zeta.security": {
    "validateInputs": true,
    "sanitizeOutputs": true,
    "rateLimiting": true,
    "maxRequestsPerMinute": 60
  }
}
```

## 🏗️ Infrastructure Management

### System Requirements

```yaml
# Production System Specifications
CPU:
  minimum: 4 cores
  recommended: 8+ cores
  architecture: x64

Memory:
  minimum: 8GB RAM
  recommended: 16GB RAM
  swap: 4GB

Storage:
  system: 20GB SSD
  models: 10GB SSD  
  logs: 5GB
  total: 35GB+ available

Network:
  bandwidth: 100Mbps+
  latency: <10ms to Ollama
  ports: 11434 (Ollama), 9100 (metrics)
```

### Service Management

```bash
# Ollama Service (Linux/macOS)
# /etc/systemd/system/ollama.service
[Unit]
Description=Ollama AI Model Service
After=network.target

[Service]
Type=simple
User=ollama
WorkingDirectory=/home/ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=5
Environment=OLLAMA_HOST=0.0.0.0:11434
Environment=OLLAMA_NUM_PARALLEL=4
Environment=OLLAMA_MAX_LOADED_MODELS=2

[Install]
WantedBy=multi-user.target

# Service commands
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

```powershell
# Windows Service Setup
# Create ollama-service.bat
@echo off
cd C:\Program Files\Ollama
ollama.exe serve

# Install as Windows Service (requires NSSM)
nssm install OllamaService "C:\Program Files\Ollama\ollama-service.bat"
nssm set OllamaService Start SERVICE_AUTO_START
nssm start OllamaService
```

### Container Deployment

```dockerfile
# Dockerfile.ollama
FROM ollama/ollama:latest

# Install models
RUN ollama pull attong39/zeta && \
    ollama pull starcoder && \
    ollama pull codellama:13b-instruct

EXPOSE 11434

CMD ["ollama", "serve"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  ollama:
    build:
      context: .
      dockerfile: Dockerfile.ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_NUM_PARALLEL=4
      - OLLAMA_MAX_LOADED_MODELS=2
    restart: unless-stopped
    
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  ollama_data:
  prometheus_data:
  grafana_data:
```

## 📊 Monitoring & Observability

### Metrics Collection

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'apps/zeta-ai-agent'
    static_configs:
      - targets: ['localhost:9100']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'ollama'
    static_configs:
      - targets: ['localhost:11434']
    metrics_path: '/api/metrics'
    scrape_interval: 30s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - localhost:9093
```

### Key Performance Indicators

```promql
# Response Time (Target: <5s)
histogram_quantile(0.95, 
  rate(zeta_request_duration_seconds_bucket[5m])
)

# Success Rate (Target: >90%)
sum(rate(zeta_requests_total{status="success"}[5m])) /
sum(rate(zeta_requests_total[5m])) * 100

# Vietnamese Quality Score (Target: >8/10)
avg(zeta_vietnamese_quality_score) by (model)

# Model Usage Distribution
sum(rate(zeta_requests_total[5m])) by (model)

# Error Rate (Target: <5%)
sum(rate(zeta_requests_total{status="error"}[5m])) /
sum(rate(zeta_requests_total[5m])) * 100
```

### Alerting Rules

```yaml
# alert_rules.yml
groups:
  - name: zeta_ai_agent
    rules:
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(zeta_request_duration_seconds_bucket[5m])) > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s"

      - alert: LowSuccessRate  
        expr: sum(rate(zeta_requests_total{status="success"}[5m])) / sum(rate(zeta_requests_total[5m])) * 100 < 85
        for: 3m
        labels:
          severity: critical
        annotations:
          summary: "Low success rate detected"
          description: "Success rate is {{ $value }}%"

      - alert: OllamaServiceDown
        expr: up{job="ollama"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Ollama service is down"
          description: "Ollama service has been down for more than 1 minute"

      - alert: LowVietnameseQuality
        expr: avg(zeta_vietnamese_quality_score) by (model) < 7
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Vietnamese quality score degraded"
          description: "Model {{ $labels.model }} quality is {{ $value }}/10"
```

### Log Management

```json
// Log configuration
{
  "logging": {
    "level": "info",
    "format": "json",
    "outputs": [
      {
        "type": "file",
        "path": "/var/log/apps/zeta-ai-agent/app.log",
        "maxSize": "100MB",
        "maxFiles": 10
      },
      {
        "type": "stdout",
        "level": "warn"
      }
    ]
  }
}
```

```bash
# Log rotation setup (Linux)
# /etc/logrotate.d/apps/zeta-ai-agent
/var/log/apps/zeta-ai-agent/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 zeta zeta
    postrotate
        systemctl reload apps/zeta-ai-agent
    endscript
}
```

## ⚡ Performance Optimization

### Model Performance Tuning

```bash
# Ollama optimization environment variables
export OLLAMA_NUM_PARALLEL=4          # Parallel request handling
export OLLAMA_MAX_LOADED_MODELS=2     # Memory optimization
export OLLAMA_FLASH_ATTENTION=1       # Enable flash attention
export OLLAMA_KEEP_ALIVE=5m          # Model caching duration

# GPU acceleration (if available)
export OLLAMA_GPU_LAYERS=32           # Offload layers to GPU
export CUDA_VISIBLE_DEVICES=0         # Specify GPU device
```

### Caching Strategy

```typescript
// Response caching configuration
interface CacheConfig {
  enabled: boolean;
  ttl: number;                    // Time to live (seconds)
  maxSize: number;               // Maximum cache entries
  strategy: 'lru' | 'fifo';     // Eviction strategy
}

const cacheConfig: CacheConfig = {
  enabled: true,
  ttl: 3600,                    // 1 hour
  maxSize: 1000,               // 1000 responses
  strategy: 'lru'              // Least recently used
};
```

### Load Balancing

```typescript
// Model load balancing
interface LoadBalancer {
  strategy: 'round_robin' | 'least_latency' | 'weighted';
  healthCheck: boolean;
  fallbackModel: string;
}

const modelConfig = {
  primary: {
    model: "attong39/zeta",
    weight: 70,
    maxConcurrent: 2
  },
  secondary: {
    model: "starcoder", 
    weight: 30,
    maxConcurrent: 4
  }
};
```

### Database Optimization

```sql
-- Feedback database optimization
CREATE INDEX idx_feedback_timestamp ON feedback(timestamp);
CREATE INDEX idx_feedback_model ON feedback(model_name);
CREATE INDEX idx_feedback_rating ON feedback(rating);

-- Query optimization
EXPLAIN ANALYZE 
SELECT model_name, AVG(rating) 
FROM feedback 
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY model_name;

-- Cleanup old data
DELETE FROM feedback 
WHERE timestamp < NOW() - INTERVAL '90 days';
```

## 🛡️ Security Operations

### Security Hardening

```bash
# File permissions (Linux/macOS)
chmod 600 ~/.config/apps/zeta-ai-agent/config.json
chmod 700 ~/.config/apps/zeta-ai-agent/
chown $USER:$USER ~/.config/apps/zeta-ai-agent/

# Network security
# Restrict Ollama to localhost only
export OLLAMA_HOST=127.0.0.1:11434

# Firewall configuration (Linux)
ufw allow from 127.0.0.1 to any port 11434
ufw deny 11434

# Firewall configuration (Windows)
netsh advfirewall firewall add rule name="Ollama Local Only" dir=in action=allow protocol=TCP localport=11434 remoteip=127.0.0.1
```

### Security Scanning

```bash
# Dependency vulnerability scanning
npm audit
npm audit fix

# OWASP dependency check
dependency-check --project "Zeta AI Agent" --scan ./

# Secret scanning
git-secrets --scan
gitleaks detect --source .

# Container security (if using Docker)
docker scout cves ollama/ollama:latest
trivy image ollama/ollama:latest
```

### Access Control

```json
// VS Code workspace security
{
  "security.workspace.trust.enabled": true,
  "security.workspace.trust.banner": "always",
  "extensions.autoCheckUpdates": false,
  "extensions.autoUpdate": false,
  "telemetry.telemetryLevel": "off"
}
```

## 💾 Backup & Recovery

### Model Backup Strategy

```bash
#!/bin/bash
# backup_models.sh

BACKUP_DIR="/backup/apps/zeta-ai-agent/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Backup Ollama models
ollama list | tail -n +2 | awk '{print $1}' > "$BACKUP_DIR/model_list.txt"
cp ~/.ollama/models/* "$BACKUP_DIR/models/" 2>/dev/null

# Backup configurations
cp -r ~/.config/apps/zeta-ai-agent "$BACKUP_DIR/config"
cp -r ~/.vscode/extensions/zeta* "$BACKUP_DIR/extensions"

# Backup database
pg_dump feedback_db > "$BACKUP_DIR/feedback_db.sql"

# Create tarball
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"

echo "Backup completed: $BACKUP_DIR.tar.gz"
```

### Recovery Procedures

```bash
#!/bin/bash
# restore_models.sh

BACKUP_FILE="$1"
RESTORE_DIR="/tmp/zeta-restore"

# Extract backup
tar -xzf "$BACKUP_FILE" -C /tmp/

# Restore models
while read -r model; do
    echo "Pulling model: $model"
    ollama pull "$model"
done < "$RESTORE_DIR/model_list.txt"

# Restore configurations
cp -r "$RESTORE_DIR/config" ~/.config/apps/zeta-ai-agent
cp -r "$RESTORE_DIR/extensions/"* ~/.vscode/extensions/

# Restore database
psql -d feedback_db < "$RESTORE_DIR/feedback_db.sql"

echo "Restore completed"
```

### Disaster Recovery Plan

```yaml
# RTO: Recovery Time Objective = 30 minutes
# RPO: Recovery Point Objective = 1 hour

Incident Response:
  1. Assess Impact:
     - Service availability
     - Data integrity  
     - Security breach

  2. Immediate Actions:
     - Stop affected services
     - Isolate compromised systems
     - Notify stakeholders

  3. Recovery Steps:
     - Restore from latest backup
     - Verify model integrity
     - Test functionality
     - Resume operations

  4. Post-Incident:
     - Root cause analysis
     - Update procedures
     - Improve monitoring
```

## 🚨 Troubleshooting Runbook

### Issue Classification

```
P1 - Critical (Service Down)
├── Ollama service not responding
├── Extension fails to load
├── Security breach detected
└── Data corruption

P2 - High (Degraded Performance)  
├── Response time >10s
├── Success rate <80%
├── Memory leaks
└── Model accuracy degraded

P3 - Medium (Minor Issues)
├── Slow responses (5-10s)
├── Occasional errors
├── UI glitches
└── Documentation gaps

P4 - Low (Enhancement Requests)
├── Feature requests  
├── Performance improvements
├── UX enhancements
└── Documentation updates
```

### Diagnostic Commands

```bash
# System health check
#!/bin/bash
echo "=== Zeta AI Agent Health Check ==="

# 1. Ollama Service
echo "Checking Ollama service..."
curl -s http://localhost:11434/api/tags | jq '.models[].name' 2>/dev/null || echo "❌ Ollama not responding"

# 2. Model availability
echo "Checking models..."
MODELS=("attong39/zeta" "starcoder" "codellama:13b-instruct")
for model in "${MODELS[@]}"; do
    if ollama list | grep -q "$model"; then
        echo "✅ $model available"
    else
        echo "❌ $model missing"
    fi
done

# 3. VS Code extension
echo "Checking VS Code extension..."
if code --list-extensions | grep -q "zeta"; then
    echo "✅ Extension installed"
else  
    echo "❌ Extension not found"
fi

# 4. System resources
echo "Checking system resources..."
echo "Memory usage: $(free -h | awk '/^Mem:/ {print $3"/"$2}')"
echo "Disk usage: $(df -h / | awk 'NR==2 {print $3"/"$2" ("$5")"}')"
echo "CPU load: $(uptime | awk -F'load average:' '{print $2}')"

# 5. Network connectivity
echo "Checking network..."
if nc -z localhost 11434; then
    echo "✅ Ollama port accessible"
else
    echo "❌ Cannot connect to Ollama"
fi
```

### Common Fixes

```bash
# Fix 1: Restart Ollama service
sudo systemctl restart ollama
# or
ollama serve &

# Fix 2: Clear VS Code extension cache
rm -rf ~/.vscode/extensions/apps/zeta-ai-agent*
code --install-extension zeta-ai-agent-1.0.0.vsix

# Fix 3: Rebuild model cache
ollama rm attong39/zeta
ollama pull attong39/zeta

# Fix 4: Reset VS Code workspace
rm -rf .vscode/settings.json
code --new-window

# Fix 5: Clear application cache
rm -rf ~/.config/apps/zeta-ai-agent/cache/
```

## 🔄 Maintenance Procedures

### Routine Maintenance Schedule

```
Daily:
├── Monitor service health
├── Check error logs
├── Verify backup completion
└── Review performance metrics

Weekly:
├── Update security patches
├── Cleanup log files
├── Analyze performance trends
├── Review feedback data
└── Model retraining assessment

Monthly:
├── Full system backup
├── Security audit
├── Performance optimization
├── Documentation updates
├── Dependency updates
└── Disaster recovery test

Quarterly:
├── Model architecture review
├── Infrastructure scaling assessment
├── Security penetration testing
├── Business continuity planning
└── Technology roadmap review
```

### Update Procedures

```bash
# Extension update
cd /path/to/apps/zeta-ai-agent

# 1. Backup current version
cp zeta-ai-agent-*.vsix backups/

# 2. Pull latest changes
git pull origin main

# 3. Update dependencies
npm update

# 4. Run tests
npm test

# 5. Build new version
npm run compile
npm run package

# 6. Test locally
code --install-extension zeta-ai-agent-*.vsix

# 7. Deploy to production
# (Follow deployment checklist)
```

### Health Monitoring

```bash
# Automated health check script
#!/bin/bash
# health_monitor.sh

LOG_FILE="/var/log/zeta-health.log"
ALERT_EMAIL="admin@zeta-ai.dev"

check_service() {
    if ! curl -s http://localhost:11434/api/tags >/dev/null; then
        echo "$(date): ❌ Ollama service down" >> "$LOG_FILE"
        mail -s "ALERT: Ollama service down" "$ALERT_EMAIL" < /dev/null
        return 1
    fi
    return 0
}

check_models() {
    local missing_models=()
    for model in "attong39/zeta" "starcoder" "codellama:13b-instruct"; do
        if ! ollama list | grep -q "$model"; then
            missing_models+=("$model")
        fi
    done
    
    if [ ${#missing_models[@]} -gt 0 ]; then
        echo "$(date): ❌ Missing models: ${missing_models[*]}" >> "$LOG_FILE"
        return 1
    fi
    return 0
}

# Run checks
if check_service && check_models; then
    echo "$(date): ✅ All systems healthy" >> "$LOG_FILE"
else
    echo "$(date): ❌ Health check failed" >> "$LOG_FILE"
fi
```

---

**🔧 DevOps Excellence for Production AI 🚀**

*For user-facing documentation, see [USER_GUIDE.md](USER_GUIDE.md)*
