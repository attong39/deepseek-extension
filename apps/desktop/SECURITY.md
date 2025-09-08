# Security Policy

## 🔐 Báo cáo lỗ hổng bảo mật (Security Vulnerabilities)

### ⚡ Báo cáo khẩn cấp
Nếu bạn phát hiện lỗ hổng bảo mật nghiêm trọng:

**KHÔNG** tạo public issue trên GitHub.

**ĐỀ NGHỊ** gửi email trực tiếp đến: **security@zetavn.com**

### 📋 Thông tin cần cung cấp

```
Subject: [SECURITY] desktop_ai_zeta - [Tóm tắt ngắn]

1. 🎯 Loại lỗ hổng: (RCE, XSS, Injection, Data Leak, etc.)
2. 🔍 Component/Module bị ảnh hưởng
3. 🚨 Mức độ nghiêm trọng: Critical/High/Medium/Low  
4. 🔄 Cách tái hiện (steps to reproduce)
5. 💥 Impact tiềm ẩn (data loss, privilege escalation, etc.)
6. 🛠️ Fix đề xuất (nếu có)
7. 📦 App version bị ảnh hưởng
8. 💻 Environment (OS, Node version, etc.)
```

### ⏱️ Response Timeline

- **24h**: Xác nhận nhận được báo cáo
- **72h**: Preliminary assessment + severity classification
- **7 days**: Fix hoặc workaround (critical/high severity)
- **30 days**: Full fix + security advisory (medium/low severity)

### 🛡️ Supported Versions

| Version | Supported       |
| ------- | --------------- |
| 1.0.x   | ✅ Yes           |
| 0.9.x   | ✅ Yes (limited) |
| < 0.9   | ❌ No            |

### 🏆 Security Hall of Fame

Chúng tôi ghi nhận đóng góp của các security researchers:

- [Sẽ cập nhật khi có reports]

### 🔒 Security Features

desktop_ai_zeta được thiết kế với các nguyên tắc security-first:

#### ✅ Build Security
- **Supply Chain**: Dependabot + CodeQL scan dependencies
- **SBOM**: Software Bill of Materials tracking
- **Signatures**: Release artifacts được sign
- **Integrity**: Checksums verification

#### ✅ Runtime Security  
- **Sandbox**: Electron renderer processes isolated
- **CSP**: Content Security Policy enforced
- **ENV**: Sensitive environment variables guarded
- **Plugins**: Plugin manifest allowlist + schema validation

#### ✅ Data Security
- **Local Storage**: Encrypted sensitive data
- **Network**: HTTPS-only communication
- **Logs**: No sensitive data in logs
- **Memory**: Secure memory cleanup

### 📚 Security Resources

- [OWASP Electron Security](https://owasp.org/www-project-electron-security/)
- [Electron Security Checklist](https://www.electronjs.org/docs/tutorial/security)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)

### 🚀 Security Development

#### Pre-commit hooks
```bash
npm run security:check  # Audit dependencies + static analysis
```

#### CI/CD Security Gates
- CodeQL static analysis
- npm audit / yarn audit
- License compliance check
- Vulnerable dependency alerts

---

**🙏 Cảm ơn** bạn đã giúp desktop_ai_zeta an toàn hơn!