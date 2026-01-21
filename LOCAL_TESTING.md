# Local Testing Guide

This guide explains how to start and test the KCL Student Bot locally.

## Quick Start (Recommended)

Use the automated startup script:

```bash
cd "/Users/harrisonzhao/Documents/KCL bot"
./start_local.sh
```

This script will:
1. Create Python virtual environment (if needed)
2. Install backend dependencies
3. Verify configuration
4. Start backend on http://localhost:8000
5. Install frontend dependencies (if needed)
6. Start frontend on http://localhost:3000

**To stop**: Press `Ctrl+C` in the terminal

---

## Manual Setup

If you prefer to start services manually or need to troubleshoot:

### Backend Setup

#### 1. Create Virtual Environment (first time only)

```bash
cd "/Users/harrisonzhao/Documents/KCL bot/backend"
python3 -m venv venv
```

#### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 3. Install Dependencies (first time only)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Verify Configuration

Make sure `backend/.env` exists and has the correct API keys:

```bash
cat .env | grep OPENROUTER_API_KEY
```

Should show: `OPENROUTER_API_KEY=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`

#### 5. Start Backend Server

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Or use the debug script:

```bash
./debug_openrouter.sh
```

**Expected output:**
```
INFO: KCL Student Bot API starting up...
INFO: Verifying OpenRouter API credentials...
INFO: ✅ OpenRouter API key verified successfully
INFO: Uvicorn running on http://0.0.0.0:8000
```

#### 6. Test Backend

Open a new terminal and run:

```bash
curl http://localhost:8000/health
```

Should return:
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

### Frontend Setup

#### 1. Install Dependencies (first time only)

```bash
cd "/Users/harrisonzhao/Documents/KCL bot/frontend"
npm install
```

#### 2. Start Frontend Server

```bash
npm start
```

This will automatically open http://localhost:3000 in your browser.

**Expected output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

---

## Testing the Application

### 1. Basic Chat Test

1. Open http://localhost:3000 in your browser
2. Type a message like "Hello" or "Tell me about King's College London"
3. You should get an AI response

### 2. Backend API Test

Test the chat API directly:

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H 'Content-Type: application/json' \
  -d '{"query":"What is KCL?","session_id":"test-123"}'
```

Should return:
```json
{
  "response": "King's College London (KCL) is...",
  "session_id": "test-123"
}
```

### 3. Check API Documentation

Visit http://localhost:8000/docs to see the interactive API documentation (Swagger UI).

---

## Troubleshooting

### Backend won't start

**Check if port is already in use:**
```bash
lsof -i:8000
```

**Kill existing processes:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Check logs for errors:**
```bash
cat backend.log
```

**Verify virtual environment is activated:**
```bash
which python
# Should show: /Users/harrisonzhao/Documents/KCL bot/backend/venv/bin/python
```

**Run verification script:**
```bash
cd backend
./verify_setup.sh
```

### Frontend won't start

**Check if port 3000 is in use:**
```bash
lsof -i:3000
```

**Kill existing processes:**
```bash
lsof -ti:3000 | xargs kill -9
```

**Clear node modules and reinstall:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Chat returns errors

**Check backend logs:**
```bash
tail -f backend.log
```

**Test OpenRouter API key:**
```bash
cd backend
./verify_setup.sh
```

**Check browser console:**
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab to see API requests

### API key issues

If you see "User not found" errors:

1. **Verify the correct key is in backend/.env:**
   ```bash
   cat backend/.env | grep OPENROUTER
   ```

2. **Should show the working key:**
   ```
   OPENROUTER_API_KEY=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
   ```

3. **Restart backend after changing .env:**
   ```bash
   # Kill backend
   lsof -ti:8000 | xargs kill -9

   # Start again
   ./debug_openrouter.sh
   ```

---

## Useful Commands

### Check what's running

```bash
# Check backend
lsof -i:8000

# Check frontend
lsof -i:3000

# Check all Node processes
ps aux | grep node

# Check all Python processes
ps aux | grep python
```

### View logs

```bash
# Backend logs (if started with start_local.sh)
tail -f backend.log

# Backend logs (if started manually in terminal)
# Just check the terminal where you ran uvicorn

# Frontend logs
# Check the terminal where you ran npm start
```

### Stop services

```bash
# Stop backend
lsof -ti:8000 | xargs kill -9

# Stop frontend
# Press Ctrl+C in the terminal running npm start

# Stop all
pkill -f uvicorn
pkill -f "react-scripts start"
```

---

## Development Workflow

1. **Start both services:**
   ```bash
   ./start_local.sh
   ```

2. **Make changes to code:**
   - Backend changes will auto-reload (if using `--reload` flag)
   - Frontend changes will auto-reload (React hot reload)

3. **Test changes:**
   - Chat in browser at http://localhost:3000
   - Test API at http://localhost:8000/docs

4. **Check logs for errors:**
   - Backend: Check terminal or `backend.log`
   - Frontend: Check terminal running `npm start`
   - Browser: Check DevTools Console (F12)

5. **Stop when done:**
   - Press `Ctrl+C` in both terminals
   - Or use kill commands above

---

## Environment Variables

### Backend (.env)

Located at: `backend/.env`

Required variables:
- `OPENROUTER_API_KEY` - Your OpenRouter API key
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase API key
- `SERPAPI_API_KEY` - SerpAPI key for search
- `FIRECRAWL_API_KEY` - Firecrawl key for web scraping

Optional:
- `APP_ENV` - Environment (development/production)
- `LOG_LEVEL` - Logging level (INFO/DEBUG)
- `DEFAULT_MODEL` - LLM model to use

### Frontend (.env)

Located at: `frontend/.env.local` (create if needed)

Optional variables:
- `REACT_APP_API_URL` - Backend API URL (defaults to http://localhost:8000)

---

## URLs Reference

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main chat interface |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/health | Backend health status |
| Root | http://localhost:8000/ | API info |

---

## Next Steps

After confirming local testing works:

1. **Deploy to production** (if needed)
2. **Set up CI/CD** for automated testing
3. **Configure monitoring** for production
4. **Add more features** to the chatbot

For production deployment, see `DEPLOYMENT.md` (if available).
