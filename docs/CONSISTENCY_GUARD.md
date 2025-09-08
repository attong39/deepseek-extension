# 🛡️ Consistency Guard – Desktop ↔ AI Server

## Why?

- Backend contract (OpenAPI, WebSocket events, feature flags) changes frequently
- If frontend doesn't update accordingly, users encounter runtime errors
- Guard automatically scans, compares, and prevents CI merge when **critical** mismatches exist

## How It Works

1. **Load OpenAPI** – tries HTTP first, then local file, finally `app.openapi()`
2. **Backend scan** – collects API routes, WebSocket routes, WebSocket events, env-var names, computes short SHA-256 of OpenAPI (hash used as version constant on frontend)
3. **Frontend scan** – regex extracts:
   - `/api/v1/...` strings (calls)
   - WebSocket endpoint strings
   - Event names (`event:` or `type:`)
   - `import.meta.env.VITE_*` flags
4. **Compare** –  
   - `fail` if any required API/WebSocket-route/event missing on frontend
   - `warn` if extra items or flag mismatches (non-blocking)
5. **Report** – JSON + Markdown saved under `reports/consistency/`
6. **CI** – workflow aborts when `severity == fail`

## Sources

| Domain | Source |
|-------|--------|
| **OpenAPI** | `OPENAPI_URL` (env) → `/apps/backend/openapi.json` → `apps.backend.app.main:app.openapi()` |
| **WebSocket events** | `apps/backend/app/contracts/ws_events.json` |
| **API routes** | Extracted from OpenAPI `paths` |
| **WebSocket routes** | `@router.websocket("<path>")` in backend Python |
| **Feature flags** | `os.getenv("NAME")` / `Field(..., env="NAME")` (backend) ↔ `import.meta.env.VITE_*` (frontend) |
| **Frontend usage** | Regex over `*.ts` / `*.tsx` in `apps/desktop/src` |

## Usage

### Run Locally

```bash
# Install dependencies
pip install httpx pydantic

# Optional: Set OpenAPI URL if backend is running
# PowerShell:
$Env:OPENAPI_URL = "http://127.0.0.1:8000/openapi.json"

# Run Guard
python tools/consistency/run_all.py

# View results
cat reports/consistency/result.md
cat reports/consistency/result.json

# Check exit code (1 if fail)
python tools/consistency/run_all.py && echo "✅ ok" || echo "❌ fail"
```

### CI Integration

The GitHub Actions workflow (`.github/workflows/consistency-guard.yml`) runs on every push and PR:

- ✅ **Pass** (`severity: ok`) - All contracts synchronized
- ⚠️ **Warning** (`severity: warn`) - Non-critical drift, job passes but creates report
- ❌ **Fail** (`severity: fail`) - Critical mismatches, blocks CI

## Adding New Contracts

### API Endpoints
- **Backend**: Add path to FastAPI routers – auto-picked by OpenAPI
- **Frontend**: Use the endpoint in fetch/axios calls

### WebSocket Events
- **Backend**: Add event name to `apps/backend/app/contracts/ws_events.json`
- **Frontend**: Reference event in WebSocket message handlers

