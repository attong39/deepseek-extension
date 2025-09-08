# 🎯 Kế Hoạch Implement Core Module - Missing Functions

## 📊 Phân Tích Hiện Trạng

**714 issues** trong core module:
- **HIGH: 183** (stub functions cần implement ngay)
- **MEDIUM: 524** (type mismatches, return types)  
- **LOW: 7** (any types, minor issues)

### 🚨 Ưu Tiên 1: Critical Domain Ports (HIGH severity)

#### 1. ASR (Automatic Speech Recognition) Port
**File**: `zeta_vn/core/domain/ports/asr.py`
- ❌ `transcribe_audio()` - Core speech-to-text function
- ❌ `transcribe_streaming()` - Real-time streaming ASR
- ❌ `get_supported_languages()` - Language capability listing
- ❌ `detect_language()` - Auto language detection
- ❌ `reduce_noise()` - Audio preprocessing
- ❌ `get_confidence_score()` - Quality assessment

#### 2. External Services Port
**File**: `zeta_vn/core/domain/ports/external_services.py`
- ❌ `embed()` - Text embedding generation
- ❌ `chunk()` - Text chunking for RAG
- ❌ `upsert()` - Vector store operations
- ❌ `query()` - Similarity search

#### 3. Repository Patterns
**File**: `zeta_vn/core/domain/ports/repositories.py`
- ❌ `get()`, `try_get()`, `add()`, `remove()`, `list()`, `update()`
- Need comprehensive CRUD implementation

#### 4. Event Store & Unit of Work
**Files**: 
- `zeta_vn/core/domain/ports/event_store.py`
- `zeta_vn/core/domain/ports/unit_of_work.py`
- ❌ Event sourcing patterns
- ❌ Transaction boundaries

### 🎯 Ưu Tiên 2: Implementation Strategy

#### Phase 1: Core Infrastructure (Domain Ports)
1. **ASR Service Implementation** 
   - OpenAI Whisper adapter
   - Local model fallback
   - Streaming capabilities

2. **Vector/Embedding Services**
   - OpenAI Embeddings adapter
   - Pinecone/Chroma vector store
   - Text chunking utilities

3. **Repository Pattern Implementation**
   - SQLAlchemy concrete implementations
   - Event sourcing patterns
   - UnitOfWork with transaction support

#### Phase 2: Application Layer
1. **Event Bus System** 
   - `zeta_vn/core/application/event_bus.py`
   - ❌ `publish()`, `subscribe()` methods

2. **Async Templates**
   - `zeta_vn/core/async_templates/async_service.py`
   - ❌ `process_async()` method

#### Phase 3: Service Layer  
1. **Advanced Memory Service**
   - `zeta_vn/core/domain/services/advanced_memory.py`
   - ❌ `ingest_memory()`, `search_memories()`

2. **Self-Improvement Services**
   - `zeta_vn/core/self_improvement/auto_updater.py`
   - Auto-learning and adaptation

## 🛠️ Implementation Plan by Module

### Module 1: ASR Implementation
```python
# Target: zeta_vn/core/adapters/asr/
├── __init__.py
├── whisper_adapter.py      # OpenAI Whisper implementation
├── local_asr_adapter.py    # Local model fallback
├── noise_reducer.py        # Audio preprocessing
└── streaming_processor.py  # Real-time ASR
```

### Module 2: Vector/RAG Services
```python
# Target: zeta_vn/core/adapters/vector/
├── __init__.py
├── openai_embeddings.py    # OpenAI embedding service
├── chunking_service.py     # Text chunking utilities
├── pinecone_adapter.py     # Pinecone vector store
└── chroma_adapter.py       # Local vector store fallback
```

### Module 3: Repository Implementations
```python
# Target: zeta_vn/core/adapters/repositories/
├── __init__.py
├── sqlalchemy_base.py      # Base SQLAlchemy repository
├── agent_repository.py     # Agent domain repository
├── memory_repository.py    # Memory domain repository
├── chat_repository.py      # Chat domain repository
└── event_store_sql.py      # Event sourcing implementation
```

### Module 4: Event System
```python
# Target: zeta_vn/core/adapters/events/
├── __init__.py
├── memory_event_bus.py     # In-memory event bus
├── redis_event_bus.py      # Redis-backed event bus
└── domain_event_handler.py # Domain event processing
```

## 🔧 Implementation Guidelines

### 1. Clean Architecture Compliance
- **Domain**: Only interfaces/contracts (ports)
- **Adapters**: Concrete implementations of ports
- **Application**: Use cases orchestrating domain + adapters
- **Infrastructure**: Framework-specific implementations

### 2. Type Safety & Testing
- 100% type hints với mypy compliance
- Unit tests cho mỗi adapter implementation
- Integration tests cho end-to-end flows
- Mocks/stubs cho external dependencies

### 3. Error Handling
- Domain-specific exceptions
- Retry mechanisms với exponential backoff
- Graceful degradation cho external services
- Observability với logging/metrics

### 4. Performance Considerations
- Async/await throughout
- Connection pooling cho databases
- Caching layers cho expensive operations
- Batch processing cho bulk operations

## 📋 Next Actions

1. **Start with ASR Module** - Critical for voice features
2. **Implement Vector/RAG** - Core for memory/search
3. **Repository Pattern** - Foundation for all data access
4. **Event System** - Enables loose coupling
5. **Testing & Integration** - Ensure reliability

## 🎯 Success Criteria

- [ ] Zero HIGH severity stub functions
- [ ] All ports have working implementations
- [ ] Comprehensive test coverage (>90%)
- [ ] Performance benchmarks meet targets
- [ ] Clean architecture maintained
- [ ] Full type safety (mypy --strict passes)

---

**Bước tiếp theo**: Implement ASR module với OpenAI Whisper adapter đầu tiên.
