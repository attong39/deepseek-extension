# ZETA_AI — CORE ROADMAP (Copilot-Ready)

Mục tiêu: Cho Copilot bối cảnh đầy đủ để *tìm–phân tích–đề xuất–triển khai* code trong `core/` theo Clean Architecture + DDD + One-Click Learning.

> Quy ước mỗi mục: **Mục đích • Public API • Phụ thuộc • Luồng dữ liệu • Lỗi/Retry • TODO (Copilot) • AC**.

---

## 0) Tổng quan thư mục `core/`
- **adapters**: tích hợp hệ ngoài (ASR/LLM/Vector/…).
- **application**: event bus, outbox, upcaster (orchestrate domain events).
- **domain**: entities/aggregates/events/value_objects/ports/services/specifications (thuần domain, **no I/O**).
- **services**: orchestration (RAG/Memory/ASR/Agent…).
- **security / observability / performance / outbox**: cross-cutting.
- **infrastructure**: DB models, UoW, repos SQL.
- **use_cases**: kịch bản nghiệp vụ dùng domain/services.

---

## 1) ADAPTERS — `core/adapters/*`

### 1.1 ASR — `core/adapters/asr/whisper_adapter.py`
- **Mục đích**: Kết nối Whisper (cloud/local) cho realtime + batch.
- **Public API**:
  - `transcribe(input: AudioInput, *, lang_hint: str|None = None) -> AsyncIterator[ASRChunk]`
  - `supports(model: str) -> bool`
  - `health_check() -> HealthStatus`
- **Phụ thuộc**: `domain/ports/asr.py` (ASRPort), vad/noise-reduction pipeline.
- **Luồng**: bytes/stream → VAD → chunk → decode → emit `ASRChunk(timecode, text, confidence)`.
- **Lỗi/Retry**: timeouts/429 → retry backoff + fallback `local_asr_adapter.py`.
- **TODO (Copilot)**:
  - Thêm **diarization tùy chọn** (speaker labels).
  - Adaptive VAD (+ năng lượng nền).
  - Streaming progress events qua WebSocket.
- **AC**:
  - Realtime < 300ms/chunk (p95), timecode chính xác ±40ms.
  - Unit test: streaming happy path + network error + fallback.
  - Test diarization với 2+ speakers.

### 1.2 ASR — `core/adapters/asr/local_asr_adapter.py`
- **Mục đích**: Fallback offline an toàn (CPU/GPU auto-select).
- **API tương thích** với WhisperAdapter.
- **TODO**: model cache + dynamic quantization + device auto-detection.
- **AC**: tốc độ ≥ 0.9x realtime với mẫu 5–10s; test CPU-only.

### 1.3 VECTOR — `core/adapters/vector/openai_embeddings.py`
- **Mục đích**: Tạo embedding chất lượng cao cho RAG/Memory.
- **Public API**: 
  - `embed_texts(texts: Sequence[str], *, model: str = "text-embedding-3-large") -> NDArray[float]`
  - `embed_query(query: str, *, model: str) -> NDArray[float]`
  - `get_dimension(model: str) -> int`
- **Phụ thuộc**: rate-limit + retry + redact logs, metrics hooks.
- **Luồng**: texts → batch → API call → normalize → return embeddings.
- **Lỗi/Retry**: 429/5xx → jitter backoff, circuit-breaker nhẹ.
- **TODO**: 
  - **fallback local embedding** (e.g., Instructor/E5) + **batch windowing**.
  - Caching layer cho expensive embeddings.
  - Cost tracking per request.
- **AC**: 
  - p95 latency ≤ 2000ms/1k tokens; 100% mypy OK; contract test qua `ports`.
  - Fallback test khi OpenAI unavailable.
  - No PII in logs verification.

### 1.4 VECTOR — `core/adapters/vector/chunking_service.py`
- **Mục đích**: Smart splitter (semantic/sentence/markdown) + overlap.
- **Public API**: 
  - `split(text: str, *, strategy: ChunkStrategy, overlap: int = 100) -> list[TextChunk]`
  - `estimate_chunks(text: str, strategy: ChunkStrategy) -> int`
- **Strategies**: semantic, sentence, markdown, code, hybrid.
- **TODO**: 
  - "table/figure anchor" rule + heuristics code-block.
  - Language-aware splitting.
  - Chunk quality scoring.
- **AC**: 
  - Recall@k tăng ≥ baseline 5% trên 20 docs mẫu.
  - Test với các loại content: code, markdown, PDF text.

