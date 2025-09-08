Running cache tests

Requirements:

- Node 18+
- `npm ci` inside `desktop_ai_zeta`
- `ts-node` or `node` with compiled JS

Quick run (dev):

1. cd into `desktop_ai_zeta`
2. npm ci
3. npx ts-node tests/test_cache.ts

If TypeScript complains about Node types, install dev types: `npm i -D @types/node`.
