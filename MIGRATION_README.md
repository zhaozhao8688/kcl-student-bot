# KCL Student Bot - React Migration

This document describes the new React + FastAPI architecture and how to run the application.

## Architecture Overview

The application has been migrated from Streamlit to a modern React + FastAPI stack:

```
┌─────────────────────┐
│   React Frontend    │  Port 3000
│  - Chat interface   │
│  - Tailwind CSS     │
└──────────┬──────────┘
           │ REST API
┌──────────▼──────────┐
│   FastAPI Backend   │  Port 8000
│  - API endpoints    │
│  - Session mgmt     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Agent System       │
│  - LangGraph        │
│  - Tools & Services │
└─────────────────────┘
```

## Project Structure

```
kcl-student-bot/
├── backend/                    # FastAPI backend
│   ├── main.py                # API entry point
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── api/                   # API routes
│   │   ├── chat.py
│   │   ├── timetable.py
│   │   └── session.py
│   ├── core/                  # Core logic
│   │   ├── session.py         # Session management
│   │   └── chat_processor.py # Chat processing
│   ├── models/                # Pydantic models
│   ├── agents/                # Agent system (from original)
│   ├── tools/                 # Tools (from original)
│   ├── services/              # Services (from original)
│   ├── config/                # Config (from original)
│   └── utils/                 # Utilities (from original)
│
└── frontend/                   # React frontend
    ├── package.json
    ├── .env.local             # Frontend env vars
    ├── src/
    │   ├── App.jsx            # Main component
    │   ├── components/        # UI components
    │   │   ├── Header.jsx
    │   │   ├── ChatMessage.jsx
    │   │   ├── ChatInput.jsx
    │   │   └── TimetableModal.jsx
    │   └── services/
    │       └── api.js         # API client
    └── tailwind.config.js     # Tailwind config
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 16+
- All API keys from original setup (OpenRouter, Supabase, SerpAPI, Firecrawl)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - The `.env` file should already be copied from the root directory
   - If not, copy `.env.example` to `.env` and fill in your API keys

5. **Run the backend:**
   ```bash
   python -m uvicorn main:app --reload --port 8000
   ```

   Or:
   ```bash
   python main.py
   ```

   The backend will be available at `http://localhost:8000`
   API docs available at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   - The `.env.local` file should already exist
   - Verify it contains:
     ```
     REACT_APP_API_URL=http://localhost:8000/api
     ```

4. **Run the frontend:**
   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## Running Both Servers

Open two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # If not already activated
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## API Endpoints

### Chat
- `POST /api/chat/message` - Send a message
- `GET /api/chat/history/{session_id}` - Get chat history

### Timetable
- `POST /api/timetable/set-url` - Set iCal URL
- `GET /api/timetable/get-url/{session_id}` - Get iCal URL

### Session
- `POST /api/session/create` - Create new session
- `GET /api/session/status/{session_id}` - Get session status
- `DELETE /api/session/{session_id}` - Delete session

## Design Features

The UI matches the design from `UIreference.html`:

- **Colors:**
  - Laboratory White (#F7F9FC) - Background
  - Charcoal (#2D3436) - Primary text/buttons
  - Muted Gold (#D4AF37) - Accents

- **Components:**
  - Fixed header with branding
  - Clean message bubbles
  - Timetable sync modal
  - Fixed bottom input area

## Key Changes from Streamlit

1. **Session Management:** Replaced `st.session_state` with backend session manager
2. **UI Framework:** Replaced Streamlit with React + Tailwind CSS
3. **API Layer:** Added FastAPI REST API
4. **Agent System:** Reused 100% of existing agent, tools, and services code
5. **Database:** Still uses Supabase (no changes)

## Troubleshooting

### Backend Issues

**Import errors:**
- Make sure you're in the backend directory when running
- Activate virtual environment
- Install all requirements

**Port already in use:**
```bash
# Change port in main.py or run with:
uvicorn main:app --reload --port 8001
```

### Frontend Issues

**API connection errors:**
- Verify backend is running on port 8000
- Check `.env.local` has correct API URL
- Check browser console for CORS errors

**Tailwind styles not working:**
- Make sure `tailwind.config.js` exists
- Restart dev server: `npm start`

## Testing the Migration

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Create Session:**
   ```bash
   curl -X POST http://localhost:8000/api/session/create
   ```

3. **Send Message:**
   ```bash
   curl -X POST http://localhost:8000/api/chat/message \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the library opening hours?", "session_id": "YOUR_SESSION_ID"}'
   ```

4. **Frontend:** Open http://localhost:3000 and test the chat interface

## Next Steps

- [ ] Deploy backend (Railway, Render, Fly.io)
- [ ] Deploy frontend (Vercel, Netlify)
- [ ] Set up production environment variables
- [ ] Configure CORS for production domains
- [ ] Add error tracking (Sentry)
- [ ] Add analytics
- [ ] Implement proper authentication (optional)

## Notes

- The original Streamlit code remains in the root directory
- Agent system code was copied (not moved) to `backend/` to preserve original
- Session storage is currently in-memory; consider Redis for production
- File upload for timetables requires additional backend implementation

## Support

For issues or questions:
1. Check the logs in both terminals
2. Verify all environment variables are set
3. Check API documentation at http://localhost:8000/docs
4. Review browser console for frontend errors
