#!/usr/bin/env bash
# Turbo API Quick Start Script
# API Key: 5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP

echo "🚀 TURBO API QUICK START"
echo "========================"

# Set environment variables
export TURBO_API_KEY="5358cc7f4f8f4162b0836a41f9f50d29.fpjkoY9kodkgdElqampPgxMP"
export TURBO_API_BASE="https://api.turbo.ai/v1"
export OLLAMA_HOST="http://127.0.0.1:11434"

echo "✅ Environment variables set"
echo "🔑 API Key: ${TURBO_API_KEY:0:20}..."
echo "🌐 Endpoint: $TURBO_API_BASE"

# Test basic functionality
echo ""
echo "🧪 Testing implementation..."
python turbo_api_implementation.py

echo ""
echo "✅ Quick start complete!"
echo "📚 Use: python -c \"from turbo_api_implementation import TurboAPIImplementation; import asyncio; asyncio.run(TurboAPIImplementation().smart_chat('Hello'))\""