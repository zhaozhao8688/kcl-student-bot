# 🧪 Local Testing Guide

## Running the App Locally (2 Terminals)

You need to run **2 services** at the same time:
1. Backend (FastAPI) - Port 8000
2. Frontend (React) - Port 3000

---

## Terminal 1: Start Backend

```bash
# Navigate to backend folder
cd /Users/harrisonzhao/Documents/KCL\ bot/backend

# Create virtual environment (if not exists)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Test it:**
Open browser: http://localhost:8000/health
Should show: `{"status":"healthy","service":"kcl-student-bot-api"}`

---

## Terminal 2: Start Frontend

**Open a NEW terminal window** (keep backend running!)

```bash
# Navigate to frontend folder
cd /Users/harrisonzhao/Documents/KCL\ bot/frontend

# Install dependencies (first time only)
npm install

# Start React dev server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Browser will auto-open** at http://localhost:3000

---

## ✅ Testing the Input Fix

1. **Frontend loads** - You should see the chat interface
2. **Input is enabled** - You can type immediately
3. **Type a message** - Try: "Hello"
4. **Send it** - Click send button or press Enter
5. **Check response** - You should get an AI response

---

## 🔍 Debugging Checklist

### If Input Still Disabled:

**Check Browser Console (F12):**
```javascript
// Should see:
API Base URL: http://localhost:8000/api
Session created: <some-uuid>
```

**Check for errors:**
- Red errors in console?
- Network tab shows failed requests?

### If Backend Won't Start:

**Missing dependencies?**
```bash
cd /Users/harrisonzhao/Documents/KCL\ bot/backend
pip install -r requirements.txt
```

**Port already in use?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Try again
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Virtual environment not activated?**
```bash
source venv/bin/activate
# You should see (venv) at the start of your prompt
```

### If Frontend Won't Start:

**Node modules not installed?**
```bash
cd /Users/harrisonzhao/Documents/KCL\ bot/frontend
npm install
```

**Port 3000 already in use?**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Try again
npm start
```

**React build errors?**
Check terminal output for syntax errors or missing packages

---

## 🧪 What to Test

### 1. Input Field
- ✅ Is enabled immediately (not grayed out)
- ✅ Can type text
- ✅ Placeholder says "Type a message..."

### 2. Send Message
- ✅ Type "Hello" and press Enter
- ✅ Message appears in chat
- ✅ Loading indicator shows (three dots)
- ✅ AI response appears

### 3. Clear Chat
- ✅ Click "Clear Chat" button (top left)
- ✅ Confirms with dialog
- ✅ Resets to welcome message

### 4. Timetable Sync
- ✅ Click "Sync Timetable" button (top right)
- ✅ Modal opens
- ✅ Can paste URL or upload file

### 5. Error Handling
- ✅ Stop backend server (Ctrl+C in Terminal 1)
- ✅ Try sending message
- ✅ Should show error: "can't connect to server"
- ✅ Input should still work (not disabled)

---

## 📊 Check Both Terminals

### Terminal 1 (Backend):
```
INFO:     127.0.0.1:xxxxx - "POST /api/chat/message HTTP/1.1" 200 OK
INFO:     Processing query for session <uuid>: Hello
INFO:     Successfully generated response for session <uuid>
```

### Terminal 2 (Frontend):
```
Compiled successfully!
```

**Browser Console (F12 → Console):**
```
API Base URL: http://localhost:8000/api
Creating session on first message...
Session created: <uuid>
```

---

## 🎯 Quick Test Commands

```bash
# Test backend is running
curl http://localhost:8000/health

# Test backend API docs
open http://localhost:8000/docs

# Test frontend
open http://localhost:3000
```

---

## 🛑 Stop Servers

When done testing:

**Terminal 1 (Backend):**
```bash
# Press Ctrl+C to stop
# Then deactivate virtual environment
deactivate
```

**Terminal 2 (Frontend):**
```bash
# Press Ctrl+C to stop
```

---

## 💡 Tips

1. **Keep both terminals visible** - Use split screen
2. **Watch for errors** - Red text in either terminal
3. **Check browser console** - F12 → Console tab
4. **Hot reload works** - Changes auto-update in browser
5. **Backend changes need restart** - Ctrl+C then start again

---

## ✅ Success Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Health endpoint works: http://localhost:8000/health
- [ ] Chat interface loads in browser
- [ ] Input field is enabled (can type)
- [ ] Can send message and get response
- [ ] Browser console shows no errors
- [ ] Both terminals show no errors

---

**Ready?** Open two terminal windows and let's test! 🚀
