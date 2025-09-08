# 🎯 COPILOT RULES - ZETA AI SERVER

## Nguyên tắc Guardrails

- **Trước khi code**: đọc toàn bộ repo, tóm tắt cấu trúc và import graph.
- **Không tạo file trùng tên** module package. Nếu thay thế, xóa file cũ và cập nhật `__init__.py`.
- **Sau mỗi patch**: chạy `ruff`, `mypy --strict`, `pytest`. Nếu fail, tự sửa đến khi pass.
- **Tôn trọng public API** đã export. Không đổi signature nếu không cập nhật toàn bộ callsites.
- **Tuân thủ style**: typing đầy đủ, docstring Google, không side-effects tại module import.

## Quality Gates

- **Type hints 100%**: mypy --strict pass
- **Lint clean**: ruff check pass
- **Tests pass**: pytest coverage ≥ 80%
- **Security**: bandit, pip-audit warnings addressed
- **Architecture**: Clean Architecture boundaries respected

## Deployment Safety

- **Feature flags**: rollout an toàn cho tính năng mới
- **Blue-green**: zero-downtime deployments
- **Observability**: metrics/traces/logs trước khi optimize
- **Least privilege**: JWT scopes, RBAC chặt chẽ
- **Idempotent**: scripts có thể chạy nhiều lần an toàn

## Code Style

- **Imports**: `from __future__ import annotations` đầu file
- **Async/await**: ưu tiên async cho I/O operations
- **Error handling**: specific exceptions, không bắt `Exception` trống
- **Logging**: structured logging, không `print()`
- **Config**: đọc từ environment, không hardcode

## Architecture Compliance

- **Core**: domain logic thuần, không import app/data
- **App**: FastAPI routers, middleware, serializers
- **Data**: repositories, external clients, migrations
- **Config**: settings, feature flags, dependencies
