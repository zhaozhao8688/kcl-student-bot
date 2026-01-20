# 🚀 Deployment Guide - KCL Student Bot

## Overview

Your app has two parts that need to be deployed separately:
1. **Frontend (React)** → Deploy to **Vercel** ✅
2. **Backend (FastAPI)** → Deploy to **Railway** or **Render** ✅

---

## Part 1: Deploy Backend (FastAPI)

### Option A: Railway (Recommended - Easy & Free)

#### 1. Create Railway Account
- Go to https://railway.app
- Sign up with GitHub

#### 2. Create New Project
```bash
# In your terminal, install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Navigate to backend
cd backend

# Initialize Railway project
railway init

# Add environment variables
railway variables set OPENROUTER_API_KEY="your_key"
railway variables set SUPABASE_URL="your_url"
railway variables set SUPABASE_KEY="your_key"
railway variables set SERPAPI_API_KEY="your_key"
railway variables set FIRECRAWL_API_KEY="your_key"
```

#### 3. Create Railway Configuration

Create `backend/railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `backend/Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 4. Deploy
```bash
railway up
```

Your backend will be deployed! Railway will give you a URL like:
`https://your-app.railway.app`

---

### Option B: Render (Alternative - Also Free)

#### 1. Create Render Account
- Go to https://render.com
- Sign up with GitHub

#### 2. Create New Web Service
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the `backend` directory

#### 3. Configure Service
- **Name**: kcl-student-bot-api
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### 4. Add Environment Variables
In Render dashboard, add:
- `OPENROUTER_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SERPAPI_API_KEY`
- `FIRECRAWL_API_KEY`

#### 5. Deploy
Click "Create Web Service" - Render will deploy automatically!

Your backend will be at: `https://your-app.onrender.com`

---

## Part 2: Deploy Frontend (React) to Vercel

### Step 1: Prepare Frontend

#### 1. Update API URL for Production

Edit `frontend/.env.production`:
```env
# Replace with your actual backend URL from Railway/Render
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

#### 2. Update CORS in Backend

Edit `backend/main.py` to allow your Vercel domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-app.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app",          # Allow all Vercel preview URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy backend after this change.

---

### Step 2: Deploy to Vercel

#### Method 1: Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Login to Vercel
vercel login

# Deploy (first time)
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? kcl-student-bot
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

#### Method 2: Vercel Dashboard (Easier)

1. **Go to https://vercel.com/new**

2. **Import Git Repository**
   - Click "Import Git Repository"
   - Connect your GitHub account
   - Select your repository

3. **Configure Project**
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

4. **Add Environment Variable**
   - Click "Environment Variables"
   - Add: `REACT_APP_API_URL` = `https://your-backend-url.railway.app/api`

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes

Your app will be live at: `https://your-app.vercel.app`

---

## Part 3: Update Backend CORS

After getting your Vercel URL, update the backend:

```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Redeploy backend to Railway/Render.

---

## Quick Deploy Checklist

### Backend (Railway/Render)
- [ ] Create account on Railway or Render
- [ ] Deploy backend with environment variables
- [ ] Get backend URL (e.g., https://your-app.railway.app)
- [ ] Test health endpoint: `curl https://your-app.railway.app/health`

### Frontend (Vercel)
- [ ] Create `frontend/.env.production` with backend URL
- [ ] Deploy to Vercel (CLI or dashboard)
- [ ] Get frontend URL (e.g., https://your-app.vercel.app)
- [ ] Update backend CORS with Vercel URL
- [ ] Test the live app!

---

## Vercel Configuration File (Optional)

Create `frontend/vercel.json` for advanced config:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

---

## Testing Deployment

### 1. Test Backend
```bash
# Health check
curl https://your-backend.railway.app/health

# Create session
curl -X POST https://your-backend.railway.app/api/session/create

# Test chat (replace SESSION_ID)
curl -X POST https://your-backend.railway.app/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!", "session_id": "test"}'
```

### 2. Test Frontend
- Open `https://your-app.vercel.app`
- Send a message
- Check browser console for errors
- Test timetable sync
- Test clear chat button

---

## Troubleshooting

### Frontend Can't Connect to Backend
- **Check CORS**: Backend must allow Vercel URL
- **Check Environment Variable**: `REACT_APP_API_URL` must be set correctly
- **Check Browser Console**: Look for CORS or network errors

### Backend Deployment Fails
- **Check Python Version**: Must be 3.9+
- **Check Environment Variables**: All API keys must be set
- **Check Logs**: Railway/Render dashboard shows deployment logs

### API Returns 500 Errors
- **Check Backend Logs**: Railway/Render dashboard
- **Check Environment Variables**: Verify all keys are correct
- **Check Database**: Supabase must be accessible

---

## Cost Estimate

### Free Tier Limits:
- **Vercel**: Unlimited personal projects, 100GB bandwidth/month
- **Railway**: $5 free credit/month (enough for small apps)
- **Render**: Free tier with some limitations (cold starts)

### Recommended:
Start with Railway free tier for backend + Vercel free tier for frontend = **$0/month**

---

## Continuous Deployment

Both Vercel and Railway support automatic deployments:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```

2. **Auto-Deploy**
   - Vercel: Automatically deploys on push
   - Railway: Automatically deploys on push
   - No manual intervention needed!

---

## Production Checklist

Before going live:

- [ ] All environment variables set correctly
- [ ] Backend health check returns healthy
- [ ] Frontend can connect to backend
- [ ] CORS configured for production domain
- [ ] Test all features (chat, timetable, clear chat)
- [ ] Check browser console for errors
- [ ] Test on mobile devices
- [ ] Update README with live URL

---

## Custom Domain (Optional)

### Add Custom Domain to Vercel:
1. Go to Vercel dashboard → Your project → Settings → Domains
2. Add your domain (e.g., `kcl-bot.yourdomain.com`)
3. Update DNS records as instructed
4. Update backend CORS with new domain

### Add Custom Domain to Railway:
1. Go to Railway dashboard → Your service → Settings
2. Add custom domain
3. Update DNS records
4. Update frontend `.env.production` with new backend URL

---

## Support & Documentation

- **Vercel Docs**: https://vercel.com/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs

---

## Summary

1. **Backend**: Deploy to Railway (easiest) or Render
2. **Frontend**: Deploy to Vercel with backend URL
3. **Update CORS**: Add Vercel URL to backend
4. **Test**: Make sure everything works!

**Estimated Time**: 15-30 minutes for first deployment

**Cost**: $0/month with free tiers

---

**Need help?** Check the troubleshooting section or deployment logs!
