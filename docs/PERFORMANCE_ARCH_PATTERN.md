# Performance Architecture Pattern

The following pattern reflects the desired high-level topology for the Zeta AI Server in production.

```
graph TB
    A[Load Balancer] --> B[API Gateway]
    B --> C[FastAPI Cluster]
    C --> D[Redis Cache Layer]
    C --> E[PostgreSQL Primary]
    C --> F[Vector DB Cluster]
    C --> G[Celery Workers]
```

Notes:
- Redis is used for request caching, rate limiting, and short-lived state.
- PostgreSQL is the source of truth; consider read replicas for heavy read workloads.
- Vector DB (e.g., pgvector, Qdrant, or Milvus) backs semantic search and RAG.
- Celery Workers handle long-running and asynchronous workloads.
- Use observability (metrics, traces, logs) across all nodes.
