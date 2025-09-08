// Ensure generated client contains Authorization interceptor
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const clientPath = resolve(process.cwd(), 'src', 'api', 'generated', 'client.ts');
const s = readFileSync(clientPath, 'utf8');

const mustHave = [
  'api.interceptors.request.use',
  'Authorization',
  'DEFAULT_API_BASE_URL',
];

const missing = mustHave.filter((m) => !s.includes(m));
if (missing.length > 0) {
  console.error('Generated client missing required parts:', missing);
  process.exit(2);
}
console.log('Generated client OK');
