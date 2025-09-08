#!/usr/bin/env node

/**
 * Bundle Budget Gate - Fail nếu assets/*.js.gz vượt ngưỡng (KB). Dùng sau build.
 */

import { createReadStream, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { createGzip } from "node:zlib";

const MAX_KB = Number(process.argv[2] || 180); // tuỳ chọn: node scripts/bundle_budget.mjs 160
const dir = "dist/assets";

// Check if dist/assets exists
if (!existsSync(dir)) {
  console.error(`[bundle-budget] Directory ${dir} not found. Run build first.`);
  process.exit(1);
}

const files = readdirSync(dir).filter(f => f.endsWith(".js"));

if (files.length === 0) {
  console.log("[bundle-budget] No JS files found in dist/assets");
  process.exit(0);
}

function gzSize(file) {
  return new Promise((res, rej) => {
    const gz = createGzip(); 
    let n = 0;
    gz.on("data", (c) => (n += c.length));
    gz.on("end", () => res(n));
    gz.on("error", rej);
    createReadStream(join(dir, file)).pipe(gz);
  });
}

console.log(`[bundle-budget] Checking ${files.length} JS files (max ${MAX_KB}KB gzip)...`);

const rows = [];
let hasViolation = false;

for (const f of files) {
  const rawKB = +(statSync(join(dir, f)).size / 1024).toFixed(1);
  const gzKB = +((await gzSize(f)) / 1024).toFixed(1);
  rows.push({ file: f, rawKB, gzKB, status: gzKB > MAX_KB ? "❌ FAIL" : "✅ OK" });
  
  if (gzKB > MAX_KB) {
    console.error(`[bundle-budget] ${f} gzip=${gzKB}KB > ${MAX_KB}KB - VIOLATION`);
    hasViolation = true;
  }
}

console.table(rows);

if (hasViolation) {
  console.error(`\n❌ Bundle budget exceeded! Some files are larger than ${MAX_KB}KB gzipped.`);
  console.error("💡 Tips:");
  console.error("  - Use dynamic imports for large dependencies");
  console.error("  - Check for duplicate dependencies");
  console.error("  - Consider code splitting");
  process.exit(2);
} else {
  console.log(`\n✅ Bundle budget OK - All files <= ${MAX_KB}KB gzipped`);
}