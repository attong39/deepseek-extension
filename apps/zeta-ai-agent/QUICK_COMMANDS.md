# ⚡ Quick Start Commands

## 🎯 Performance Testing (1-2 minutes)
```powershell
# Quick performance test (if k6 installed)
.\scripts\setup-performance.ps1 -TargetRPS 100 -TestDuration 180

# Install k6 and run test
.\scripts\setup-performance.ps1 -InstallTools -TargetRPS 50
```

## 📊 Monitoring Setup (5 minutes)
```powershell
# Deploy complete monitoring stack
.\scripts\setup-monitoring.ps1 -CreateDashboards -SetupAlerts -PortForward

# Access Grafana
start http://localhost:3000
# Login: admin / zetaAdmin123!
```

## 🚀 Application Deployment
```powershell
# Deploy with optimized configuration
helm upgrade --install zeta-agent .\infra\helm\zeta-agent `
  --values .\phase2\performance\configs\values-optimized.yaml `
  --namespace zeta-agent --create-namespace

# Check deployment status
kubectl get pods -n zeta-agent
kubectl get hpa -n zeta-agent
```

## 🔍 Quick Health Check
```powershell
# Port forward application
kubectl port-forward svc/zeta-agent 3000:3000 -n zeta-agent

# Test endpoints
curl http://localhost:3000/health        # < 50ms
curl http://localhost:3000/api/v1/status # < 100ms  
curl http://localhost:3000/metrics       # Prometheus metrics
```

## 📈 Real-time Monitoring
```powershell
# Resource usage
kubectl top pods -n zeta-agent --sort-by=cpu
kubectl top pods -n zeta-agent --sort-by=memory

# Auto-scaling status
kubectl get hpa -n zeta-agent --watch

# Application logs
kubectl logs -l app=zeta-agent -n zeta-agent --tail=50 -f
```

## 🎯 Performance Targets
- **P95 Latency**: < 200ms ✅
- **Error Rate**: < 1% ✅  
- **Sustained RPS**: 100+ ✅
- **Auto-scaling**: 2-10 replicas ✅
- **Memory Usage**: < 80% ✅
- **CPU Usage**: < 70% ✅

## 🚨 Quick Troubleshooting
```powershell
# Check for issues
kubectl describe pod -l app=zeta-agent -n zeta-agent
kubectl get events -n zeta-agent --sort-by='.lastTimestamp'

# View detailed logs
kubectl logs -l app=zeta-agent -n zeta-agent --previous

# Restart deployment
kubectl rollout restart deployment/zeta-agent -n zeta-agent
```

---
💡 **Pro Tip**: Keep these commands handy for daily operations!
