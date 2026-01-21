# Product Requirements Document (PRD)
## KCL Student Bot - AI-Powered University Assistant

**Version:** 2.0.0
**Last Updated:** January 2026
**Status:** Production-Ready

---

## 1. Executive Summary

KCL Student Bot is an AI-powered conversational assistant designed specifically for King's College London (KCL) students. The application provides intelligent access to university-related information through natural language queries, combined with personal academic timetable integration. Built with a modern React frontend and FastAPI backend, it leverages LangGraph for agentic workflow orchestration and Claude AI for response generation.

**Target Users:** King's College London students seeking quick access to university information and personal schedule management.

---

## 2. Product Vision & Goals

### Vision
Provide KCL students with an intelligent, always-available assistant that understands university context and personal schedules, eliminating the need to navigate multiple university websites and systems.

### Primary Goals
1. **Instant Information Access** - Enable students to get KCL-specific answers via natural language
2. **Personalized Schedule Management** - Integrate personal timetables without requiring university login
3. **Seamless User Experience** - Zero-friction onboarding with no authentication required
4. **Contextual Intelligence** - Combine web search, content scraping, and personal data for comprehensive responses

### Success Metrics
- User engagement: Messages per session
- Query resolution rate: Percentage of queries answered satisfactorily
- Timetable adoption: Percentage of users who sync their timetable
- Session duration and return visits

---

## 3. User Stories & Use Cases

### Primary User Stories

| ID | User Story | Priority |
|----|------------|----------|
| US-01 | As a student, I want to ask questions about KCL in natural language so I can get quick answers | P0 |
| US-02 | As a student, I want to sync my academic timetable so I can ask about my schedule | P0 |
| US-03 | As a student, I want to see my upcoming classes so I can plan my day | P0 |
| US-04 | As a student, I want to search for KCL resources so I can find relevant information | P1 |
| US-05 | As a student, I want my chat history preserved so I can reference previous answers | P1 |
| US-06 | As a student, I want well-formatted responses so I can easily read complex information | P2 |

### Use Case Examples

**UC-01: General KCL Query**
```
User: "What are the library opening hours?"
System: Searches web → Scrapes relevant page → Generates formatted response with hours
```

**UC-02: Timetable Query**
```
User: "What do I have tomorrow?"
System: Fetches iCal events → Filters for tomorrow → Returns schedule with times and locations
```

**UC-03: Combined Context Query**
```
User: "Where is my next lecture?"
System: Checks timetable → Finds next event → May search for building location info
```

---

## 4. Functional Requirements

### 4.1 Chat System

| Req ID | Requirement | Description |
|--------|-------------|-------------|
| FR-01 | Natural Language Input | Accept free-text queries from users |
| FR-02 | AI Response Generation | Generate contextual responses using Claude LLM |
| FR-03 | Markdown Formatting | Support headers, lists, code blocks, links, tables |
| FR-04 | Chat History | Persist messages per session (up to 50 messages) |
| FR-05 | Session Management | Auto-create sessions, 24-hour cleanup policy |
| FR-06 | Loading States | Visual feedback during AI processing |

### 4.2 Timetable Integration

| Req ID | Requirement | Description |
|--------|-------------|-------------|
| FR-07 | iCal URL Sync | Accept iCalendar subscription URLs |
| FR-08 | Event Parsing | Parse VEVENT components with summary, time, location |
| FR-09 | Date Filtering | Show events for next 7 days |
| FR-10 | No-Login Access | Support read-only iCal URLs (no authentication) |
| FR-11 | Timetable Context | Include schedule data in AI response context |

### 4.3 Web Search & Scraping

| Req ID | Requirement | Description |
|--------|-------------|-------------|
| FR-12 | Web Search | Search for KCL-related information via SerpAPI |
| FR-13 | Query Enhancement | Auto-append "King's College London" to searches |
| FR-14 | Content Scraping | Extract page content via Firecrawl API |
| FR-15 | Result Formatting | Present search results with title, link, snippet |

### 4.4 Social Media Tools

| Req ID | Requirement | Description |
|--------|-------------|-------------|
| FR-16 | Instagram Scraping | Scrape Instagram posts, profiles, and hashtags via Apify |
| FR-17 | TikTok Scraping | Scrape TikTok videos, profiles, and hashtags via Apify |
| FR-18 | Content Analysis | Extract engagement metrics, captions, and media URLs |
| FR-19 | Result Formatting | Present social media content with structured metadata |

