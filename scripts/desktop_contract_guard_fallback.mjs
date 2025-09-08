#!/usr/bin/env node
import fs from 'fs';
import process from 'process';

function usage() {
  console.error('Usage: node contract_guard_fallback.mjs --repo <repo_snapshot> --new <new_snapshot>');
  process.exit(2);
}

const argv = process.argv.slice(2);
const repoIdx = argv.indexOf('--repo');
const newIdx = argv.indexOf('--new');
if (repoIdx === -1 || newIdx === -1) usage();
const repoPath = argv[repoIdx + 1];
const newPath = argv[newIdx + 1];
if (!fs.existsSync(repoPath) || !fs.existsSync(newPath)) {
  console.error('Snapshot file(s) missing:', repoPath, newPath);
  process.exit(2);
}

const repo = JSON.parse(fs.readFileSync(repoPath, 'utf8'));
const neu = JSON.parse(fs.readFileSync(newPath, 'utf8'));

function compare(a, b, prefix = '') {
  let breaking = [];
  if (a && typeof a === 'object' && !Array.isArray(a)) {
    for (const k of Object.keys(a)) {
      if (!(k in b)) {
        breaking.push(`${prefix}/${k}`);
      } else {
        breaking = breaking.concat(compare(a[k], b[k], `${prefix}/${k}`));
      }
    }
  }
  return breaking;
}

const breaks = compare(repo, neu, '');
if (breaks.length > 0) {
  console.error('Contract BREAKING changes detected:');
  breaks.slice(0, 100).forEach((p) => console.error('  -', p));
  process.exit(1);
}
console.log('No breaking contract changes detected.');
process.exit(0);
