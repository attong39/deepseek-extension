# 🚀 Đề Xuất Nhất Quán Dự Án ZETA AI Agent

Tài liệu này tổng hợp và chuẩn hóa các tiêu chuẩn/code conventions, quy trình, và chất lượng cho monorepo ZETA (apps/backend, extension, apps/desktop), nhằm đảm bảo tính nhất quán, dễ mở rộng, và chất lượng cao.

## 🎯 1. Tiêu Chuẩn Phát Triển

- TypeScript
  - Bật strict mode; sử dụng ESLint + Prettier; base tsconfig ở root, các package kế thừa.
  - Import từ `shared` (nếu có) để tránh trùng lặp type/model.
- Python
  - PEP8; type hints cho mọi function; định dạng Black; lint Ruff; mypy tối thiểu cho core modules.
- PowerShell
  - Tương thích Windows PowerShell 5.1; comment-based help; không hardcode secrets; set-exitcode đúng.

### 1.2 Cấu Trúc Thư Mục Chuẩn (đề xuất)

```
apps/zeta-ai-agent/
├─ src/                  # Source chính (Python/TS theo module)
├─ packages/             # Các packages độc lập (TS/Node)
├─ scripts/              # PowerShell & tiện ích CLI
├─ config/               # Cấu hình (YAML/JSON/env)
├─ docs/                 # Tài liệu (docs-as-code)
├─ tests/                # Unit/Integration/Perf
└─ .github/              # Workflows, templates, CODEOWNERS
```

Lưu ý: Repo hiện có các thư mục `apps/backend/`, `apps/desktop/`, `extension/`, `apps/zeta-ai-agent/`, `packages/ollama/`, v.v. Các tiêu chuẩn trong tài liệu này áp dụng xuyên suốt, không yêu cầu di chuyển cấu trúc ngay lập tức.

## 🔧 2. Quy Trình Development

- Branch Strategy
  - `main`: production-ready
  - `develop`: integration
  - `feature/*`: phát triển tính năng
  - `hotfix/*`: sửa lỗi khẩn
- Commit Convention (Conventional Commits)
  - `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Code Review
  - Tối thiểu 1 reviewer; checklist; CI bắt buộc pass.

## 🧪 3. Quality Assurance

- Testing
  - Unit: ≥80% coverage (mục tiêu); Integration: E2E các workflow chính; Perf: stress weekly.
- Security & Dependency Scans
  - Quét định kỳ; SBOM (nếu khả dụng); pin phiên bản quan trọng.
- Monitoring
  - Prometheus metrics; Grafana dashboards provisioning; alerting cho sự cố critical.

## 🚀 4. Deployment & Operations

- Environments (profiles trong docker-compose)
  - development: Ollama local + basic monitoring
  - staging: preloaded models + full monitoring + perf testing
  - production: HA + advanced monitoring + automated backups
- CI/CD Pipeline (khung)
  - Lint & Build → Unit → Integration → Security Scan → Deploy Staging → Stress Test → Deploy Production

## 📊 5. Documentation Standards

- Bắt buộc: OpenAPI/Swagger, C4 diagrams, runbooks, troubleshooting.
- Docs-as-code: theo dõi version; auto-update từ code comments khi hợp lý.

## 🔐 6. Security Standards

- Yêu cầu: audits định kỳ; dependency scans; secrets quản lý bởi Vault/AWS Secrets Manager; network isolation.
- Compliance: OWASP Top 10; GDPR (nếu áp dụng); pen testing định kỳ.

## 📈 7. Performance Standards

- Mục tiêu: Latency < 3s (VN queries); Availability 99.9%; Throughput ≥100 RPS.
- Scaling: horizontal cho stateless; tối ưu GPU cho inference; DB pooling.

## 👥 8. Team Collaboration

- Giao tiếp: daily standups; weekly architecture review; bi-weekly sprint planning.
- Chia sẻ tri thức: tech talks; pair programming; docs chung.

## 🎯 9. Success Metrics

- Kỹ thuật: ESLint warnings, coverage, latency, error rates, uptime, MTTR.
- Kinh doanh: active users, session duration, NPS, cost/request, utilization.

## 🔄 10. Continuous Improvement

- Retrospective hàng tháng; item cải tiến đo lường được; 20% thời gian innovation.

---

## 📋 Lộ Trình Triển Khai (Tóm tắt)

- Phase 1: Nền tảng (Tuần 1–2)
  - Chuẩn hóa môi trường dev; thiết lập lint/test tự động; tiêu chuẩn tài liệu.
- Phase 2: Tự động hóa (Tuần 3–4)
  - Hoàn thiện CI/CD; monitoring & alerting; security scanning.
- Phase 3: Tối ưu (Tuần 5–6)
  - Benchmarking hiệu năng; tối ưu chi phí; chuẩn bị scaling.

## ✅ Acceptance Criteria (nhanh)

- CI lint/test chạy cho `apps/backend`, `extension`, `apps/desktop` (không phá vỡ pipeline hiện có).
- Có checklist PR; tài liệu standards được commit trong `docs/`.
- Báo cáo coverage tối thiểu có mặt (mức mục tiêu 80% theo lộ trình).

## 🔗 Mapping nhanh vào repo hiện tại

- Backend Python: `apps/backend/pyproject.toml` đã có Black/Ruff/Mypy – dùng làm chuẩn.
- TypeScript: `apps/desktop/`, `extension/`, `packages/ollama/`, `apps/zeta-ai-agent/` đã có tsconfig/eslint – hợp nhất dần.
- Workflows: `.github/workflows/` đã hiện diện ở nhiều thư mục – thêm workflow tổng ở root để kiểm tra nhất quán.