### 4.5 Real-Time Streaming

| Req ID | Requirement | Description |
|--------|-------------|-------------|
| FR-20 | SSE Streaming | Stream agent responses via Server-Sent Events |
| FR-21 | Agent Logs | Display real-time tool execution and thinking steps |
| FR-22 | Progress Updates | Show intermediate results as tools complete |
| FR-23 | Graceful Fallback | Fall back to polling if SSE connection fails |

### 4.6 Agent Workflow (ReAct Architecture)

| Req ID | Requirement | Description |
|--------|-------------|-------------|
| FR-24 | ReAct Agent | Reasoning + Acting loop for multi-step tool usage |
| FR-25 | Tool Selection | LLM dynamically selects tools based on user query |
| FR-26 | Iterative Execution | Execute tools in a loop until task is complete |
| FR-27 | Context Assembly | Combine tool outputs for response generation |
| FR-28 | Fallback Responses | Handle missing timetable URL gracefully |
| FR-29 | Planning Step | Optional high-level strategy creation before reasoning (configurable) |
| FR-30 | Configurable Iterations | Max reasoning iterations configurable via environment variable |

---

## 5. Non-Functional Requirements

### 5.1 Performance
- API response time: < 10 seconds for complex queries
- Frontend load time: < 3 seconds
- iCal fetch timeout: 10 seconds

### 5.2 Reliability
- Graceful degradation when tools fail
- Error messages that guide user action
- Session persistence across browser refreshes

### 5.3 Scalability
- Stateless API design (except in-memory sessions)
- Database-backed chat history
- Configurable LLM model selection

### 5.4 Security
- No user authentication required (privacy by design)
- No storage of university credentials
- Environment-based secret management

### 5.5 Usability
- Zero-friction onboarding
- Mobile-responsive design
- Accessible color contrast ratios

---

## 6. Technical Architecture

### 6.1 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    KCL Student Bot                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐          ┌──────────────────────────┐│
│  │  React Frontend  │          │   FastAPI Backend        ││
│  │  (Port 3000)     │◄────────►│   (Port 8000)            ││
│  │  - React 19      │ REST API │   - LangGraph agents     ││
│  │  - Tailwind CSS  │          │   - Session management   ││
│  │  - Axios client  │          │   - LLM integration      ││
│  └──────────────────┘          └──────────────────────────┘│
│                                         │                   │
│                          ┌──────────────┼──────────────┐    │
│                          ▼              ▼              ▼    │
│                    ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│                    │OpenRouter│  │ Supabase │  │SerpAPI/ │ │
│                    │ (Claude) │  │(Database)│  │Firecrawl│ │
│                    └──────────┘  └──────────┘  └─────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | React 19, Tailwind CSS | UI/UX |
| API Client | Axios | HTTP requests |
| Backend | FastAPI (Python 3.11+) | REST API server |
| Agent Orchestration | LangGraph | Workflow management |
| LLM | Claude 3.5 Sonnet (via OpenRouter) | Response generation |
| Database | Supabase (PostgreSQL) | Chat persistence |
| Search | SerpAPI | Web search |
| Scraping | Firecrawl | Content extraction |
| Calendar | iCalendar library | Schedule parsing |

### 6.3 Agent Workflow Pipeline (ReAct Architecture)

```
                     ENABLE_PLANNING=true
                            │
                            ▼
                    ┌───────────────┐
START ──────────────► planning_node │  ← Analyze query, produce strategy
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ reasoning_node│ ←─────────────────────────┐
                    └───────┬───────┘                           │
                            │                                   │
            ┌───────────────┴───────────────┐                   │
            ▼                               ▼                   │
    action = tool                   action = final_answer       │
            │                               │                   │
            ▼                               ▼                   │
    tool_execution_node                    END                  │
            │                                                   │
            ▼                                                   │
    observation_node ───────────────────────────────────────────┘
```

The agent uses a **ReAct (Reasoning + Acting)** architecture with optional planning:

| Node | Function | Description |
|------|----------|-------------|
| Planning | Strategy Creation | (Optional) Analyze query and create high-level approach |
| Reasoning | Tool Selection | LLM decides which tool to call next, references strategy if available |
| Tool Execution | Execute Tool | Execute selected tool (search, scrape, timetable, Instagram, TikTok) |
| Observation | Process Result | Format tool output for next reasoning step |
| Response | Final Answer | Generate response when reasoning decides to stop |

