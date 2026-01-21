# 🎓 KCL Student Bot

An AI-powered chat assistant for King's College London students that provides intelligent access to university information through natural language queries.

## ✨ Features

- 💬 **Modern React UI**: Clean, responsive interface with Tailwind CSS
- 🎨 **Markdown Support**: Formatted AI responses with code blocks, lists, headers, and more
- 🔍 **Web Search**: Intelligent search for KCL-related information
- 📅 **Timetable Integration**: Sync your personal timetable via iCal URL
- 🤖 **AI-Powered Responses**: Context-aware answers using Claude 3.5 Sonnet (configurable)
- ⚙️ **Flexible Model Configuration**: Switch between AI models via environment variables
- 💾 **Chat History**: Persistent storage in Supabase
- 🗑️ **Clear Chat**: Easy reset of conversation history
- 🔓 **No Login Required**: Simple timetable URL paste for schedule access
- 🔧 **Auto-retry on Errors**: Automatic API key verification and error handling

### New in v2.1
- 📸 **Instagram Scraping**: Scrape Instagram posts, profiles, and hashtags via Apify
- 🎵 **TikTok Scraping**: Scrape TikTok videos, profiles, and hashtags via Apify
- ⚡ **Real-Time Streaming**: Server-Sent Events (SSE) for live agent responses
- 🧠 **ReAct Agent Architecture**: Intelligent tool selection with reasoning loop
- 📊 **Agent Logs UI**: Real-time visibility into tool execution and agent thinking

## 🚀 Quick Start Navigation

Choose your path:

1. **Local Development** → [LOCAL_TESTING.md](./LOCAL_TESTING.md) - Automated setup and local testing guide
2. **Quick Deploy (15 min)** → [QUICK_START_RENDER.md](./QUICK_START_RENDER.md) - Fast deployment to Render
3. **Detailed Deployment** → [RENDER_DEPLOY.md](./RENDER_DEPLOY.md) - Step-by-step deployment guide with screenshots
4. **Model Configuration** → [MODEL_CONFIGURATION.md](./MODEL_CONFIGURATION.md) - Change AI models via environment variables
5. **Troubleshooting** → [backend/OPENROUTER_DEBUG_README.md](./backend/OPENROUTER_DEBUG_README.md) - Fix OpenRouter 401 errors

## 🏗️ Architecture

```
┌─────────────────────┐
│   React Frontend    │  Port 3000
│  - Tailwind CSS     │
│  - SSE Streaming    │
│  - AgentLogs UI     │
└──────────┬──────────┘
           │ REST API + SSE
┌──────────▼──────────┐
│   FastAPI Backend   │  Port 8000
│  - Session mgmt     │
│  - Stream processor │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  ReAct Agent        │
│  - LangGraph        │
│  - Reasoning Loop   │
│  - Dynamic Tools    │
└─────────────────────┘
```

**Tech Stack:**
- **Frontend**: React 18, Tailwind CSS, Axios, React Markdown, Lucide Icons
- **Backend**: FastAPI, Python 3.11+
- **Agent System**: LangGraph (ReAct workflow orchestration)
- **LLM**: OpenRouter (Claude 3.5 Sonnet, configurable)
- **Database**: Supabase
- **Tools**: SerpAPI (search), Firecrawl (scraping), iCalendar (timetable), Apify (Instagram, TikTok)

## 📁 Project Structure

