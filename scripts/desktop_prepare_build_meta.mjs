// Tạo .env.build để Vite đọc vào lúc build (không commit secrets)
import { execSync } from "node:child_process";
import { writeFileSync } from "node:fs";

const gitSha = execSync("git rev-parse --short HEAD").toString().trim();
const buildTime = new Date().toISOString();
const version = process.env.npm_package_version ?? "0.0.0-dev";

const content = `VITE_APP_VERSION=${version}
VITE_GIT_SHA=${gitSha}
VITE_BUILD_TIME=${buildTime}
`;

writeFileSync(".env.build", content);
console.log("[build-meta] generated .env.build");