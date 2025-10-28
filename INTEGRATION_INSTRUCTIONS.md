# Integration Instructions for Multi-Agent System

## Current Setup

Your app starts via `run.py` which imports `backend.main:app`.

## Simple Integration (3 Steps)

### Step 1: Add Imports to backend/main.py

Add these lines at the top of `backend/main.py` (after existing imports):

```python
# Multi-Agent System imports
from backend.startup import startup_handler, shutdown_handler
from backend.routes.multi_agent_checkin import router as multi_agent_router
```

### Step 2: Add Event Handlers

Add these lines after `app = FastAPI(...)` and before the CORS middleware:

```python
# Multi-Agent System lifecycle
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)
```

### Step 3: Register the Router

Add this line after `app.include_router(checkin.router)`:

```python
# Multi-Agent System endpoints (v2)
app.include_router(multi_agent_router)
```

## Complete Example

Here's what the relevant section of `backend/main.py` should look like:

```python
from backend.services.rag_service import RAGService
from backend.services.langgraph_service import LangGraphService
from backend.routes import checkin
# Multi-Agent System imports
from backend.startup import startup_handler, shutdown_handler
from backend.routes.multi_agent_checkin import router as multi_agent_router

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# ... rest of imports ...

# Create FastAPI application instance
app = FastAPI(
    title="Lumina API",
    description="Backend API for the Lumina document processing system",
    version="0.1.0"
)

# Multi-Agent System lifecycle
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

# Initialize LangGraph service at startup (singleton)
app.state.langgraph_service = LangGraphService()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(checkin.router)
# Multi-Agent System endpoints (v2)
app.include_router(multi_agent_router)

# ... rest of your code ...
```

## Testing

### 1. Start the server (as usual):

```bash
python run.py
```

### 2. Check health:

```bash
curl http://localhost:8000/api/v2/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "multi-agent-depth-system",
  "version": "1.0.0"
}
```

### 3. Test check-in:

```bash
curl -X POST http://localhost:8000/api/v2/checkin \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_input": "chest tight, breath shallow"
  }'
```

## What Happens

### On Startup (via startup_handler):

1. Creates MultiAgentService singleton
2. Connects to PostgresStore
3. Compiles LangGraph workflow
4. Logs: "✓ Multi-Agent Service initialized successfully"

### On Each Request:

1. Uses the same service instance (fast!)
2. Runs through all 5 agents
3. Returns comprehensive response

### On Shutdown (via shutdown_handler):

1. Closes PostgresStore connection gracefully
2. Logs: "✓ Multi-Agent Service shut down successfully"

## Endpoints

### New Endpoints (v2):

- `POST /api/v2/checkin` - Multi-agent check-in
- `GET /api/v2/health` - Health check

### Existing Endpoints (unchanged):

- `POST /api/checkin` - Original check-in (still works!)
- `GET /health` - Original health check
- `POST /chat` - Chat endpoint
- All other existing endpoints

## Migration Strategy

### Option 1: Test in Parallel (Recommended)

- Keep both `/api/checkin` and `/api/v2/checkin`
- Test v2 with yourself first
- Compare responses
- Gradually migrate users

### Option 2: Immediate Switch

- Update frontend to use `/api/v2/checkin`
- Keep v1 as fallback
- Monitor for issues

## Troubleshooting

### "DATABASE_URL not found"

Make sure your `.env` file has:

```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### First-time setup (create Store tables):

```bash
python -c "from backend.services.multi_agent_service import get_multi_agent_service; get_multi_agent_service().setup_store()"
```

### Check logs:

The multi-agent system logs to `lumina.multi_agent`:

```python
import logging
logging.getLogger("lumina.multi_agent").setLevel(logging.DEBUG)
```

## Summary

✅ **3 simple additions to main.py**
✅ **No modifications to existing code**
✅ **Works with your current run.py**
✅ **New v2 endpoints alongside v1**
✅ **Production-ready**

That's it! Just 3 additions to `backend/main.py` and you're ready to go! 🚀
