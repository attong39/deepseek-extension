#!/usr/bin/env bash
set -euo pipefail

IMAGE=${IMAGE:-"zeta-api:latest"}

echo "🚀 [Phase4] Production Deployment - Đóng gói và triển khai"
echo "=========================================================="

echo "🐳 Building production Docker image: $IMAGE"
docker build -t "$IMAGE" -f Dockerfile.production . || {
    echo "❌ Docker build failed!"
    exit 1
}

echo "✅ Successfully built Docker image: $IMAGE"
echo ""
echo "🚀 To run the production container:"
echo "   docker run -p 8000:8000 $IMAGE"
echo ""
echo "🔧 For production deployment with environment variables:"
echo "   docker run -p 8000:8000 \\"
echo "     -e DATABASE_URL=postgresql://... \\"
echo "     -e REDIS_URL=redis://... \\"
echo "     -e SECRET_KEY=your-secret-key \\"
echo "     $IMAGE"
echo ""
echo "📊 Check container health:"
echo "   curl http://localhost:8000/health"
echo ""
echo "✅ [Phase4] Production deployment ready!"
echo "🎉 All phases completed successfully!"