# ✅ npm Permissions Fixed!

## What I Did

1. ✅ Created `~/.npm-global` directory for global packages
2. ✅ Configured npm to use this directory (no more sudo needed)
3. ✅ Added to your PATH in `~/.zshrc`
4. ✅ Installed Railway CLI (version 4.26.0)
5. ✅ Installed Vercel CLI (version 50.4.8)

## How to Use

### In Your Current Terminal

The commands should work immediately:

```bash
railway --version
vercel --version
```

### In New Terminals

Open a **new terminal window** and the commands will work automatically:

```bash
railway login
vercel login
```

## Important Notes

⚠️ **If commands don't work in a new terminal:**

1. Close all terminal windows
2. Open a brand new terminal
3. Try again - the PATH should be loaded automatically

The PATH was added to `~/.zshrc` which loads every time you open a new terminal.

## Deployment Commands

You can now deploy without `npx` or `sudo`:

### Deploy Backend to Railway:

```bash
cd backend
railway login
railway init
railway variables set OPENROUTER_API_KEY="your_key"
railway variables set SUPABASE_URL="your_url"
railway variables set SUPABASE_KEY="your_key"
railway variables set SERPAPI_API_KEY="your_key"
railway variables set FIRECRAWL_API_KEY="your_key"
railway up
railway domain
```

### Deploy Frontend to Vercel:

```bash
cd frontend
vercel login
vercel --prod
```

## Verify Installation

Run these commands to verify everything works:

```bash
railway --version    # Should show: railway 4.26.0
vercel --version     # Should show: Vercel CLI 50.4.8
```

## Troubleshooting

**If commands still not found:**

1. Reload your shell configuration:
   ```bash
   source ~/.zshrc
   ```

2. Or open a new terminal window

3. Verify PATH includes npm-global:
   ```bash
   echo $PATH
   ```
   Should include: `/Users/harrisonzhao/.npm-global/bin`

---

**Status: Ready to Deploy!** 🚀

Next step: See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for deployment instructions.
