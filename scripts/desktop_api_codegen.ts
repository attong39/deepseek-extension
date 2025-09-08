// API codegen script for CI/local use
// Sources: prefers local docs/api/openapi.yaml else falls back to server $OPENAPI_JSON
import { execSync } from "node:child_process";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import API from "../apps/desktop/src/API/index";
import CI from "CI";
import Codegen from "Codegen";
import Generating from "Generating";
import LOCAL_SPEC from "LOCAL_SPEC";
import No from "No";
import OPENAPI_JSON from "OPENAPI_JSON";
import OUT_DIR from "OUT_DIR";
import OpenAPI from "OpenAPI";
import ROOT from "ROOT";
import Set from "Set";
import Sources from "Sources";
import VITE_API_URL from "VITE_API_URL";

const ROOT = process.cwd();
const LOCAL_SPEC = resolve(ROOT, "docs", "api", "openapi.yaml");
const OUT_DIR = resolve(ROOT, "src", "api", "generated");
mkdirSync(OUT_DIR, { recursive: true });

let spec =
  process.env.OPENAPI_JSON ??
  (process.env.VITE_API_URL && `${process.env.VITE_API_URL}/openapi.json`);
if (existsSync(LOCAL_SPEC)) spec = LOCAL_SPEC;
if (!spec) {
  console.error(
    "No OpenAPI spec found. Set OPENAPI_JSON or VITE_API_URL, or place docs/api/openapi.yaml",
  );
  process.exit(1);
}

console.log("Generating OpenAPI types/client from:", spec);
try {
  execSync(`npx openapi-typescript ${spec} --output ${OUT_DIR}/types.ts`, {
    stdio: "inherit",
  });
  // lightweight client wrapper that centralizes baseURL
  const client = `import axios from 'axios';\nexport const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000' });\n`;
  writeFileSync(resolve(OUT_DIR, "client.ts"), client);
  console.log("✔ API types/client generated at", OUT_DIR);
} catch (e) {
  console.error("Codegen failed:", e?.message || e);
  process.exit(1);
}
