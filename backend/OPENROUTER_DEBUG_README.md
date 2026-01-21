# OpenRouter 401 "User Not Found" - Debug Guide

This guide explains the fixes implemented to resolve the persistent OpenRouter 401 "User not found" error.

## Problem

The backend returned "User not found" from OpenRouter API even after changing to a different OpenRouter account and updating the API key in `.env`.

## Root Cause

**Module-level singleton caching**: The backend uses singleton instances created at import time that cache API credentials and never refresh them. When the `.env` file is updated, if the Python process isn't fully killed, the singletons persist in memory with old credentials.

## Fixes Implemented

### 1. HTTP Headers Added to OpenRouter Client

**File**: `backend/services/llm_service.py`

Added required HTTP headers that OpenRouter expects:

```python
self.client = OpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key,
    default_headers={
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "KCL Student Bot"
    }
)
```

### 2. Lazy Initialization for LLM Service

**File**: `backend/services/llm_service.py`

Replaced module-level singleton with lazy initialization:

```python
def get_llm_service() -> LLMService:
    """Get or create LLM service instance (lazy initialization)."""
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance

def reset_llm_service():
    """Reset the LLM service instance when settings change."""
    global _llm_service_instance
    _llm_service_instance = None
```

### 3. Startup Credential Verification

**File**: `backend/main.py`

Added automatic API key verification on startup:

```python
@app.on_event("startup")
async def startup_event():
    # Verify OpenRouter API key
    try:
        from services.llm_service import llm_service
        test_response = llm_service.generate(
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        logger.info("✅ OpenRouter API key verified successfully")
    except Exception as e:
        logger.error(f"❌ OpenRouter API key verification failed: {str(e)}")
```

### 4. Enhanced Health Check Endpoint

**File**: `backend/main.py`

Added configuration validation to `/health` endpoint:

```python
@app.get("/health")
async def health_check():
    """Health check with API key validation."""
    # Checks if OpenRouter and Supabase credentials are configured
    # Returns status: "healthy" or "degraded" with warnings
```

### 5. Debug Utility Scripts

Created two helper scripts:

#### `verify_setup.sh`
Verifies your setup without starting the server:
- Checks `.env` file exists
- Verifies API key is configured
- Tests API key with OpenRouter directly
- Checks for running processes
- Validates Python environment

**Usage**:
```bash
cd backend
./verify_setup.sh
```

#### `debug_openrouter.sh`
Complete debug and restart workflow:
1. Kills all backend processes
2. Verifies `.env` configuration
3. Tests API key with OpenRouter
4. Checks Python environment
5. Starts backend with proper monitoring

**Usage**:
```bash
cd backend
./debug_openrouter.sh
```

## Quick Fix Steps

### If You're Getting "User Not Found" Error

1. **Kill all processes**:
   ```bash
   lsof -ti:8000 | xargs kill -9
   pkill -9 uvicorn
   ```

2. **Verify your setup**:
   ```bash
   cd backend
   ./verify_setup.sh
   ```

3. **If verification passes, start the server**:
   ```bash
   ./debug_openrouter.sh
   ```

4. **Watch for these startup messages**:
   ```
   INFO: KCL Student Bot API starting up...
   INFO: LLM Service initialized with model: anthropic/claude-3.5-sonnet
   INFO: ✅ OpenRouter API key verified successfully
   ```

### If Verification Fails

1. **Check your OpenRouter account**:
   - Visit https://openrouter.ai/keys - Is your key active?
   - Visit https://openrouter.ai/account - Do you have credits?

2. **Generate a new API key**:
   - Go to https://openrouter.ai/keys
   - Create a new key
   - Update `backend/.env`:
     ```env
     OPENROUTER_API_KEY=your_new_key_here
     ```

