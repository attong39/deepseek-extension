#!/usr/bin/env node
/**
 * Cross-platform SBOM và license scanning cho enterprise compliance
 * 
 * Generates:
 * - CycloneDX SBOM (JSON + XML)  
 * - License inventory (JSON + CSV)
 * - Compliance report summary
 */

import { execSync } from 'child_process';
import { existsSync, mkdirSync, writeFileSync } from 'fs';
import { join } from 'path';

const SBOM_DIR = 'sbom';
const LICENSE_DIR = 'licenses';

function ensureDir(dir) {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
    console.log(`📁 Created directory: ${dir}`);
  }
}

function runCommand(cmd, description, continueOnError = false) {
  console.log(`🔄 ${description}...`);
  try {
    const output = execSync(cmd, { encoding: 'utf8', stdio: 'pipe' });
    console.log(`✅ ${description} completed`);
    return output;
  } catch (error) {
    console.error(`❌ ${description} failed:`, error.message);
    if (!continueOnError) {
      process.exit(1);
    }
    return null;
  }
}

function generateSBOM() {
  console.log('\n📄 Generating SBOM (Software Bill of Materials)...');
  ensureDir(SBOM_DIR);
  
  // Generate JSON format
  runCommand(
    `npx @cyclonedx/cyclonedx-npm --output-file ${SBOM_DIR}/bom.json --output-format JSON`,
    'SBOM JSON generation',
    true
  );
  
  // Generate XML format  
  runCommand(
    `npx @cyclonedx/cyclonedx-npm --output-file ${SBOM_DIR}/bom.xml --output-format XML`,
    'SBOM XML generation',
    true
  );
  
  console.log(`📄 SBOM files saved to: ${SBOM_DIR}/`);
}

function scanLicenses() {
  console.log('\n⚖️ Scanning licenses...');
  ensureDir(LICENSE_DIR);
  
  // JSON format for programmatic analysis
  runCommand(
    `npx license-checker-rseidelsohn --production --json --out ${LICENSE_DIR}/licenses.json`,
    'License JSON scan',
    true
  );
  
  // CSV format for human review
  runCommand(
    `npx license-checker-rseidelsohn --production --csv --out ${LICENSE_DIR}/licenses.csv`,
    'License CSV scan', 
    true
  );
  
  console.log(`⚖️ License reports saved to: ${LICENSE_DIR}/`);
}

function generateComplianceReport() {
  console.log('\n📊 Generating compliance summary...');
  
  const report = {
    timestamp: new Date().toISOString(),
    sbom: {
      json: existsSync(join(SBOM_DIR, 'bom.json')),
      xml: existsSync(join(SBOM_DIR, 'bom.xml'))
    },
    licenses: {
      json: existsSync(join(LICENSE_DIR, 'licenses.json')),
      csv: existsSync(join(LICENSE_DIR, 'licenses.csv'))
    },
    compliance_status: 'GENERATED'
  };
  
  writeFileSync('compliance-report.json', JSON.stringify(report, null, 2));
  console.log('📊 Compliance report: compliance-report.json');
  
  // Summary
  console.log('\n🎯 Compliance Artifacts Summary:');
  console.log(`   SBOM JSON: ${report.sbom.json ? '✅' : '❌'}`);
  console.log(`   SBOM XML: ${report.sbom.xml ? '✅' : '❌'}`);
  console.log(`   License JSON: ${report.licenses.json ? '✅' : '❌'}`);
  console.log(`   License CSV: ${report.licenses.csv ? '✅' : '❌'}`);
}

function main() {
  console.log('🚀 Enterprise Compliance Scanner');
  console.log('================================\n');
  
  generateSBOM();
  scanLicenses();
  generateComplianceReport();
  
  console.log('\n✨ Compliance scan completed!');
  console.log('📁 Upload sbom/ and licenses/ folders to CI artifacts');
}

main();