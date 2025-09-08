// Kiểm định artifacts sau build: liệt kê file, SHA256, kích thước.
// Viết: dist/CHECKSUMS.txt + dist/artifacts.json. Exit code !=0 nếu thiếu targets.
import { createHash } from "node:crypto";
import { createReadStream, existsSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { extname, join } from "node:path";

const dist = "dist";
if (!existsSync(dist)) {
  console.error("[postflight] dist/ chưa tồn tại. Hãy chạy: npm run dist");
  process.exit(1);
}

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap(d => {
    const p = join(dir, d.name);
    return d.isDirectory() ? walk(p) : [p];
  });
}

function sha256(file) {
  return new Promise((res, rej) => {
    const h = createHash("sha256");
    const s = createReadStream(file);
    s.on("data", (c) => h.update(c));
    s.on("error", rej);
    s.on("end", () => res(h.digest("hex")));
  });
}

const files = walk(dist).filter(f =>
  [".exe", ".dmg", ".AppImage", ".yml", ".blockmap"].includes(extname(f)) || f.includes("index.html")
);

const expected = [
  (arr) => arr.some(f => f.endsWith(".exe")),
  (arr) => arr.some(f => f.endsWith(".dmg")),
  (arr) => arr.some(f => f.endsWith(".AppImage")),
];

if (!expected.every(fn => fn(files))) {
  console.error("[postflight] Thiếu 1 hoặc nhiều artifacts (.exe/.dmg/.AppImage).");
  process.exit(2);
}

const rows = [];
const meta = [];
const tasks = files.map(async (f) => {
  const hash = await sha256(f);
  const size = statSync(f).size;
  rows.push(`${hash}  ${f}`);
  meta.push({ file: f, sha256: hash, size });
});
await Promise.all(tasks);
writeFileSync(join(dist, "CHECKSUMS.txt"), rows.join("\n") + "\n");
writeFileSync(join(dist, "artifacts.json"), JSON.stringify(meta, null, 2));
console.log("[postflight] OK → dist/CHECKSUMS.txt, dist/artifacts.json");