# FastAPI Integration Guide - Multi-Agent System

## Overview

This guide shows how to integrate the Multi-Agent Depth System into your FastAPI application **without modifying existing code**.

## New Files Created

1. `backend/routes/multi_agent_checkin.py` - New v2 endpoint
2. `backend/startup.py` - Startup/shutdown handlers
3. This guide

## Integration Steps

### Step 1: Add Startup/Shutdown Handlers to main.py

Add these lines to your `main.py` (or wherever you create your FastAPI app):

```python
from fastapi import FastAPI
from backend.startup import startup_handler, shutdown_handler

app = FastAPI()

# Add event handlers
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)
```

**What this does**:

- Creates MultiAgentService singleton on startup
- Keeps PostgresStore and compiled graph alive
- Closes connections gracefully on shutdown

### Step 2: Include the New Router

Add the new router to your app:

```python
from backend.routes.multi_agent_checkin import router as multi_agent_router

app.include_router(multi_agent_router)
```

**What this does**:

- Adds `/api/v2/checkin` endpoint (new multi-agent system)
- Adds `/api/v2/health` endpoint (health check)
- Does NOT affect existing `/api/checkin` endpoint

### Step 3: Test the New Endpoint

Start your server:

```bash
uvicorn main:app --reload
```

Test the new endpoint:

```bash
curl -X POST http://localhost:8000/api/v2/checkin \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_input": "chest tight, breath shallow, meeting soon"
  }'
```

Expected response:

```json
{
  "response": "Your chest is a throne built for fear...",
  "depth": "deep",
  "card_decision": {
    "award_card": true,
    "card_id": "heart_opening",
    "rarity": "common",
    "reason": "Deep reflection, specificity above baseline"
  },
  "teaching_strategy": {
    "strategy": "reflect",
    "guidance": "Mirror their awareness and offer wisdom",
    "reason": "User progressing well, reflect their depth"
  },
  "extraction": {
    "body_signals": ["chest: tight", "breath: shallow"],
    "triggers": ["meeting"],
    "temporal": "future",
    "specificity_score": 8.0
  }
}
```

## Complete main.py Example

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import startup handlers
from backend.startup import startup_handler, shutdown_handler

# Import routers
from backend.routes.multi_agent_checkin import router as multi_agent_router
# Your existing routers
# from backend.routes.checkin import router as checkin_router

app = FastAPI(title="Lumina API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup/Shutdown
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

# Routers
app.include_router(multi_agent_router)  # New v2 endpoints
# app.include_router(checkin_router)    # Existing v1 endpoints

@app.get("/")
async def root():
    return {"message": "Lumina API", "version": "2.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## API Endpoints

### New Multi-Agent Endpoints

#### POST /api/v2/checkin

Process check-in using multi-agent system.

**Request**:

```json
{
  "user_input": "chest tight, breath shallow",
  "session_id": "optional-session-id"
}
```

**Response**:

```json
{
  "response": "Lumina's response...",
  "depth": "deep",
  "card_decision": {...},
  "teaching_strategy": {...},
  "extraction": {...}
}
```

#### GET /api/v2/health

Health check for multi-agent system.

**Response**:

```json
{
  "status": "healthy",
  "service": "multi-agent-depth-system",
  "version": "1.0.0"
}
```

## Migration Strategy

### Phase 1: Parallel Running (Recommended)

- Keep existing `/api/checkin` endpoint
- Add new `/api/v2/checkin` endpoint
- Test v2 with subset of users
- Compare results

### Phase 2: Gradual Migration

- Route percentage of traffic to v2
- Monitor performance and quality
- Increase percentage over time

### Phase 3: Full Migration

- Switch all traffic to v2
- Deprecate v1 endpoint
- Remove old code after grace period

## Deployment Considerations

### Environment Variables

Ensure `DATABASE_URL` is set in your environment:

```bash
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"
```

### First-Time Setup

Run once to create Store tables:

```python
from backend.services.multi_agent_service import get_multi_agent_service

service = get_multi_agent_service()
service.setup_store()
```

Or via Python:

```bash
python -c "from backend.services.multi_agent_service import get_multi_agent_service; get_multi_agent_service().setup_store()"
```

### Production Deployment

**Uvicorn** (single worker):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Gunicorn** (multiple workers):

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

- Each worker gets its own MultiAgentService instance
- No conflicts between workers

**Docker**:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring

### Logs

The multi-agent system logs to `lumina.multi_agent`:

```python
import logging
logging.getLogger("lumina.multi_agent").setLevel(logging.INFO)
```

### Metrics to Monitor

- Request latency (should be < 3s)
- Error rate
- Card award rate
- Depth distribution (shallow/medium/deep)
- Teaching strategy distribution

## Troubleshooting

### Service Won't Start

**Error**: "DATABASE_URL not found"
**Solution**: Set DATABASE_URL environment variable

### Slow Responses

**Expected**: First request may be slower (graph compilation)
**Normal**: Subsequent requests should be < 3s

### Connection Errors

**Error**: "the connection is closed"
**Solution**: Restart the application (Store will reconnect)

## Testing

Run the test suite:

```bash
python test_workflow_correct.py
```

Expected: 5/5 tests pass

## Support

For issues or questions:

1. Check logs: `lumina.multi_agent`
2. Review `PREPARED_STATEMENT_SOLUTION.md`
3. Check `SOLUTION_SUMMARY.md`

## Summary

✅ **Zero modifications to existing code**
✅ **New v2 endpoint alongside v1**
✅ **Production-ready implementation**
✅ **Gradual migration path**
✅ **Comprehensive monitoring**

Ready to deploy! 🚀
