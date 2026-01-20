# 🔧 Railway Settings Fix - Port Configuration

## The Problem

Your deployment shows:
- ✅ Build: Success
- ✅ Deploy: Success
- ❌ **Healthcheck: FAILED**
- Status: **"Unexposed service"**

**This means:** The app is running but not listening on the correct port that Railway expects.

---

## ✅ I've Fixed The Configuration Files

Updated these files:
1. **railway.json** - Explicit start command with port binding
2. **nixpacks.toml** - Better Python setup
3. **Increased healthcheck timeout** to 300 seconds

---

## 🛠️ You Need To: Update Railway Settings

Since I can't redeploy directly (multiple services issue), **please do this in Railway dashboard**:

### Step 1: Open Settings

In your Railway dashboard:
1. Click on the **"Settings"** tab
2. Scroll to the **"Deploy"** section

### Step 2: Set Start Command

Find **"Custom Start Command"** and set it to:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Generate Domain (Expose Service)

1. Scroll to **"Networking"** section
2. Click **"Generate Domain"** if not already done
3. This will expose your service publicly

### Step 4: Check Variables

Make sure **PORT** variable is set (Railway usually sets this automatically, but verify):
- Go to **"Variables"** tab
- Railway should automatically provide `$PORT`
- If not, you don't need to add it manually (Railway injects it)

### Step 5: Redeploy

1. Go back to **"Deployments"** tab
2. Click the **3 dots** on the latest deployment
3. Click **"Redeploy"**

OR just click **"Deploy"** button in top right

---

## 🎯 Expected Result

After redeploying with the correct start command:

1. Build: ✅ Success
2. Deploy: ✅ Success
3. **Healthcheck: ✅ Success** (this should now pass!)

Then test:
```bash
curl https://kbot13-production.up.railway.app/health
```

Should return: `{"status":"healthy","service":"kcl-student-bot-api"}`

---

## 📋 Quick Checklist

In Railway dashboard, verify:

- [ ] Settings → Deploy → Start Command = `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Settings → Networking → Domain is generated
- [ ] Variables → All 5 environment variables are set (especially full Supabase key)
- [ ] Redeploy the service

---

## 🔍 Why This Happened

**The issue:** Railway couldn't connect to your app because:
1. The app wasn't binding to the correct port (`$PORT`)
2. OR the start command wasn't properly configured
3. OR the service wasn't exposed with a public domain

**The fix:** Explicitly tell Railway to start uvicorn on `$PORT` with host `0.0.0.0`

---

## ⚡ After It Works

Once healthcheck passes, update your frontend:

```bash
# Edit frontend/.env.production
REACT_APP_API_URL=https://kbot13-production.up.railway.app/api

# Deploy frontend
cd frontend
vercel --prod
```

---

**Next:** Go to Railway dashboard → Settings → Update start command → Redeploy! 🚀
