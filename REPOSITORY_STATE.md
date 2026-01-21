# Repository State Summary

Last updated: 2026-01-21

## 🎯 Current Status

The KCL Student Bot is a **fully functional AI-powered chat assistant** built with React and FastAPI. The latest version (v2.1) includes Instagram/TikTok scraping, real-time streaming, and a ReAct agent architecture. All features are working and production-ready.

---

## 📊 Key Features Implemented

### ✅ Core Features
- **Modern React UI** with Tailwind CSS
- **Markdown Support** for formatted AI responses (react-markdown)
- **Web Search** via SerpAPI for KCL-related queries
- **Timetable Integration** using iCal URLs
- **AI-Powered Responses** via OpenRouter
- **Configurable AI Models** via environment variables
- **Chat History** persisted in Supabase
- **Session Management** for multi-turn conversations
- **Auto-retry on Errors** with startup API key verification

### ✅ v2.1 Features (Current Release)
1. **Instagram Scraping** - via Apify
   - Scrape Instagram posts, profiles, and hashtags
   - Extract engagement metrics, captions, and media URLs
   - Configurable via `APIFY_API_TOKEN`

2. **TikTok Scraping** - via Apify
   - Scrape TikTok videos, profiles, and hashtags
   - Extract view counts, likes, and video metadata
   - Uses same `APIFY_API_TOKEN` as Instagram

3. **Real-Time Streaming** - Server-Sent Events (SSE)
   - Stream agent responses in real-time
   - Show intermediate tool execution results
   - AgentLogs UI component for visibility

4. **ReAct Agent Architecture** - Reasoning + Acting loop
   - LLM dynamically selects tools based on user query
   - Iterative execution until task is complete
   - More intelligent tool orchestration than linear pipelines

### ✅ Previous Additions
1. **Markdown Rendering** - AI responses now support:
   - Headers (h1, h2, h3)
   - Lists (ordered and unordered)
   - Code blocks with syntax highlighting
   - Links (open in new tab)
   - Bold, italic, blockquotes
   - GitHub Flavored Markdown (tables, etc.)

2. **Model Configuration** - Easy switching between AI models:
   - Configured via `DEFAULT_MODEL` environment variable
   - No code changes needed
   - Supports Claude, GPT, Gemini, Llama models
   - Documented in MODEL_CONFIGURATION.md

3. **OpenRouter Error Handling** - Fixed 401 "User not found" errors:
   - Added HTTP headers (HTTP-Referer, X-Title)
   - Implemented lazy initialization for singletons
   - Added startup API key verification
   - Enhanced health check endpoint
   - Created debug scripts (debug_openrouter.sh, verify_setup.sh)

---

## 📁 Repository Structure

```
kcl-student-bot/
├── backend/                          # FastAPI Backend
│   ├── main.py                      # API entry point (with startup verification)
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Local environment variables (not in git)
│   ├── .env.example                 # Template for environment setup
│   ├── debug_openrouter.sh          # Debug script for OpenRouter issues
│   ├── verify_setup.sh              # Pre-flight verification script
│   ├── OPENROUTER_DEBUG_README.md   # Troubleshooting guide
│   ├── api/                         # API endpoints
│   │   ├── chat.py                  # Chat endpoints (with streaming)
│   │   ├── timetable.py             # Timetable endpoints
│   │   └── session.py               # Session management
│   ├── config/                      # Configuration
│   │   └── settings.py              # Pydantic settings (reads .env)
│   ├── services/                    # Services
│   │   ├── llm_service.py           # OpenRouter LLM service (with headers)
│   │   └── supabase_service.py      # Database service
│   ├── agents/                      # ReAct Agent System
│   │   ├── react_graph.py           # ReAct agent graph (NEW)
│   │   ├── react_nodes.py           # ReAct node implementations (NEW)
│   │   ├── react_state.py           # ReAct state definition (NEW)
│   │   └── prompts.py               # Agent prompts (NEW)
│   ├── tools/                       # Tools
│   │   ├── search_tool.py           # SerpAPI search
│   │   ├── scraper_tool.py          # Firecrawl scraper
│   │   ├── timetable_tool.py        # iCal parser
│   │   ├── instagram_tool.py        # Instagram scraping (NEW)
│   │   ├── tiktok_tool.py           # TikTok scraping (NEW)
│   │   ├── tool_definitions.py      # LLM tool schemas (NEW)
│   │   └── tool_registry.py         # Tool registration
│   └── core/                        # Core logic
│       ├── session.py               # Session manager
│       ├── chat_processor.py        # Chat processor
│       └── stream_processor.py      # SSE streaming (NEW)
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── App.js                   # Main application (with streaming)
│   │   ├── components/
│   │   │   ├── Header.jsx           # App header
│   │   │   ├── ChatMessage.jsx      # Message bubble (with Markdown)
│   │   │   ├── ChatInput.jsx        # Input field
│   │   │   ├── TimetableModal.jsx   # Timetable modal
│   │   │   └── AgentLogs.jsx        # Real-time agent logs (NEW)
│   │   └── services/
│   │       └── api.js               # API client (with SSE)
│   ├── package.json                 # Dependencies (includes react-markdown)
│   └── tailwind.config.js           # Tailwind configuration
│
├── Documentation/                    # All .md files
├── PRD.md                           # Product requirements document
├── REPOSITORY_STATE.md              # This file
├── start_local.sh                   # Automated local startup script
└── render.yaml                      # Render deployment config

```

