// Coverage gate script - Fail nếu lines % < threshold (mặc định 80)
import fs from "node:fs";

const threshold = Number(process.argv[2] || 80);
const summaryPath = "coverage/coverage-summary.json";

if (!fs.existsSync(summaryPath)) {
  console.error("[coverage-gate] summary not found:", summaryPath);
  process.exit(2);
}

const summary = JSON.parse(fs.readFileSync(summaryPath, "utf8"));
const pct = summary.total.lines.pct ?? 0;

console.log("[coverage-gate] lines % =", pct, "threshold =", threshold);

if (pct < threshold) {
  console.error(`[coverage-gate] FAILED: ${pct}% < ${threshold}%`);
  process.exit(3);
} else {
  console.log(`[coverage-gate] PASSED: ${pct}% >= ${threshold}%`);
}