// Báo cáo kích thước bundle (gzip) cho JS/CSS trong dist/assets.
import { createReadStream, existsSync, readdirSync } from "node:fs";
import { extname, join } from "node:path";
import { pipeline } from "node:stream";
import { createGzip } from "node:zlib";

function gzipSize(file) {
  return new Promise((res, rej) => {
    let n = 0;
    pipeline(createReadStream(file), createGzip(), (err) => err && rej(err));
    const gz = createGzip();
    const src = createReadStream(file);
    src.on("error", rej);
    gz.on("data", (c) => (n += c.length));
    gz.on("end", () => res(n));
    src.pipe(gz);
  });
}

const dir = "dist/assets";
if (!existsSync(dir)) {
  console.error("[bundle-report] dist/assets/ chưa tồn tại. Hãy chạy build trước.");
  process.exit(1);
}

const files = readdirSync(dir).filter(f => [".js", ".css"].includes(extname(f)));
const rows = [];
for (const f of files) {
  const p = join(dir, f);
  const gz = await gzipSize(p);
  rows.push({ file: `assets/${f}`, gzipKB: +(gz / 1024).toFixed(1) });
}
console.table(rows);