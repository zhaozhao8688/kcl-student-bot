# ⚡ Quick Start - Deploy to Render (15 minutes)

## Step 1: Push to GitHub (3 minutes)

```bash
cd /Users/harrisonzhao/Documents/KCL\ bot

# Create new repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/kcl-student-bot.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend (5 minutes)

1. Go to https://render.com → Sign up/Login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. **Settings**:
   - Name: `kcl-bot-backend`
   - Root Directory: `backend`
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables** (click Advanced):
   ```
   OPENROUTER_API_KEY=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
   SUPABASE_URL=https://vmtuttkmxrxsozyrtirw.supabase.co
   SUPABASE_KEY=sb_publishable_gUvKQxFlsT-QIuHgtTjyYg_EI1MdGqL
   SERPAPI_API_KEY=71abaee6398044473d2d6cdf5bb61ab473b394ca74b5ba354e6741aed503b4de
   FIRECRAWL_API_KEY=fc-7f6944361db34b1caf88b4044df2548c
   APP_ENV=production
   LOG_LEVEL=INFO
   ```

6. Click **"Create Web Service"**
7. Wait 5-10 minutes
8. Get your URL: `https://kcl-bot-backend.onrender.com`

## Step 3: Update Frontend Config (2 minutes)

```bash
cd /Users/harrisonzhao/Documents/KCL\ bot/frontend

# Create .env.production file
echo "REACT_APP_API_URL=https://kcl-bot-backend.onrender.com/api" > .env.production

git add .env.production
git commit -m "Add backend URL"
git push
```

## Step 4: Deploy Frontend (5 minutes)

1. Render dashboard → **"New +"** → **"Web Service"**
2. Same GitHub repo
3. **Settings**:
   - Name: `kcl-bot-frontend`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Start Command: `npx serve -s build -l $PORT`
   - Environment Variable:
     ```
     REACT_APP_API_URL=https://kcl-bot-backend.onrender.com/api
     ```

4. Click **"Create Web Service"**
5. Wait 5-10 minutes
6. Get your URL: `https://kcl-bot-frontend.onrender.com`

## Step 5: Update CORS (2 minutes)

Edit `backend/main.py`:

```python
allow_origins=[
    "http://localhost:3000",
    "https://kcl-bot-frontend.onrender.com",  # Add this
],
```

Push:
```bash
git add backend/main.py
git commit -m "Add CORS for frontend"
git push
```

## ✅ Done!

Open: `https://kcl-bot-frontend.onrender.com`

---

**Note**: First load takes 30-60 seconds (free tier cold start). After that, it's fast!

Full guide: [RENDER_DEPLOY.md](./RENDER_DEPLOY.md)
