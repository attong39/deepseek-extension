// Fail-fast nếu ENV nguy hiểm hoặc thiếu
import fs from "node:fs";

const req = ["VITE_API_BASE", "VITE_APP_VERSION"];
const danger = [/sk-[a-zA-Z0-9]{20,}/i, /api_key\s*=/i];

const envFiles = [".env", ".env.build"].filter(fs.existsSync.bind(fs));
let content = "";
envFiles.forEach(f => (content += fs.readFileSync(f, "utf8") + "\n"));

const miss = req.filter(k => !content.includes(k));
if (miss.length) {
  console.error("[env_guard] Missing:", miss.join(", "));
  process.exit(2);
}

if (danger.some(re => re.test(content))) {
  console.error("[env_guard] Secret pattern found! Remove secrets from .env!");
  process.exit(3);
}

console.log("[env_guard] OK");