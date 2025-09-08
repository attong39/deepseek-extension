// Gộp crash logs + build meta + health snapshot (nếu có) → zip nhỏ gọn.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import zlib from "node:zlib";

const out = path.join(process.cwd(), `diagnostics_${Date.now()}.ndjson.gz`);
const gz = zlib.createGzip();
const ws = fs.createWriteStream(out);
gz.pipe(ws);

// mask nhẹ
const mask = (s) =>
  s.replace(/sk-[a-zA-Z0-9]{20,}/g, "[REDACTED]").replace(/\b[\w.-]+@[\w.-]+\.\w+\b/g, "[REDACTED]");

// userData/crashes (điền đúng path nếu khác)
const candidates = ["dist/CHECKSUMS.txt", "sbom.json", "THIRD_PARTY_LICENSES.html"];
candidates.forEach((f) => {
  if (fs.existsSync(f)) {
    gz.write(JSON.stringify({ file: f, content: mask(fs.readFileSync(f, "utf8")) }) + "\n");
  }
});

gz.write(JSON.stringify({ platform: os.type() + " " + os.release(), arch: os.arch() }) + "\n");
gz.end();

ws.on("close", () => console.log("[diagnostics] ->", out));