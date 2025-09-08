# ⚡ Performance Guide - ZETA AI Server

Tune and scale ZETA AI Server for low latency and high throughput.

## 🔧 App Tuning

- Use async I/O, proper pooling for DB/Redis
- Configure uvicorn workers and thread limits
- Reuse HTTP sessions; connection pooling
- Cache hot data and model outputs

## 🗄 Database

- Index frequently queried fields
- Use EXPLAIN and analyze slow queries
- Batch operations and pagination

## 🧠 Models

- Choose right model; tune temperature and max_tokens
- Use streaming for long responses
- Trim context; summarize and store memories

## 📦 Infrastructure

- Horizontal scale API and workers
- Autoscaling triggers (CPU, latency, queue depth)
- CDN for static content

## 🔎 Observability

- Track p95 latency, error rate, queue time, token usage
- Profilers: py-spy, scalene
- Logging and sampling strategies

## 🧪 Load Testing

- k6/Locust scenarios
- RPS targets and breaking point

## 🔗 References

- API Reference: ./API_REFERENCE.md
- OpenAPI Spec: ./api/openapi.yaml
- TROUBLESHOOTING.md

Last updated: 2025-08-14
