#!/usr/bin/env node
import Ajv from "ajv";
import addFormats from "ajv-formats";
import { glob } from "glob";
import fs from "node:fs";
import path from "node:path";

console.log("🔍 Validating plugin manifests...");

const root = process.cwd();
const schemaPath = path.join(root, "contracts/plugins/plugin-manifest.schema.json");

if (!fs.existsSync(schemaPath)) {
  console.error("❌ Plugin schema not found:", schemaPath);
  process.exit(1);
}

const schema = JSON.parse(fs.readFileSync(schemaPath, "utf8"));
const ajv = new Ajv({ allErrors: true, strict: false }); // strict: false for meta-schema
addFormats(ajv);
const validate = ajv.compile(schema);

// Find all plugin manifests
const manifests = await glob("plugins/**/manifest.json", { cwd: root });

if (manifests.length === 0) {
  console.log("ℹ️  No plugin manifests found");
  process.exit(0);
}

let ok = true;
for (const manifestPath of manifests) {
  const fullPath = path.join(root, manifestPath);
  try {
    const data = JSON.parse(fs.readFileSync(fullPath, "utf8"));
    const valid = validate(data);
    
    if (!valid) {
      ok = false;
      console.error(`❌ ${manifestPath} invalid:`);
      for (const error of validate.errors) {
        console.error(`   ${error.instancePath} ${error.message}`);
      }
    } else {
      console.log(`✅ ${manifestPath} ok (${data.name} v${data.version})`);
    }
  } catch (error) {
    ok = false;
    console.error(`❌ ${manifestPath} parse error:`, error.message);
  }
}

if (!ok) {
  console.error("\n❌ Plugin validation failed");
  process.exit(1);
}

console.log("\n🎉 All plugin manifests valid");