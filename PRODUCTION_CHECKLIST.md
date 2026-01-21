# Production Deployment Checklist

## Security
- [ ] All API keys removed from `render.yaml`
- [ ] Environment variables set in Render dashboard
- [ ] `.env` file not committed to git
- [ ] API keys rotated if repo was ever public

## Code Quality
- [ ] No console.log in production code
- [ ] No unused dependencies
- [ ] No __pycache__ in git

## Configuration
- [ ] CORS includes production frontend URL
- [ ] Backend deployed and healthy
- [ ] Frontend deployed and connects to backend
- [ ] Health endpoint responds: /health

## Testing
- [ ] Local backend starts: `uvicorn main:app`
- [ ] Local frontend starts: `npm start`
- [ ] Can send message and get response
- [ ] Timetable sync works
- [ ] Clear chat works

## Documentation
- [ ] README.md is up to date
- [ ] Deployment guides are current
- [ ] No outdated guides in root

## Post-Deployment Verification

### Backend
```bash
curl https://kcl-bot-backend.onrender.com/health
```
Expected: `{"status":"healthy","service":"kcl-student-bot-api"}`

### Frontend
Visit: https://kcl-bot-frontend.onrender.com
- [ ] Page loads successfully
- [ ] Can open timetable modal
- [ ] Can send a message
- [ ] Receives AI response
- [ ] Browser console has no errors

## Environment Variables to Set in Render Dashboard

### Backend Service
1. `OPENROUTER_API_KEY` - OpenRouter API key for LLM access
2. `SUPABASE_URL` - Supabase project URL
3. `SUPABASE_KEY` - Supabase anonymous/public key
4. `SERPAPI_API_KEY` - SerpAPI key for search functionality
5. `FIRECRAWL_API_KEY` - Firecrawl API key for web scraping
6. `APP_ENV` - Set to "production"
7. `LOG_LEVEL` - Set to "INFO"

### Frontend Service
1. `REACT_APP_API_URL` - Set to "https://kcl-bot-backend.onrender.com/api"

## Rollback Plan

If deployment breaks:
```bash
git revert HEAD~4..HEAD  # Reverts last 4 commits
git push origin main
```

If frontend won't build:
```bash
cd frontend
npm install  # Reinstall all dependencies
```

If backend won't start:
- Check Render logs for errors
- Verify environment variables set in dashboard
- Check CORS configuration

## Success Criteria

All checkboxes above should be checked before considering the deployment production-ready.
