# 🚀 Alternative: Deploy to Render (Easier!)

If Railway keeps having issues, **Render** is easier for Python apps!

---

## ✅ Deploy Backend to Render (5 minutes)

### Step 1: Create Render Account
1. Go to **https://render.com**
2. Click **"Sign Up"**
3. Sign up with GitHub (easiest)

### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Click **"Connect a repository"**
3. Connect your GitHub account
4. Select your **KCL bot repository**

### Step 3: Configure Service

Fill in these settings:

- **Name**: `kcl-student-bot-api`
- **Region**: Oregon (US West) or closest to you
- **Branch**: `main` (or your branch name)
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 4: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**

Add these **5 variables**:

| Key | Value |
|-----|-------|
| `OPENROUTER_API_KEY` | `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` |
| `SUPABASE_URL` | `https://vmtuttkmxrxsozyrtirw.supabase.co` |
| `SUPABASE_KEY` | `eyJ...` (get full key from Supabase) |
| `SERPAPI_API_KEY` | `71abaee6398044473d2d6cdf5bb61ab473b394ca74b5ba354e6741aed503b4de` |
| `FIRECRAWL_API_KEY` | `fc-7f6944361db34b1caf88b4044df2548c` |

⚠️ **IMPORTANT**: Get the **full** Supabase key from:
- Supabase Dashboard → Settings → API → Copy `anon` key

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build
3. You'll get a URL like: `https://kcl-student-bot-api.onrender.com`

### Step 6: Test It

```bash
curl https://your-app.onrender.com/health
```

Should return: `{"status":"healthy","service":"kcl-student-bot-api"}`

---

## ✅ Why Render is Easier

- ✓ Better Python detection
- ✓ Clear dashboard interface
- ✓ Free tier available
- ✓ No CLI issues
- ✓ Auto-deploys from GitHub

---

## 🎯 After Backend Deploys Successfully

Copy your Render URL (e.g., `https://kcl-student-bot-api.onrender.com`)

Then deploy frontend to Vercel:

```bash
cd frontend

# Edit .env.production with your Render URL
# REACT_APP_API_URL=https://your-app.onrender.com/api

vercel --prod
```

---

## 📋 Complete Checklist

### Backend (Render):
- [ ] Sign up at render.com
- [ ] Create new Web Service
- [ ] Set root directory to `backend`
- [ ] Add 5 environment variables (with FULL Supabase key!)
- [ ] Deploy and wait for build
- [ ] Test: `curl https://your-app.onrender.com/health`
- [ ] Copy your Render URL

### Frontend (Vercel):
- [ ] Update `frontend/.env.production` with Render URL
- [ ] Deploy: `vercel --prod`
- [ ] Update backend CORS with Vercel URL
- [ ] Redeploy backend
- [ ] Test live app!

---

## ⚠️ Free Tier Limitations

**Render Free Tier:**
- Automatically spins down after 15 min of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month free

**For always-on service**, upgrade to paid ($7/month)

---

## 🆚 Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| Setup | CLI required | Web dashboard |
| Python detection | Sometimes fails | Always works |
| Free tier | $5 credit | 750 hours |
| Cold starts | No | Yes (15 min) |
| Ease of use | Medium | Easy |

**Recommendation**: Use **Render** for simplicity! 🎯

---

## Need Help?

Render has great docs: https://render.com/docs/web-services

Or try Railway one more time with the updated railway.json!
