# 🇻🇳 HƯỚNG DẪN TRIỂN KHAI PRODUCTION - ZETA AI

**Tác giả**: Duy BG VN
**Ngày cập nhật**: 15/08/2025
**Phiên bản**: 2.0
**Trạng thái**: ✅ SẴN SÀNG TRIỂN KHAI

---

## 📋 TỔNG QUAN HỆ THỐNG

### 🎯 Mục tiêu
Triển khai hệ thống ZETA AI lên môi trường production với độ tin cậy cao, bảo mật tốt và khả năng mở rộng.

### 🏗️ Kiến trúc hệ thống
- **API Server**: FastAPI với Gunicorn (2-10 instances tự động)
- **Worker**: Celery workers cho xử lý bất đồng bộ
- **Database**: PostgreSQL với replication
- **Cache**: Redis với Sentinel
- **Load Balancer**: Nginx với SSL termination
- **Monitoring**: Prometheus + Grafana + ELK + Jaeger

---

## ✅ KIỂM TRA TIỀN ĐIỀU KIỆN

### 🖥️ Môi trường server
```bash
# Kiểm tra Docker
docker --version
docker-compose --version

# Kiểm tra Python
python --version  # >= 3.11

# Kiểm tra disk space
df -h

# Kiểm tra memory
free -h
```

### 🔐 Bảo mật
- [ ] SSL certificate đã được cấp
- [ ] Firewall đã được cấu hình
- [ ] DNS đã được trỏ đúng domain
- [ ] Backup storage đã sẵn sàng

---

## 🚀 CÁC BƯỚC TRIỂN KHAI

### Bước 1: Kiểm tra Infrastructure
```bash
# Di chuyển đến thư mục dự án
cd E:\zeta

# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Kiểm tra tình trạng infrastructure
python scripts\validate_infrastructure.py
```

**Kết quả mong đợi:**
```
✅ Successful checks: 15/15
⚠️ Warnings: 7 (không nghiêm trọng)
❌ Critical errors: 0
🎉 Ready for production deployment!
```

### Bước 2: Cấu hình môi trường Production
```bash
# Sao chép file cấu hình môi trường
cp .env.production.template .env.production

# Chỉnh sửa các thông số cần thiết
notepad .env.production
```

**Các thông số quan trọng cần cấu hình:**
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/zeta_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_SENTINEL_HOSTS=localhost:26379

# Security
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
ALLOWED_HOSTS=api.zeta-ai.vn,*.zeta-ai.vn

# External APIs
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_ENABLED=true
GRAFANA_ADMIN_PASSWORD=secure-password
```

### Bước 3: Triển khai tự động
```bash
# Triển khai đơn giản (khuyến nghị cho lần đầu)
python scripts\deploy_production_automated.py

# Hoặc triển khai nâng cao với monitoring đầy đủ
python scripts\deployment\production_deploy_complete.py --environment production
```

### Bước 4: Kiểm tra Health Check
```bash
# Kiểm tra API health
curl https://api.zeta-ai.vn/api/v1/health

# Kiểm tra tất cả services
python scripts\monitoring\performance_check.py
```

---

## 🔧 CÁC LỆNH TRIỂN KHAI CHI TIẾT

### 🐳 Triển khai bằng Docker Compose
```bash
# Di chuyển đến thư mục docker
cd deployment\docker

# Xây dựng images
docker-compose -f docker-compose.production.yml build

# Khởi động services
docker-compose -f docker-compose.production.yml up -d

# Kiểm tra trạng thái
docker-compose -f docker-compose.production.yml ps
```

### ☸️ Triển khai bằng Kubernetes
```bash
# Áp dụng manifests
kubectl apply -f deployment\kubernetes\production-complete.yaml

# Kiểm tra pods
kubectl get pods -n zeta-ai

# Kiểm tra services
kubectl get services -n zeta-ai

# Kiểm tra ingress
kubectl get ingress -n zeta-ai
```

### 📊 Thiết lập Monitoring
```bash
# Khởi động monitoring stack
docker-compose -f deployment\docker\docker-compose.production.yml up -d prometheus grafana

# Import Grafana dashboard
curl -X POST http://admin:password@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @monitoring\grafana\dashboards\zeta-ai-production.json
```

---

## 🌐 DANH SÁCH CÁC ENDPOINT

### 🔗 Production URLs
| Service | URL | Mô tả |
|---------|-----|-------|
| **API Chính** | https://api.zeta-ai.vn | Endpoint chính của API |
| **Tài liệu API** | https://api.zeta-ai.vn/docs | Swagger UI documentation |
| **Health Check** | https://api.zeta-ai.vn/api/v1/health | Kiểm tra tình trạng hệ thống |
| **Admin Panel** | https://admin.zeta-ai.vn | Giao diện quản trị |

### 📈 Monitoring URLs
| Service | URL | Mô tả |
|---------|-----|-------|
| **Prometheus** | https://prometheus.zeta-ai.vn | Thu thập metrics |
| **Grafana** | https://grafana.zeta-ai.vn | Dashboard và visualization |
| **Jaeger** | https://jaeger.zeta-ai.vn | Distributed tracing |
| **Kibana** | https://kibana.zeta-ai.vn | Log analysis |
| **Flower** | https://flower.zeta-ai.vn | Celery monitoring |

### 🏠 Local Development URLs
| Service | URL | Mô tả |
|---------|-----|-------|
| **API** | http://localhost:8000 | Local API server |
| **Prometheus** | http://localhost:9090 | Local metrics |
| **Grafana** | http://localhost:3000 | Local dashboard |
| **Jaeger** | http://localhost:16686 | Local tracing |
| **Kibana** | http://localhost:5601 | Local logs |

---

## 🧪 KIỂM TRA VÀ TESTING

### 🏥 Health Checks
```bash
# Kiểm tra API status
curl -f https://api.zeta-ai.vn/api/v1/health

