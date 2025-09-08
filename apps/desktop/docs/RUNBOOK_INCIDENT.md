# Runbook Sự Cố (Desktop)

## 🎯 Mục tiêu

Chẩn đoán nhanh WS/API/APP; không rò rỉ PII/secret.

## 🚨 Quy trình 5 bước

### 1. **Chụp Health**
- Dashboard → HealthBadge (xem màu: 🟢 ok / 🟡 degraded / 🔴 down)
- About → Copy diagnostics (dán vào ticket support)

### 2. **Kiểm tra API**
- GET `/health` (<= 500ms response time)
- WS `/ws/health` (pong trong 1s)

### 3. **Xem crash logs**
- Electron userData/crashes
- Lọc theo timestamp của incident
- Tìm stack trace (đã mask PII)

### 4. **So khớp version**
- About: version + gitSha + buildTime
- Khớp với tag release trên GitHub
- Xác nhận user đang dùng version mới nhất

### 5. **Phân loại & Escalate**

#### Đứt mạng/WS
- Thử lại connection
- Xem backoff/jitter pattern
- Kiểm tra proxy/VPN settings

#### API 5xx
- Ghi issue apps/backend team
- Đính kèm diagnostics payload
- Escalate đến DevOps nếu cần

#### Renderer error
- Kiểm tra browser console
- Log đã mask PII tự động
- Reboot Electron app

## 🔄 Rollback

Dùng `scripts/release_rollback.mjs` → đưa "latest" về tag trước (không rebuild).

```bash
npm run rollback
```

## 📋 Diagnostics Payload Sample

```json
{
  "version": "1.0.0",
  "gitSha": "abc123def",
  "buildTime": "2025-08-28T10:00:00.000Z",
  "platform": "Win32",
  "health": {
    "app": { "ok": true },
    "main": { "pid": 12345, "memoryMB": 45, "ok": true },
    "server": { "http": false, "ws": false },
    "time": "2025-08-28T10:05:00.000Z", 
    "level": "down"
  }
}
```

## 📞 Escalation Matrix

| Severity             | Response Time | Contact             |
| -------------------- | ------------- | ------------------- |
| P0 - App won't start | 15 min        | @dev-team + @devops |
| P1 - Health degraded | 1 hour        | @dev-team           |
| P2 - UI glitch       | 4 hours       | @dev-team           |
| P3 - Feature request | Next sprint   | Product team        |

## 🛠️ Common Fixes

### Health Badge shows "down" but app works
```bash
# Check if apps/backend is running
curl http://localhost:8000/health

# Check WebSocket endpoint  
wscat -c ws://localhost:8000/ws/health
```

### Build metadata missing
```bash
# Regenerate build metadata
npm run prebuild

# Verify .env.build exists
cat .env.build
```

### Electron crashes on startup
```bash
# Check crash dumps
ls -la ~/Library/Application\ Support/ZETA\ Desktop/crashes/

# Clear user data (last resort)
rm -rf ~/Library/Application\ Support/ZETA\ Desktop/
```

## 📊 Health Check Details

### Tri-state Logic
- **ok**: API ✅ + WS ✅ + Main ✅
- **degraded**: 1-2 components failing
- **down**: All 3 components failing

### Polling Behavior
- Interval: 30 seconds
- Timeout: 800ms per check
- Cleanup: setInterval cleared on unmount
- Error handling: Preserve last known state

## 🔐 Security Notes

- Diagnostics payload **không chứa** secrets/tokens
- PII được mask tự động trong logs
- Crash reports **không gửi** về server tự động
- User phải manually copy diagnostics

---

**Last Updated**: 2025-08-28  
**Version**: 1.0.0  
**Owner**: DevOps Team