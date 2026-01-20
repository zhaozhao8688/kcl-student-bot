# 🎯 Render UI Guide - Where to Find Everything

## When Creating a New Web Service

After you click "New +" → "Web Service" and connect your GitHub repo, you'll see a form with these fields:

---

## 📝 Fields You'll See (In Order)

### 1. **Name**
- Enter: `kcl-bot-backend`

### 2. **Region**
- Select: Oregon (US West) or Singapore

### 3. **Branch**
- Select: `main`

### 4. **Root Directory** (Important!)
- Enter: `backend`
- ⚠️ This tells Render to look in the /backend folder

### 5. **Runtime**
- It should auto-detect: `Python 3`
- If not, select: `Python 3` from dropdown

### 6. **Build Command** ← HERE IT IS!
- Enter exactly:
  ```
  pip install --upgrade pip && pip install -r requirements.txt
  ```

### 7. **Start Command** ← HERE IT IS!
- Enter exactly:
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### 8. **Instance Type**
- Select: `Free` ($0/month)

---

## 🔧 Don't See Build Command or Start Command?

### Option A: Scroll Down
They might be below the fold. Scroll down on the page.

### Option B: Look for "Advanced" Button
Some versions of Render UI hide these under an "Advanced" section. Click "Advanced" to expand.

### Option C: They Might Auto-Detect
If Render sees your `requirements.txt`, it might auto-fill these commands. Check if they're already filled in!

---

## 🌟 Adding Environment Variables

After entering the commands above, look for:

**"Environment Variables"** or **"Add Environment Variable"** button

Click it and add these one by one:

| Variable Name | Value |
|---------------|-------|
| `OPENROUTER_API_KEY` | `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` |
| `SUPABASE_URL` | `https://vmtuttkmxrxsozyrtirw.supabase.co` |
| `SUPABASE_KEY` | `sb_publishable_gUvKQxFlsT-QIuHgtTjyYg_EI1MdGqL` |
| `SERPAPI_API_KEY` | `71abaee6398044473d2d6cdf5bb61ab473b394ca74b5ba354e6741aed503b4de` |
| `FIRECRAWL_API_KEY` | `fc-7f6944361db34b1caf88b4044df2548c` |
| `APP_ENV` | `production` |
| `LOG_LEVEL` | `INFO` |

---

## 📸 What the Form Looks Like

```
┌─────────────────────────────────────────┐
│  Name: kcl-bot-backend                  │
├─────────────────────────────────────────┤
│  Region: [Oregon ▼]                     │
├─────────────────────────────────────────┤
│  Branch: [main ▼]                       │
├─────────────────────────────────────────┤
│  Root Directory: backend                │
├─────────────────────────────────────────┤
│  Runtime: [Python 3 ▼]                  │
├─────────────────────────────────────────┤
│  Build Command:                         │
│  pip install --upgrade pip && ...       │
├─────────────────────────────────────────┤
│  Start Command:                         │
│  uvicorn main:app --host 0.0.0.0 ...    │
├─────────────────────────────────────────┤
│  Instance Type: [Free ▼]                │
├─────────────────────────────────────────┤
│  [Advanced ▼]                           │
│    • Environment Variables              │
│    • Auto-Deploy                        │
│    • Health Check Path                  │
└─────────────────────────────────────────┘

        [Create Web Service]
```

---

## 🚨 Alternative: Use render.yaml Instead

If you can't find the command fields, Render can read from `render.yaml` file!

You already have this file in your repo root: `render.yaml`

### Using render.yaml (Easier!)

1. In Render dashboard, click "New +" → "Blueprint"
2. Select your repo
3. Render will read the `render.yaml` file
4. Click "Apply" to create both services automatically!

**This is actually EASIER** because:
- ✅ Creates backend AND frontend at once
- ✅ All commands already configured in the file
- ✅ You just need to add environment variables

---

## 🎯 Recommended: Use Blueprint (render.yaml)

### Step 1: Create Blueprint

1. Render Dashboard: https://dashboard.render.com
2. Click **"New +"**
3. Select **"Blueprint"** (not "Web Service"!)
4. Connect your GitHub repo: `kcl-student-bot`
5. Render will detect `render.yaml`
6. Review the configuration
7. Click **"Apply"**

### Step 2: Add Environment Variables

After it creates the services:

1. Click on **"kcl-bot-backend"** service
2. Go to **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add all 7 variables from the table above

### Step 3: Done!

Render will automatically:
- Build your backend
- Build your frontend
- Deploy both services
- Give you URLs

---

## ✅ Which Method Should You Use?

### Use Blueprint (Recommended) ✨
- Easier
- Creates both services at once
- All commands already in render.yaml

### Use Manual Web Service
- More control
- Good if you only want to deploy backend first

---

## 🆘 Still Can't Find It?

Take a screenshot and share it, or try the Blueprint method instead!

Blueprint link: https://dashboard.render.com/select-repo?type=blueprint

---

**Next**: Once services are created, test the health endpoint! 🚀
