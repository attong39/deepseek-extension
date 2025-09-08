# 🚀 TRIỂN KHAI NHANH - Zeta AI Agent DevOps

> **Quick Start Guide cho Windows + Docker Desktop**  
> **Thời gian:** ~30-45 phút | **Mục tiêu:** Production-ready deployment  

## 🎯 **Mục Tiêu**

✅ Cài đặt DevOps tools (Docker Desktop, kubectl, Helm, Terraform)  
✅ Build & push image (multi-arch: amd64 + arm64)  
✅ Deploy bằng Terraform + Helm  
✅ Kiểm tra health, metrics, integration test  
✅ Xác nhận **Green Indicators** trong Success Criteria  

---

## 📋 **BƯỚC 1: Cài Đặt DevOps Tools (15-30 phút)**

### 🛠️ **Script Tự Động** (Khuyến nghị)

```powershell
# Mở PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force
.\scripts\setup-devops-tools.ps1

# Sau khi cài đặt xong, RESTART terminal
```

### 📦 **Tools sẽ được cài đặt:**

| Tool | Chức năng | Version |
|------|-----------|---------|
| 🐳 **Docker Desktop** | Container runtime + K8s | Latest |
| ⚙️ **kubectl** | Kubernetes CLI | Latest |
| ⛵ **Helm** | K8s package manager | v3.x |
| 🏗️ **Terraform** | Infrastructure as Code | Latest |

---

## 🚀 **BƯỚC 2: Build & Deploy (15-20 phút)**

### 🔨 **Build Multi-Arch Image**

```powershell
# Build và push Docker image
.\scripts\build_docker.sh
# Hoặc Windows:
.\scripts\deploy.ps1 build
```

**Kết quả mong đợi:**
- ✅ Multi-platform image (linux/amd64, linux/arm64)
- ✅ Security scan passed
- ✅ Image pushed to registry

### 🚀 **Deploy Infrastructure**

```powershell
# Full deployment: Terraform + Helm
.\scripts\deploy.ps1

# Hoặc từng bước:
.\scripts\deploy.ps1 terraform plan
.\scripts\deploy.ps1 terraform apply  
.\scripts\deploy.ps1 helm install
```

**Infrastructure được tạo:**
- ✅ Kubernetes namespace (`zeta-agent`)
- ✅ Deployment với auto-scaling
- ✅ Services và Ingress
- ✅ Persistent Volume Claims
- ✅ ConfigMaps và Secrets

---

## 🔍 **BƯỚC 3: Verification (10-15 phút)**

### 📊 **Health Checks**

```powershell
# 1. Kiểm tra deployment status
kubectl get pods -n zeta-agent
kubectl get services -n zeta-agent

# 2. Health endpoint test
.\scripts\verify-deployment.ps1

# 3. Port forward để test local
kubectl port-forward svc/zeta-agent 8080:3000 -n zeta-agent
# Test: http://localhost:8080/health
```

### 📈 **Metrics & Monitoring**

```powershell
# Kiểm tra ServiceMonitor
kubectl get servicemonitor -n zeta-agent

# Port forward Prometheus (nếu có)
kubectl port-forward svc/prometheus 9090:9090
# Browse: http://localhost:9090/graph
# Search: zeta_*
```

### 🧪 **Integration Testing**

```bash
# Full end-to-end test
.\scripts\test_integration.sh

# Test cases:
# ✅ Docker build & functionality
# ✅ Terraform configuration
# ✅ Helm chart validation
# ✅ Kubernetes deployment
# ✅ Application health
# ✅ Scaling tests
# ✅ Cleanup verification
```

---

## ✨ **SUCCESS CRITERIA - Green Indicators**

### 🎯 **Must Have (Critical)**

| Check | Command | Expected Result |
|-------|---------|-----------------|
| 🐳 **Docker Build** | `docker images \| grep zeta-agent` | Multi-arch image present |
| ☸️ **K8s Deployment** | `kubectl get pods -n zeta-agent` | All pods `Running` |
| 🔧 **Service Ready** | `kubectl get svc -n zeta-agent` | Service `ClusterIP` assigned |
| 💚 **Health Check** | `curl http://localhost:8080/health` | HTTP 200 OK |
| 📊 **Metrics** | `curl http://localhost:8080/metrics` | Prometheus metrics |

### 🚀 **Nice to Have (Optional)**

| Check | Command | Expected Result |
|-------|---------|-----------------|
| 📈 **Auto-scaling** | `kubectl get hpa -n zeta-agent` | HPA configured |
| 🔒 **Security Scan** | `docker scout cves zeta-agent:latest` | No critical vulnerabilities |
| 🌐 **Ingress** | `kubectl get ingress -n zeta-agent` | External access configured |
| 📋 **Helm Tests** | `helm test zeta-agent -n zeta-agent` | All tests passed |

---

## 🛠️ **TROUBLESHOOTING**

### ❌ **Common Issues**

| Problem | Solution |
|---------|----------|
| 🚫 Docker không start | Enable Hyper-V, restart Windows |
| ⚠️ kubectl connection refused | Enable Kubernetes in Docker Desktop |
| 🔴 Helm install failed | Check namespace exists, verify values.yaml |
| 💥 Pod CrashLoopBackOff | Check logs: `kubectl logs <pod> -n zeta-agent` |

### 🔍 **Debug Commands**

```powershell
# Check cluster info
kubectl cluster-info

# Describe failed resources
kubectl describe pod <pod-name> -n zeta-agent

# View events
kubectl get events -n zeta-agent --sort-by=.metadata.creationTimestamp

# Check logs
kubectl logs deployment/zeta-agent -n zeta-agent --tail=50
```

---

## 📈 **PHASE 2 - Next Steps**

### 🎯 **Production Readiness**

1. **🔒 Security Hardening**
   - TLS certificates setup
   - RBAC refinement
   - Network policies
   - Security scanning integration

2. **📊 Monitoring & Observability**
   - Prometheus + Grafana dashboards
   - Log aggregation (ELK/Loki)
   - Distributed tracing
   - Alerting rules

3. **🚀 CI/CD Pipeline**
   - GitHub Actions integration
   - Automated testing
   - Blue-green deployments
   - Rollback strategies

4. **⚡ Performance Optimization**
   - Resource tuning
   - Caching strategies
   - Database optimization
   - Load testing

### 🏆 **Success Metrics**

- **🎯 Deployment Time:** < 5 minutes
- **💚 Uptime:** 99.9%+
- **⚡ Response Time:** < 200ms
- **🛡️ Security Score:** A+
- **📈 Scalability:** 1-100 pods auto-scale

---

## 📞 **Support & Resources**

- **📖 Documentation:** `./docs/` folder
- **🐛 Issues:** GitHub Issues
- **💬 Support:** Team chat channel
- **📊 Monitoring:** Grafana dashboards
- **🔍 Logs:** Kibana/Loki interface

**🎉 Happy Deploying! 🚀**
