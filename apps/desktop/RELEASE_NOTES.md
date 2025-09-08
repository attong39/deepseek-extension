# ZETA Desktop v1.0.0 Release Notes

## 🎉 Highlights

- **Production-Ready Health Monitoring**: Real-time triad health check (Renderer ⇆ Main ⇆ Backend)
- **Complete Build Metadata**: Version, commit SHA, build time embedded in About dialog
- **Enhanced Crash Reporting**: Automatic crash detection with file-based logging
- **Supply Chain Security**: SBOM (Software Bill of Materials) and license compliance
- **Release Automation**: Quality gates + semver automation + multi-platform artifacts

## 🔒 Security & Compliance

- ✅ **SBOM Generation**: CycloneDX format với vulnerability scan
- ✅ **License Report**: Automated third-party license compliance
- ✅ **Quality Gates**: TypeScript, tests, contract validation, duplication check
- ✅ **Crash Reporter**: Electron crashReporter với diagnostic payload

## 🏥 Health & Observability

- **Health Badge**: Live status với 30s polling (✓ ok / ⚠ degraded / ✗ down)
- **Tri-state Logic**: 
  - `ok` = API + WebSocket + Main Process đều hoạt động
  - `degraded` = ít nhất 1 component fail
  - `down` = tất cả components fail
- **Copy Diagnostics**: About → Copy diagnostics → clipboard JSON với full context

## 🛠️ Developer Experience

- **Release Workflow**: `npm version 1.0.0` → auto quality check → build → push tags
- **Build Metadata**: Auto-inject version/commit/time vào UI
- **Contract Guard**: Schema validation để tránh breaking changes
- **Multi-platform**: Windows (NSIS), macOS (DMG), Linux (AppImage)

## 🚨 Known Issues

1. **WebSocket Health Check**: Timeout 800ms có thể gây false-negative với mạng chậm
2. **OpenAPI BASE**: Cần đảm bảo BASE URL đúng môi trường khi build
3. **Code Signing**: Cần bổ sung certificates cho distribution chính thức

## 📋 Upgrade Notes

### From v0.x → v1.0.0:

1. **Health API Change**: 
   ```typescript
   // Old
   { apiOk: boolean; wsOk: boolean }
   
   // New  
   { level: "ok"|"degraded"|"down"; app: {...}; main: {...}; server: {...} }
   ```

2. **Build Process**: 
   ```bash
   # Old
   npm run build
   
   # New (với metadata)
   npm run prebuild  # auto chạy trong npm run build
   npm run build
   ```

3. **Release Process**:
   ```bash
   # Thay vì manual tag
   npm version 1.0.0  # auto chạy preversion/version/postversion
   ```

## 🔬 Testing Matrix

| OS            | Build | Health Check | Dropzone | About/Diagnostics |
| ------------- | ----- | ------------ | -------- | ----------------- |
| Windows 11    | ✅     | ✅            | ✅        | ✅                 |
| macOS 14+     | ✅     | ✅            | ✅        | ✅                 |
| Ubuntu 22.04+ | ✅     | ✅            | ✅        | ✅                 |

## 🎯 Next Steps

- [ ] **Code Signing**: Apple Developer + Windows certificates
- [ ] **Auto-Update**: Electron-updater integration
- [ ] **Telemetry**: Anonymous usage analytics
- [ ] **Plugin System**: Extensible architecture với isolated sandboxes

---

**Full Changelog**: https://github.com/your-org/zeta/compare/v0.9.0...v1.0.0
**Download**: See [Releases](https://github.com/your-org/zeta/releases/tag/v1.0.0) for platform-specific binaries