#!/usr/bin/env node
import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import { readFileSync } from 'node:fs'
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
  console.log('OpenAPI sha256:', openapiHash)

  // Export server WS schemas via Python
  const serverRoot = resolve(process.cwd(), '..')
  const venvPython = resolve(serverRoot, '.venv', 'Scripts', 'python.exe')
  const pyTry = spawnSync(venvPython, ['-c', 'print(1)'])
  const py = pyTry.status === 0 ? venvPython : 'python'
  const mod = resolve(serverRoot, 'zeta_vn', 'app', 'websockets', 'export_ws_schema.py')
  const out = spawnSync(py, [mod], { encoding: 'utf8' })
  if (out.status !== 0) {
    console.error('[contract-guard] export_ws_schema failed:', out.stderr || out.stdout)
    process.exit(1)
  }
  const wsSchemasJson = out.stdout
  const wsHash = sha256(wsSchemasJson)
  console.log('WS Schemas sha256:', wsHash)

  // X-WS-Protocol header optional check
  const wsProto = headers['x-ws-protocol'] || ''
  console.log('X-WS-Protocol:', wsProto)

  // Load client snapshot if exists
  const snapPath = resolve(process.cwd(), 'scripts', '.contract_snapshot.json')
  let snap = null
  try { snap = JSON.parse(readFileSync(snapPath, 'utf8')) } catch {}

  if (snap) {
    if (snap.openapi !== openapiHash) {
      console.error('[contract-guard] OpenAPI hash mismatch! expected:', snap.openapi)
      process.exit(2)
    }
    if (snap.wsSchema !== wsHash) {
      console.error('[contract-guard] WS schema hash mismatch! expected:', snap.wsSchema)
      process.exit(3)
    }
    if (snap.wsProtocol && wsProto && snap.wsProtocol !== wsProto) {
      console.error('[contract-guard] X-WS-Protocol mismatch! expected:', snap.wsProtocol)
      process.exit(4)
    }
  } else {
    console.warn('[contract-guard] No snapshot found; printing current values')
    console.log(JSON.stringify({ openapi: openapiHash, wsSchema: wsHash, wsProtocol: wsProto }, null, 2))
  }
}

main().catch((e) => { console.error(e); process.exit(10) })
