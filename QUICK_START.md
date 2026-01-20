# Quick Start Guide - KCL Student Bot

## ✅ Setup Complete!

Your environment is ready. Here's how to use the bot:

## 🚀 Start the App

```bash
source venv/bin/activate
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 💬 Basic Usage

### Ask General Questions (No Setup Required)

Just type and ask:
- "What is King's College London known for?"
- "Tell me about KCL's computer science department"
- "Where is the main campus?"

The bot will:
1. 🔍 Search the web
2. 📄 Scrape relevant pages
3. 🤖 Generate AI-powered answers

## 📅 Add Your Timetable (Optional)

### Step 1: Get Your iCal URL

1. Go to your KCL timetable: https://mytimetable.kcl.ac.uk/
2. Login with your KCL credentials
3. Click the **"Subscribe"** button (usually top right)
4. A popup will appear - scroll down to **"Manual subscription"**
5. Copy the long URL that looks like:
   ```
   https://scientia-eu-v4-api-d4-02.azurewebsites.net/api/ical/ca05f91a-6c36-45db-9b40-6d011398ed58/...
   ```

### Step 2: Add URL to Bot

1. In the sidebar, find **"📅 Timetable Setup"**
2. Paste your iCal URL in the text area
3. Click **"💾 Save Timetable URL"**
4. You'll see **"✅ Timetable connected"**

### Step 3: Ask About Your Schedule

Now you can ask:
- "Show me my timetable"
- "What classes do I have today?"
- "When is my next lecture?"
- "Do I have anything on Friday?"

## 🎯 Key Features

### No Login Required
- Simply paste your timetable URL
- No Microsoft authentication needed
- Privacy-focused design

### Intelligent Search
- Automatically searches KCL information
- Scrapes and summarizes content
- Provides source links

### Persistent Chat
- Chat history saved during session
- Clear chat button in sidebar
- Fresh start anytime

## 🔧 Sidebar Features

- **📅 Timetable Setup**: Add/remove your iCal URL
- **🗑️ Clear Chat**: Start a new conversation
- **About Section**: Quick reference guide

## 📝 Example Conversation

```
You: What is KCL's motto?

Bot: King's College London's motto is "Sancte et Sapienter" which
means "With Holiness and Wisdom" in Latin...

You: Show me my timetable

Bot: [If URL not set]
To access your timetable, please add your iCal subscription URL
in the sidebar.

How to get your iCal URL:
1. Go to your KCL timetable (Scientia)
2. Click 'Subscribe' button
3. Copy the URL from 'Manual subscription' section
4. Paste it in the sidebar

[If URL is set]
Your Timetable

**Advanced Machine Learning**
📅 Monday, January 20 at 02:00 PM
📍 KINGS BLDG KIN G36

**Database Systems**
📅 Tuesday, January 21 at 10:00 AM
📍 KINGS BLDG KIN 427
...
```

## ⚙️ Configuration

All working! Your `.env` file has:
- ✅ OpenRouter API key
- ✅ Supabase credentials
- ✅ SerpAPI key
- ✅ Firecrawl key

## 🆘 Troubleshooting

**"Thinking..." takes too long**
- Normal for first query (10-15 seconds)
- Subsequent queries are faster

**Timetable not showing**
- Verify iCal URL is correct
- Check URL hasn't expired
- Try getting a fresh URL from KCL timetable

**Search returns no results**
- Check your internet connection
- SerpAPI might have rate limits

**Error messages**
- Check terminal/console for detailed logs
- Most errors are self-explanatory

## 🎉 You're Ready!

Start the app and begin asking questions about KCL!

```bash
streamlit run app.py
```

---

**Need help?** Check the full README.md or review logs in terminal.
