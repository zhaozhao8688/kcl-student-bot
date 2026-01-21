# 🌐 Which URL Should I Use?

## You Have TWO Services Running

When you deployed with Blueprint (render.yaml), Render created **2 separate services**:

### 1. Backend API 🔧
- **URL**: `https://kcl-bot-backend.onrender.com`
- **Purpose**: Processes chat requests, handles AI logic
- **Shows**: JSON responses (what you're seeing now)
- **Example**:
  ```json
  {"name":"KCL Student Bot API","version":"2.0.0","status":"online"}
  ```

### 2. Frontend App 🎨
- **URL**: `https://kcl-bot-frontend.onrender.com`
- **Purpose**: The actual chat interface users interact with
- **Shows**: Beautiful chat UI with King's AI branding
- **This is what you want!** ✅

---

## 🎯 Access Your Chat Interface

**Go to the FRONTEND URL:**

```
https://kcl-bot-frontend.onrender.com
```

This is where you'll see:
- Chat interface
- Message bubbles
- Timetable sync button
- Clear chat button
- The actual product! 🎉

---

## 🔍 How to Find Both URLs

### In Render Dashboard:

1. Go to: https://dashboard.render.com
2. You'll see **2 services**:
   - `kcl-bot-backend` ← API (JSON responses)
   - `kcl-bot-frontend` ← Chat Interface (your product!)
3. Click on **"kcl-bot-frontend"**
4. Copy the URL at the top (looks like: `https://kcl-bot-frontend.onrender.com`)
5. Open that URL in your browser

---

## 🔧 The URLs Work Together

```
User's Browser
     ↓
Frontend (React App)
https://kcl-bot-frontend.onrender.com
     ↓ (sends chat message via API)
Backend (FastAPI)
https://kcl-bot-backend.onrender.com/api
     ↓
AI Agent → Search → Scrape → Response
     ↓
Frontend (shows response)
```

---

## ✅ Quick Check

### Backend is working if:
```bash
curl https://kcl-bot-backend.onrender.com/health
# Returns: {"status":"healthy","service":"kcl-student-bot-api"}
```

### Frontend is working if:
- Open `https://kcl-bot-frontend.onrender.com` in browser
- You see a chat interface
- You can type and send messages
- You get AI responses

---

## 🆘 If Frontend Shows Error

### "Network Error" or "Cannot connect to API"

**Problem**: Frontend can't reach backend

**Solution**: Update backend CORS to allow frontend

1. Check your backend URL is correct
2. Make sure CORS is configured in `backend/main.py`:
   ```python
   allow_origins=[
       "http://localhost:3000",
       "https://kcl-bot-frontend.onrender.com",  # Must match frontend URL!
   ]
   ```

### "Service Unavailable" (First Load)

**This is normal!** Free tier services sleep after 15 minutes of inactivity.

- First request takes 30-60 seconds to wake up
- After that, it's fast
- This is expected behavior on free tier

---

## 📋 Your Service URLs

**Backend API**: https://kcl-bot-backend.onrender.com
- Use this for: Testing health endpoint, API docs at `/docs`

**Frontend Chat**: https://kcl-bot-frontend.onrender.com
- Use this for: Actual chat interface (your product!)

---

**Next**: Open the FRONTEND URL to see your actual chat interface! 🎨
