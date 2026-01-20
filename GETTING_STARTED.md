# Getting Started with KCL Student Bot (React + FastAPI)

## Quick Start Guide

The migration is complete! Here's how to run your new React + FastAPI application.

### Prerequisites Check

Make sure you have:
- ✅ Python 3.9+ installed
- ✅ Node.js 16+ installed
- ✅ All API keys (check `backend/.env`)

### Step 1: Start the Backend (Terminal 1)

```bash
# Navigate to backend
cd backend

# Activate virtual environment (if you have one)
# source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
python -m uvicorn main:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Verify backend is running:**
- Open http://localhost:8000 in browser → Should see welcome message
- Open http://localhost:8000/docs → Should see API documentation

### Step 2: Start the Frontend (Terminal 2)

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start the dev server
npm start
```

The browser should automatically open to http://localhost:3000

### Step 3: Test the Application

1. **Initial Load:** You should see:
   - Header with "King's AI" branding
   - Initial welcome message from the AI
   - "Sync Timetable" button in header
   - Input field at the bottom

2. **Send a Test Message:**
   - Type "What are the library opening hours?"
   - Press Enter or click Send
   - AI should process and respond

3. **Test Timetable Sync:**
   - Click "Sync Timetable" button in header
   - Paste your iCal URL
   - Click "Sync Timetable"
   - Button should change to "Timetable Synced" with gold accent

## Troubleshooting

### Backend Won't Start

**Error: `ModuleNotFoundError`**
```bash
# Make sure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: `Port 8000 already in use`**
```bash
# Kill the existing process
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn main:app --reload --port 8001
```

**Error: Missing environment variables**
```bash
# Check backend/.env exists
ls backend/.env

# If not, copy from root
cp .env backend/.env
```

### Frontend Won't Start

**Error: `npm ERR!`**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: `Module not found: Can't resolve`**
```bash
# Make sure all files are in place
ls src/components/  # Should show Header.jsx, ChatMessage.jsx, etc.
ls src/services/    # Should show api.js
```

**Error: API calls failing (CORS errors)**
- Check backend is running on port 8000
- Check `frontend/.env.local` has `REACT_APP_API_URL=http://localhost:8000/api`
- Restart both servers

### Styles Not Working

If Tailwind styles aren't applied:
```bash
# Verify tailwind.config.js exists
cat tailwind.config.js

# Restart the dev server
# Press Ctrl+C, then npm start again
```

## Development Workflow

### Making Changes

**Backend Changes:**
- Edit files in `backend/`
- Server auto-reloads (if using `--reload` flag)
- Check terminal for errors

**Frontend Changes:**
- Edit files in `frontend/src/`
- Browser auto-refreshes
- Check browser console for errors

### Viewing Logs

**Backend logs:** Terminal 1 (where uvicorn is running)
**Frontend logs:** Browser console (F12 → Console tab)

### API Documentation

FastAPI provides interactive API docs:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test API endpoints directly from the docs!

## Common Tasks

### Reset Session

If you want to start a fresh session:
```bash
# Restart the backend server
# Or just refresh the frontend (creates new session)
```

### Check Backend Health

```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","service":"kcl-student-bot-api"}
```

### Test API Manually

```bash
# Create a session
curl -X POST http://localhost:8000/api/session/create

# Send a message (replace SESSION_ID)
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!", "session_id": "SESSION_ID"}'
```

## What's Different from Streamlit?

| Feature | Streamlit | React + FastAPI |
|---------|-----------|-----------------|
| **UI Framework** | Streamlit | React + Tailwind CSS |
| **Backend** | Built-in | FastAPI (REST API) |
| **Session** | `st.session_state` | Backend session manager |
| **Real-time** | Auto-rerun | API calls |
| **Styling** | st.markdown + CSS | Tailwind utility classes |
| **Agent System** | ✅ Same | ✅ Same (100% reused) |
| **Tools** | ✅ Same | ✅ Same (100% reused) |
| **Database** | ✅ Supabase | ✅ Supabase (same) |

## File Structure Quick Reference

```
backend/
├── main.py              → API entry point (START HERE)
├── api/
│   ├── chat.py         → Chat endpoints
│   ├── timetable.py    → Timetable endpoints
│   └── session.py      → Session endpoints
├── core/
│   ├── chat_processor.py → Chat logic
│   └── session.py       → Session management
└── agents/              → Agent system (from original)

frontend/
├── src/
│   ├── App.jsx         → Main component (START HERE)
│   ├── components/     → UI components
│   └── services/
│       └── api.js      → API client
```

## Next Steps

1. ✅ Get both servers running
2. ✅ Test chat functionality
3. ✅ Test timetable sync
4. 🔄 Customize the UI (colors, text, etc.)
5. 🔄 Deploy to production (see MIGRATION_README.md)

## Need Help?

1. **Check logs:** Both terminal outputs
2. **Check browser console:** F12 → Console
3. **Check API docs:** http://localhost:8000/docs
4. **Check MIGRATION_README.md:** For detailed architecture info

## Success Criteria ✅

You should be able to:
- [x] Start backend server without errors
- [x] Start frontend server without errors
- [x] See the chat interface in browser
- [ ] Send messages and get AI responses
- [ ] Sync timetable via URL
- [ ] See messages persist in Supabase

---

**Happy hacking!** 🎓