**Available Tools:**
- `web_search` - Search for KCL-related information via SerpAPI
- `web_scrape` - Extract content from URLs via Firecrawl
- `timetable` - Fetch and parse iCal events
- `instagram_scrape` - Scrape Instagram content via Apify
- `tiktok_scrape` - Scrape TikTok content via Apify

---

## 7. API Specification

### 7.1 Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/api/chat/message` | POST | Send message | `{query, session_id?, ical_url?}` | `{response, session_id}` |
| `/api/chat/history/{session_id}` | GET | Get history | - | `{messages[], session_id}` |
| `/api/session/create` | POST | Create session | - | `{session_id}` |
| `/api/session/status/{session_id}` | GET | Session status | - | `{session_id, has_ical_url, message_count, created_at}` |
| `/api/session/{session_id}` | DELETE | Delete session | - | `{success}` |
| `/api/timetable/set-url` | POST | Set iCal URL | `{session_id, ical_url}` | `{ical_url, has_timetable}` |
| `/api/timetable/get-url/{session_id}` | GET | Get iCal URL | - | `{ical_url, has_timetable}` |
| `/health` | GET | Health check | - | `{status, services}` |

### 7.2 Data Models

**ChatRequest**
```json
{
  "query": "string (required)",
  "session_id": "string (optional)",
  "ical_url": "string (optional)"
}
```

**ChatResponse**
```json
{
  "response": "string",
  "session_id": "string"
}
```

**AgentState** (Internal)
```python
{
  "messages": List[Dict],
  "query": str,
  "query_type": str,  # "timetable" | "general"
  "needs_search": bool,
  "needs_scraping": bool,
  "needs_timetable": bool,
  "search_results": List[Dict],
  "scraped_content": str,
  "timetable_events": List[Dict],
  "final_response": str,
  "ical_url": str
}
```

---

## 8. UI/UX Requirements

### 8.1 Component Hierarchy

```
App
├── Header
│   ├── Logo & Branding
│   ├── Clear Chat Button
│   └── Sync Timetable Button
├── Chat Area
│   └── ChatMessage (multiple)
│       └── Markdown Content
├── Loading Indicator
├── ChatInput
└── TimetableModal (conditional)
```

### 8.2 User Interface Elements

| Component | Behavior |
|-----------|----------|
| Header | Fixed top, contains branding and action buttons |
| Chat Area | Scrollable, auto-scroll to newest message |
| User Messages | Right-aligned, dark background |
| AI Messages | Left-aligned, white background, markdown rendered |
| Chat Input | Fixed bottom, disabled during loading |
| Timetable Modal | Overlay with URL input and file upload options |
| Loading Indicator | 3 animated dots during AI processing |

### 8.3 Responsive Design
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Touch-friendly input controls
- Readable font sizes on mobile

---

## 9. Integration Requirements

### 9.1 External Services

| Service | Purpose | Required Keys |
|---------|---------|---------------|
| OpenRouter | LLM API access | `OPENROUTER_API_KEY` |
| Supabase | Database storage | `SUPABASE_URL`, `SUPABASE_KEY` |
| SerpAPI | Web search | `SERPAPI_API_KEY` |
| Firecrawl | Web scraping | `FIRECRAWL_API_KEY` |
| Apify | Social media scraping (Instagram, TikTok) | `APIFY_API_TOKEN` |

### 9.2 iCalendar Integration
- **Protocol:** HTTP/HTTPS
- **Format:** iCalendar (.ics)
- **Source:** KCL timetable subscription URL
- **No Authentication:** Read-only public URLs only

---

## 10. Configuration

### 10.1 Environment Variables

**Required:**
```
OPENROUTER_API_KEY=<key>
SUPABASE_URL=<url>
SUPABASE_KEY=<key>
SERPAPI_API_KEY=<key>
FIRECRAWL_API_KEY=<key>
```

**Optional:**
```
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
APP_ENV=production
LOG_LEVEL=INFO
SESSION_MAX_AGE_HOURS=24
PORT=8000
REACT_APP_API_URL=http://localhost:8000/api

# Agent Configuration
MAX_AGENT_ITERATIONS=5      # Max reasoning loops (default: 5)
ENABLE_PLANNING=false       # Enable planning step (default: false)
```

