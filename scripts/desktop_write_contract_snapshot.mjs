#!/usr/bin/env node
import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import { writeFileSync } from 'node:fs'
import http from 'node:http'
import { resolve } from 'node:path'

const API = process.env.CONTRACT_API_BASE || 'http://localhost:8000'

function sha256(buf) {
  return crypto.createHash('sha256').update(buf).digest('hex')
}

async function fetchOpenAPI() {
  return new Promise((resolveP, reject) => {
    http.get(`${API}/openapi.json`, (res) => {
      let data = ''
      res.on('data', (c) => (data += c))
      res.on('end', () => resolveP({ body: data, headers: res.headers }))
    }).on('error', reject)
  })
}

async function main() {
  const { body, headers } = await fetchOpenAPI()
  const openapiHash = sha256(body)

  const serverRoot = resolve(process.cwd(), '..')
  const venvPython = resolve(serverRoot, '.venv', 'Scripts', 'python.exe')
  const pyTry = spawnSync(venvPython, ['-c', 'print(1)'])
  const py = pyTry.status === 0 ? venvPython : 'python'
  const mod = resolve(serverRoot, 'zeta_vn', 'app', 'websockets', 'export_ws_schema.py')
  const out = spawnSync(py, [mod], { encoding: 'utf8' })
  if (out.status !== 0) {
    console.error('[write_contract_snapshot] export_ws_schema failed:', out.stderr || out.stdout)
    process.exit(1)
  }
  const wsHash = sha256(out.stdout)
  const wsProto = headers['x-ws-protocol'] || ''

  const snapPath = resolve(process.cwd(), 'scripts', '.contract_snapshot.json')
  const snap = { openapi: openapiHash, wsSchema: wsHash, wsProtocol: wsProto }
  writeFileSync(snapPath, JSON.stringify(snap, null, 2))
  console.log('[write_contract_snapshot] wrote', snapPath)
}

main().catch((e) => { console.error(e); process.exit(10) })
