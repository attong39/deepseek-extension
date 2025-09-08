// Rollback nhanh: reset tag "latest" về tag trước, không rebuild.
import { execSync } from "node:child_process";

try {
  const last = execSync("git describe --tags --abbrev=0 --exclude='*+hotfix*'").toString().trim();
  const prev = execSync(`git describe --tags --abbrev=0 ${last}^`).toString().trim();
  console.log(`[rollback] current=${last} → previous=${prev}`);
  execSync(`git tag -f latest ${prev}`);
  execSync("git push -f origin latest");
  console.log("[rollback] done (điều chỉnh release page thủ công nếu cần).");
} catch (error) {
  console.error("[rollback] Lỗi:", error.message);
  console.error("Đảm bảo bạn đang ở git repo và có ít nhất 2 tags.");
  process.exit(1);
}