### 10.2 Supported LLM Models
- `anthropic/claude-3.5-sonnet` (default)
- `anthropic/claude-opus-4.5`
- `anthropic/claude-3.5-haiku`
- `google/gemini-3-flash-preview`
- `openai/gpt-4o`

---

## 11. Error Handling

| Scenario | User Experience |
|----------|-----------------|
| Server unavailable | "I can't connect to the server. Check internet and try again." |
| Missing timetable URL | Instructions to sync timetable with step-by-step guide |
| iCal parse failure | "I couldn't retrieve your timetable. Please check: 1) URL correct 2) URL not expired 3) Internet connection" |
| LLM error | "I encountered an error processing your request. Please try again." |
| Search/scrape failure | Graceful degradation - continues with available context |

---

## 12. Deployment

### 12.1 Supported Platforms
- **Render** (Primary) - `render.yaml` configured
- **Docker** - `Dockerfile` available
- **Vercel** - Frontend deployment support
- **Local Development** - `start_local.sh` script

### 12.2 Production Checklist
- [ ] All API keys configured
- [ ] CORS origins set for production domain
- [ ] Database tables created in Supabase
- [ ] Health check endpoint responding
- [ ] SSL/HTTPS enabled

---

## 13. Future Considerations

### Potential Enhancements
1. **User Authentication** - Persistent user accounts and preferences
2. **Multi-University Support** - Expand beyond KCL
3. **Push Notifications** - Upcoming class reminders
4. **Offline Mode** - Cached responses for common queries
5. **Voice Interface** - Speech-to-text input
6. **File Upload Processing** - Direct .ics file parsing (currently placeholder)
7. **Analytics Dashboard** - Usage insights for administrators

### Recently Implemented Features
- ✅ **Real-time Streaming** - SSE-based streaming for agent responses
- ✅ **Instagram Scraping** - Extract posts, profiles, and hashtags via Apify
- ✅ **TikTok Scraping** - Extract videos, profiles, and hashtags via Apify
- ✅ **ReAct Agent Architecture** - Reasoning + Acting loop for dynamic tool selection
- ✅ **Planning Step** - Optional high-level strategy creation before reasoning (ENABLE_PLANNING)
- ✅ **Configurable Iterations** - Max reasoning loops configurable via MAX_AGENT_ITERATIONS

### Known Limitations
- In-memory session storage (sessions lost on server restart)
- File upload UI exists but not fully implemented
- Timetable limited to 7-day lookahead
- Social media scraping requires Apify API token

---

## 14. Appendix

### A. File Structure

```
KCL bot/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── api/                 # REST endpoints
│   │   ├── chat.py          # Chat endpoints (with streaming)
│   │   ├── session.py
│   │   └── timetable.py
│   ├── agents/              # ReAct Agent System
│   │   ├── react_graph.py   # ReAct agent graph
│   │   ├── react_nodes.py   # ReAct node implementations
│   │   ├── react_state.py   # ReAct state definition
│   │   └── prompts.py       # Agent prompts
│   ├── core/                # Core logic
│   │   └── stream_processor.py  # SSE streaming
│   ├── services/            # External integrations
│   │   ├── llm_service.py
│   │   └── supabase_service.py
│   ├── tools/               # Agent tools
│   │   ├── search_tool.py
│   │   ├── scraper_tool.py
│   │   ├── timetable_tool.py
│   │   ├── instagram_tool.py    # Instagram scraping
│   │   ├── tiktok_tool.py       # TikTok scraping
│   │   └── tool_definitions.py  # LLM tool schemas
│   ├── models/              # Pydantic models
│   ├── config/              # Settings
│   └── utils/               # Utilities
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main component (with streaming)
│   │   ├── components/      # UI components
│   │   │   └── AgentLogs.jsx    # Real-time agent logs
│   │   └── services/api.js  # API client (with SSE)
│   └── public/
└── Documentation files (*.md)
```

### B. Query Classification Keywords

**Timetable Queries:**
- timetable, schedule, class, lecture
- when is my, what do i have, show me my
- tomorrow, today, this week
- module, course, professor

**General Queries:**
- All other queries → Web search + scraping

---

*Document generated by reverse-engineering the KCL Student Bot codebase.*