### 1.5 VECTOR — `core/adapters/vector/memory_vector_store.py`
- **Mục đích**: VectorStore in-memory cho dev/test.
- **Public API**: 
  - `add(docs: list[Document]) -> list[str]`
  - `search(query: str | NDArray, k: int = 10) -> list[SearchResult]`
  - `delete(ids: list[str]) -> int`
  - `persist(path: Path | None = None) -> None`
- **Features**: cosine similarity, MMR re-ranking, metadata filtering.
- **AC**: 
  - CRUD test, deterministic results.
  - Performance: 1M vectors < 100ms search.
  - Persistence/restore test.

### 1.6 LLM — `core/adapters/llm/openai_adapter.py`
- **Mục đích**: Kết nối OpenAI GPT models cho completion + chat.
- **Public API**:
  - `complete(prompt: str, *, model: str, max_tokens: int) -> CompletionResult`
  - `chat(messages: list[Message], *, model: str) -> ChatResult`
  - `stream_chat(messages: list[Message]) -> AsyncIterator[ChatChunk]`
- **TODO**: 
  - Function calling support.
  - Vision model integration.
  - Cost tracking + budget limits.
- **AC**: 
  - Streaming < 50ms first token.
  - Function calls test.
  - Rate limit handling.

---

## 2) APPLICATION — `core/application/*`

### 2.1 `event_bus.py`
- **Mục đích**: Pub/Sub nội bộ (async) cho domain events.
- **Public API**: 
  - `subscribe(event_type: type[Event], handler: EventHandler) -> None`
  - `publish(event: Event) -> None`
  - `publish_batch(events: list[Event]) -> None`
- **Phụ thuộc**: asyncio queues, observability hooks.
- **Luồng**: publish → queue → async dispatch → handlers.
- **TODO**: 
  - ưu tiên (priority queue) + tracing span + bounded buffer.
  - Dead letter queue cho failed handlers.
  - Handler retry policies.
- **AC**: 
  - < 5ms/event nội bộ; backpressure không drop event.
  - Handler failure doesn't affect other handlers.
  - Observability: event counts, handler latency.

### 2.2 `outbox_hardened.py`
- **Mục đích**: Outbox pattern bền vững (idempotency, retry, DLQ).
- **Public API**:
  - `enqueue(event: DomainEvent) -> None`
  - `process_batch(limit: int = 100) -> ProcessResult`
  - `replay_dlq(since: datetime | None = None) -> int`
  - `get_metrics() -> OutboxMetrics`
- **Phụ thuộc**: `core/outbox/*` (idempotency, metrics, upcaster), UoW.
- **Luồng**: enqueue → persist → process → publish → mark processed.
- **Lỗi/Retry**: exponential backoff; poison message → DLQ.
- **TODO**: 
  - **exactly-once** bằng processed store + dedup key.
  - Monitoring dashboard integration.
  - Auto-scaling based on queue depth.
- **AC**: 
  - crash không mất event; contract test handlers.
  - DLQ replay success rate > 95%.
  - Processing latency p95 < 100ms.

### 2.3 `upcaster.py`
- **Mục đích**: Upcast event version cũ → schema mới.
- **Public API**:
  - `register_upcaster(from_version: int, to_version: int, fn: UpcasterFn) -> None`
  - `upcast_event(event: dict, target_version: int) -> dict`
- **TODO**: 
  - Version conflict detection.
  - Batch upcasting for performance.
- **AC**: 
  - coverage ≥ 90% trên map version → transformer functions.
  - No data loss during upcasting.

---

## 3) DOMAIN — `core/domain/*`

> Chuẩn: **no I/O**, bất biến ở Value Objects, Aggregate raise events.

### 3.1 Aggregates — `domain/aggregates/*`

#### 3.1.1 `agent_aggregate.py`
- **Mục đích**: Quản lý Agent lifecycle + domain events.
- **Public API**: 
  - `create_agent(spec: AgentSpec) -> Agent`
  - `update_configuration(config: AgentConfig) -> None`
  - `activate() -> None`
  - `deactivate() -> None`
  - `get_uncommitted_events() -> list[DomainEvent]`
- **Events**: AgentCreated, AgentConfigUpdated, AgentActivated, AgentDeactivated.
- **TODO**: 
  - Agent capability validation.
  - Performance metrics collection.
