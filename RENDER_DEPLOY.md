# 🚀 Deploy to Render - Complete Guide

## Why Render?

✅ Free tier available
✅ Automatic deployments from Git
✅ Built-in health checks
✅ Simpler configuration than Railway
✅ Better error logging

---

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- Your code pushed to GitHub

---

## Step 1: Push Code to GitHub (5 minutes)

### Option A: Create New Repository

```bash
cd /Users/harrisonzhao/Documents/KCL\ bot

# Initialize git if not already done
git init

# Create a new repository on GitHub (via web interface)
# Then connect it:
git remote add origin https://github.com/YOUR_USERNAME/kcl-student-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Use Existing Repository

```bash
cd /Users/harrisonzhao/Documents/KCL\ bot

# Add all changes
git add -A
git commit -m "Clean up and prepare for Render deployment"
git push origin main
```

---

## Step 2: Deploy Backend on Render (10 minutes)

### 2.1: Create Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `kcl-bot-backend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Free

### 2.2: Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** for each:

| Key | Value |
|-----|-------|
| `OPENROUTER_API_KEY` | `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` |
| `SUPABASE_URL` | `https://vmtuttkmxrxsozyrtirw.supabase.co` |
| `SUPABASE_KEY` | `sb_publishable_gUvKQxFlsT-QIuHgtTjyYg_EI1MdGqL` |
| `SERPAPI_API_KEY` | `71abaee6398044473d2d6cdf5bb61ab473b394ca74b5ba354e6741aed503b4de` |
| `FIRECRAWL_API_KEY` | `fc-7f6944361db34b1caf88b4044df2548c` |
| `APP_ENV` | `production` |
| `LOG_LEVEL` | `INFO` |

### 2.3: Create Service

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for build and deployment
3. You'll get a URL like: `https://kcl-bot-backend.onrender.com`

### 2.4: Test Backend

```bash
# Test health endpoint
curl https://kcl-bot-backend.onrender.com/health

# Should return:
# {"status":"healthy","service":"kcl-student-bot-api"}
```

---

## Step 3: Deploy Frontend on Render (10 minutes)

### 3.1: Update Frontend API URL

First, update the frontend to point to your Render backend:

```bash
cd /Users/harrisonzhao/Documents/KCL\ bot/frontend

# Create production environment file
cat > .env.production << EOF
REACT_APP_API_URL=https://kcl-bot-backend.onrender.com/api
EOF

# Commit the change
git add .env.production
git commit -m "Add Render backend URL to frontend"
git push origin main
```

### 3.2: Create Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository (same repo)
4. Configure:
   - **Name**: `kcl-bot-frontend`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Runtime**: `Node`
   - **Build Command**:
     ```
     npm install && npm run build
     ```
   - **Start Command**:
     ```
     npx serve -s build -l $PORT
     ```
   - **Plan**: Free

### 3.3: Add Environment Variable

Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://kcl-bot-backend.onrender.com/api` |

### 3.4: Create Service

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for build and deployment
3. You'll get a URL like: `https://kcl-bot-frontend.onrender.com`

---

## Step 4: Update Backend CORS (5 minutes)

The backend needs to allow requests from the frontend domain.

### 4.1: Update main.py

Edit `backend/main.py`:

```python
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://kcl-bot-frontend.onrender.com",  # ADD THIS LINE - your actual frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2: Push Update

```bash
cd /Users/harrisonzhao/Documents/KCL\ bot
git add backend/main.py
git commit -m "Add frontend URL to CORS"
git push origin main
```

Render will automatically redeploy the backend.

---

## Step 5: Test Complete Application

1. Open your frontend URL: `https://kcl-bot-frontend.onrender.com`
2. You should see the chat interface
3. Send a test message: "Hello"
4. Verify you get a response from the AI

---

## Common Issues & Solutions

### Issue: Backend build fails

**Solution**: Check the logs in Render dashboard → Your service → Logs

Common causes:
- Missing dependencies in `requirements.txt`
- Python version mismatch (add `runtime.txt` with `python-3.11.0`)

### Issue: Frontend shows "Network Error"

**Solution**:
1. Check frontend environment variable is correct
2. Verify backend CORS includes frontend URL
3. Check browser console for detailed error

### Issue: "Service Unavailable" after deployment

**Solution**:
- Render free tier services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- This is normal behavior on free tier

### Issue: Agent system errors

**Solution**:
- Check environment variables are set correctly in Render
- Verify API keys are valid
- Check Render logs for detailed error messages

---

## Free Tier Limitations

⚠️ **Important**: Render free tier has limitations:

- Services sleep after 15 minutes of inactivity
- 750 hours/month of runtime
- Slower cold starts
- Lower bandwidth

For production use, consider upgrading to paid tier ($7/month per service).

---

## Monitoring & Logs

### View Logs

1. Go to Render dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time logs

### Set Up Alerts

1. Service settings → **"Notifications"**
2. Add email/Slack webhook
3. Get notified of deployment failures

---

## Automatic Deployments

✅ Render automatically redeploys when you push to GitHub!

```bash
# Make a change
cd /Users/harrisonzhao/Documents/KCL\ bot
# Edit some files...
git add .
git commit -m "Update feature"
git push origin main

# Render will automatically:
# 1. Detect the push
# 2. Build the new version
# 3. Deploy it
# 4. Switch traffic to new version
```

---

## Custom Domain (Optional)

To use your own domain:

1. Render dashboard → Your service → **"Settings"**
2. Scroll to **"Custom Domain"**
3. Add your domain
4. Update DNS records as instructed
5. SSL certificate is automatic and free!

---

## Next Steps

✅ Backend deployed and healthy
✅ Frontend deployed and working
✅ Chat functionality works
✅ Automatic deployments enabled

🎉 **Your KCL Student Bot is now live!**

---

## Useful Commands

```bash
# View backend logs
curl https://kcl-bot-backend.onrender.com/

# Test health
curl https://kcl-bot-backend.onrender.com/health

# Test API docs (FastAPI auto-generated)
open https://kcl-bot-backend.onrender.com/docs
```

---

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev

---

**Questions?** Check Render logs first - they're very detailed and helpful! 🔍
