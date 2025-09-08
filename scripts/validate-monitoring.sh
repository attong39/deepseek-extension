#!/bin/bash
set -euo pipefail

echo "🔍 Validating monitoring stack configuration..."

# Check network connectivity
echo "Testing network connectivity..."
if ping -c 1 host.docker.internal &> /dev/null; then
    echo "✅ host.docker.internal is reachable"
else
    echo "⚠️  host.docker.internal not reachable, using fallback IP"
    export TARGET_HOST=172.17.0.1
fi

# Validate YAML files (optional: requires yamllint)
if command -v yamllint >/dev/null 2>&1; then
  echo "Validating configuration files with yamllint..."
  yamllint config/prometheus/ config/grafana/ config/alertmanager/ || true
else
  echo "yamllint not installed; skipping YAML validation"
fi

# Check folder structure
echo "Checking dashboard organization..."
find config/grafana/dashboards -name "*.json" | head -5

echo "✅ Monitoring validation complete"