### Feature Flags
- **Backend**: Declare env var (e.g., `ENABLE_X = os.getenv("ENABLE_X")`)
- **Frontend**: Reference `import.meta.env.VITE_ENABLE_X`
- Guard automatically maps backend flags to `VITE_*` prefixed versions

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   OpenAPI Doc   │    │  WS Contract    │    │  Feature Flags  │
│   (HTTP/File)   │    │   (JSON file)   │    │  (env parsing)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Backend Scanner                               │
│  • Extract API routes from OpenAPI paths                       │
│  • Load WebSocket events from contract file                    │
│  • Parse feature flags from Python code                        │
│  • Generate OpenAPI hash for versioning                        │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Frontend Scanner                               │
│  • Regex scan *.ts/*.tsx files for API calls                   │
│  • Extract WebSocket endpoints and events                       │
│  • Find Vite environment variable usage                         │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Contract Comparer                             │
│  • Compare backend vs frontend usage                            │
│  • Determine severity (ok/warn/fail)                            │
│  • Generate detailed diff report                                │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Report Generator                             │
│  • JSON report (machine readable)                               │
│  • Markdown report (human readable)                             │
│  • CI integration with PR comments                              │
└─────────────────────────────────────────────────────────────────┘
```

## Severity Levels

### ❌ FAIL (Blocks CI)
- API routes missing in frontend
- WebSocket routes missing in frontend  
- WebSocket events missing in frontend

### ⚠️ WARN (Non-blocking)
- Extra API routes in frontend (unused)
- Extra WebSocket routes in frontend (unused)
- Extra WebSocket events in frontend (unused)
- Backend flags not used in frontend
- Frontend flags not defined in backend

### ✅ OK
- All contracts are synchronized

## FAQ

### Why regex instead of AST?
Regex is lightweight, runs in < 200ms across the whole repo, sufficient for contract names (`/api/v1/...`) and string literals. If project grows, replace with TypeScript compiler API.

### Can I suppress a warning?
Add a comment `// guard:ignore` next to the line. Guard will still count the item but CI treats the diff as `warn` (does not fail).

### What if OpenAPI changes without version bump?
Guard tracks `openapi_hash` and writes it into the report. Frontend should expose the same hash (e.g., `import.meta.env.VITE_OPENAPI_HASH`). When hash differs, CI will show a **warn**.

### How to handle dynamic API construction?
Guard includes patterns for:
- Template literals: `` `/api/v1/${id}` ``
- Dynamic construction: `"/api/v1/" + endpoint`
- Add `// guard:ignore` for complex cases

## Risks & Solutions

| Risk | Description | Solution |
|------|-------------|----------|
| **Regex false positives** | Dynamic endpoints not detected | Add ignore comments or extend regex patterns |
| **WebSocket contract drift** | `ws_events.json` not updated | Add pre-commit hook to auto-generate from backend enum |
| **Feature flag inconsistency** | Backend `ENABLE_X` ↔ Frontend `VITE_ENABLE_X` | Define conversion rules in `compare_contracts.py` |
| **OpenAPI hash drift** | Changes without frontend update | Add hash constant check to Guard |
| **Performance** | Scanning whole repo takes ~200ms | Cache frontend scan results in CI |

## Future Enhancements

1. **OpenAPI hash constant** in frontend (`src/constants/openapiHash.ts`) with Guard validation
2. **Auto-generate WebSocket contract** from backend enum → pre-commit hook
3. **Response schema comparison** - Pydantic/SQLModel ↔ Zod/IO-TS validation
4. **Auto-fix PRs** - Generate stub fetch calls for missing API endpoints
5. **UI integration** - Display OpenAPI version + Guard status in Desktop settings

## Files Structure

```
tools/
└─ consistency/
   ├─ __init__.py              # Package initialization
   ├─ utils.py                 # Utility functions (mask secrets)
   ├─ openapi_loader.py        # Load OpenAPI (HTTP → file → app)
   ├─ frontend_scanner.py      # Regex scan TypeScript files
   ├─ backend_scanner.py       # Extract backend contracts
   ├─ compare_contracts.py     # Compare and determine severity
   ├─ report.py                # Generate JSON/Markdown reports
   └─ run_all.py               # Main entry point

apps/
├─ backend/app/contracts/
│  └─ ws_events.json           # WebSocket events contract (source of truth)
└─ desktop/src/types/
   └─ ws.ts                    # TypeScript WebSocket event types

.github/workflows/
└─ consistency-guard.yml       # CI workflow

reports/consistency/           # Generated reports
├─ result.json                # Machine-readable results
└─ result.md                  # Human-readable report
```

---

**🎯 Result**: Enterprise-grade contract synchronization with automated CI gates and comprehensive reporting!