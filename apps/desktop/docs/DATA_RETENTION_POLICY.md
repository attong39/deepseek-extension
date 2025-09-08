# Chính sách Lưu trữ Dữ liệu

## 🎯 Mục tiêu

Đảm bảo dữ liệu được lưu trữ an toàn, thời gian hợp lý, và tôn trọng quyền riêng tư người dùng.

## 📁 Loại dữ liệu

### Crash logs
- **Vị trí**: `userData/crashes/`
- **Thời gian lưu**: 30 ngày (mặc định, có thể tuỳ chỉnh 1-365 ngày)
- **Cơ chế xóa**: Tự động theo `retentionDays` trong config
- **Kiểm soát**: User có thể xóa thủ công qua Settings
- **Nội dung**: Stack traces (đã mask PII), system info, app version

### Application logs
- **Vị trí**: Console và userData/logs (nếu có)
- **Thời gian lưu**: Theo session, không lưu vĩnh viễn
- **Bảo vệ**: PII masking tự động
- **Kiểm soát**: Không lưu sensitive data

### User settings
- **Vị trí**: `localStorage` và `userData/settings.json`
- **Thời gian lưu**: Đến khi user xóa hoặc uninstall
- **Backup**: Local only, không sync cloud
- **Kiểm soát**: User có thể reset/export

### Cache data
- **Vị trí**: `userData/cache/`
- **Thời gian lưu**: Không giới hạn (để tối ưu performance)
- **Kiểm soát**: User có thể clear cache
- **Nội dung**: File checksums, processed data (non-sensitive)

## 🔧 Cơ chế Retention

### Tự động
```typescript
// Crash logs purge (daily check)
setInterval(() => {
  const retentionDays = getConfig().retentionDays;
  window.zetaBridge.purgeLogs(retentionDays);
}, 24 * 3600 * 1000);
```

### Thủ công
- Settings > Storage > "Clear old crash logs"
- Settings > Storage > "Reset all settings"
- Settings > Storage > "Clear cache"

## 🛡️ Bảo mật

### PII Protection
- **Email masking**: `user@domain.com` → `[EMAIL]`
- **Card numbers**: `1234-5678-9012-3456` → `[CARD]`
- **SSN**: `123-45-6789` → `[SSN]`
- **Passwords/Tokens**: `"password":"secret"` → `"password":"[MASKED]"`

### Access Control
- Chỉ main process có quyền read/write userData
- Renderer process qua IPC channels được whitelist
- Không có network access đến user data trừ khi consent

### Encryption
- Sensitive settings encrypted với system key
- Crash logs không chứa plain-text passwords
- API keys/tokens encrypted trong storage

## 📊 Audit & Compliance

### Logging
- Retention operations được log (không chi tiết nội dung)
- User actions (export, delete) có audit trail
- No logging của sensitive data content

### Compliance
- GDPR-ready: Right to be forgotten (delete all data)
- Privacy-by-design: Minimal data collection
- Transparency: User biết rõ data nào được lưu, bao lâu

### Data Export
```typescript
// Diagnostic export (cho support)
const diagnostics = {
  version: getAppVersion(),
  config: maskSensitive(getConfig()),
  crashLogsCount: getCrashLogsCount(),
  // Không export nội dung logs
};
```

## 🔄 Lifecycle Management

### Installation
- Tạo userData structure
- Set default retention policies
- Apply PII masking rules

### Updates
- Migrate old data format (nếu cần)
- Preserve user retention settings
- Clean incompatible cache

### Uninstallation
- Prompt user: "Keep personal data?"
- Option: "Delete all data" (secure wipe)
- Leave system clean nếu user chọn xóa

## 📞 Support & Recovery

### Data Recovery
- Settings backup/restore từ exported file
- Crash logs không thể recover sau khi xóa
- Cache rebuild tự động nếu bị corrupt

### Support Access
- User export diagnostic data để gửi support
- Support không bao giờ direct access user machine
- Remote assistance chỉ với explicit consent

---

**Áp dụng**: desktop_ai_zeta v1.0.0+  
**Review**: 6 tháng/lần  
**Contact**: privacy@zetavn.com