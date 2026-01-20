# ⚡ Quick Deploy - 5 Steps

Deploy your KCL Student Bot to the internet in ~15 minutes!

---

## Step 1: Deploy Backend to Railway (5 min)

### A. Install Railway CLI
```bash
npm install -g @railway/cli
```

### B. Deploy Backend
```bash
# Navigate to backend
cd backend

# Login to Railway (opens browser)
railway login

# Create new project
railway init

# Set environment variables (replace with your actual keys)
railway variables set OPENROUTER_API_KEY="sk-or-v1-..."
railway variables set SUPABASE_URL="https://xxx.supabase.co"
railway variables set SUPABASE_KEY="eyJhbG..."
railway variables set SERPAPI_API_KEY="..."
railway variables set FIRECRAWL_API_KEY="fc-..."

# Deploy!
railway up
```

### C. Get Your Backend URL
```bash
railway domain
# Output: https://kcl-student-bot-production.up.railway.app
```

**Copy this URL - you'll need it for the frontend!**

---

## Step 2: Update Frontend Config (1 min)

Edit `frontend/.env.production`:
```bash
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

Replace with your actual Railway URL from Step 1.

---

## Step 3: Deploy Frontend to Vercel (5 min)

### A. Install Vercel CLI
```bash
npm install -g vercel
```

### B. Deploy Frontend
```bash
# Navigate to frontend
cd frontend

# Login to Vercel (opens browser)
vercel login

# Deploy to production
vercel --prod
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Link to existing project?** No
- **Project name?** kcl-student-bot (or your choice)
- **Directory?** `./`
- **Override settings?** No

### C. Get Your Frontend URL
Vercel will output your URL:
```
✅ Production: https://kcl-student-bot.vercel.app
```

---

## Step 4: Update Backend CORS (2 min)

Edit `backend/main.py`:

Find this section:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
```

Add your Vercel URL:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://kcl-student-bot.vercel.app",  # Your Vercel URL
        "https://*.vercel.app",                  # All Vercel preview URLs
    ],
```

Redeploy backend:
```bash
cd backend
railway up
```

---

## Step 5: Test Your Live App! (2 min)

1. Open your Vercel URL: `https://kcl-student-bot.vercel.app`
2. Send a test message: "What are the library hours?"
3. Test timetable sync
4. Test clear chat button

**If it works → You're done! 🎉**

---

## Troubleshooting

### Frontend Shows "Failed to connect"
- Check `frontend/.env.production` has correct backend URL
- Check backend CORS includes your Vercel URL
- Redeploy frontend: `vercel --prod`

### Backend Shows "Unhealthy"
- Check Railway logs: `railway logs`
- Verify all environment variables are set
- Check Python version in Railway settings (must be 3.9+)

### CORS Errors in Browser Console
- Update `backend/main.py` CORS settings
- Redeploy backend: `railway up`
- Hard refresh browser (Cmd+Shift+R)

---

## Commands Reference

### Deploy Backend
```bash
cd backend
railway up
```

### Deploy Frontend
```bash
cd frontend
vercel --prod
```

### View Backend Logs
```bash
cd backend
railway logs
```

### View Vercel Logs
```bash
cd frontend
vercel logs
```

---

## Cost

**Free tier is enough for moderate usage:**
- Railway: $5 free credit/month
- Vercel: Free for personal projects

---

## Auto-Deploy (Optional)

### Link to GitHub
Both Railway and Vercel can auto-deploy from GitHub:

**Railway:**
1. Go to Railway dashboard
2. Connect GitHub repository
3. Auto-deploys on push to main

**Vercel:**
1. Go to Vercel dashboard
2. Connect GitHub repository
3. Auto-deploys on push to main

**Then:** Just `git push` and both deploy automatically!

---

## Your Live URLs

After deployment, you'll have:

- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://your-app.railway.app
- **API Docs**: https://your-app.railway.app/docs

Share the frontend URL with friends! 🚀

---

**Need detailed instructions?** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
