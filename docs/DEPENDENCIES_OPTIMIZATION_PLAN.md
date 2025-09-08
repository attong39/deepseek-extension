# ZETA AI Dependencies Optimization Plan
# Kế hoạch tối ưu hóa dependencies

## Current Issues:
1. Heavy AI dependencies in main package
2. Circular imports
3. Unused dependencies
4. Security vulnerabilities

## Optimization Strategy:

### Phase 1: Dependency Audit
```bash
# Check for security issues
uv run pip-audit

# Find unused dependencies  
uv run python tools/find_unused_deps.py

# Check for circular imports
uv run python tools/analyze_imports.py
```

### Phase 2: Restructure Dependencies
```toml
# Optimized pyproject.toml structure
[project]
dependencies = [
  # Core only - lightweight
  "fastapi>=0.115.0,<1.0.0",
  "pydantic>=2.11.0,<3.0.0", 
  "sqlalchemy>=2.0.35,<3.0.0"
]

[project.optional-dependencies]
# Move heavy deps to extras
ai = ["openai", "transformers", "torch"]
cv = ["opencv-python", "easyocr"] 
vector = ["pinecone-client", "weaviate-client"]
```

### Phase 3: Import Optimization
```python
# Use lazy imports for heavy modules
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from transformers import AutoModel
    
def get_model():
    # Import only when needed
    from transformers import AutoModel
    return AutoModel.from_pretrained(...)
```

### Phase 4: Module Splitting
- Split large modules into smaller ones
- Use dependency injection
- Implement plugin architecture