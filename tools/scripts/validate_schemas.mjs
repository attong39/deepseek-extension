#!/usr/bin/env node
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { resolve } from 'node:path'

// Resolve Ajv and ajv-formats from desktop_ai_zeta's node_modules to avoid root devDeps
const req = createRequire(new URL('../desktop_ai_zeta/package.json', import.meta.url))
const Ajv = req('ajv')
const addFormats = req('ajv-formats')

const root = resolve(process.cwd())
const ajv = new Ajv({ strict: false })
addFormats(ajv)

function loadJSON(p) { return JSON.parse(readFileSync(p, 'utf8')) }

const actionSchema = loadJSON(resolve(root, 'contracts', 'actions', 'action.schema.json'))
const errorSchema = loadJSON(resolve(root, 'contracts', 'errors', 'error.schema.json'))
const wsSchemas = loadJSON(resolve(root, 'contracts', 'ws', 'events.schema.json'))

ajv.compile(actionSchema)
ajv.compile(errorSchema)
ajv.compile(wsSchemas)

console.log('[validate_schemas] All schemas compiled OK')
