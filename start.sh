#!/bin/bash
set -euo pipefail
echo "🚀 Starting EasyX System..."
############################################
# 0) Paths and database configuration
############################################
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"   # project root (/EasyX)
SQL_FILE="$ROOT_DIR/db/init_tables.sql"            # schema + seed SQL

DB_NAME="easyxdb"
DB_SUPER="postgres"                         # system + DB superuser
LINUX_USER="$(id -un)"                      # current OS user (peer auth target)

############################################
# 1) Ensure PostgreSQL service is running
############################################
echo "🐘 Checking PostgreSQL service..."
if ! pg_isready >/dev/null 2>&1; then
  if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl start postgresql || true
  elif command -v service >/dev/null 2>&1; then
    sudo service postgresql start || true
  fi
  # wait until ready
  for i in {1..20}; do
    if pg_isready >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done
fi
echo "✅ PostgreSQL is running."

############################################
# 2) Create database if missing (peer auth; no password)
############################################
echo "🗃️ Checking database '$DB_NAME'..."
DB_EXISTS=$(sudo -u "$DB_SUPER" psql -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}';" || echo "")
if [ "$DB_EXISTS" != "1" ]; then
  echo "🆕 Creating database '$DB_NAME'..."
  sudo -u "$DB_SUPER" psql -v ON_ERROR_STOP=1 -d postgres -c "CREATE DATABASE ${DB_NAME};"
else
  echo "ℹ️ Database '$DB_NAME' already exists."
fi

############################################
# 3) Ensure a matching DB role for current OS user (peer auth)
############################################
echo "👤 Ensuring DB role for OS user '$LINUX_USER'..."
ROLE_EXISTS=$(sudo -u "$DB_SUPER" psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='${LINUX_USER}';" || echo "")
if [ "$ROLE_EXISTS" != "1" ]; then
  sudo -u "$DB_SUPER" psql -v ON_ERROR_STOP=1 -d postgres -c "CREATE ROLE \"${LINUX_USER}\" LOGIN;"
  echo "✅ Created role '${LINUX_USER}'."
else
  echo "ℹ️ Role '${LINUX_USER}' already exists."
fi

# Make OS user the owner of the database so app objects are owned by that user
echo "🔧 Setting database owner to '${LINUX_USER}'..."
sudo -u "$DB_SUPER" psql -v ON_ERROR_STOP=1 -d postgres -c "ALTER DATABASE ${DB_NAME} OWNER TO \"${LINUX_USER}\";"

############################################
# 4) Run initialization SQL as the DB owner (so objects are owned correctly)
############################################
if [ -f "$SQL_FILE" ]; then
  echo "📜 Running initialization SQL: $SQL_FILE"
  # Use sudo -u <linux_user> to connect via peer auth over the local socket
  sudo -u "$LINUX_USER" psql -v ON_ERROR_STOP=1 -d "$DB_NAME" -f "$SQL_FILE"
  echo "✅ Initialization SQL completed."
else
  echo "⚠️ SQL file not found: $SQL_FILE. Skipping initialization."
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
