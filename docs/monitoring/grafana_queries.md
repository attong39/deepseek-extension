# Grafana & Monitoring Playbook

## Vietnamese quality tracking

Example SQL (Timescale/Postgres) to chart Vietnamese quality score by hour:

```sql
SELECT 
  time_bucket('1 hour', created_at) AS time,
  AVG(vietnamese_quality_score) AS quality_score
FROM user_feedback
WHERE language = 'vietnamese'
GROUP BY 1
ORDER BY 1;
```

## Complexity thresholds in auto-router

Example thresholds to route traffic based on prompt token estimates:

```ts
export const complexityThreshold = {
  low: 50,    // < 50 tokens -> defaultModel
  medium: 150, // 50-150 tokens -> highQualityModel
  high: 150    // > 150 tokens -> heavyModel
};
```

Tuning tips:
- Start conservative; monitor latency, cost, and quality feedback.
- Add hysteresis or smoothing to avoid flapping between models.
- Track per-route success/error rates and user satisfaction.

## Alerts reference

See `docs/monitoring/alertmanager/ollama_alerts.yml` for load, availability, and latency alerts aligned with apps/backend Prometheus metrics (`zeta_ollama_*`).

## Request distribution by model

Example SQL to monitor per-model request volume and latency distribution:

```sql
SELECT
  model,
  COUNT(*) AS request_count,
  AVG(duration_ms) AS avg_duration,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_ms) AS p95_duration
FROM ollama_requests
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY model
ORDER BY request_count DESC;
```