- **AC**: 
  - Event replay tái tạo đúng state.
  - Business rules enforcement (e.g., can't activate invalid agent).

#### 3.1.2 `chat_aggregate.py`
- **Mục đích**: Chat session state + message history.
- **Events**: ChatStarted, MessageAdded, ChatEnded.
- **TODO**: Message thread support, context window management.

#### 3.1.3 `memory_aggregate.py`
- **Mục đích**: Memory storage + retrieval logic.
- **Events**: MemoryStored, MemoryRetrieved, MemoryExpired.
- **TODO**: Memory importance scoring, automatic expiry.

### 3.2 Entities — `domain/entities/*`

#### 3.2.1 `agent.py`
- **Mục đích**: Core Agent entity với business logic.
- **Public API**:
  - `Agent(id: AgentId, spec: AgentSpec, config: AgentConfig)`
  - `can_process(request: Request) -> bool`
  - `estimate_cost(request: Request) -> Cost`
- **Invariants**: Valid spec, active config, non-negative costs.
- **AC**: 
  - Validation tests for all invariants.
  - Immutability tests.

#### 3.2.2 `chat.py`, `memory.py`, `user.py`
- **Mục đích**: Core entities cho chat, memory, user management.
- **AC**: Complete CRUD operations, validation, immutability.

### 3.3 Events — `domain/events/*`
- **Mục đích**: Domain event definitions với versioning.
- **Structure**: BaseEvent → specific events với typed data.
- **TODO**: 
  - Version pinning + migration paths.
  - Event sourcing support.
- **AC**: 
  - Schema stability tests.
  - Serialization round-trip tests.

### 3.4 Value Objects — `domain/value_objects/*`
- **Mục đích**: Immutable values (Identity/Permissions/Embedding…).
- **Examples**: AgentId, UserId, Embedding, Permission, Cost.
- **AC**: 
  - Hashable, equality correct.
  - Validation rules documented and tested.

### 3.5 Ports — `domain/ports/*`
- **Mục đích**: Interfaces for external dependencies.
- **Key Ports**:
  - `ASRPort`: Audio transcription interface.
  - `VectorStorePort`: Vector storage interface.
  - `LLMPort`: Language model interface.
  - `EventStorePort`: Event persistence interface.
- **TODO**: 
  - Contract testing framework.
  - Performance specifications.
- **AC**: 
  - All adapters implement port contracts.
  - Contract tests pass for all implementations.

### 3.6 Services — `domain/services/*`
- **Mục đích**: Pure domain logic services (no I/O).
- **Examples**:
  - `AgentScoringService`: Agent performance scoring.
  - `CostCalculationService`: Cost estimation logic.
  - `SecurityPolicyService`: Security rule evaluation.
- **AC**: 
  - Deterministic behavior.
  - Property-based tests where applicable.

### 3.7 Specifications — `domain/specifications/*`
- **Mục đích**: Business rules as composable specifications.
- **API**: `is_satisfied_by(candidate) -> bool`
- **Composability**: AND, OR, NOT operations.
- **AC**: 
  - Composition correctness tests.
  - No infrastructure dependencies.

---

## 4) SERVICES (orchestration) — `core/services/*`

> Trọng tâm **One-Click Learning**: ingest → chunk → embed → index → query; WS progress; budget/latency guard.

### 4.1 RAG Services

#### 4.1.1 `rag_service.py`
- **Mục đích**: Main RAG orchestration service.
- **Public API**:
  - `ingest(sources: list[Source], *, profile: RAGProfile = "optimized") -> IngestReport`
  - `query(request: QueryRequest) -> RAGResponse`
  - `get_progress(session_id: str) -> ProgressStatus`
- **Profiles**: simple, optimized, production.
- **TODO**:
  - Multi-modal support (text + images).
  - Adaptive chunking based on content type.
  - Cost optimization strategies.
- **AC**:
  - Recall@5/10 meets baseline targets.
  - p95 latency < 2s for queries.
  - Progress events accurate and timely.

#### 4.1.2 `retrieval_service.py`
- **Mục đích**: Advanced retrieval with re-ranking.
- **API**:
  - `retrieve(query: str, *, k: int, rerank: bool = True) -> list[RetrievalResult]`
  - `hybrid_search(query: str, filters: dict) -> list[RetrievalResult]`
- **Features**: Semantic + keyword search, MMR re-ranking.

#### 4.1.3 `rag_chunker.py`, `chunking.py`
- **Mục đích**: Document chunking strategies.
- **Strategies**: Fixed-size, semantic, recursive, adaptive.

#### 4.1.4 `rag_budgeter.py`
- **Mục đích**: Cost and latency budget management.
- **API**:
  - `check_budget(operation: Operation) -> BudgetStatus`
  - `track_usage(operation: Operation, cost: Cost) -> None`

### 4.2 Memory Services

#### 4.2.1 `memory_service.py`
- **Mục đích**: Memory storage and retrieval orchestration.
- **API**:
  - `store(content: str, *, metadata: dict) -> MemoryId`
  - `retrieve(query: str, *, limit: int = 10) -> list[Memory]`
  - `update(memory_id: MemoryId, content: str) -> None`
  - `delete(memory_id: MemoryId) -> None`
- **Features**: Semantic search, importance scoring, auto-expiry.

#### 4.2.2 `semantic_memory.py`
- **Mục đích**: Semantic memory implementation.
- **TODO**: 
  - Memory consolidation algorithms.
  - Forgetting curves implementation.

#### 4.2.3 `memory_manager_service.py`
- **Mục đích**: Memory lifecycle management.
- **Features**: GC, compression, backup/restore.

### 4.3 ASR Services

#### 4.3.1 `asr_service.py`
- **Mục đích**: Audio transcription orchestration.
- **API**:
  - `transcribe_file(file_path: Path) -> TranscriptionResult`
  - `transcribe_stream(audio_stream: AsyncIterator[bytes]) -> AsyncIterator[TranscriptionChunk]`
  - `start_realtime_session() -> RealtimeSession`
- **Features**: Multi-language, speaker diarization, confidence scoring.

### 4.4 Agent Services

#### 4.4.1 `agent_service.py`
- **Mục đích**: Agent lifecycle and execution.
- **API**:
  - `create_agent(spec: AgentSpec) -> AgentId`
  - `execute_task(agent_id: AgentId, task: Task) -> TaskResult`
  - `get_agent_status(agent_id: AgentId) -> AgentStatus`

#### 4.4.2 `agent_orchestrator_service.py`
- **Mục đích**: Multi-agent coordination.
- **Features**: Task routing, load balancing, conflict resolution.

### 4.5 Chat Services

#### 4.5.1 `chat_service.py`
- **Mục đích**: Chat session management.
- **API**:
  - `start_chat(user_id: UserId, agent_id: AgentId) -> ChatId`
  - `send_message(chat_id: ChatId, message: str) -> ChatResponse`
  - `get_history(chat_id: ChatId) -> list[Message]`

---

## 5) OUTBOX — `core/outbox/*`
- **Mục đích**: Dedicated outbox pattern implementation.
- **Components**:
  - `handlers/`: Event handlers.
  - `idempotency/`: Duplicate detection.
  - `metrics/`: Performance tracking.
  - `upcaster/`: Event migration.
- **API**: 
  - Processed-store (Redis/DB).
  - DLQ replay CLI.
  - Metrics hooks.
- **AC**: 
  - DLQ dashboard available.
  - No duplicate processing.
  - Monitoring alerts configured.

---

## 6) SECURITY — `core/security/*`
- **Mục đích**: Security policies and enforcement.
- **Components**:
  - Permission management.
  - Content safety filtering.
  - Audit logging.
  - OPA integration.
- **TODO**: 
  - Context-aware redaction.
  - Prompt injection detection.
  - Real-time threat monitoring.
- **AC**: 
  - Zero HIGH findings in bandit.
  - 100% PII field masking.
  - Policy violations fail-fast.

---

## 7) OBSERVABILITY — `core/observability/*`
- **Mục đích**: Monitoring, logging, tracing.
- **Components**:
  - `metrics.py`: Prometheus metrics.
  - `tracing.py`: OpenTelemetry tracing.
  - `logging.py`: Structured logging.
- **API**:
  - `track_latency(operation: str) -> ContextManager`
  - `increment_counter(metric: str, tags: dict) -> None`
  - `start_span(name: str) -> Span`
- **AC**: 
  - SLO dashboard shows p95 latencies.
  - Error budgets tracked daily.
  - Trace coverage > 80%.

---

## 8) INFRASTRUCTURE — `core/infrastructure/*`
- **Mục đích**: Database models, UoW pattern, repository implementations.
- **Components**:
  - SQLAlchemy models.
  - Unit of Work implementation.
  - Repository base classes.
- **TODO**: 
  - Deadlock retry logic.
  - N+1 query detection.
  - Connection pooling optimization.
- **AC**: 
  - Transaction rollback tests pass.
  - Performance baseline established.
  - Connection leaks prevented.

---

## 9) USE CASES — `core/use_cases/*`
- **Mục đích**: High-level business scenarios.
- **Examples**:
  - `ChatFlowUseCase`: Complete chat interaction.
  - `MemoryOperationsUseCase`: Memory CRUD operations.
  - `AgentExecutionUseCase`: Agent task execution.
- **Features**: 
  - WebSocket progress events.
  - Policy enforcement.
  - Error handling.
- **AC**: 
  - End-to-end tests for main flows.
  - Policy violations properly handled.
  - Progress events accurate.

---

## 10) Performance & Quality

### 10.1 PERFORMANCE — `core/performance/*`
- **Mục đích**: Performance monitoring and optimization.
- **Features**: 
  - Benchmark suites.
  - Performance regression detection.
  - Resource usage tracking.

### 10.2 QUALITY — `core/quality/*`
- **Features**: 
  - Code quality metrics.
  - Technical debt tracking.
  - Automated refactoring suggestions.

---

## 11) Prompt Templates cho Copilot

### 11.1 Implementation Task
```
@copilot/task
Context: Clean Architecture + DDD; no I/O inside Domain; adapters follow ports; WS progress events.
Goal: Implement retry+idempotency for core/application/outbox_hardened.py with DLQ + metrics hooks.
Constraints: Type-safe, Pydantic v2 schemas, mypy OK, tests (happy path + poison message).
Return: patch + tests under tests/core/application/outbox/.
```

### 11.2 Refactoring Task
```
@copilot/refactor
Context: RAG pipeline; chunking strategies; adapters/vector/openai_embeddings.py.
Goal: Add local embedding fallback with batch windowing + jitter backoff on 429. Ensure logs redacted.
AC: p95 latency budget, tests for fallback path, ruff/mypy/pytest pass.
```

### 11.3 Feature Enhancement
```
@copilot/enhance
Context: Memory service with semantic search; core/services/memory_service.py.
Goal: Add memory consolidation algorithm that merges similar memories.
Constraints: Preserve semantic meaning, configurable similarity threshold, background processing.
AC: Memory count reduced by 20%+, retrieval quality maintained, performance tests pass.
```

---

## 12) Checklist khi thêm/sửa file
- [ ] Docstring module + Public API rõ (input/output, exceptions)
- [ ] Type hints 100% (`from __future__ import annotations`)
- [ ] Không log secret/PII; redaction hợp lệ
- [ ] Retry/backoff + metrics/tracing hooks nơi gọi IO
- [ ] Tests: happy/error/edge; property-based nếu hợp lý
- [ ] Performance benchmarks cho critical paths
- [ ] Security review cho external interfaces
- [ ] Documentation update cho API changes
- [ ] Cập nhật ROADMAP nếu đổi Public API

---

## 13) Acceptance Criteria Templates

### 13.1 API Service AC
```yaml
performance:
  p95_latency: "< 2000ms"
  throughput: "> 100 req/s"
  availability: "> 99.9%"

quality:
  test_coverage: "> 90%"
  type_safety: "100% mypy pass"
  security: "0 HIGH bandit issues"

functionality:
  happy_path: "✓ Core use cases work"
  error_handling: "✓ Graceful degradation"
  monitoring: "✓ Metrics + alerts configured"
```

### 13.2 Domain Model AC
```yaml
correctness:
  invariants: "✓ All business rules enforced"
  immutability: "✓ Value objects immutable"
  events: "✓ Proper event emission"

testing:
  unit_tests: "> 95% coverage"
  property_tests: "✓ Where applicable"
  example_based: "✓ Edge cases covered"

documentation:
  business_rules: "✓ Clearly documented"
  examples: "✓ Usage examples provided"
  constraints: "✓ Limitations explained"
```

---

## 14) Assumptions (nếu thiếu chi tiết)
- Helper files (`__init__.py` minimal) không cần mô tả riêng.
- Performance budgets (ms/token) sẽ được cập nhật sau benchmark.
- Security policies sẽ được định nghĩa cụ thể theo compliance requirements.
- Monitoring thresholds sẽ được điều chỉnh dựa trên production data.

---

## 15) Integration Points

### 15.1 External Systems
- **OpenAI API**: Rate limiting, cost tracking, fallback strategies.
- **Vector Databases**: Pinecone, Weaviate, Qdrant integration.
- **Message Queues**: Redis, RabbitMQ, Kafka for event streaming.
- **Monitoring**: Prometheus, Grafana, Jaeger integration.

### 15.2 Internal Dependencies
- **Database**: PostgreSQL with async SQLAlchemy.
- **Cache**: Redis for session state and caching.
- **File Storage**: S3-compatible storage for documents.
- **Config**: Environment-based configuration management.

---

## 16) Migration Strategy
- **Phase 1**: Core domain models + basic services.
- **Phase 2**: Advanced features + performance optimization.
- **Phase 3**: Production hardening + monitoring.
- **Phase 4**: AI/ML feature enhancement.

---

## 17) Success Metrics
- **Development Velocity**: Features delivered per sprint.
- **Quality**: Bug rate, test coverage, performance regressions.
- **Reliability**: Uptime, error rates, recovery time.
- **Performance**: Latency, throughput, resource utilization.
- **Security**: Vulnerability count, audit findings, compliance score.
