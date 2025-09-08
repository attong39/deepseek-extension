#!/usr/bin/env node
import Ajv from "ajv";
import addFormats from "ajv-formats";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const schemaPath = path.join(root, "contracts/config/app-config.schema.json");
const defaultCfgPath = path.join(root, "contracts/config/app-config.default.json");

if (!fs.existsSync(schemaPath)) {
  console.error("❌ Schema not found:", schemaPath);
  process.exit(1);
}

if (!fs.existsSync(defaultCfgPath)) {
  console.error("❌ Default config not found:", defaultCfgPath);
  process.exit(1);
}

const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const config = JSON.parse(fs.readFileSync(defaultCfgPath, "utf8"));

const ajv = new Ajv({ allErrors: true, strict: true });
addFormats(ajv);
const validate = ajv.compile(schema);

if (!validate(config)) {
  console.error("❌ Config invalid:", validate.errors);
  process.exit(1);
}

console.log("✅ Config valid against schema");
console.log(`   Schema: ${schema.$id}`);
console.log(`   Config: ${JSON.stringify(config, null, 2)}`);