# Kiểm tra database connection
curl -f https://api.zeta-ai.vn/api/v1/health/database

# Kiểm tra Redis connection
curl -f https://api.zeta-ai.vn/api/v1/health/redis

# Kiểm tra Celery workers
curl -f https://api.zeta-ai.vn/api/v1/health/workers
```

### ⚡ Load Testing
```bash
# Chạy load test
python scripts\testing\load_test.py --target https://api.zeta-ai.vn

# Load test với Apache Bench
ab -n 1000 -c 10 https://api.zeta-ai.vn/api/v1/health

# Load test với artillery
artillery run scripts\testing\artillery-config.yml
```

### 🔍 Performance Monitoring
```bash
# Kiểm tra performance tổng thể
python scripts\monitoring\performance_check.py

# Kiểm tra memory usage
docker stats

# Kiểm tra disk usage
df -h

# Kiểm tra network
netstat -tlnp
```

---

## 🛡️ BẢO MẬT VÀ BACKUP

### 🔐 Cấu hình bảo mật
```bash
# Kiểm tra SSL certificate
openssl s_client -connect api.zeta-ai.vn:443

# Kiểm tra security headers
curl -I https://api.zeta-ai.vn

# Scan vulnerabilities
python scripts\security\vulnerability_scan.py
```

### 💾 Backup dữ liệu
```bash
# Backup database
python scripts\backup_data.py --type database

# Backup files
python scripts\backup_data.py --type files

# Backup configuration
python scripts\backup_data.py --type config

# Full backup
python scripts\backup_data.py --type full
```

### 🔄 Restore dữ liệu
```bash
# Restore database
python scripts\restore_data.py --type database --file backup_20250815.sql

# Restore files
python scripts\restore_data.py --type files --file files_backup_20250815.tar.gz
```

---

## 🚨 XỬ LÝ SỰ CỐ VÀ ROLLBACK

### 🔙 Rollback nhanh
```bash
# Rollback bằng deployment script
python scripts\deployment\production_deploy_complete.py --rollback

# Rollback manual với Docker Compose
cd deployment\docker
docker-compose -f docker-compose.production.yml down
docker-compose -f docker-compose.production.yml.backup up -d
```

### 🆘 Xử lý sự cố thường gặp

#### 1. Service không khởi động được
```bash
# Kiểm tra logs
docker-compose -f deployment\docker\docker-compose.production.yml logs zeta-api

# Kiểm tra resource usage
docker stats

# Restart service
docker-compose -f deployment\docker\docker-compose.production.yml restart zeta-api
```

#### 2. Database connection lỗi
```bash
# Kiểm tra database status
docker-compose -f deployment\docker\docker-compose.production.yml exec postgres pg_isready

# Kiểm tra connection
psql -h localhost -U zeta_user -d zeta_db

# Restart database
docker-compose -f deployment\docker\docker-compose.production.yml restart postgres
```

#### 3. High memory usage
```bash
# Scale services
docker-compose -f deployment\docker\docker-compose.production.yml up -d --scale zeta-api=3

# Kiểm tra memory leaks
python scripts\monitoring\memory_profiler.py
```

---

## 📊 MONITORING VÀ ALERTING

### 📈 Thiết lập alerts
```bash
# Cấu hình Prometheus alerts
kubectl apply -f monitoring\prometheus\alert-rules.yml

# Cấu hình Grafana notifications
python scripts\monitoring\setup_notifications.py
```

### 🔔 Các thông báo quan trọng
- **High CPU usage** (> 80% trong 5 phút)
- **High memory usage** (> 90% trong 3 phút)
- **Database connection errors** (> 5 lỗi/phút)
- **API response time** (> 2 giây cho 95th percentile)
- **Disk space low** (< 10% còn lại)

---

## 📞 LIÊN HỆ HỖ TRỢ

### 👥 Team liên hệ
- **DevOps Lead**: Duy BG VN
- **Infrastructure**: devops@zeta-ai.vn
- **Security**: security@zeta-ai.vn
- **On-call**: +84-xxx-xxx-xxxx

### 📚 Tài liệu tham khảo
- [Hướng dẫn Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Security Best Practices](docs/SECURITY.md)

---

## ✅ CHECKLIST TRIỂN KHAI

### Trước khi triển khai
- [ ] Infrastructure validation passed (15/15)
- [ ] SSL certificate đã chuẩn bị
- [ ] DNS đã cấu hình
- [ ] Backup storage đã sẵn sàng
- [ ] Monitoring stack đã test
- [ ] Team đã được training

### Trong quá trình triển khai
- [ ] Build images thành công
- [ ] Services khởi động OK
- [ ] Health checks pass
- [ ] Database migration thành công
- [ ] Load balancer hoạt động

### Sau khi triển khai
- [ ] Performance test pass
- [ ] Security scan clean
- [ ] Monitoring alerts hoạt động
- [ ] Backup procedures test
- [ ] Documentation cập nhật

---

**🎉 CHÚC MỪNG BẠN ĐÃ TRIỂN KHAI THÀNH CÔNG ZETA AI PRODUCTION! 🎉**

*Hệ thống đã sẵn sàng phục vụ workload production với hiệu suất cao và độ tin cậy tốt.*
