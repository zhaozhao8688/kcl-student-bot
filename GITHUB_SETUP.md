# 📦 Push Your Code to GitHub

## Your GitHub Account

✅ **Username**: zhaozhao8688
✅ **Repository**: kcl-student-bot (needs to be created)

---

## Step 1: Create Repository on GitHub (2 minutes)

### Option A: Quick Create (Easiest)

1. **Go to**: https://github.com/new

2. **Fill in**:
   - Repository name: `kcl-student-bot`
   - Description: `KCL Student Bot - AI assistant for King's College London students`
   - Visibility: **Public** (or Private if you prefer)
   - ❌ **DO NOT** check "Add a README file"
   - ❌ **DO NOT** check "Add .gitignore"
   - ❌ **DO NOT** choose a license yet

3. Click **"Create repository"**

### Option B: From GitHub Homepage

1. Go to https://github.com
2. Click the **"+"** icon (top right)
3. Select **"New repository"**
4. Follow same settings as Option A above

---

## Step 2: Push Your Code (30 seconds)

After creating the repo on GitHub, run these commands:

```bash
cd /Users/harrisonzhao/Documents/KCL\ bot

# Push to GitHub
git push -u origin main
```

If it asks for authentication:
- **Username**: zhaozhao8688
- **Password**: Use a Personal Access Token (not your GitHub password)

### Need a Personal Access Token?

If you don't have one:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name it: `KCL Bot Deployment`
4. Check: `repo` (full control of private repositories)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

---

## Step 3: Verify Upload

After pushing, go to:
https://github.com/zhaozhao8688/kcl-student-bot

You should see your code! 🎉

---

## Next: Deploy to Render

Once your code is on GitHub, follow:
- [QUICK_START_RENDER.md](./QUICK_START_RENDER.md) - Quick deployment
- [RENDER_DEPLOY.md](./RENDER_DEPLOY.md) - Detailed guide

---

## Alternative: Use GitHub Desktop (Visual Tool)

If you prefer a GUI instead of command line:

1. Download: https://desktop.github.com
2. Install and sign in with your GitHub account
3. File → Add Local Repository → Choose your folder
4. Click "Publish repository"
5. Done! ✅

---

## Troubleshooting

### "Repository not found" error
- Make sure you created the repo on GitHub first
- Check the repo name matches exactly: `kcl-student-bot`

### Authentication failed
- Use a Personal Access Token, not your password
- Create one at: https://github.com/settings/tokens

### "Updates were rejected"
- The remote has changes you don't have locally
- Run: `git pull origin main --rebase` then `git push`

---

**Next Step**: Create the repository on GitHub, then run `git push -u origin main`! 🚀
