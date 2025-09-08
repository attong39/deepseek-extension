# SECURITY MODEL (ZETA_AI)

## Bảo mật Baseline Vận hành

- **No secrets in code/logs**: Sử dụng env & GitHub secrets
- **PII mask**: Ở API logs, tracing. Không ghi body file raw  
- **Rate limit + request_id + audit log**: Đã có modules trong zeta_vn
- **CI Quality Gates**: ruff/mypy/pytest>80%/bandit/pip-audit
- **Release**: SBOM + artifact signatures (apps/desktop sbom đã có)

## Hardening Checklist

### Code Security
- ✅ Ruff với rules bảo mật (S-series)
- ✅ Bandit static analysis 
- ✅ pip-audit for dependency vulnerabilities
- ✅ Type safety với mypy strict
- ✅ No secrets trong code

### Infrastructure  
- ✅ Docker containers với minimal base image
- ✅ Environment separation (dev/staging/prod)
- ✅ Database migrations secured
- ✅ Redis configuration hardened

### CI/CD Pipeline
- ✅ Quality gates tại mọi PR
- ✅ Coverage threshold 80%
- ✅ Automated security scanning
- ✅ Artifact signing cho releases

### Monitoring & Observability
- ✅ Request tracing với correlation IDs
- ✅ Audit logging cho sensitive operations  
- ✅ Error handling không leak thông tin
- ✅ Performance monitoring

## Implementation Notes

Repo này tuân thủ "One-Click Learning" pipeline:
1. **Setup nhanh**: `make setup` cho dev environment
2. **Quality check**: `make lint test sec` trước commit
3. **Docker dev**: `make up` cho local stack
4. **CI automation**: GitHub Actions tự động chạy khi push

Mọi thay đổi security phải pass qua quality gates trước khi merge.
