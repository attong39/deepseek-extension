# 🚀 QUICK START GUIDE - Zeta AI Agent Deployment

> **⏱️ Tổng thời gian:** 30-60 phút  
> **🎯 Mục tiêu:** Deploy production-ready Zeta AI Agent với Kubernetes

## 📋 **Prerequisites Checklist**

- [ ] Windows 10/11 với PowerShell 5.1+
- [ ] Administrator access cho việc cài đặt tools
- [ ] Internet connection tốc độ cao
- [ ] 8GB+ RAM available cho Docker Desktop

---

## ⚡ **Express Deployment (5 Commands)**

```powershell
# 1. Setup DevOps tools (15-20 phút - chạy 1 lần)
.\scripts\setup-devops-tools.ps1

# 2. Enable Kubernetes in Docker Desktop
# Settings > Kubernetes > Enable Kubernetes > Apply & Restart

# 3. Deploy everything (10-15 phút)
.\scripts\deploy.ps1

# 4. Verify deployment (5 phút)
.\scripts\verify-deployment.ps1 -FullVerification

# 5. Access application
kubectl port-forward svc/zeta-agent 8080:3000 -n zeta-agent
# Visit: http://localhost:8080/health
```

---

## 🔧 **Step-by-Step Detailed**

### **Phase 1: Setup Environment** ⏱️ ~20-30 phút

```powershell
# 1.1 Install DevOps tools (run as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force
.\scripts\setup-devops-tools.ps1

# 1.2 Restart PowerShell and verify
docker version
kubectl version --client
helm version
terraform version

# 1.3 Enable Kubernetes in Docker Desktop
# GUI: Settings > Kubernetes > Enable Kubernetes > Apply & Restart
# Wait for green indicator (5-10 phút)

# 1.4 Verify Kubernetes cluster
kubectl cluster-info
kubectl get nodes
```

### **Phase 2: Build & Deploy** ⏱️ ~10-20 phút

```powershell
# 2.1 Build multi-arch Docker image
.\scripts\deploy.ps1 build

# 2.2 Deploy infrastructure với Terraform + Helm
.\scripts\deploy.ps1

# 2.3 Kiểm tra deployment status
kubectl get all -n zeta-agent
```

### **Phase 3: Verification** ⏱️ ~5-10 phút

```powershell
# 3.1 Run comprehensive verification
.\scripts\verify-deployment.ps1 -FullVerification

# 3.2 Manual health check
kubectl port-forward svc/zeta-agent 8080:3000 -n zeta-agent &
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/status

# 3.3 Integration testing (optional)
.\scripts\test_integration.sh
```

---

## ✅ **Success Indicators**

### **🟢 All Green = Production Ready**

| Component | Check | Command | Status |
|-----------|-------|---------|--------|
| **Docker** | Multi-arch build | `docker images \| findstr zeta-agent` | ✅ |
| **Kubernetes** | Cluster running | `kubectl get nodes` | ✅ |
| **Application** | Pods running | `kubectl get pods -n zeta-agent` | ✅ |
| **Health** | Endpoint OK | `curl localhost:8080/health` | ✅ |
| **API** | Status OK | `curl localhost:8080/api/v1/status` | ✅ |

### **🎯 Performance Metrics**
- **Container startup time:** < 30 seconds
- **Health check response:** < 500ms
- **Memory usage:** < 512Mi per pod
- **CPU usage:** < 500m per pod

---

## 🚨 **Troubleshooting Quick Fixes**

```powershell
# Problem: Docker not responding
docker system prune -f
Restart-Service docker

# Problem: Kubernetes not ready
kubectl config use-context docker-desktop
kubectl get nodes

# Problem: Deployment failed
kubectl delete namespace zeta-agent
.\scripts\deploy.ps1

# Problem: Pod not starting
kubectl logs -f deployment/zeta-agent -n zeta-agent
kubectl describe pod -n zeta-agent

# Problem: Can't access application
kubectl port-forward svc/zeta-agent 8080:3000 -n zeta-agent
netstat -an | findstr 8080
```

---

## 📊 **What Gets Deployed**

```yaml
Kubernetes Resources:
  - Namespace: zeta-agent
  - Deployment: zeta-agent (1-3 replicas)
  - Service: LoadBalancer/ClusterIP
  - PVC: 10Gi for vector database
  - HPA: Auto-scaling 1-10 replicas
  - ServiceAccount: RBAC permissions
  - ConfigMap: Application configuration
  - Secret: Sensitive data (if any)

Container Specs:
  - Image: zetaai/zeta-agent:latest
  - Platforms: linux/amd64, linux/arm64
  - Memory: 256Mi-512Mi
  - CPU: 100m-500m
  - Security: Non-root user
```

---

## 🎯 **Next Steps After Deployment**

### **Development Phase**
```powershell
# 1. Test API endpoints
curl http://localhost:8080/api/v1/chat
curl http://localhost:8080/api/v1/code-analysis

# 2. Check logs for debugging
kubectl logs -f deployment/zeta-agent -n zeta-agent

# 3. Scale up for testing
kubectl scale deployment zeta-agent --replicas=3 -n zeta-agent
```

### **Production Readiness**
```powershell
# 1. Setup monitoring
helm install prometheus prometheus-community/kube-prometheus-stack

# 2. Configure ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# 3. Setup SSL certificates
# Use cert-manager for Let's Encrypt
```

---

## 📞 **Support & Documentation**

- **📖 Full Documentation:** `DEPLOYMENT_ASSESSMENT.md`
- **🔧 Scripts Location:** `./scripts/`
- **🐛 Debug Mode:** `.\scripts\verify-deployment.ps1 -Debug`
- **📊 Monitoring:** `kubectl port-forward svc/prometheus 9090:9090`

---

> **🎉 Congratulations!**  
> Bạn đã successfully deploy một production-ready AI system với:  
> ✅ Multi-arch Docker images  
> ✅ Kubernetes orchestration  
> ✅ Auto-scaling capabilities  
> ✅ Health monitoring  
> ✅ Security hardening  

**🚀 Ready to code with AI assistance!** 🤖
