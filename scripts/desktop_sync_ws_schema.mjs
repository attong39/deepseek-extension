#!/usr/bin/env node
import { spawnSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'

// Run server-side exporter using the local venv python if available; fallback to `python`
const serverRoot = resolve(process.cwd(), '..')
const venvPython = resolve(serverRoot, '.venv', 'Scripts', 'python.exe')
const py = spawnSync(venvPython, ['-c', 'import sys; print("ok")'])
const pythonExe = py.status === 0 ? venvPython : 'python'

const modulePath = resolve(serverRoot, 'zeta_vn', 'app', 'websockets', 'export_ws_schema.py')
const run = spawnSync(pythonExe, [modulePath], { encoding: 'utf8' })
if (run.status !== 0) {
  console.error('[sync_ws_schema] failed to export from server:', run.stderr || run.stdout)
  process.exit(run.status || 1)
}

const outJson = run.stdout
const outTsPath = resolve(process.cwd(), 'src', 'services', 'wsSchema.ts')
const contractsDir = resolve(process.cwd(), '..', 'contracts')
const outJsonPath = resolve(contractsDir, 'ws.schemas.json')
mkdirSync(dirname(outTsPath), { recursive: true })

const header = `// AUTO-GENERATED. Do not edit.
// Generated from server websocket schemas via scripts/sync_ws_schema.mjs
/* eslint-disable */
`;
const body = `export const WS_SCHEMAS = ${outJson} as const;
export type WSEventType = keyof typeof WS_SCHEMAS;
`;
writeFileSync(outTsPath, header + body)
console.log('[sync_ws_schema] wrote', outTsPath)
try {
  mkdirSync(contractsDir, { recursive: true })
  writeFileSync(outJsonPath, outJson)
  console.log('[sync_ws_schema] wrote', outJsonPath)
} catch {}
