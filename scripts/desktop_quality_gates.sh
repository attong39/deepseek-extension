#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Running Quality Gates for Release..."

echo "📝 TypeScript type check..."
npm run ts:check

echo "🏗️  Build test..."
npm run build

echo "🧪 Running unit tests..."
npm run test:unit

echo "💨 Running smoke tests..."
npm run test:smoke

echo "📋 Contract validation..."
npm run contract:guard

echo "📊 Code duplication check..."
npm run dup:js

echo "🔗 API schema sync check..."
npm run api:gen
if ! git diff --quiet --exit-code src/api/generated/ 2>/dev/null; then
  echo "❌ API schema is out of sync. Run 'npm run api:gen' and commit changes."
  exit 1
fi

echo "✅ All quality gates passed!"
echo "🚀 Ready for release!"