```
kcl-student-bot/
├── backend/                    # FastAPI backend
│   ├── main.py                # API entry point
│   ├── requirements.txt       # Python dependencies
│   ├── api/                   # API routes
│   │   ├── chat.py           # Chat endpoints (with streaming)
│   │   ├── timetable.py      # Timetable endpoints
│   │   └── session.py        # Session endpoints
│   ├── core/                  # Core business logic
│   │   ├── session.py        # Session management
│   │   ├── chat_processor.py # Chat processing
│   │   └── stream_processor.py # SSE streaming
│   ├── models/                # Pydantic models
│   ├── agents/                # ReAct Agent System
│   │   ├── react_graph.py    # ReAct agent graph
│   │   ├── react_nodes.py    # ReAct node implementations
│   │   ├── react_state.py    # ReAct state definition
│   │   └── prompts.py        # Agent prompts
│   ├── tools/                 # Agent tools
│   │   ├── search_tool.py    # SerpAPI web search
│   │   ├── scraper_tool.py   # Firecrawl web scraping
│   │   ├── timetable_tool.py # iCal parsing
│   │   ├── instagram_tool.py # Instagram scraping
│   │   ├── tiktok_tool.py    # TikTok scraping
│   │   └── tool_definitions.py # LLM tool schemas
│   ├── services/              # LLM & database services
│   └── config/                # Configuration
│
├── frontend/                   # React frontend
│   ├── package.json
│   ├── src/
│   │   ├── App.js            # Main component (with streaming)
│   │   ├── components/       # UI components
│   │   │   ├── Header.jsx
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatInput.jsx
│   │   │   ├── TimetableModal.jsx
│   │   │   └── AgentLogs.jsx # Real-time agent logs
│   │   └── services/
│   │       └── api.js        # API client (with SSE)
│   └── tailwind.config.js
│
├── README.md                   # This file
├── PRD.md                     # Product requirements document
├── REPOSITORY_STATE.md        # Repository documentation
└── render.yaml                # Render deployment config
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- API Keys: OpenRouter, Supabase, SerpAPI, Firecrawl

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### 2. Start Frontend

```bash
cd frontend
npm install
npm start
```

### 3. Open Browser

Visit **http://localhost:3000** to start chatting!

## 📚 Documentation

### Getting Started
- **[LOCAL_TESTING.md](LOCAL_TESTING.md)** - Local setup with automated scripts
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Manual setup guide & troubleshooting

### Deployment
- **[QUICK_START_RENDER.md](QUICK_START_RENDER.md)** - Fast Render deployment (15 min)
- **[RENDER_DEPLOY.md](RENDER_DEPLOY.md)** - Detailed deployment guide with screenshots
- **[RENDER_UI_GUIDE.md](RENDER_UI_GUIDE.md)** - Navigating Render dashboard

### Configuration & Troubleshooting
- **[MODEL_CONFIGURATION.md](MODEL_CONFIGURATION.md)** - Switch AI models easily
- **[backend/OPENROUTER_DEBUG_README.md](backend/OPENROUTER_DEBUG_README.md)** - Fix 401 errors
- **[WHICH_URL.md](WHICH_URL.md)** - Understanding frontend vs backend URLs

### Architecture
- **[MIGRATION_README.md](MIGRATION_README.md)** - Architecture overview & system design

## 🔧 Configuration

### Backend (.env)

Create `backend/.env` with:

```env
# OpenRouter API
OPENROUTER_API_KEY=your_key
DEFAULT_MODEL=anthropic/claude-3.5-sonnet  # Optional: change AI model

# Database
SUPABASE_URL=your_url
SUPABASE_KEY=your_key

# Tools
SERPAPI_API_KEY=your_key
FIRECRAWL_API_KEY=your_key
APIFY_API_TOKEN=your_token  # For Instagram & TikTok scraping
```

See [MODEL_CONFIGURATION.md](MODEL_CONFIGURATION.md) for available models.

### Frontend (.env.local)

Create `frontend/.env.local` with:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🎨 Design

The UI features a clean, minimalist design with:
- **Laboratory White** (#F7F9FC) - Background
- **Charcoal** (#2D3436) - Primary text & buttons
- **Muted Gold** (#D4AF37) - Accents & highlights

## 🛠️ Development

### Backend Development

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### Frontend Development

```bash
cd frontend
npm start
```

Hot reload enabled - changes reflect immediately.

## 📦 Building for Production

### Frontend Build

```bash
cd frontend
npm run build
```

Outputs to `frontend/build/` directory.

### Backend Deployment

Deploy to Railway, Render, or Fly.io. See [MIGRATION_README.md](MIGRATION_README.md) for details.

## 🧪 Testing

### Test Backend Health

```bash
curl http://localhost:8000/health
```

### Test Session Creation

```bash
curl -X POST http://localhost:8000/api/session/create
```

### Test Chat

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!", "session_id": "test-123"}'
```

## 🐛 Troubleshooting

### Backend won't start

- Check Python version: `python --version` (need 3.9+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify `.env` file exists with all required keys

### Frontend won't start

- Check Node version: `node --version` (need 16+)
- Clear cache: `rm -rf node_modules package-lock.json && npm install`
- Check port 3000 is available

### API errors

- Verify backend is running on port 8000
- Check browser console for CORS errors
- Verify `REACT_APP_API_URL` in `.env.local`

## 🤝 Contributing

This is a student project for King's College London. Contributions welcome!

## 📝 License

MIT License - feel free to use for your own projects!

## 🙏 Acknowledgments

- King's College London for inspiration
- Anthropic for Claude AI
- OpenRouter for LLM access
- Supabase for database hosting

---

**Made with ❤️ for KCL students**
