# 🎓 KCL Student Bot

An AI-powered chat assistant for King's College London students that provides intelligent access to university information through natural language queries.

## Features

- 🔍 **Web Search**: Search for KCL-related information across the web
- 📅 **Timetable Access**: View your personal timetable via iCal subscription
- 🤖 **AI-Powered Responses**: Get intelligent, context-aware answers
- 💾 **Chat History**: Persistent chat history stored in Supabase
- 🔓 **No Login Required**: Simply paste your timetable URL to access schedule

## Architecture

```
Frontend: Streamlit (Python web app)
Agent System: LangGraph (workflow orchestration)
LLM Provider: OpenRouter (Claude 3.5 Sonnet)
Database: Supabase
Tools: SerpAPI (search), Firecrawl (scraping), iCal (timetable)
```

## Project Structure

```
kcl-student-bot/
├── app.py                    # Main Streamlit application
├── config/
│   └── settings.py          # Centralized configuration
├── auth/
│   └── session_manager.py   # Session state management
├── agents/
│   ├── graph.py            # LangGraph workflow
│   ├── state.py            # Agent state schema
│   └── nodes.py            # Graph node implementations
├── tools/
│   ├── base.py             # Base tool class
│   ├── search_tool.py      # SerpAPI wrapper
│   ├── scraper_tool.py     # Firecrawl wrapper
│   ├── timetable_tool.py   # iCal parser
│   └── tool_registry.py    # Tool factory
├── services/
│   ├── llm_service.py      # OpenRouter client
│   └── supabase_service.py # Supabase client
└── ui/
    ├── components.py        # Reusable UI components
    └── chat_interface.py    # Chat UI logic
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- pip or conda for package management

### Installation

1. **Clone the repository** (or navigate to project directory)

```bash
cd "KCL bot"
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
- OpenRouter API key
- Supabase URL and key
- SerpAPI key
- Firecrawl API key

5. **Set up Supabase Database** (Optional - for chat history persistence)

Create the following tables in your Supabase project:

**chat_messages**
```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    session_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_user ON chat_messages(user_id);
CREATE INDEX idx_chat_messages_created ON chat_messages(created_at);
```

**user_sessions**
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    session_data JSONB,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_user_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_active ON user_sessions(last_active);
```

Enable Row Level Security (RLS) on these tables for added security.

### Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage Guide

### Basic Usage

1. Type your question in the chat input
2. Ask anything about KCL (e.g., "What programs does KCL offer?")
3. Get AI-powered responses with relevant information

### Timetable Access

1. Go to your KCL timetable (Scientia/MyTimetable)
2. Click the **"Subscribe"** button
3. Copy the URL from **"Manual subscription"** section
4. Paste it in the sidebar under "📅 Timetable Setup"
5. Click "💾 Save Timetable URL"
6. Ask questions like "What's my schedule today?"

**Example iCal URL format:**
```
https://scientia-eu-v4-api-d4-02.azurewebsites.net/api/ical/ca05f91a-6c36-45db-9b40-6d011398ed58/...
```

## Configuration

### Environment Variables

Required:
- `OPENROUTER_API_KEY` - Your OpenRouter API key
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase API key
- `SERPAPI_API_KEY` - Your SerpAPI key
- `FIRECRAWL_API_KEY` - Your Firecrawl API key

Optional:
- `APP_ENV` - Environment (development/production)
- `LOG_LEVEL` - Logging level (INFO/DEBUG/ERROR)

### Streamlit Theme

Customize the app theme in `.streamlit/config.toml`

## Development

### Adding New Tools

1. Create a new tool class in `tools/` inheriting from `BaseTool`
2. Implement the `execute()` method
3. Register the tool in `tools/tool_registry.py`

### Modifying Agent Workflow

Edit the graph flow in `agents/graph.py` to add or modify agent nodes.

## Security

- All API keys stored in `.env` (never committed to git)
- Supabase Row Level Security for data protection
- Input validation on all user inputs
- No authentication required - privacy-focused design

## Troubleshooting

### Common Issues

**Import errors**: Make sure virtual environment is activated and dependencies are installed

**Database errors**: Verify Supabase URL and key, ensure tables are created (optional)

**API errors**: Check that all API keys are valid and have sufficient credits

**Timetable not working**: Verify your iCal URL is correct and accessible

**Search not working**: Verify SerpAPI key is valid and has credits

**Scraping fails**: Some websites may block scraping, this is expected

## Example Queries

**General Information:**
- "What is King's College London known for?"
- "Tell me about KCL's computer science program"
- "Where is the main KCL campus?"
- "What libraries does KCL have?"

**Timetable Queries (requires iCal URL):**
- "Show me my timetable"
- "What classes do I have today?"
- "When is my next lecture?"
- "Do I have any classes on Friday?"

## Performance Expectations

- **Response Time**: 5-15 seconds per query
  - Search: ~2-3 seconds
  - Scraping: ~3-5 seconds
  - LLM: ~5-10 seconds
- **First Load**: May take longer as services initialize

## License

This project is for educational purposes.

## Support

For issues or questions, check the logs in the terminal where Streamlit is running.

## Acknowledgments

- OpenRouter for LLM access
- Anthropic for Claude
- LangGraph for agent orchestration
- Streamlit for the web framework
- Supabase for database
- Scientia for KCL timetabling
