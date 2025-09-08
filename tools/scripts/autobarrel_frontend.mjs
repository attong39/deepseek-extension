#!/usr/bin/env node
// Tạo barrel index.ts cho frontend (có thể chỉnh lại targets tuỳ dự án)
import { readdirSync, statSync, writeFileSync } from "fs";
import { join } from "path";

const ROOT = process.cwd();
const TARGETS = [
  "zeta_vn/frontend/src/api",
  // có thể thêm src/components, src/hooks, ...
];

function genBarrel(dir) {
  const entries = readdirSync(dir)
    .filter((f) => f !== "index.ts" && !f.startsWith("."))
    .filter((f) => !f.endsWith(".test.ts") && !f.endsWith(".spec.ts"));

  const exports = [];
  for (const e of entries) {
    const full = join(dir, e);
    const rel = "./" + e.replace(/\.tsx?$/, "");
    if (statSync(full).isDirectory()) {
      // export từ subfolder nếu có index.ts con
      exports.push(`export * as ${e} from '${rel}';`);
    } else if (e.endsWith(".ts") || e.endsWith(".tsx")) {
      const name = e.replace(/\.tsx?$/, "");
      exports.push(`export * from '${rel}';`);
      exports.push(`export { default as ${name} } from '${rel}';`);
    }
  }
  const out = exports.join("\n") + "\n";
  writeFileSync(join(dir, "index.ts"), out);
  console.log("Updated barrel:", join(dir, "index.ts"));
}

for (const t of TARGETS) {
  const p = join(ROOT, t);
  try {
    genBarrel(p);
  } catch (e) {
    // ignore missing targets
  }
}
