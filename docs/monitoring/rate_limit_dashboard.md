# Zeta Desktop Rate Limit Overview (Grafana)

File dashboard: `monitoring/grafana/dashboards/zeta_desktop_rate_limit_overview.json`

## Import dashboard

1. Mở Grafana → Dashboards → New → Import
2. Chọn Upload JSON và chọn file trên
3. Chọn Datasource Prometheus tương ứng (template variable `DS_PROMETHEUS`)
4. Save

## Metrics yêu cầu

- `http_rate_limited_total{service, path?}`: counter tăng khi client bị rate-limit
  - Interceptor FE đã phát sự kiện `http.rate_limited`; bạn cần gom và export thành Prometheus metric trên apps/backend/telemetry pipeline.

## Panels trong dashboard

- Rate-limited (per second) — 5m rate:
  - Query: `sum(rate(http_rate_limited_total[5m])) by (service)`
  - Mục đích: nhìn nhanh bottleneck theo service
- Top 5 endpoints bị rate-limit (5m):
  - Query: `topk(5, sum(rate(http_rate_limited_total[5m])) by (service, path))`
  - Mục đích: phát hiện endpoint cụ thể chịu áp lực lớn

## Tips

- Kết hợp tracing: dùng `traceparent`/`X-Request-ID` trong logs để drilldown theo request cụ thể.
- Nếu bạn dùng Loki/Grafana Stack, có thể tạo link từ panel sang log explorer bằng `${__value.labels.request_id}` (nếu thêm label này vào metric/log).
