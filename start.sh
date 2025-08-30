#!/bin/bash
#set -euo pipefail
echo "🚀 Starting EasyX System..."

############################################
# 0) Paths and database configuration
############################################
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"   # project root (/EasyX)
SQL_BOOTSTRAP="$ROOT_DIR/db/bootstrap.sql"  # friendly bootstrap with echo/timing/etc.
SQL_INIT="$ROOT_DIR/db/init_tables.sql"     # included by bootstrap.sql

DB_HOST="localhost"
DB_PORT="5432"

LINUX_USER="$(id -un)"
OS="$(uname -s)"

# On macOS (Homebrew PG), current user通常就是 DB 超级用户；Linux/WSL 用系统 postgres
if [ "$OS" = "Darwin" ]; then
  DB_SUPER="$LINUX_USER"
else
  DB_SUPER="postgres"
fi

# tools check
need_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "❌ Missing command: $1"; exit 1; }; }
need_cmd psql
need_cmd pg_isready
need_cmd date
mkdir -p "$ROOT_DIR/logs"

############################################
# 1) Ensure PostgreSQL service is running
############################################
echo "🐘 Checking PostgreSQL service..."
if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; then
  if [ "$OS" = "Darwin" ]; then
    brew services start postgresql@16 >/dev/null 2>&1 || \
    brew services start postgresql@15 >/dev/null 2>&1 || \
    brew services start postgresql       >/dev/null 2>&1 || true
  else
    if command -v systemctl >/dev/null 2>&1; then
      sudo systemctl start postgresql || true
    elif command -v service >/dev/null 2>&1; then
      sudo service postgresql start || true
    fi
  fi
  for i in {1..30}; do
    if pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; then break; fi
    sleep 1
    [ "$i" -eq 30 ] && { echo "❌ PostgreSQL not ready."; exit 1; }
  done
fi
echo "✅ PostgreSQL is running."

############################################
# 2) Bootstrap DB via SQL (terminal only; no logfile)
############################################
if [ ! -f "$SQL_BOOTSTRAP" ]; then
  echo "❌ Missing $SQL_BOOTSTRAP"; exit 1
fi
if [ ! -f "$SQL_INIT" ]; then
  echo "❌ Missing $SQL_INIT (required by bootstrap.sql)"; exit 1
fi

echo "🧭 Running DB bootstrap (terminal only): $SQL_BOOTSTRAP"

# 先尝试用当前用户执行（macOS Homebrew 常是超级用户）
if psql -v ON_ERROR_STOP=1 -v VERBOSITY=verbose -v ECHO=all --echo-errors -a \
        -d postgres -f "$SQL_BOOTSTRAP"; then
  echo "✅ Bootstrap executed as current user."
else
  echo "ℹ️ Retrying bootstrap as '$DB_SUPER'..."
  sudo -u "$DB_SUPER" psql -v ON_ERROR_STOP=1 -v VERBOSITY=verbose -v ECHO=all --echo-errors -a \
        -d postgres -f "$SQL_BOOTSTRAP"
  echo "✅ Bootstrap executed as '$DB_SUPER'."
fi

############################################
# 5) Start Flask backend
############################################

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
