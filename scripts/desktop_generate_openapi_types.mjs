// Generate TypeScript types from OpenAPI (JSON or YAML)
// Usage: npm run openapi:gen
import { execSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

// Prefer explicit spec file if provided
const SPEC_FILE = process.env.OPENAPI_SPEC;
const API_URL = process.env.OPENAPI_JSON || process.env.VITE_API_URL || 'http://127.0.0.1:8000';
const OUT_DIR = resolve(process.cwd(), 'src', 'api', 'generated');
mkdirSync(OUT_DIR, { recursive: true });

const schemaInput = SPEC_FILE || `${API_URL}/openapi.json`;
console.log('Generating OpenAPI types from:', schemaInput);
try {
  // Use npx openapi-typescript to generate d.ts
  execSync(`npx openapi-typescript ${schemaInput} --output ${OUT_DIR}/schema.d.ts`, { stdio: 'inherit' });
  // Index barrel
  writeFileSync(resolve(OUT_DIR, 'index.d.ts'), "export * from './schema';\n");
  console.log('✔ OpenAPI types generated at', OUT_DIR);
} catch (e) {
  console.error('Failed to generate OpenAPI types:', e?.message || e);
  process.exitCode = 1;
}
