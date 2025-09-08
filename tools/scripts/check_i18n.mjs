#!/usr/bin/env node
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

const root = resolve(process.cwd())
const en = JSON.parse(readFileSync(resolve(root, 'desktop_ai_zeta', 'src', 'i18n', 'en.json'), 'utf8'))
const vi = JSON.parse(readFileSync(resolve(root, 'desktop_ai_zeta', 'src', 'i18n', 'vi.json'), 'utf8'))

function flatten(obj, prefix = '') {
  return Object.entries(obj).reduce((acc, [k, v]) => {
    const key = prefix ? `${prefix}.${k}` : k
    if (v && typeof v === 'object' && !Array.isArray(v)) {
      Object.assign(acc, flatten(v, key))
    } else {
      acc[key] = true
    }
    return acc
  }, {})
}

const ke = Object.keys(flatten(en))
const kv = Object.keys(flatten(vi))
const missingInEn = kv.filter(k => !ke.includes(k))
const missingInVi = ke.filter(k => !kv.includes(k))

if (missingInEn.length) {
  console.error('[check_i18n] Missing in en:', missingInEn.join(', '))
}
if (missingInVi.length) {
  console.error('[check_i18n] Missing in vi:', missingInVi.join(', '))
}
if (missingInEn.length || missingInVi.length) process.exit(1)
console.log('[check_i18n] OK')
