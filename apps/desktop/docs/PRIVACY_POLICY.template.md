# Chính sách Quyền riêng tư (Template)

## 🔐 Nguyên tắc chung

desktop_ai_zeta tuân thủ nguyên tắc **privacy-first** và **opt-in** cho mọi thu thập dữ liệu.

## 📊 Telemetry (Tuỳ chọn)

### Trạng thái mặc định
- **Telemetry TẮT** theo mặc định
- Người dùng phải **chủ động bật** qua Settings
- Có thể tắt bất cứ lúc nào

### Dữ liệu thu thập (chỉ khi được bật)
- **Sự kiện kỹ thuật**: phiên bản app, lỗi, hiệu năng
- **Metadata**: thời gian sử dụng, tính năng được dùng
- **Không thu thập**: nội dung tệp, dữ liệu cá nhân, passwords, tokens

### Bảo vệ dữ liệu
- **PII Masking**: Email, số thẻ, SSN tự động được che
- **Local-first**: Mặc định chỉ log local, không gửi network
- **Encryption**: Dữ liệu nhạy cảm được mã hóa trong storage

## 🗂️ Dữ liệu lưu trữ

### Crash logs
- **Mục đích**: Debug và cải thiện ổn định
- **Thời gian**: Tự động xóa sau 30 ngày (có thể tuỳ chỉnh)
- **Vị trí**: Local trong thư mục userData
- **Kiểm soát**: Người dùng có thể xóa thủ công

### Settings & Cache
- **Lưu trữ**: Local storage và userData folder
- **Kiểm soát**: Người dùng có thể reset/xóa
- **Backup**: Không tự động backup ra cloud

## 👤 Quyền người dùng

### Telemetry
- ✅ Bật/tắt telemetry
- ✅ Xem dữ liệu được thu thập
- ✅ Xuất diagnostic data để hỗ trợ

### Dữ liệu
- ✅ Xóa crash logs cũ
- ✅ Reset toàn bộ settings
- ✅ Backup/restore cấu hình

### Minh bạch
- ✅ Chính sách này luôn có trong app (Help > Privacy)
- ✅ Thông báo khi có thay đổi quyền riêng tư
- ✅ Open source - có thể audit code

## 🔗 Third-party Services

### API Connections
- Chỉ kết nối server được cấu hình
- Không gửi dữ liệu đến third-party mà không consent
- API keys/tokens lưu local, không share

### Updates
- Auto-update chỉ kiểm tra version, không gửi usage data
- Người dùng có thể tắt auto-update

## 📞 Liên hệ

Câu hỏi về quyền riêng tư: **privacy@zetavn.com**

---

**Cập nhật**: 2025-08-28  
**Version**: 1.0.0  
**Áp dụng**: desktop_ai_zeta v1.0.0+