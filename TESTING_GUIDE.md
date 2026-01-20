# Testing Guide for KCL Student Bot

## Quick Start

### 1. Start the Application

In your terminal, run:
```bash
source venv/bin/activate  # Activate virtual environment
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### 2. Basic Testing (No Login Required)

Test the public features that work without authentication:

**Test Queries:**
1. "What is King's College London known for?"
2. "Tell me about KCL's computer science program"
3. "Where is King's College London located?"
4. "What facilities does KCL offer?"

**Expected Behavior:**
- Chat input appears at bottom
- Your message shows on the right
- "Thinking..." spinner appears
- Bot searches the web (using SerpAPI)
- Bot scrapes relevant content (using Firecrawl)
- Response appears with information and sources

### 3. Authentication Testing

**Important Note:** Before testing authentication, you need to set up Microsoft SSO credentials.

#### To Set Up Microsoft SSO:
1. Go to [Azure Portal](https://portal.azure.com)
2. Register a new application in Azure AD
3. Get your:
   - Client ID
   - Client Secret
   - Tenant ID
4. Update `.env` file with these credentials
5. Set redirect URI to `http://localhost:8501` in Azure

**Test Login Flow:**
1. Click "🔐 Login with Microsoft" button
2. Click the login link that appears
3. Authenticate with Microsoft
4. Copy the redirect URL
5. Paste it in "Handle Redirect After Login" section
6. Click "Process Login"

**Expected:** Welcome message with your name

### 4. Timetable Testing (Requires Authentication)

**Setup:**
1. Login first (see above)
2. In sidebar, find "⚙️ Settings"
3. Paste your KCL timetable iCal URL
4. Click save

**Test Queries:**
1. "Show me my timetable"
2. "What classes do I have today?"
3. "When is my next lecture?"

**Expected:** Your upcoming classes/events displayed

### 5. Feature Checklist

- [ ] App starts without errors
- [ ] Chat interface renders correctly
- [ ] Can send messages
- [ ] Messages appear in chat history
- [ ] Search queries return results
- [ ] Responses include relevant information
- [ ] Login button appears when not authenticated
- [ ] Login flow works (if SSO configured)
- [ ] User name appears after login
- [ ] Logout works
- [ ] Settings panel appears when authenticated
- [ ] Chat history persists during session
- [ ] Clear chat button works

### 6. Database Testing (Optional)

To verify Supabase integration:

1. Go to your Supabase dashboard
2. Check the `chat_messages` table
3. Your messages should be saved there

**Create Tables if Not Done:**

```sql
-- chat_messages table
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

-- user_sessions table
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

### 7. Common Issues

**Issue: "Module not found" errors**
- Solution: Make sure virtual environment is activated
- Run: `source venv/bin/activate`

**Issue: "Missing API key" errors**
- Solution: Check `.env` file has all required keys
- Make sure `.env` is in the project root

**Issue: Supabase connection errors**
- Solution: Verify Supabase URL and key in `.env`
- Check tables exist in Supabase dashboard

**Issue: Search not working**
- Solution: Verify SerpAPI key is valid
- Check SerpAPI account has credits

**Issue: Scraping fails**
- Solution: Verify Firecrawl API key
- Some websites may block scraping

**Issue: Microsoft login not working**
- Solution: Need to configure Microsoft Azure AD app first
- This is optional for MVP testing

### 8. Stopping the Application

Press `Ctrl+C` in the terminal where Streamlit is running.

### 9. Viewing Logs

Logs appear in the terminal where you ran `streamlit run app.py`.

Look for:
- INFO logs showing normal operations
- ERROR logs if something fails
- Tool execution logs (search, scraper, etc.)

### 10. Testing Workflow

**Recommended Testing Order:**

1. ✅ Run `python test_setup.py` - Verify setup
2. ✅ Start app: `streamlit run app.py`
3. ✅ Test basic chat (no login)
4. ✅ Ask KCL-related questions
5. ✅ Check if answers are relevant
6. ⏭️ (Optional) Set up Microsoft SSO
7. ⏭️ (Optional) Test authentication
8. ⏭️ (Optional) Test timetable features
9. ✅ Test UI features (clear chat, sidebar, etc.)
10. ✅ Check Supabase for saved messages

### 11. Next Steps After Basic Testing

If basic testing works:
1. Set up Microsoft Azure AD for authentication
2. Create Supabase tables for persistence
3. Add your timetable iCal URL
4. Test with real KCL student queries
5. Customize responses and UI
6. Add more tools as needed

### 12. Performance Expectations

- **Response Time**: 5-15 seconds per query
  - Search: ~2-3 seconds
  - Scraping: ~3-5 seconds
  - LLM: ~5-10 seconds
- **First Load**: May take longer as services initialize
- **Concurrent Users**: Streamlit handles multiple sessions well

### Need Help?

Check the logs in terminal for detailed error messages. Most issues are related to missing API keys or configuration.
