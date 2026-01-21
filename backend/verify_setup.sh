#!/bin/bash

###############################################################################
# OpenRouter Setup Verification Script
#
# This script verifies your OpenRouter setup without starting the server.
# Use this to diagnose issues before attempting to start the backend.
###############################################################################

BACKEND_DIR="/Users/harrisonzhao/Documents/KCL bot/backend"
PORT=8000

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  OpenRouter Setup Verification${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

cd "$BACKEND_DIR"

# Check 1: .env file exists
echo -e "${YELLOW}[1/5] Checking .env file...${NC}"
if [ -f .env ]; then
    echo -e "  ${GREEN}✓ .env file found${NC}"
else
    echo -e "  ${RED}✗ .env file not found!${NC}"
    exit 1
fi
echo ""

# Check 2: API key is configured
echo -e "${YELLOW}[2/5] Checking API key configuration...${NC}"
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

# Check 3: No processes running on port
echo -e "${YELLOW}[3/5] Checking for running processes...${NC}"
if lsof -i:$PORT >/dev/null 2>&1; then
    echo -e "  ${RED}✗ Processes still running on port $PORT${NC}"
    echo "  → Run: lsof -ti:$PORT | xargs kill -9"
    lsof -i:$PORT
else
    echo -e "  ${GREEN}✓ Port $PORT is clear${NC}"
fi

if ps aux | grep uvicorn | grep -v grep >/dev/null 2>&1; then
    echo -e "  ${RED}✗ Uvicorn processes still running${NC}"
    echo "  → Run: pkill -9 uvicorn"
else
    echo -e "  ${GREEN}✓ No uvicorn processes running${NC}"
fi
echo ""

# Check 4: Test API key with curl
echo -e "${YELLOW}[4/5] Testing API key with OpenRouter...${NC}"
echo "  → Sending test request..."

TEST_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: http://localhost:3000" \
  -H "X-Title: KCL Student Bot" \
  -d '{"model":"anthropic/claude-3.5-sonnet","messages":[{"role":"user","content":"test"}],"max_tokens":5}')

HTTP_CODE=$(echo "$TEST_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$TEST_RESPONSE" | sed '$d')

echo "  → HTTP Code: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "  ${GREEN}✓ API key is valid and working!${NC}"
    echo "  → Response: $(echo $RESPONSE_BODY | jq -r '.choices[0].message.content' 2>/dev/null || echo 'OK')"
elif echo "$RESPONSE_BODY" | grep -q "User not found"; then
    echo -e "  ${RED}✗ FAILED: 'User not found' error${NC}"
    echo ""
    echo "  This means your API key is not associated with a valid OpenRouter account."
    echo ""
    echo "  Action required:"
    echo "  1. Visit https://openrouter.ai/keys"
    echo "  2. Verify your API key is listed and active"
    echo "  3. Visit https://openrouter.ai/account"
    echo "  4. Ensure you have credits in your account"
    echo "  5. If key is invalid, generate a new one and update .env"
    echo ""
    exit 1
elif echo "$RESPONSE_BODY" | grep -q "insufficient"; then
    echo -e "  ${YELLOW}⚠ API key works but insufficient credits${NC}"
    echo "  → Add credits at https://openrouter.ai/account"
elif echo "$RESPONSE_BODY" | grep -q "error"; then
    ERROR_MSG=$(echo $RESPONSE_BODY | jq -r '.error.message' 2>/dev/null || echo $RESPONSE_BODY)
    echo -e "  ${RED}✗ Error: $ERROR_MSG${NC}"
    exit 1
else
    echo "  → Response: $RESPONSE_BODY"
    echo -e "  ${YELLOW}⚠ Unexpected response${NC}"
fi
echo ""

# Check 5: Python environment
echo -e "${YELLOW}[5/5] Checking Python environment...${NC}"
if [ -d "venv" ]; then
    echo -e "  ${GREEN}✓ Virtual environment found${NC}"

    # Check if requirements are installed
    if [ -f "requirements.txt" ]; then
        echo "  → Checking installed packages..."
        source venv/bin/activate

        # Check for key packages
        if python -c "import openai" 2>/dev/null; then
            echo -e "  ${GREEN}✓ openai package installed${NC}"
        else
            echo -e "  ${RED}✗ openai package not installed${NC}"
            echo "  → Run: pip install -r requirements.txt"
        fi

        if python -c "import fastapi" 2>/dev/null; then
            echo -e "  ${GREEN}✓ fastapi package installed${NC}"
        else
            echo -e "  ${RED}✗ fastapi package not installed${NC}"
            echo "  → Run: pip install -r requirements.txt"
        fi
    fi
else
    echo -e "  ${YELLOW}⚠ No virtual environment found${NC}"
    echo "  → Consider creating one: python -m venv venv"
fi
echo ""

# Summary
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Verification complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. If all checks passed, run: ./debug_openrouter.sh"
echo "  2. Or manually start: uvicorn main:app --reload --port 8000"
echo "  3. Test chat at: http://localhost:3000"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
