# Optimized Dockerfile for Raspberry Pi deployment
# Multi-stage build for Raspberry Pi
FROM node:18-slim AS frontend-build

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend with Debian slim
FROM python:3.11-slim AS backend

# Install system dependencies for pdfplumber and potential PDF processing
# poppler-utils provides pdftotext, which pdfplumber uses for text extraction
RUN apt-get update && apt-get install -y \
    gcc \
    libc6-dev \
    libffi-dev \
    libssl-dev \
    wget \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./

# Copy frontend build from previous stage
COPY --from=frontend-build /app/frontend/build ./static

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Change ownership
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:5001/health || exit 1

# Environment variables
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
