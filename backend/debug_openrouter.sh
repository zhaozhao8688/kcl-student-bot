#!/bin/bash

###############################################################################
# OpenRouter Debug Script
#
# This script helps debug and fix the "User not found" 401 error from OpenRouter
# by ensuring all backend processes are killed and the new API key is loaded.
###############################################################################

set -e  # Exit on error

BACKEND_DIR="/Users/harrisonzhao/Documents/KCL bot/backend"
PORT=8000

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  OpenRouter Debug & Restart Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Kill all backend processes
echo -e "${YELLOW}[1/5] Killing all backend processes...${NC}"
if lsof -ti:$PORT >/dev/null 2>&1; then
    echo "  → Found processes on port $PORT"
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    echo -e "  ${GREEN}✓ Processes killed${NC}"
else
    echo "  → No processes found on port $PORT"
fi

# Check for uvicorn processes
if ps aux | grep uvicorn | grep -v grep >/dev/null 2>&1; then
    echo "  → Found uvicorn processes"
    pkill -9 uvicorn 2>/dev/null || true
    echo -e "  ${GREEN}✓ Uvicorn processes killed${NC}"
fi

# Verify no processes running
if lsof -i:$PORT >/dev/null 2>&1; then
    echo -e "  ${RED}✗ Warning: Processes still running on port $PORT${NC}"
else
    echo -e "  ${GREEN}✓ Port $PORT is clear${NC}"
fi
echo ""

# Step 2: Verify .env file
echo -e "${YELLOW}[2/5] Verifying .env configuration...${NC}"
cd "$BACKEND_DIR"

if [ ! -f .env ]; then
    echo -e "  ${RED}✗ .env file not found!${NC}"
    exit 1
fi

# Check for API key
if grep -q "OPENROUTER_API_KEY=" .env; then
    API_KEY=$(grep OPENROUTER_API_KEY .env | cut -d= -f2 | tr -d ' ')
    if [ -z "$API_KEY" ]; then
        echo -e "  ${RED}✗ OPENROUTER_API_KEY is empty${NC}"
        exit 1
    else
        echo "  → API Key: ${API_KEY:0:20}..."
        echo -e "  ${GREEN}✓ API key configured${NC}"
    fi
else
    echo -e "  ${RED}✗ OPENROUTER_API_KEY not found in .env${NC}"
    exit 1
fi
echo ""

# Step 3: Test API key directly
echo -e "${YELLOW}[3/5] Testing API key with OpenRouter...${NC}"
TEST_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: http://localhost:3000" \
  -H "X-Title: KCL Student Bot" \
  -d '{"model":"anthropic/claude-3.5-sonnet","messages":[{"role":"user","content":"test"}],"max_tokens":5}')

HTTP_CODE=$(echo "$TEST_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$TEST_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "  ${GREEN}✓ API key is valid and working!${NC}"
elif echo "$RESPONSE_BODY" | grep -q "User not found"; then
    echo -e "  ${RED}✗ API key returned 'User not found'${NC}"
    echo "  → Check your OpenRouter account at https://openrouter.ai/keys"
    echo "  → Make sure you have credits at https://openrouter.ai/account"
    exit 1
elif echo "$RESPONSE_BODY" | grep -q "insufficient"; then
    echo -e "  ${YELLOW}⚠ API key works but insufficient credits${NC}"
    echo "  → Add credits at https://openrouter.ai/account"
else
    echo "  → HTTP Code: $HTTP_CODE"
    echo "  → Response: $RESPONSE_BODY"
    echo -e "  ${YELLOW}⚠ Unexpected response (but not 'User not found')${NC}"
fi
echo ""

# Step 4: Check Python virtual environment
echo -e "${YELLOW}[4/5] Checking Python environment...${NC}"
if [ -d "venv" ]; then
    echo -e "  ${GREEN}✓ Virtual environment found${NC}"
    if [ ! -z "$VIRTUAL_ENV" ]; then
        echo "  → Already activated: $VIRTUAL_ENV"
    else
        echo "  → Activating virtual environment..."
        source venv/bin/activate
    fi
else
    echo -e "  ${YELLOW}⚠ No virtual environment found${NC}"
    echo "  → Will use system Python"
fi
echo ""

# Step 5: Start backend
echo -e "${YELLOW}[5/5] Starting backend server...${NC}"
echo -e "  ${BLUE}Starting uvicorn on port $PORT...${NC}"
echo ""
echo -e "${GREEN}Watch for these startup messages:${NC}"
echo "  1. 'KCL Student Bot API starting up...'"
echo "  2. 'LLM Service initialized with model: anthropic/claude-3.5-sonnet'"
echo "  3. '✅ OpenRouter API key verified successfully'"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port $PORT --reload