3. **Test the new key directly**:
   ```bash
   curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
     -H "Authorization: Bearer YOUR_NEW_KEY" \
     -H "Content-Type: application/json" \
     -H "HTTP-Referer: http://localhost:3000" \
     -H "X-Title: KCL Student Bot" \
     -d '{"model":"anthropic/claude-3.5-sonnet","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
   ```

4. **Run verification again**:
   ```bash
   ./verify_setup.sh
   ```

## Manual Process Management

If scripts don't work, use these manual commands:

### Kill all backend processes:
```bash
# Kill by port
lsof -ti:8000 | xargs kill -9

# Kill by process name
pkill -9 uvicorn
ps aux | grep uvicorn  # Should show nothing

# Verify port is clear
lsof -i:8000  # Should be empty
```

### Check current .env:
```bash
cd backend
cat .env | grep OPENROUTER_API_KEY
```

### Test API key:
```bash
cd backend
NEW_KEY=$(grep OPENROUTER_API_KEY .env | cut -d= -f2)

curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $NEW_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: http://localhost:3000" \
  -H "X-Title: KCL Student Bot" \
  -d '{"model":"anthropic/claude-3.5-sonnet","messages":[{"role":"user","content":"test"}],"max_tokens":5}'
```

### Start backend:
```bash
cd backend
source venv/bin/activate  # If using venv
uvicorn main:app --reload --port 8000
```

## Health Check Endpoint

After starting the backend, check its health:

```bash
curl http://localhost:8000/health
```

**Healthy response**:
```json
{
  "status": "healthy",
  "service": "kcl-student-bot-api",
  "checks": {
    "api": "ok",
    "openrouter_api_key": "configured",
    "supabase": "configured"
  }
}
```

**Degraded response**:
```json
{
  "status": "degraded",
  "service": "kcl-student-bot-api",
  "checks": {
    "api": "ok",
    "openrouter_api_key": "missing"
  },
  "warning": "OpenRouter API key not configured"
}
```

## Troubleshooting

### Still getting "User not found" after following all steps?

1. **Verify account has credits**:
   - https://openrouter.ai/account
   - Add credits if balance is $0

2. **Try a different model**:
   Update `.env`:
   ```env
   DEFAULT_MODEL=openai/gpt-3.5-turbo
   ```

3. **Check for network/firewall issues**:
   ```bash
   curl -v https://openrouter.ai/api/v1/models | head
   ```
   Should return HTTP 200

4. **Enable debug logging**:
   Update `.env`:
   ```env
   LOG_LEVEL=DEBUG
   ```
   Restart and check logs

5. **Verify Python environment**:
   ```bash
   cd backend
   source venv/bin/activate
   python -c "from config.settings import settings; print('API Key:', settings.openrouter_api_key[:20])"
   ```

### Multiple Python processes?

```bash
# Check all Python processes
ps aux | grep python

# Kill specific process
kill -9 <PID>
```

### Backend not restarting properly with uvicorn --reload?

Use manual restart instead:
```bash
# Stop all
lsof -ti:8000 | xargs kill -9

# Start without reload
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Prevention

To prevent this issue in the future:

1. **Always use the debug script** when changing API keys:
   ```bash
   ./debug_openrouter.sh
   ```

2. **Monitor startup logs** for the verification message:
   ```
   ✅ OpenRouter API key verified successfully
   ```

3. **Use health check** to verify configuration:
   ```bash
   curl http://localhost:8000/health
   ```

4. **If changing API keys**, use the reset function (future enhancement):
   ```python
   from services.llm_service import reset_llm_service
   reset_llm_service()  # This will force recreation with new key
   ```

## Summary

The core issue was singleton caching of API credentials at module import time. The fixes ensure:

1. ✅ Required HTTP headers are sent to OpenRouter
2. ✅ Services can be recreated if needed (lazy initialization)
3. ✅ API keys are verified on startup
4. ✅ Health checks validate configuration
5. ✅ Debug tools make troubleshooting easy

**Key takeaway**: When changing API keys, always fully kill the backend process and start fresh - don't rely on hot reload.
