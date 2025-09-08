// API codegen script for CI/local use
// Sources: prefers local docs/api/openapi.yaml else falls back to server $OPENAPI_JSON
import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const ROOT = process.cwd();
const LOCAL_SPEC = resolve(ROOT, 'docs', 'api', 'openapi.yaml');
const OUT_DIR = resolve(ROOT, 'src', 'api', 'generated');
mkdirSync(OUT_DIR, { recursive: true });

let spec = process.env.OPENAPI_JSON ?? (process.env.VITE_API_URL && `${process.env.VITE_API_URL}/openapi.json`);
if (existsSync(LOCAL_SPEC)) spec = LOCAL_SPEC;
if (!spec) {
  console.error('No OpenAPI spec found. Set OPENAPI_JSON or VITE_API_URL, or place docs/api/openapi.yaml');
  process.exit(1);
}

console.log('Generating OpenAPI types/client from:', spec);
try {
  execSync(`npx openapi-typescript ${spec} --output ${OUT_DIR}/types.ts`, { stdio: 'inherit' });
  // client with baseURL + auth interceptor (Bearer from session/localStorage)
  const client = `// AUTO-GENERATED with patch by scripts/api_codegen.mjs\n`
    + `import axios from 'axios';\n`
    + `import { DEFAULT_API_BASE_URL } from '../../constants';\n`
    + `import { session } from '../../services/session';\n`
    + `function normalizeBase(u) {\n`
    + `  try {\n`
    + `    const url = new URL(u);\n`
    + `    let path = url.pathname || '';\n`
    + `    if (path.endsWith('/api/v1')) path = path.slice(0, -8);\n`
    + `    if (path.endsWith('/')) path = path.slice(0, -1);\n`
    + `    url.pathname = path;\n`
    + `    return url.origin + url.pathname;\n`
    + `  } catch {\n`
    + `    let s = String(u || '');\n`
    + `    if (s.endsWith('/api/v1')) s = s.slice(0, -8);\n`
    + `    if (s.endsWith('/')) s = s.slice(0, -1);\n`
    + `    return s;\n`
    + `  }\n`
    + `}\n`
    + `export const api = axios.create({\n`
    + `  baseURL: (import.meta && import.meta.env && import.meta.env.VITE_API_URL) || normalizeBase(DEFAULT_API_BASE_URL),\n`
    + `});\n`
    + `api.interceptors.request.use((config) => {\n`
    + `  const token = (session && session.getToken && session.getToken()) || localStorage.getItem('zeta_token');\n`
    + `  if (token) {\n`
    + `    config.headers = config.headers || {};\n`
    + `    config.headers.Authorization = 'Bearer ' + token;\n`
    + `  }\n`
    + `  return config;\n`
    + `});\n`;
  writeFileSync(resolve(OUT_DIR, 'client.ts'), client);
  console.log('✔ API types/client generated at', OUT_DIR);
} catch (e) {
  console.error('Codegen failed:', e?.message || e);
  process.exit(1);
}
