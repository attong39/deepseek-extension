# 🎯 Performance Optimization Quick Start

## 🚀 Instant Performance Testing

### Option 1: Quick Performance Test (< 2 minutes)
```powershell
# Install k6 and run immediate test
.\scripts\setup-performance.ps1 -InstallTools -TargetRPS 50

# Or if k6 is already installed
.\scripts\setup-performance.ps1 -TargetRPS 100 -TestDuration 180
```

### Option 2: Full Performance Suite (5-10 minutes)
```powershell
# Complete performance optimization setup
.\scripts\phase2-setup.ps1 -Mode Performance
```

## 📊 Performance Targets

| Metric | Target | Critical |
|--------|--------|----------|
| **P95 Latency** | < 200ms | < 500ms |
| **P99 Latency** | < 500ms | < 1000ms |
| **Error Rate** | < 1% | < 5% |
| **Sustained RPS** | 100+ | 50+ |
| **CPU Usage** | < 70% | < 90% |
| **Memory Usage** | < 80% | < 95% |

## 🔧 Optimization Commands

### Load Testing
```powershell
# Basic load test
k6 run .\phase2\performance\load-tests\optimized-load.js

# Stress test with higher load
k6 run .\phase2\performance\load-tests\optimized-load.js --env TARGET_RPS=200

# Spike test
k6 run .\phase2\performance\load-tests\spike-test.js
```

### Kubernetes Optimization
```powershell
# Apply optimized configuration
helm upgrade zeta-agent .\infra\helm\zeta-agent `
  --values .\phase2\performance\configs\values-optimized.yaml

# Check resource usage
kubectl top pods -n zeta-agent
kubectl get hpa -n zeta-agent

# View auto-scaling events
kubectl describe hpa zeta-agent -n zeta-agent
```

### Performance Monitoring
```powershell
# Start Grafana dashboard
kubectl port-forward svc/grafana 3000:3000 -n monitoring

# Check application metrics
curl http://localhost:3000/metrics

# View performance logs
kubectl logs -l app=zeta-agent -n zeta-agent --tail=100
```

## 📈 Quick Diagnostics

### Check Application Health
```powershell
# Health endpoint (< 50ms target)
curl http://localhost:3000/health

# Status endpoint (< 100ms target)
curl http://localhost:3000/api/v1/status

# Metrics endpoint
curl http://localhost:3000/metrics | grep -E "(request_duration|request_total|memory_usage)"
```

### Resource Monitoring
```powershell
# Real-time resource monitoring
kubectl top pods -n zeta-agent --sort-by=cpu
kubectl top pods -n zeta-agent --sort-by=memory

# Check for resource limits
kubectl describe pod -l app=zeta-agent -n zeta-agent | grep -A 5 "Limits\|Requests"
```

## 🎯 Performance Optimization Steps

### 1. Baseline Measurement (5 minutes)
```powershell
# Run baseline test
.\scripts\setup-performance.ps1 -TargetRPS 50 -TestDuration 300

# Review results
start performance-report.html
```

### 2. Resource Optimization (10 minutes)
```powershell
# Apply optimized resources
helm upgrade zeta-agent .\infra\helm\zeta-agent `
  --values .\phase2\performance\configs\values-optimized.yaml

# Wait for rollout
kubectl rollout status deployment/zeta-agent -n zeta-agent
```

### 3. Load Testing (10 minutes)
```powershell
# Progressive load testing
.\scripts\setup-performance.ps1 -TargetRPS 75 -TestDuration 300
.\scripts\setup-performance.ps1 -TargetRPS 100 -TestDuration 300
.\scripts\setup-performance.ps1 -TargetRPS 150 -TestDuration 180
```

### 4. Auto-scaling Validation (15 minutes)
```powershell
# Monitor auto-scaling during load test
kubectl get hpa -n zeta-agent --watch &
.\scripts\setup-performance.ps1 -TargetRPS 200 -TestDuration 600
```

## 🚨 Performance Troubleshooting

### High Latency (P95 > 200ms)
```powershell
# Check resource constraints
kubectl describe pod -l app=zeta-agent -n zeta-agent | grep -E "(Limits|Requests|Events)"

# Increase resources
helm upgrade zeta-agent .\infra\helm\zeta-agent `
  --set resources.limits.cpu=1000m `
  --set resources.limits.memory=1Gi
```

### High Error Rate (> 1%)
```powershell
# Check application logs
kubectl logs -l app=zeta-agent -n zeta-agent --tail=200 | grep -i error

# Check readiness probe failures
kubectl get events -n zeta-agent | grep -i probe
```

### Memory Issues
```powershell
# Check memory usage
kubectl top pods -n zeta-agent --sort-by=memory

# Optimize Node.js memory
helm upgrade zeta-agent .\infra\helm\zeta-agent `
  --set env.NODE_OPTIONS="--max-old-space-size=512 --gc-interval=100"
```

### CPU Throttling
```powershell
# Check CPU usage patterns
kubectl top pods -n zeta-agent --sort-by=cpu

# Increase CPU limits
helm upgrade zeta-agent .\infra\helm\zeta-agent `
  --set resources.limits.cpu=1500m `
  --set resources.requests.cpu=500m
```

## 📊 Performance Metrics Dashboard

### Key URLs
- **Grafana**: http://localhost:3000 (after port-forward)
- **Prometheus**: http://localhost:9090
- **Application Metrics**: http://localhost:3000/metrics
- **K8s Dashboard**: https://kubernetes-dashboard.example.com

### Essential Grafana Queries
```promql
# Request rate
rate(http_requests_total[5m])

# Response time P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Memory usage
container_memory_usage_bytes{pod=~"zeta-agent.*"}

# CPU usage
rate(container_cpu_usage_seconds_total{pod=~"zeta-agent.*"}[5m])
```

## 🏆 Performance Success Criteria

✅ **Production Ready Checklist:**
- [ ] P95 latency < 200ms under 100 RPS
- [ ] Error rate < 1% during sustained load
- [ ] Auto-scaling works (2-10 replicas)
- [ ] Memory usage stable < 80%
- [ ] CPU usage < 70% under normal load
- [ ] Health checks respond < 50ms
- [ ] Graceful handling of 2x load spikes

## 🎯 Next Steps After Performance Optimization

1. **Set up Monitoring** - Deploy Prometheus/Grafana stack
2. **Configure Alerts** - Set up performance degradation alerts  
3. **Load Testing CI** - Integrate k6 into CI/CD pipeline
4. **Capacity Planning** - Plan for 3x current load
5. **Service Mesh** - Implement Istio for advanced traffic management

---
💡 **Pro Tip**: Run performance tests after every deployment to ensure consistent performance!
