# Run Web UI (Local)

This web template uses Vite (React + TypeScript) and proxies API/WS to FastAPI.

## Prereqs
- Node 18+ and pnpm
- Backend running on http://localhost:8000 (API + WS)

## Setup
```bash
cp web/.env.local.example web/.env.local
# If apps/backend runs on a different host/port, edit VITE_API_BASE and VITE_WS_URL
```

## Start Dev Server
```bash
bash scripts/run_web_local.sh
# or
cd web && pnpm i && pnpm dev
# open http://localhost:5173
```

## What the demo page does
- Calls GET /health to check API status
- Calls POST /api/v1/automation/execute with a minimal "UI plan" to trigger automation

## Headless vs interactive
- VITE_AI_UI_HEADLESS=true: headless (CI/server)
- VITE_AI_UI_HEADLESS=false: interactive; may require OS permissions
