#!/bin/bash

# Simple build script for EasyX
set -e

echo "🏗️ Building EasyX Docker image..."

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t easyx:latest .

# Show image info
echo "📊 Image info:"
docker images easyx:latest

echo "✅ Build complete!"
echo "To run: docker-compose up"
