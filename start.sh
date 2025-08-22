#!/bin/bash

echo "🚀 Starting EasyX System..."

# Create and activate virtual environment
echo "🐍 Setting up Python virtual environment..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Start backend service
echo "🔧 Starting Flask backend on port 5001..."
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd ../frontend
npm install

# Start frontend service
echo "🎨 Starting React frontend on port 3000..."
npm start &
FRONTEND_PID=$!

echo "✅ System started successfully!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for all processes
wait
