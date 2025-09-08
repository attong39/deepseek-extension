# 📋 DEPLOYMENT COMMANDS CHEAT SHEET

## 🚀 **Quick Start Commands**

### 🛠️ **1. Setup (Run as Administrator)**
```powershell
# Install all DevOps tools
.\scripts\setup-devops-tools.ps1

# Quick setup với default options
.\scripts\setup-devops-tools.ps1 -QuickStart
```

### 🔨 **2. Build & Deploy**
```powershell
# Full deployment pipeline
.\scripts\deploy.ps1

# Step by step:
.\scripts\deploy.ps1 build      # Build Docker image
.\scripts\deploy.ps1 terraform  # Deploy infrastructure  
.\scripts\deploy.ps1 helm       # Deploy application
```

### 🔍 **3. Verification**
```powershell
# Quick health check
.\scripts\verify-deployment.ps1

# Manual checks
kubectl get pods -n zeta-agent
kubectl get svc -n zeta-agent
kubectl port-forward svc/zeta-agent 8080:3000 -n zeta-agent
```

### 🧪 **4. Testing**
```bash
# Full integration test
.\scripts\test_integration.sh

# Individual components
docker build -t test-image .
helm lint .\infra\helm\zeta-agent
terraform validate .\infra\terraform
```

---

## ✅ **Success Indicators**

| ✓ | Check | Command | Expected |
|---|-------|---------|----------|
| 🐳 | Docker running | `docker version` | Client & Server versions |
| ☸️ | Kubernetes ready | `kubectl cluster-info` | Cluster endpoints |
| ⛵ | Helm working | `helm version` | Version info |
| 🏗️ | Terraform ready | `terraform version` | Version info |
| 🚀 | App deployed | `kubectl get pods -n zeta-agent` | Running pods |
| 💚 | Health OK | `curl http://localhost:8080/health` | HTTP 200 |

---

## 🛠️ **Troubleshooting**

### ❌ **Docker Issues**
```powershell
# Enable Hyper-V (requires restart)
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# Start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### ⚠️ **Kubernetes Issues**  
```powershell
# Enable K8s in Docker Desktop Settings
# Or reset Kubernetes cluster in Docker Desktop
```

### 🔴 **Deployment Issues**
```powershell
# Check logs
kubectl logs deployment/zeta-agent -n zeta-agent --tail=50

# Describe resources
kubectl describe pod <pod-name> -n zeta-agent

# Check events
kubectl get events -n zeta-agent --sort-by=.metadata.creationTimestamp
```

---

## 📈 **Next Steps**

1. **🔒 Production Security** - TLS, RBAC, Network Policies
2. **📊 Monitoring Setup** - Prometheus, Grafana, Alerting  
3. **🚀 CI/CD Integration** - GitHub Actions automation
4. **⚡ Performance Tuning** - Resource optimization, caching

**🎯 Target: < 5 min deployment, 99.9% uptime, < 200ms response**
