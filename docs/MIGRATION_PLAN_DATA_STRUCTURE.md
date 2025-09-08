# Data Structure Migration Plan

## Mục tiêu

Chuẩn hóa cấu trúc `zeta_vn/data` để:

- Loại bỏ trùng lặp giữa `clients/` và `external/`
- Separation of concerns rõ ràng
- Naming convention nhất quán
- Easier maintenance và testing

## Phase 1: Consolidate Clients (1-2 days)

### Step 1.1: Move & Rename LLM Clients

```bash
# Move all LLM clients to clients/llm/
mv zeta_vn/data/external/openai_client.py zeta_vn/data/clients/llm/
mv zeta_vn/data/external/anthropic_client.py zeta_vn/data/clients/llm/
mv zeta_vn/data/external/llm/gemini_client.py zeta_vn/data/clients/llm/
mv zeta_vn/data/external/llm/enhanced_openai_client.py zeta_vn/data/clients/llm/

# Rename for consistency  
mv zeta_vn/data/clients/openai_adapter.py zeta_vn/data/clients/llm/openai_client.py
```

### Step 1.2: Move Storage Clients

```bash
mkdir -p zeta_vn/data/clients/storage
mv zeta_vn/data/external/s3_client.py zeta_vn/data/clients/storage/
mv zeta_vn/data/external/gcp_client.py zeta_vn/data/clients/storage/gcs_client.py
mv zeta_vn/data/clients/s3_blob_adapter.py zeta_vn/data/clients/storage/s3_client.py
```

### Step 1.3: Move Database Clients

```bash
mkdir -p zeta_vn/data/clients/database
mv zeta_vn/data/external/postgres_client.py zeta_vn/data/clients/database/
mv zeta_vn/data/external/redis_client.py zeta_vn/data/clients/database/
mv zeta_vn/data/external/database_client.py zeta_vn/data/clients/database/
```

### Step 1.4: Move Search Clients

```bash
mkdir -p zeta_vn/data/clients/search
mv zeta_vn/data/external/elasticsearch_client.py zeta_vn/data/clients/search/
mv zeta_vn/data/external/pinecone_client.py zeta_vn/data/clients/search/
mv zeta_vn/data/clients/vector_store_client.py zeta_vn/data/clients/search/
```

## Phase 2: Organize Adapters (1 day)

### Step 2.1: Create Specialized Adapters

```bash
# Create adapters từ external/*_adapters.py
mv zeta_vn/data/external/advanced_alerts_adapters.py zeta_vn/data/adapters/monitoring_adapters.py
mv zeta_vn/data/external/backup_adapters.py zeta_vn/data/adapters/storage_adapters.py  
mv zeta_vn/data/external/documentation_adapters.py zeta_vn/data/adapters/content_adapters.py
mv zeta_vn/data/external/feature_toggle_adapters.py zeta_vn/data/adapters/config_adapters.py
mv zeta_vn/data/external/observability_adapters.py zeta_vn/data/adapters/monitoring_adapters.py
```

### Step 2.2: Consolidate Business Logic Adapters

```python
# Tạo file zeta_vn/data/adapters/llm_adapters.py tích hợp:
# - OpenAI, Anthropic, Gemini adapters
# - Retry logic, fallbacks
# - Model routing integration

# Tạo file zeta_vn/data/adapters/storage_adapters.py tích hợp:
# - S3, GCS, local storage
# - File upload/download logic
# - Metadata handling
```

## Phase 3: Update Imports & Barrels (0.5 day)

### Step 3.1: Update __init__.py Files

```python
# zeta_vn/data/clients/__init__.py
from . import llm, storage, database, search, monitoring

# zeta_vn/data/adapters/__init__.py  
from . import llm_adapters, storage_adapters, monitoring_adapters

# zeta_vn/data/__init__.py
from . import clients, adapters, repositories, dto, utils
```

### Step 3.2: Fix Import References

```bash
# Run trong toàn bộ codebase để update imports
grep -r "from zeta_vn.data.external" . --include="*.py" | \
  sed 's/external/clients/' > import_fixes.txt

# Apply systematically
```

## Phase 4: Testing & Validation (0.5 day)

### Step 4.1: Run Quality Gates

```bash
uv run ruff check .
uv run mypy .
uv run pytest tests/
```

### Step 4.2: Integration Tests

```bash
# Test key integration points
uv run pytest tests/data/ -v
```

## File Mapping Reference

| Current Location | New Location | Action |
|-----------------|--------------|--------|
| `external/openai_client.py` | `clients/llm/openai_client.py` | move + rename |
| `external/anthropic_client.py` | `clients/llm/anthropic_client.py` | move |
| `external/llm/gemini_client.py` | `clients/llm/gemini_client.py` | move |
| `external/s3_client.py` | `clients/storage/s3_client.py` | move |
| `external/postgres_client.py` | `clients/database/postgres_client.py` | move |
| `external/elasticsearch_client.py` | `clients/search/elasticsearch_client.py` | move |
| `external/*_adapters.py` | `adapters/*.py` | consolidate |
| `clients/openai_adapter.py` | `clients/llm/openai_client.py` | merge/rename |

## Benefits

- ✅ __Clear separation__: clients (raw) vs adapters (business logic)
- ✅ __No duplication__: Single source of truth per service
- ✅ __Easy maintenance__: Grouped by capability
- ✅ __Better testing__: Isolated responsibilities
- ✅ __Consistent naming__: `*_client.py` for raw clients, `*_adapters.py` for business logic

## Risks & Mitigation

- __Import breaks__: Comprehensive search/replace + testing
- __Circular deps__: Clear layer boundaries (clients → adapters → services)
- __Missing files__: Use git mv để preserve history
