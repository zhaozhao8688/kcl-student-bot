# 🔧 Railway Deployment Fix

## Issue Identified

Your deployment failed. Here's how to fix it:

---

## Problem 1: Supabase Key Incomplete

Your Supabase key looks incomplete:
```
sb_publishable_gUvKQxFlsT-QIuHgtTjyYg_EI1MdGqL
```

This should be much longer (starts with `eyJ...`).

### Fix: Get the Correct Supabase Key

1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **API**
4. Copy the **`anon` key** (public) - it's very long, starts with `eyJ`

---

## Problem 2: Railway Service Not Linked

Let me help you redeploy properly.

---

## Solution: Redeploy with Correct Configuration

### Step 1: Update Supabase Key in Railway

```bash
# In your terminal, set the CORRECT Supabase key
railway variables set SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZtdHV0dGtteHJ4c296eXJ0aXJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ0NTA2NzIsImV4cCI6MjA1MDAyNjY3Mn0.YOUR_ACTUAL_KEY_HERE"
```

Replace with your actual key from Supabase dashboard!

---

### Step 2: Redeploy

I've added better configuration files. Now redeploy:

```bash
cd backend
railway up
```

---

### Step 3: Check the Deployment

```bash
# Get your domain
railway domain

# Check if it's healthy (replace with your actual URL)
curl https://your-app.railway.app/health
```

---

## Alternative: Use Railway Dashboard

If CLI deployment keeps failing:

### 1. Go to Railway Dashboard
- Visit: https://railway.com/dashboard
- Find your project

### 2. Check Environment Variables
Make sure these are all set correctly:
- `OPENROUTER_API_KEY` = `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`
- `SUPABASE_URL` = `https://vmtuttkmxrxsozyrtirw.supabase.co`
- `SUPABASE_KEY` = **[Get the long eyJ... key from Supabase]**
- `SERPAPI_API_KEY` = `71abaee6398044473d2d6cdf5bb61ab473b394ca74b5ba354e6741aed503b4de`
- `FIRECRAWL_API_KEY` = `fc-7f6944361db34b1caf88b4044df2548c`

### 3. Check Build Logs
- Click on your service
- Go to "Deployments" tab
- Click on the failed deployment
- Read the logs to see the exact error

### 4. Manual Redeploy
- In the Railway dashboard
- Click "Deploy" button
- Or push a small change to trigger rebuild

---

## Configuration Files Added

I've created these files to help deployment:

1. ✅ `backend/runtime.txt` - Specifies Python 3.11
2. ✅ `backend/nixpacks.toml` - Railway build config
3. ✅ `backend/railway.json` - Updated deployment settings
4. ✅ `backend/Procfile` - Start command

---

## Common Deployment Errors

### Error: "Module not found"
**Fix**: Make sure all dependencies are in `requirements.txt`

### Error: "Port already in use"
**Fix**: Railway handles this automatically, use `$PORT` variable

### Error: "Database connection failed"
**Fix**: Check Supabase key is correct and complete

### Error: "Environment variable not set"
**Fix**: Set all required variables in Railway dashboard

---

## Quick Commands

```bash
# Check Railway status
railway status

# View logs
railway logs

# Get your URL
railway domain

# Redeploy
railway up

# Open Railway dashboard
railway open
```

---

## Next Steps

1. **Get correct Supabase key** from dashboard (the long `eyJ...` one)
2. **Set it in Railway**: `railway variables set SUPABASE_KEY="eyJ..."`
3. **Redeploy**: `railway up`
4. **Test**: `curl https://your-app.railway.app/health`

---

## If Still Failing

Share the Railway logs with me:
```bash
railway logs
```

Or check the logs in Railway dashboard → Your Service → Deployments → View Logs

---

**Most common fix:** Update the SUPABASE_KEY to the complete `eyJ...` key! 🔑
