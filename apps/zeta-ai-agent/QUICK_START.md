# 🚀 Zeta AI Agent - Quick Start Guide

## ⚡ **Immediate Next Steps** (Total: ~1-2 hours)

### **Step 1: Install DevOps Tools** ⏱️ 15-30 minutes

**Option A: Automated Setup (Recommended)**
```powershell
# Run as Administrator
.\scripts\setup-devops-tools.ps1
```

**Option B: Manual Installation**
```powershell
# Install Chocolatey package manager
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install tools
choco install docker-desktop kubernetes-cli kubernetes-helm terraform -y
```

**Option C: winget (Windows 10+)**
```powershell
winget install Docker.DockerDesktop
winget install Kubernetes.kubectl  
winget install Helm.Helm
winget install HashiCorp.Terraform
```

### **Step 2: Configure Kubernetes** ⏱️ 5-10 minutes

1. **Start Docker Desktop**
2. **Enable Kubernetes**: Settings → Kubernetes → ✅ Enable Kubernetes
3. **Wait for green indicator** (usually 2-5 minutes)
4. **Verify**: `kubectl cluster-info`

### **Step 3: Verify Setup** ⏱️ 2 minutes
```powershell
# Restart PowerShell first (to refresh PATH)
.\scripts\verify-deployment.ps1 -Verbose
```

**Expected Output:**
```
✓ Docker - Available
✓ Kubernetes CLI - Available  
✓ Helm Package Manager - Available
✓ Terraform - Available
✓ Kubernetes cluster accessible
```

---

## 🎯 **Deployment Process** (After tools are installed)

### **Quick Deploy** ⏱️ 10-20 minutes
```powershell
# Full automated deployment
.\scripts\deploy.ps1

# Monitor progress
kubectl get pods -n zeta-agent -w
```

### **Manual Step-by-Step** ⏱️ 15-30 minutes
```powershell
# 1. Build image (if pushing to registry)
docker buildx build --platform linux/amd64 --tag zetaai/zeta-agent:latest .

# 2. Initialize Terraform
cd infra/terraform
terraform init
terraform plan
terraform apply

# 3. Deploy with Helm
cd ../..
helm upgrade --install zeta-agent infra/helm/zeta-agent --namespace zeta-agent --create-namespace --wait

# 4. Verify deployment
kubectl get all -n zeta-agent
```

---

## ✅ **Verification Checklist**

### **Infrastructure Health**
```powershell
# ✅ Check pods are running
kubectl get pods -n zeta-agent

# ✅ Check services are accessible
kubectl get svc -n zeta-agent

# ✅ Check persistent storage
kubectl get pvc -n zeta-agent

# ✅ Check auto-scaling
kubectl get hpa -n zeta-agent
```

### **Application Health**
```powershell
# ✅ Port forward for testing
kubectl port-forward svc/zeta-agent 8080:3000 -n zeta-agent

# ✅ Test health endpoint (in another terminal)
curl http://localhost:8080/health
# Expected: HTTP 200 OK

# ✅ Test API status
curl http://localhost:8080/api/v1/status  
# Expected: JSON response with status info
```

### **End-to-End Testing** ⏱️ 10-15 minutes
```bash
# Run comprehensive integration tests
./scripts/test_integration.sh

# Expected: All tests pass ✓
```

---

## 🔧 **Troubleshooting Quick Fixes**

### **Docker Issues**
```powershell
# Docker Desktop not starting
Restart-Service docker
# Check Windows features: Hyper-V, WSL2

# Docker buildx not available
docker buildx install
```

### **Kubernetes Issues**
```powershell
# Cluster not accessible
kubectl config current-context
kubectl config use-context docker-desktop

# Pods stuck in Pending
kubectl describe pod <pod-name> -n zeta-agent
# Usually: insufficient resources or image pull issues
```

### **Deployment Issues**
```powershell
# Check deployment events
kubectl get events --sort-by=.metadata.creationTimestamp -n zeta-agent

# Check pod logs
kubectl logs -f deployment/zeta-agent -n zeta-agent

# Restart deployment
kubectl rollout restart deployment/zeta-agent -n zeta-agent
```

---

## 📊 **Expected Performance Metrics**

### **Startup Metrics**
- **Container Start**: < 30 seconds
- **Pod Ready**: < 60 seconds  
- **Service Available**: < 90 seconds
- **Health Check**: < 5 seconds response time

### **Resource Usage**
```
Memory: ~256MB per replica
CPU: ~0.1-0.3 cores per replica
Storage: 10GB persistent volume
Network: Minimal egress for AI model calls
```

### **Scaling Behavior**
```
Min Replicas: 1
Max Replicas: 10
Scale-up trigger: >70% CPU
Scale-down delay: 5 minutes
```

---

## 🎊 **Success Indicators**

**🟢 Green Status = Ready for Production Testing**

1. ✅ All pods Running (1/1 Ready)
2. ✅ `/health` returns 200 OK
3. ✅ `/api/v1/status` returns valid JSON
4. ✅ HPA shows current metrics
5. ✅ PVC is bound and accessible
6. ✅ Integration tests all pass
7. ✅ Logs show no errors

**When all green → Ready for Phase 2 enhancements!**

---

## 📞 **Quick Help**

**Need Help?** Run verification script:
```powershell
.\scripts\verify-deployment.ps1 -Verbose
```

**Full Reset** (if needed):
```powershell
# Cleanup everything
helm uninstall zeta-agent -n zeta-agent
kubectl delete namespace zeta-agent
terraform destroy -chdir=infra/terraform
docker system prune -f
```

**Start Fresh**:
```powershell
.\scripts\deploy.ps1
```

---

**🎯 Goal**: Get from current state to fully deployed and verified Zeta AI Agent in ~1-2 hours!
