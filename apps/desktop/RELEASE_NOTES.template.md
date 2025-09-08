# ZETA Desktop vX.Y.Z — Release Notes

## 🎉 Highlights

- **[Feature]** Tri-state health monitoring (Renderer ⇆ Main ⇆ Backend)
- **[Feature]** Real-time HealthBadge với 30s polling + tri-state colors
- **[Feature]** Copy diagnostics với full build metadata + health snapshot
- **[Feature]** Build metadata embedded (version/commit/time) in About modal
- **[Enhancement]** Release automation với quality gates + semver workflow

## 🔒 Security & Compliance

- ✅ **CSP/IPC hardening**: Secure IPC channels cho health check
- ✅ **PII masking logs**: Không log sensitive data trong diagnostics
- ✅ **SBOM (CycloneDX)**: Software Bill of Materials attached
- ✅ **Third-party licenses**: Complete license compliance report
- ✅ **Crash reporting**: File-based crash detection với metadata

## 📝 Changes

### Added
- Tri-state health system (`ok | degraded | down`)
- HealthBadge component với real-time polling
- Copy diagnostics functionality trong About modal
- Build metadata injection (version, git SHA, build time)
- Release automation scripts với quality gates
- Multi-platform artifact validation
- Bundle size reporting với gzip compression

### Fixed
- Memory leak trong health polling (proper cleanup)
- WebSocket timeout handling (800ms với proper error handling)
- Build metadata không sync giữa environments

### Breaking
- **None** - Backward compatible với v0.x

## 🚨 Known Issues

1. **WebSocket Health Check**: Timeout 800ms có thể gây false-negative với mạng chậm
2. **OpenAPI BASE**: Cần đảm bảo BASE URL đúng môi trường khi build
3. **TypeScript Errors**: Một số legacy code chưa fix strict type check

## 📋 Upgrade Notes

### From v0.x → v1.0.0

- **Safe to upgrade**: Không cần thay đổi config
- **Health API**: Mở rộng từ `{apiOk, wsOk}` → `{level, app, main, server}`
- **Build Process**: Tự động inject metadata, không cần thay đổi workflow

### Configuration

```json
{
  "healthCheck": {
    "pollInterval": 30000,
    "timeout": 800
  }
}
```

## 🔍 Checksums

> Xem file: `dist/CHECKSUMS.txt` cho SHA256 hashes của tất cả artifacts

## 📦 Artifacts

- **Windows**: `ZETA-Desktop-Setup-vX.Y.Z.exe`
- **macOS**: `ZETA-Desktop-vX.Y.Z.dmg`  
- **Linux**: `ZETA-Desktop-vX.Y.Z.AppImage`
- **SBOM**: `sbom.json` (CycloneDX format)
- **Licenses**: `THIRD_PARTY_LICENSES.html`

---

**Full Changelog**: https://github.com/your-org/zeta/compare/vX.Y.Z-1...vX.Y.Z  
**Download**: [GitHub Releases](https://github.com/your-org/zeta/releases/tag/vX.Y.Z)