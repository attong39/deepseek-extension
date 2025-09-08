#!/usr/bin/env node

/**
 * Validate Plugin Manifests
 * Kiểm tra tất cả plugin manifests khớp schema và allowlist
 */

import Ajv from 'ajv';
import fs from 'fs/promises';
import path from 'path';

const PLUGINS_DIR = './plugins';
const SCHEMA_PATH = './contracts/plugins/plugin-manifest.schema.json';
const ALLOWLIST_PATH = './config/plugins.allowlist.json';

async function loadJsonFile(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    throw new Error(`Failed to load ${filePath}: ${error.message}`);
  }
}

async function findManifests() {
  const manifests = [];
  
  try {
    const plugins = await fs.readdir(PLUGINS_DIR);
    
    for (const plugin of plugins) {
      const pluginDir = path.join(PLUGINS_DIR, plugin);
      const manifestPath = path.join(pluginDir, 'manifest.json');
      
      try {
        await fs.access(manifestPath);
        const manifest = await loadJsonFile(manifestPath);
        manifests.push({
          path: manifestPath,
          data: manifest,
          pluginDir
        });
      } catch {
        console.warn(`⚠️  No manifest found in ${pluginDir}`);
      }
    }
  } catch (error) {
    if (error.code === 'ENOENT') {
      console.log('ℹ️  No plugins directory found');
      return [];
    }
    throw error;
  }
  
  return manifests;
}

async function validatePlugins() {
  console.log('🔍 Validating plugin manifests...\n');
  
  // Load schema and allowlist
  const schema = await loadJsonFile(SCHEMA_PATH);
  const allowlist = await loadJsonFile(ALLOWLIST_PATH);
  const allowedKeys = new Set(allowlist.allow);
  
  // Setup Ajv validator
  const ajv = new Ajv({ strict: true });
  const validate = ajv.compile(schema);
  
  // Find all manifests
  const manifests = await findManifests();
  
  if (manifests.length === 0) {
    console.log('✅ No plugins to validate');
    return;
  }
  
  let errors = 0;
  
  for (const { path: manifestPath, data: manifest, pluginDir } of manifests) {
    console.log(`📦 Validating ${manifestPath}`);
    
    // Schema validation
    const isValid = validate(manifest);
    if (!isValid) {
      console.error(`❌ Schema validation failed:`);
      for (const error of validate.errors) {
        console.error(`   ${error.instancePath} ${error.message}`);
      }
      errors++;
      continue;
    }
    
    // Allowlist check
    if (!allowedKeys.has(manifest.key)) {
      console.error(`❌ Plugin "${manifest.key}" not in allowlist`);
      errors++;
      continue;
    }
    
    // Entry file check
    const entryPath = path.join(pluginDir, manifest.entry);
    try {
      await fs.access(entryPath);
    } catch {
      console.error(`❌ Entry file not found: ${manifest.entry}`);
      errors++;
      continue;
    }
    
    console.log(`✅ ${manifest.key} v${manifest.version} - OK`);
  }
  
  console.log(`\n📊 Validation Summary:`);
  console.log(`   Total plugins: ${manifests.length}`);
  console.log(`   Valid: ${manifests.length - errors}`);
  console.log(`   Errors: ${errors}`);
  
  if (errors > 0) {
    console.error(`\n❌ Plugin validation failed with ${errors} errors`);
    process.exit(1);
  } else {
    console.log('\n✅ All plugins valid!');
  }
}

// Run validation
validatePlugins().catch(error => {
  console.error('💥 Plugin validation crashed:', error.message);
  process.exit(1);
});