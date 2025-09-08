# Compliance Checklist (Desktop AI ZETA)

Checklist này đảm bảo mọi PR tuân thủ enterprise quality gates trước khi merge.

## 🔒 Hard Gates (Fail CI nếu vi phạm)

- [ ] **Config Schema Validation**: App config tuân thủ `contracts/config/app-config.schema.json`
- [ ] **Plugin Manifest Validation**: Tất cả plugin manifests tuân thủ schema + semver
- [ ] **TypeScript Compilation**: `tsc --noEmit` pass hoàn toàn  
- [ ] **Unit Test Coverage**: Coverage ≥ 80% (lines, functions, branches, statements)
- [ ] **Build Success**: Production build hoàn tất không lỗi
- [ ] **Bundle Budget**: Mỗi JS asset ≤ 170KB gzip (configurable)

## ⚠️ Soft Gates (Advisory - không fail CI)

- [ ] **SBOM Generated**: CycloneDX JSON + XML artifacts được tạo
- [ ] **License Scan**: JSON + CSV license report được tạo
- [ ] **No PII in Logs**: Không có personally identifiable information trong logs
- [ ] **No Secrets**: Không có API keys, passwords, tokens trong code/logs

## 📊 Quality Metrics

### Coverage Thresholds (Vitest)
```typescript
thresholds: {
  lines: 80,      // ≥ 80% line coverage
  functions: 80,  // ≥ 80% function coverage  
  branches: 80,   // ≥ 80% branch coverage
  statements: 80  // ≥ 80% statement coverage
}
```

### Bundle Budget
- **Main JS**: ≤ 170KB gzip
- **Vendor JS**: ≤ 300KB gzip (libs/frameworks)
- **CSS**: ≤ 50KB gzip
- **Total**: ≤ 500KB gzip (first-load)

## 🚀 Local Pre-commit Commands

```bash
# Full quality gate check (matches CI)
npm ci
npm run config:validate && npm run plugins:validate
npm run typecheck
npm run test:ci  # includes coverage check
npm run build && npm run bundle:budget 170
npm run sbom:gen && npm run license:scan
```

## 📋 PR Requirements

1. **All hard gates pass** in CI
2. **No new TypeScript errors** introduced
3. **Coverage doesn't decrease** from baseline
4. **Bundle size impact** documented if >5% increase
5. **SBOM/license artifacts** uploaded for compliance audit

## 🔍 Compliance Artifacts

### CI Uploads (GitHub Actions)
- `coverage-report/`: HTML coverage report + lcov
- `sbom-artifacts/`: CycloneDX JSON/XML for dependency tracking
- `license-report/`: CSV/JSON license inventory

### Local Development
- `coverage/`: Local coverage reports
- `sbom/`: SBOM files for offline audit
- `licenses/`: License scan results

## 🎯 Next Steps for Enhanced Compliance

1. **License Allowlist**: Enforce MIT/Apache-2.0/BSD-3 only
2. **SBOM Signing**: Sign SBOM with organization key
3. **Cross-platform Builds**: Add Windows/macOS smoke tests
4. **Security Scanning**: Add SAST/DAST to release pipeline
5. **PR Comment Bot**: Auto-comment coverage/bundle/license diff

## 📚 Related Documents

- `docs/PRIVACY_POLICY.template.md` - Privacy policy template
- `docs/DATA_RETENTION_POLICY.md` - Data retention guidelines  
- `.github/PULL_REQUEST_TEMPLATE.md` - PR quality checklist
- `.github/CODEOWNERS` - Code review assignments