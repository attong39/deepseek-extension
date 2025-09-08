# Minimal backend Dockerfile for dev compose
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
      PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential ca-certificates curl && \
      rm -rf /var/lib/apt/lists/*

# Copy backend package
COPY backend/ /app/

# Install python deps
RUN pip install --no-cache-dir -U pip && \
      if [ -f "/app/pyproject.toml" ]; then \
      pip install --no-cache-dir "."; \
      elif [ -f "/app/requirements.txt" ]; then \
      pip install --no-cache-dir -r requirements.txt; \
      fi

# Expose port
EXPOSE 8000

# Default command (adjust if FastAPI app exists)
CMD ["python", "-m", "backend.application"]
