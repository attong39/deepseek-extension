# Hợp đồng Server–Desktop: Danh mục đồng bộ và kiểm tra

Tài liệu này liệt kê các hợp đồng cần đồng bộ giữa `zeta_vn` (FastAPI server) và `desktop_ai_zeta` (Electron + Vite + TS), kèm theo vị trí mã nguồn và script kiểm tra tự động.

## 1) API Endpoints (REST)

- Nguồn Desktop: `desktop_ai_zeta/src/constants/index.ts` (object `API`)
- Nguồn Server: OpenAPI sinh từ `zeta_vn/app/main.py` + routers `zeta_vn/app/api/v1/*`
- Kiểm tra: `python tools/consistency/openapi_consistency.py --openapi-url http://127.0.0.1:8000/openapi.json`
- Kỳ vọng: Mọi path `/api/v1/<endpoint>` trong OpenAPI phải bao trùm các path Desktop tham chiếu (thêm prefix `/api/v1`).

## 2) WebSocket Events

- Nguồn Server: `zeta_vn/app/websockets/schemas.py` (Pydantic models + `type: Literal[...]`)
- Nguồn Desktop: `desktop_ai_zeta/src/services/wsSchema.ts` (AJV validators)
- Kiểm tra: `python tools/consistency/ws_events_consistency.py`
- Kỳ vọng: Tập `type` sự kiện trùng nhau; tập trường required từng event khớp.

## 3) Xử lý Token & Header

- Desktop: `src/api/generated/client.ts`, `src/services/session.ts`, `src/services/auth.ts`
- Server: `app/auth/security_middleware.py`, `app/middleware/auth_middleware.py`
- Kiểm tra thủ công: Đảm bảo `Authorization: Bearer <token>` được thêm vào axios interceptor và server cho phép whitelist `/openapi.json`, `/docs*` khi cần.

## 4) Mã lỗi & Mapping

- Server: `core/exceptions/*`, `app/exceptions/*`, các nơi raise `HTTPException`
- Desktop: `src/services/feedbackProcessor.ts` (ví dụ mapping 403 -> forbidden)
- Khuyến nghị: Chuẩn hóa danh mục `error_code` và viết mapping TS tập trung.

## 5) Giới hạn tỉ lệ (Rate limiting)

- Server: `app/middleware/rate_limiting.py`
- Desktop: `src/utils/rateLimiter.ts`
- Kiểm tra: đảm bảo thông số client-side tương thích UX với limit server (ví dụ capacity/interval).

## 6) i18n Keys

- Desktop: `src/i18n/*.json`
- Kiểm tra: `python tools/consistency/i18n_consistency.py` (so sánh key set các ngôn ngữ)

## 7) Biến môi trường

- Desktop: `.env*` (`VITE_API_BASE_URL`, `VITE_WS_URL`, `VITE_I18N_DEFAULT_LANG`, ...)
- Server: `.env*` (`ENABLE_DOCS`, `CORS_ORIGINS`, `JWT_SECRET`, ...)
- Kiểm tra: `python tools/consistency/env_consistency.py`

## 8) Logging & Observability

- Server: `app/observability/*`, `config/logging.py`
- Desktop: `src/services/telemetry.ts` (client logs, optional)
- Thống nhất: format, correlation id (`X-Request-ID`).

## 9) Versioning

- Server version: `app/main.py` (field `version`), `config/models.py`
- Desktop hiển thị: UI `About`, logic cập nhật.

## 10) Checklist mở rộng

- DTO/Schema: bám theo OpenAPI types generated (`desktop_ai_zeta/scripts/openapi...`)
- Files Upload/Download: endpoints `FILES_*` vs server `/api/v1/files*`
- Training WS: Desktop `TrainingSocket` vs server `app/websockets/training_ws.py`

---

## Cách chạy nhanh bộ kiểm tra

- Server đang chạy tại `http://127.0.0.1:8000`:

```powershell
python tools/consistency/run_all.py
```

- Hoặc chỉ chạy kiểm tra OpenAPI với file đã export:

```powershell
python tools/consistency/openapi_consistency.py --openapi-file zeta_vn/reports/openapi.json
```

Kết quả JSON sẽ nằm trong `reports/*.json`.