---

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# OpenRouter API
OPENROUTER_API_KEY=sk-or-v1-...
DEFAULT_MODEL=anthropic/claude-3.5-sonnet

# Database
SUPABASE_URL=https://...
SUPABASE_KEY=...

# Tools
SERPAPI_API_KEY=...
FIRECRAWL_API_KEY=...
APIFY_API_TOKEN=...  # For Instagram & TikTok scraping

# App Config
APP_ENV=development
LOG_LEVEL=INFO
```

#### Frontend (.env.local)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

#### Render (Environment Variables)
All backend environment variables must be set in the Render dashboard, including the new `DEFAULT_MODEL` variable.

---

## 📚 Documentation Files

### Core Documentation
- **README.md** - Main project overview (UPDATED with new features)
- **MIGRATION_README.md** - Architecture details

### Getting Started
- **LOCAL_TESTING.md** - Automated local setup (uses start_local.sh)
- **GETTING_STARTED.md** - Manual setup guide
- **start_local.sh** - One-command startup script

### Deployment
- **QUICK_START_RENDER.md** - 15-minute Render deployment
- **RENDER_DEPLOY.md** - Detailed deployment with screenshots
- **RENDER_UI_GUIDE.md** - Navigating Render dashboard
- **render.yaml** - Render configuration file

### Configuration & Troubleshooting
- **MODEL_CONFIGURATION.md** - How to change AI models
- **backend/OPENROUTER_DEBUG_README.md** - Fix OpenRouter 401 errors
- **WHICH_URL.md** - Understanding URLs
- **SECURITY_NOTE.md** - Security best practices
- **PRODUCTION_CHECKLIST.md** - Pre-deployment checklist

### Setup & Git
- **GITHUB_SETUP.md** - GitHub repository setup

### Removed (Cleanup)
- ~~LOCAL_TEST.md~~ - Outdated, replaced by LOCAL_TESTING.md
- ~~NPM_SETUP_COMPLETE.md~~ - Temporary setup note, removed

---

## 🚀 Tech Stack

### Frontend
- **React** 18.2.3
- **Tailwind CSS** 3.4.19
- **React Markdown** 10.1.0 (NEW)
- **Remark GFM** 4.0.1 (NEW)
- **Axios** 1.13.2
- **Lucide React** 0.562.0

### Backend
- **FastAPI** (latest)
- **Python** 3.9+
- **Uvicorn** (ASGI server)
- **Pydantic Settings** (config management)

### AI & Agent System
- **LangGraph** (agent workflow orchestration)
- **OpenRouter** (LLM gateway)
- **OpenAI SDK** (for OpenRouter API)

### Database & Storage
- **Supabase** (PostgreSQL + Auth)

### Tools & Integrations
- **SerpAPI** (Google search)
- **Firecrawl** (web scraping)
- **iCalendar** (timetable parsing)

---

## 🎨 Current AI Model

**Default Model**: `anthropic/claude-3.5-sonnet`

**Configurable via**:
- Local: `backend/.env` → `DEFAULT_MODEL=...`
- Render: Environment variable `DEFAULT_MODEL`

**Available Models**:
- Anthropic: claude-opus-4.5, claude-3.5-sonnet, claude-3.5-haiku
- OpenAI: gpt-5, gpt-5-mini, gpt-4o
- Google: gemini-3-flash-preview, gemini-2.5-pro
- Meta: llama-3.3-70b
- See MODEL_CONFIGURATION.md for full list

---

## 🔑 API Keys Status

### Required Keys
1. ✅ **OPENROUTER_API_KEY** - LLM access (working key in .env)
2. ✅ **SUPABASE_URL** + **SUPABASE_KEY** - Database
3. ✅ **SERPAPI_API_KEY** - Web search
4. ✅ **FIRECRAWL_API_KEY** - Web scraping
5. ✅ **APIFY_API_TOKEN** - Instagram & TikTok scraping

### Key Validation
- **Startup verification** - Backend tests OpenRouter key on startup
- **Health check** - `/health` endpoint shows key configuration status
- **Debug scripts** - `verify_setup.sh` tests keys before starting

---

## 🛠️ Development Workflow

### Local Development
```bash
# Quick start (automated)
./start_local.sh

