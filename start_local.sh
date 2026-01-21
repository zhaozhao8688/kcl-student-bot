#!/bin/bash

###############################################################################
# Local Development Startup Script
#
# This script starts both the backend and frontend for local testing
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_DIR="/Users/harrisonzhao/Documents/KCL bot"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  KCL Student Bot - Local Development Startup${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Setup Backend
echo -e "${YELLOW}[1/4] Setting up backend...${NC}"
cd "$BACKEND_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "  → Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "  ${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "  → Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "  → Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "  ${GREEN}✓ Backend dependencies installed${NC}"
echo ""

# Step 2: Verify backend configuration
echo -e "${YELLOW}[2/4] Verifying backend configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "  ${RED}✗ .env file not found!${NC}"
    echo "  → Please create backend/.env file with your API keys"
    exit 1
fi

API_KEY=$(grep OPENROUTER_API_KEY .env | cut -d= -f2)
if [ -z "$API_KEY" ]; then
    echo -e "  ${RED}✗ OPENROUTER_API_KEY not configured${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓ Backend configuration OK${NC}"
echo ""

# Step 3: Start Backend
echo -e "${YELLOW}[3/4] Starting backend server...${NC}"
echo "  → Starting on http://localhost:8000"

# Kill any existing backend processes
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start backend in background
nohup python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > "$PROJECT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "  → Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "  → Waiting for backend to be ready..."
for i in {1..10}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ Backend is ready!${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "  ${RED}✗ Backend failed to start${NC}"
        echo "  → Check backend.log for errors"
        exit 1
    fi
    sleep 1
done
echo ""

# Step 4: Start Frontend
echo -e "${YELLOW}[4/4] Starting frontend...${NC}"
cd "$FRONTEND_DIR"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "  → Installing frontend dependencies (this may take a while)..."
    npm install
    echo -e "  ${GREEN}✓ Frontend dependencies installed${NC}"
fi

echo "  → Starting on http://localhost:3000"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🚀 Starting frontend server...${NC}"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Start frontend (this will run in foreground)
npm start
