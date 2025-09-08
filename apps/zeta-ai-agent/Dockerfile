# =============================================================================
# 🚀 Zeta AI Agent - Production Docker Image
# Multi-stage build for optimal size and security
# =============================================================================

# Build stage - Node.js assets
FROM node:20-alpine AS node-builder
LABEL stage="builder"

WORKDIR /app

# Install build dependencies and pnpm
RUN apk add --no-cache g++ git make python3 && \
    npm install -g pnpm && \
    rm -rf /var/cache/apk/*

# Copy package files
COPY package*.json pnpm-lock.yaml* tsconfig*.json ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code and build
COPY src/ ./src/
COPY webpack.config.js ./
RUN pnpm run build && pnpm run compile

# Run tests during build (optional, can be disabled for faster builds)
# RUN npm test

# ---------- Runtime Stage ----------
FROM node:20-alpine AS runtime

# Install runtime dependencies
RUN apk add --no-cache \
    dumb-init \
    ca-certificates \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S zetaai -u 1001 -G nodejs

# Set working directory
WORKDIR /app

# Copy package files for production dependency installation
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy compiled application from builder stage
COPY --from=builder --chown=zetaai:nodejs /app/out ./out

# Copy any additional runtime files
COPY --chown=zetaai:nodejs README.md ./
COPY --chown=zetaai:nodejs LICENSE ./

# Create necessary directories with proper permissions
RUN mkdir -p /data/vector /data/cache /tmp/zeta && \
    chown -R zetaai:nodejs /data /tmp/zeta

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV METRICS_PORT=9090
ENV LOG_LEVEL=info
ENV VECTOR_DB_PATH=/data/vector
ENV CACHE_PATH=/data/cache

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })" || exit 1

# Security: Switch to non-root user
USER zetaai

# Expose ports
EXPOSE 3000 9090

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]

# Start the application
CMD ["node", "out/extension.js"]

# Labels for metadata
LABEL maintainer="Zeta AI Team" \
      description="Zeta AI Agent - Intelligent coding assistant" \
      version="1.0.0" \
      org.opencontainers.image.title="Zeta AI Agent" \
      org.opencontainers.image.description="AI-powered coding assistant for VS Code" \
      org.opencontainers.image.vendor="Zeta" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/zeta/zeta-ai-agent"