# Manual start
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

### Testing
```bash
# Backend health
curl http://localhost:8000/health

# Chat API
curl -X POST http://localhost:8000/api/chat/message \
  -H 'Content-Type: application/json' \
  -d '{"query":"test","session_id":"test-123"}'
```

### Changing AI Model
```bash
# Edit backend/.env
DEFAULT_MODEL=anthropic/claude-opus-4.5

# Restart backend
# Changes take effect immediately
```

---

## 🚢 Deployment Status

### Current Deployment
- **Platform**: Render
- **Backend URL**: https://kcl-bot-backend.onrender.com
- **Frontend URL**: https://kcl-bot-frontend.onrender.com
- **Status**: Ready to deploy

### Deployment Files
- `render.yaml` - Configuration for both services
- Environment variables set in Render dashboard

### Important Notes
- Backend must be deployed before frontend
- Frontend needs backend URL in environment
- All API keys must be set in Render dashboard
- `DEFAULT_MODEL` can be configured in Render

---

## 🔍 Recent Changes (Commit History)

```
05166af - Clean up documentation and update README
27cf860 - Add Markdown support for chat output
51bc5f9 - Add model configuration documentation
3db3fae - Make AI model configurable via environment variable
578329b - Change model to Gemini and fix OpenRouter 401 errors
ad466b0 - Add production checklist and verify CORS
80c7e38 - Consolidate documentation
```

---

## 🐛 Known Issues & Solutions

### OpenRouter 401 Errors
**Issue**: "User not found" after changing API keys
**Cause**: Singleton caching in Python
**Solution**: Use `debug_openrouter.sh` or fully restart backend
**Prevention**: Lazy initialization implemented, startup verification added
**Documentation**: backend/OPENROUTER_DEBUG_README.md

### Model Not Changing
**Issue**: Model doesn't change after updating .env
**Solution**: Fully restart backend (not just reload)
**Verification**: Check startup logs for model name

---

## 📈 Next Steps / Future Enhancements

Potential improvements (not implemented):
- [ ] Code syntax highlighting in Markdown (syntax-highlighter package)
- [x] ~~Streaming responses for faster UX~~ (IMPLEMENTED in v2.1)
- [ ] User authentication
- [ ] Rate limiting
- [ ] Caching for repeated queries
- [ ] Analytics/usage tracking

---

## 🎯 Quick Reference

### Startup
```bash
./start_local.sh
```

### Change Model
```bash
echo "DEFAULT_MODEL=anthropic/claude-opus-4.5" >> backend/.env
```

### Debug OpenRouter
```bash
cd backend
./verify_setup.sh
./debug_openrouter.sh
```

### Deploy to Render
```bash
git push origin main
# Then manual deploy in Render dashboard
```

### View Documentation
- All docs: https://github.com/zhaozhao8688/kcl-student-bot
- Main README: README.md
- Quick start: LOCAL_TESTING.md
- Model config: MODEL_CONFIGURATION.md
- Troubleshooting: backend/OPENROUTER_DEBUG_README.md

---

## ✅ Quality Checklist

- [x] All features working
- [x] Documentation updated and accurate
- [x] No duplicate/outdated files
- [x] Environment variables documented
- [x] API keys validated on startup
- [x] Error handling implemented
- [x] Health check endpoint
- [x] Debug tools provided
- [x] README reflects current state
- [x] Git history clean
- [x] Instagram & TikTok tools implemented
- [x] Real-time streaming working
- [x] ReAct agent architecture

---

**Repository is clean, well-documented, and production-ready with v2.1 features! 🚀**
