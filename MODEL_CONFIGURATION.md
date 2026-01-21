# AI Model Configuration Guide

The AI model is now fully configurable via environment variables. You can change models without modifying any code!

## Quick Change

### Local Development

Edit `backend/.env`:
```env
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
```

Restart backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Render (Production)

1. Go to: https://dashboard.render.com
2. Select your `kcl-bot-backend` service
3. Go to **Environment** tab
4. Find or add `DEFAULT_MODEL`
5. Set value (e.g., `anthropic/claude-opus-4.5`)
6. Click **Save Changes**
7. **Manual Deploy** → **Deploy latest commit**

---

## Available Models

### Anthropic Claude (Recommended)

```env
# Best for complex reasoning - highest quality
DEFAULT_MODEL=anthropic/claude-opus-4.5

# Balanced - good quality and speed (default)
DEFAULT_MODEL=anthropic/claude-3.5-sonnet

# Fastest and cheapest - good for simple tasks
DEFAULT_MODEL=anthropic/claude-3.5-haiku
```

### OpenAI GPT

```env
# Latest GPT models
DEFAULT_MODEL=openai/gpt-5
DEFAULT_MODEL=openai/gpt-5-mini
DEFAULT_MODEL=openai/gpt-4o
DEFAULT_MODEL=openai/gpt-4o-mini
```

### Google Gemini

```env
# Latest Gemini models
DEFAULT_MODEL=google/gemini-3-flash-preview
DEFAULT_MODEL=google/gemini-2.5-pro
DEFAULT_MODEL=google/gemini-2.5-flash
```

### Meta Llama

```env
DEFAULT_MODEL=meta-llama/llama-3.3-70b
DEFAULT_MODEL=meta-llama/llama-3.1-405b
```

### Other Providers

Visit https://openrouter.ai/models for the complete list of available models.

---

## Model Comparison

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| claude-opus-4.5 | Slow | Highest | $$$$ | Complex reasoning, difficult tasks |
| claude-3.5-sonnet | Medium | High | $$ | General purpose (recommended) |
| claude-3.5-haiku | Fast | Good | $ | Simple queries, high volume |
| gpt-5 | Medium | High | $$$ | Latest OpenAI capabilities |
| gpt-4o | Fast | High | $$ | Good balance |
| gemini-3-flash-preview | Very Fast | Good | $ | Cost-effective, fast responses |
| gemini-2.5-pro | Medium | High | $$ | Complex tasks, good value |

---

## Configuration Files

### 1. Local: `backend/.env`

This is your local configuration (not committed to git):

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_key_here
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
```

### 2. Example: `backend/.env.example`

Template file showing all options (committed to git):

```env
# OpenRouter API
OPENROUTER_API_KEY=your_openrouter_api_key_here
DEFAULT_MODEL=anthropic/claude-3.5-sonnet
# Options: anthropic/claude-opus-4.5, anthropic/claude-3.5-sonnet,
#          anthropic/claude-3.5-haiku, google/gemini-3-flash-preview,
#          openai/gpt-5, openai/gpt-4o, etc.
```

### 3. Render: `render.yaml`

Render deployment configuration (committed to git):

```yaml
envVars:
  - key: DEFAULT_MODEL
    value: anthropic/claude-3.5-sonnet
    # AI model to use - can override in Render dashboard
```

### 4. Code: `backend/config/settings.py`

Python settings that read the environment variable:

```python
default_model: str = "anthropic/claude-3.5-sonnet"  # Can be overridden via DEFAULT_MODEL env var
```

---

## How It Works

1. **Environment Variable Priority**:
   - If `DEFAULT_MODEL` is set in `.env`, it uses that value
   - If not set, it falls back to the default in `settings.py`

2. **Pydantic Settings**:
   - Automatically reads from `.env` file
   - Case-insensitive (DEFAULT_MODEL or default_model both work)

3. **No Code Changes Needed**:
   - Just update the environment variable
   - Restart the service
   - New model is active!

---

## Testing Different Models

### Test Locally First

1. Update `backend/.env`:
   ```env
   DEFAULT_MODEL=anthropic/claude-opus-4.5
   ```

2. Restart backend:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

3. Check startup logs:
   ```
   INFO: LLM Service initialized with model: anthropic/claude-opus-4.5
   ```

4. Send a test chat message and verify it works

5. If satisfied, update Render with the same model

### Test Without Changing Default

You can test a model in a single request without changing the default:

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Hello",
    "session_id": "test",
    "model": "anthropic/claude-opus-4.5"
  }'
```

---

## Troubleshooting

### Model Not Changing

**Symptom**: Logs still show old model after updating `.env`

**Solution**:
1. Make sure you saved the `.env` file
2. Fully restart the backend (don't rely on hot reload)
3. Check startup logs for confirmation

### Model Not Working

**Symptom**: 401 errors or "model not found"

**Solutions**:
1. Check model name is correct: https://openrouter.ai/models
2. Verify your OpenRouter API key has access to that model
3. Check you have sufficient credits
4. Some models require specific API keys or permissions

### Different Models on Local vs Render

**This is normal!** You can have:
- Local: `claude-3.5-haiku` (cheap for testing)
- Render: `claude-3.5-sonnet` (better quality for production)

Just make sure each environment has the correct `DEFAULT_MODEL` set.

---

## Best Practices

### 1. Test Locally First
Always test a new model locally before deploying to Render.

### 2. Consider Cost
- Development: Use cheaper models like `claude-3.5-haiku` or `gemini-3-flash-preview`
- Production: Use balanced models like `claude-3.5-sonnet`
- Special cases: Use `claude-opus-4.5` only when needed

### 3. Monitor Usage
Check your OpenRouter dashboard regularly:
- https://openrouter.ai/activity
- Monitor costs per model
- Adjust based on usage patterns

### 4. Document Your Choice
If you change from the default, document why in your deployment notes.

---

## Examples

### Example 1: Switch to Faster Model

For high-volume, simple queries:

**Local** (`backend/.env`):
```env
DEFAULT_MODEL=anthropic/claude-3.5-haiku
```

**Render**:
1. Set `DEFAULT_MODEL=anthropic/claude-3.5-haiku`
2. Redeploy

**Expected**: Faster responses, lower costs

### Example 2: Switch to Most Powerful Model

For complex reasoning tasks:

**Local** (`backend/.env`):
```env
DEFAULT_MODEL=anthropic/claude-opus-4.5
```

**Render**:
1. Set `DEFAULT_MODEL=anthropic/claude-opus-4.5`
2. Redeploy

**Expected**: Best quality answers, higher costs

### Example 3: Try Google Gemini

For cost-effective alternative:

**Local** (`backend/.env`):
```env
DEFAULT_MODEL=google/gemini-2.5-flash
```

**Render**:
1. Set `DEFAULT_MODEL=google/gemini-2.5-flash`
2. Redeploy

**Expected**: Fast, cheap, good quality

---

## Summary

✅ **No code changes needed** - just update environment variable
✅ **Different models for local vs production** - configure separately
✅ **Easy to test** - change, restart, verify in logs
✅ **Documented defaults** - in `.env.example` and `render.yaml`
✅ **Flexible** - try any model on OpenRouter

Visit https://openrouter.ai/models for the complete model catalog!
