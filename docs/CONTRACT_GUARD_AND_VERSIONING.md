# Contract Guard & Versioning

Tài liệu tóm tắt cơ chế kiểm soát hợp đồng API/WS và versioning giữa Server và Desktop.

## Contract Guard (CI)

- Workflow: `.github/workflows/contract-guard.yml`.
- Quy trình:
  1. Generate OpenAPI types + WS schema snapshot từ server.
  2. Đồng bộ sang client (scripts đã có trong `desktop_ai_zeta/scripts/*`).
  3. So sánh với snapshot repo `desktop_ai_zeta/contracts/snapshot.json`.
  4. CI fail nếu có breaking (thiếu key) — dùng `contract_guard.mjs` nếu có, fallback `contract_guard_fallback.mjs`.
- Khi thay đổi hợp đồng có chủ ý: regenerate snapshot và commit snapshot trong cùng PR, mô tả rõ thay đổi và backward-compat.

## Versioning

- REST: middleware `ApiVersionHeaderMiddleware` thêm header `X-API-Version` (đọc từ env `API_VERSION`).
- WebSocket: message envelope `WSBase` có `version` và `corrId`.
- Client validate `version` trước khi xử lý, và gắn `corrId` để trace.

## Đường dẫn đầu mối

- OpenAPI spec (server): `docs/api/openapi.yaml` (nếu có) hoặc đường build export.
- WS schemas (server): `zeta_vn/app/websockets/schemas.py`.
- Scripts client: `desktop_ai_zeta/scripts/*.mjs`.

## Ghi chú

- Không commit secrets vào repo.
- Ưu tiên cập nhật snapshot và test trước khi merge vào nhánh chính.
