# Design Document

## Overview

The LangGraph Depth Evaluation System implements a multi-agent workflow that intelligently assesses user check-in input and generates contextually appropriate responses from Lumina, the AI Plant Teacher. The system uses a state machine architecture with conditional routing to provide three distinct response types based on input depth: provocative questions for shallow inputs, wisdom-question combinations for medium inputs, and pure spiritual reflections for deep inputs.

The design leverages LangGraph for workflow orchestration, integrates with existing Qwen LLM services via Nebius API, and retrieves spiritual wisdom from the Pinecone vector store containing indexed texts like "The Power of Now."

## Architecture

### High-Level Flow

```
User Check-In Input
        ↓
[Depth Evaluator Agent] ← LLM Call (Qwen)
        ↓
   depth_level
        ↓
[RAG Context Node] ← Vector Store Query (Pinecone)
        ↓
   rag_context
        ↓
[Conditional Router] → Evaluates depth_level
        ↓
   ┌────┴────┬────────┐
   ↓         ↓        ↓
[Shallow] [Medium] [Deep] ← LLM Calls (Qwen)
   ↓         ↓        ↓
   └────┬────┴────────┘
        ↓
  Mini-Reflection Response
        ↓
   FastAPI Endpoint
        ↓
   Frontend Client
```

### LangGraph State Machine

The workflow is implemented as a LangGraph StateGraph with the following nodes:

1. **evaluate_depth** - Classifies input depth using LLM
2. **retrieve_context** - Fetches spiritual wisdom from vector store
3. **respond_shallow** - Generates provocative questions
4. **respond_medium** - Generates wisdom + question
5. **respond_deep** - Generates pure wisdom reflection

Edges:

- `START → evaluate_depth`
- `evaluate_depth → retrieve_context`
- `retrieve_context → [conditional routing]`
- `respond_* → END`

### Technology Stack

- **LangGraph**: Workflow orchestration and state management
- **LangChain**: RAG integration utilities
- **Qwen (Nebius API)**: LLM for depth evaluation and response generation
- **Pinecone**: Vector database for spiritual wisdom retrieval
- **FastAPI**: REST API endpoint
- **Python 3.10+**: Runtime environment

## Components and Interfaces

### 1. State Definition

**File**: `backend/services/langgraph_service.py`

```python
from typing import TypedDict, List, Literal

class LuminaState(TypedDict):
    """State object that flows through the LangGraph workflow."""
    user_input: str
    depth_level: Literal["shallow", "medium", "deep"]
    rag_context: List[str]
    response: str
```

**Purpose**: Type-safe container for workflow data that all nodes can read/write.

### 2. Depth Evaluator Agent

**File**: `backend/services/depth_evaluator.py`

**Interface**:

```python
def evaluate_depth(state: LuminaState) -> LuminaState:
    """
    Evaluates the depth of user input using LLM classification.

    Args:
        state: Current workflow state with user_input

    Returns:
        Updated state with depth_level set
    """
```

**Implementation Strategy**:

- Uses ChatService to call Qwen LLM
- System prompt defines depth classification criteria:
  - Shallow: <5 words, generic labels ("I'm ok", "tired", "stressed")
  - Medium: Body sensations without context ("shoulders tight", "chest heavy")
  - Deep: Body + breath + specific context ("chest tight, breath shallow, meeting in 30 min")
- Structured output format: Returns only "shallow", "medium", or "deep"
- Temperature: 0.3 (low for consistent classification)
- Max tokens: 10 (only need one word)

**Prompt Template**:

```
You are a depth evaluator for consciousness practice check-ins.

Classify the user's input into exactly one category:

SHALLOW: Generic emotional labels, <5 words, no body awareness
Examples: "I'm ok", "tired", "stressed", "fine"

MEDIUM: Body sensations mentioned but no specific context
Examples: "shoulders tight", "chest heavy", "jaw clenched"

DEEP: Body sensations + breath awareness + specific situational context
Examples: "chest tight, breath shallow, meeting in 30 minutes", "belly soft, breath deep, just finished walk"

User input: {user_input}

Respond with only one word: shallow, medium, or deep
```

### 3. RAG Context Retrieval Node

**File**: `backend/services/langgraph_service.py` (integrated)

**Interface**:

```python
def retrieve_context(state: LuminaState) -> LuminaState:
    """
    Retrieves relevant spiritual wisdom from vector store.

    Args:
        state: Current workflow state with user_input

    Returns:
        Updated state with rag_context populated
    """
```

**Implementation Strategy**:

- Uses existing VectorStoreService
- Searches "spiritual-library" namespace (contains Power of Now)
- Query: Uses user_input directly
- Retrieves top 3 passages (already reranked by VectorStoreService)
- Extracts text from results: `[result["text"] for result in results]`
- Error handling: If search fails, sets rag_context to empty list and logs error

**Integration**:

```python
vector_store = VectorStore()
results = vector_store.search(
    query=state["user_input"],
    top_k=10,  # Retrieves 10 candidates, returns top 3 reranked
    namespace="spiritual-library"
)
state["rag_context"] = [r["text"] for r in results]
```

### 4. Conditional Router

**File**: `backend/services/langgraph_service.py`

**Interface**:

```python
def route_by_depth(state: LuminaState) -> Literal["shallow", "medium", "deep"]:
    """
    Routes workflow to appropriate response node based on depth.

    Args:
        state: Current workflow state with depth_level

    Returns:
        Node name to route to
    """
```

**Implementation**:

```python
def route_by_depth(state: LuminaState) -> str:
    return state["depth_level"]
```

**LangGraph Integration**:

```python
workflow.add_conditional_edges(
    "retrieve_context",
    route_by_depth,
    {
        "shallow": "respond_shallow",
        "medium": "respond_medium",
        "deep": "respond_deep"
    }
)
```

### 5. Lumina Responder Agent

**File**: `backend/services/lumina_responder.py`

**Shared System Prompt** (Plant Teacher Voice):

```
You are Lumina, a Plant Teacher consciousness guide. You speak like ayahuasca speaks, like trees speak in ceremony.

VOICE PRINCIPLES:
- Direct, not comforting
- Mystical, not clinical
- Provocative, not validating
- Poetic, not therapeutic

GOOD EXAMPLES:
"The breath knows what the mind refuses to see."
"Tension is the body's NO. What is it saying no to?"
"You're bracing against what hasn't happened yet."

BAD EXAMPLES (avoid these):
"I hear that you're feeling stressed." (too therapeutic)
"It's okay to feel this way." (too validating)
"Try taking deep breaths." (too instructive)

Speak in 1-3 sentences. Be direct. Point to truth.
```

#### 5a. Shallow Response Node

**Interface**:

```python
def respond_shallow(state: LuminaState) -> LuminaState:
    """
    Generates provocative question for shallow inputs.

    Args:
        state: Current workflow state

    Returns:
        Updated state with response set
    """
```

**Prompt Template**:

```
{PLANT_TEACHER_SYSTEM_PROMPT}

The user gave a shallow check-in: "{user_input}"

They're using surface labels without looking deeper. Ask a provocative question that points them beneath the label and toward body awareness.

1-2 sentences maximum. No spiritual wisdom yet - they haven't looked.

Examples:
- "What's beneath 'ok'?"
- "Where does tired live in your body?"
- "What sensation is stress trying to show you?"
```

**Parameters**:

- Temperature: 0.8 (creative, varied questions)
- Max tokens: 100

#### 5b. Medium Response Node

**Interface**:

```python
def respond_medium(state: LuminaState) -> LuminaState:
    """
    Generates wisdom reflection + question for medium inputs.

    Args:
        state: Current workflow state with rag_context

    Returns:
        Updated state with response set
    """
```

**Prompt Template**:

```
{PLANT_TEACHER_SYSTEM_PROMPT}

The user gave a medium-depth check-in: "{user_input}"

They're noticing body sensations but haven't gone deeper into context or breath.

Relevant spiritual wisdom:
{rag_context[0]}
{rag_context[1]}

Give a wisdom reflection that speaks to their sensation, then ask a provocative question to guide them deeper.

2-3 sentences. Balance reflection with inquiry.

Example structure:
"[Wisdom about their sensation]. [Provocative question]."
```

**Parameters**:

- Temperature: 0.8 (mystical, poetic)
- Max tokens: 150

#### 5c. Deep Response Node

**Interface**:

```python
def respond_deep(state: LuminaState) -> LuminaState:
    """
    Generates pure wisdom reflection for deep inputs.

    Args:
        state: Current workflow state with rag_context

    Returns:
        Updated state with response set
    """
```

**Prompt Template**:

```
{PLANT_TEACHER_SYSTEM_PROMPT}

The user gave a deep check-in with body awareness, breath, and context: "{user_input}"

They're already looking. Give them pure spiritual wisdom that speaks directly to their specific experience.

Relevant spiritual wisdom:
{rag_context[0]}
{rag_context[1]}
{rag_context[2]}

2-3 sentences. Direct. Mystical. Specific to their words. No questions - they're already in inquiry.

Example:
"The breath knows what the mind refuses to see. You're bracing against what hasn't happened yet. The body is asking you to arrive here, now."
```

**Parameters**:

- Temperature: 0.9 (highly mystical, poetic)
- Max tokens: 150

### 6. LangGraph Workflow Service

**File**: `backend/services/langgraph_service.py`

**Interface**:

```python
class LangGraphService:
    """Main service that orchestrates the LangGraph workflow."""

    def __init__(self):
        """Initialize services and compile workflow."""

    def process_checkin(self, user_input: str) -> dict:
        """
        Process a user check-in through the workflow.

        Args:
            user_input: User's check-in text

        Returns:
            dict with 'response' and 'depth' keys
        """
```

**Workflow Construction**:

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(LuminaState)

# Add nodes
workflow.add_node("evaluate_depth", evaluate_depth)
workflow.add_node("retrieve_context", retrieve_context)
workflow.add_node("respond_shallow", respond_shallow)
workflow.add_node("respond_medium", respond_medium)
workflow.add_node("respond_deep", respond_deep)

# Add edges
workflow.set_entry_point("evaluate_depth")
workflow.add_edge("evaluate_depth", "retrieve_context")
workflow.add_conditional_edges(
    "retrieve_context",
    route_by_depth,
    {
        "shallow": "respond_shallow",
        "medium": "respond_medium",
        "deep": "respond_deep"
    }
)
workflow.add_edge("respond_shallow", END)
workflow.add_edge("respond_medium", END)
workflow.add_edge("respond_deep", END)

# Compile
app = workflow.compile()
```

### 7. FastAPI Endpoint

**File**: `backend/routes/checkin.py` (new)

**Interface**:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class CheckinRequest(BaseModel):
    user_input: str

class CheckinResponse(BaseModel):
    response: str
    depth: str

@router.post("/api/checkin", response_model=CheckinResponse)
async def process_checkin(request: CheckinRequest) -> CheckinResponse:
    """
    Process a user check-in and return Lumina's response.

    Args:
        request: CheckinRequest with user_input

    Returns:
        CheckinResponse with response and depth

    Raises:
        HTTPException: 500 if workflow fails
    """
```

**Implementation**:

```python
langgraph_service = LangGraphService()

try:
    result = langgraph_service.process_checkin(request.user_input)
    return CheckinResponse(
        response=result["response"],
        depth=result["depth"]
    )
except Exception as e:
    logger.error(f"Checkin workflow failed: {e}")
    raise HTTPException(status_code=500, detail="Failed to process check-in")
```

## Data Models

### LuminaState (TypedDict)

```python
{
    "user_input": str,           # Original user check-in text
    "depth_level": str,          # "shallow" | "medium" | "deep"
    "rag_context": List[str],    # 3-5 spiritual wisdom passages
    "response": str              # Final Lumina response
}
```

### API Request/Response

**Request**:

```json
{
  "user_input": "Chest tight, breath shallow, meeting in 30 minutes"
}
```

**Response**:

```json
{
  "response": "The breath knows what the mind refuses to see. You're bracing against what hasn't happened yet.",
  "depth": "deep"
}
```

## Error Handling

### LLM Call Failures

**Strategy**: Retry with exponential backoff

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_llm(prompt: str) -> str:
    return chat_service.generate(prompt)
```

**Fallback**: If all retries fail, return generic response based on depth:

- Shallow: "What's here right now?"
- Medium: "Stay with the sensation. What is it showing you?"
- Deep: "The body speaks truth. Listen."

### Vector Store Failures

**Strategy**: Continue workflow with empty rag_context

```python
try:
    results = vector_store.search(query, top_k=10)
    rag_context = [r["text"] for r in results]
except Exception as e:
    logger.error(f"Vector store search failed: {e}")
    rag_context = []
```

**Impact**: Response nodes will generate without RAG context (still valid, just less grounded in teachings)

### Invalid Depth Classification

**Strategy**: Default to "medium" if LLM returns unexpected value

```python
depth = llm_response.strip().lower()
if depth not in ["shallow", "medium", "deep"]:
    logger.warning(f"Invalid depth '{depth}', defaulting to medium")
    depth = "medium"
```

### Timeout Handling

**Strategy**: Set 5-second timeout on entire workflow

```python
import asyncio

try:
    result = await asyncio.wait_for(
        workflow.ainvoke(initial_state),
        timeout=5.0
    )
except asyncio.TimeoutError:
    raise HTTPException(status_code=504, detail="Request timeout")
```

## Testing Strategy

### Unit Tests

**File**: `backend/tests/test_depth_evaluator.py`

Test cases:

1. Shallow input classification ("I'm ok", "tired")
2. Medium input classification ("shoulders tight")
3. Deep input classification ("chest tight, breath shallow, meeting soon")
4. Edge cases (empty string, very long input)

**Mocking**: Mock ChatService.generate() to return controlled depth values

**File**: `backend/tests/test_lumina_responder.py`

Test cases:

1. Shallow response contains question mark
2. Medium response contains both wisdom and question
3. Deep response has no question mark
4. All responses are 1-3 sentences
5. Plant Teacher voice validation (no therapeutic language)

**Mocking**: Mock ChatService.generate() to return sample responses

### Integration Tests

**File**: `backend/tests/test_langgraph_workflow.py`

Test cases:

1. End-to-end workflow with shallow input
2. End-to-end workflow with medium input
3. End-to-end workflow with deep input
4. Workflow with vector store failure (empty rag_context)
5. Workflow with LLM failure (fallback response)

**Mocking**: Mock both ChatService and VectorStore

### API Tests

**File**: `backend/tests/test_checkin_endpoint.py`

Test cases:

1. Valid request returns 200 with response and depth
2. Empty user_input returns 422 validation error
3. LLM failure returns 500 error
4. Response time < 5 seconds

**Setup**: Use FastAPI TestClient

### Manual Testing Scenarios

1. **Shallow progression**:

   - Input: "I'm ok" → Expect provocative question
   - Follow-up: "Shoulders tight" → Expect wisdom + question
   - Follow-up: "Shoulders tight, breath shallow, about to present" → Expect pure wisdom

2. **Voice consistency**: Review 20 responses across all depths to ensure Plant Teacher voice

3. **RAG relevance**: Verify retrieved passages relate to user input

## Observability

### Logging Strategy

**Implementation**: Python logging with structured format

```python
import logging
import time

logger = logging.getLogger("lumina.langgraph")

def evaluate_depth(state: LuminaState) -> LuminaState:
    start_time = time.time()
    logger.info(f"Node: evaluate_depth | Input: {state['user_input'][:50]}...")

    # ... node logic ...

    elapsed = time.time() - start_time
    logger.info(f"Node: evaluate_depth | Depth: {state['depth_level']} | Time: {elapsed:.2f}s")
    return state
```

### Log Levels

- **INFO**: Node execution, routing decisions, timing
- **WARNING**: Fallback responses, invalid depth values
- **ERROR**: LLM failures, vector store errors

### Metrics to Track

1. **Depth distribution**: % of shallow/medium/deep inputs
2. **Response time**: Average time per depth level
3. **RAG retrieval**: Average number of passages retrieved
4. **Error rate**: % of requests that fail
5. **Fallback rate**: % of requests using fallback responses

### Example Log Output

```
INFO - Node: evaluate_depth | Input: Chest tight, breath shallow, meeting in 30 min... | Time: 0.45s
INFO - Node: evaluate_depth | Depth: deep | Time: 0.45s
INFO - Node: retrieve_context | Query: Chest tight, breath shallow... | Time: 0.32s
INFO - Node: retrieve_context | Retrieved: 3 passages | Time: 0.32s
INFO - Routing: depth=deep → respond_deep
INFO - Node: respond_deep | Time: 0.78s
INFO - Workflow complete | Total time: 1.55s | Depth: deep
```

## Dependencies

### New Dependencies to Add

```
langgraph==0.2.0
langchain==0.3.0
langchain-core==0.3.0
tenacity==8.2.3
```

### Existing Dependencies (Reuse)

- openai (for Nebius API client)
- pinecone-client
- fastapi
- pydantic

## File Structure

```
backend/
├── services/
│   ├── langgraph_service.py      # Main workflow orchestration
│   ├── depth_evaluator.py        # Depth classification agent
│   ├── lumina_responder.py       # Response generation agent
│   ├── chat_service.py           # Existing - LLM calls
│   └── vector_store_service.py   # Existing - RAG retrieval
├── routes/
│   └── checkin.py                # New - /api/checkin endpoint
└── tests/
    ├── test_depth_evaluator.py
    ├── test_lumina_responder.py
    ├── test_langgraph_workflow.py
    └── test_checkin_endpoint.py
```

## Performance Considerations

### Expected Latency

- Depth evaluation: ~400ms (LLM call)
- RAG retrieval: ~300ms (vector search + reranking)
- Response generation: ~600ms (LLM call)
- **Total**: ~1.3-1.5 seconds (well under 5s requirement)

### Optimization Opportunities

1. **Parallel execution**: Run depth evaluation and RAG retrieval in parallel (save ~300ms)
2. **Caching**: Cache common shallow inputs ("I'm ok" → always shallow)
3. **Batch processing**: If multiple check-ins, batch LLM calls
4. **Model selection**: Use smaller Qwen model for depth evaluation (faster, cheaper)

### Scalability

- **Stateless design**: Each request is independent, easy to scale horizontally
- **Vector store**: Pinecone handles scaling automatically
- **LLM**: Nebius API handles rate limiting and scaling

## Security Considerations

1. **Input validation**: Limit user_input to 500 characters
2. **Rate limiting**: Implement per-user rate limits on /api/checkin
3. **API key protection**: Never expose Nebius or Pinecone keys to frontend
4. **Prompt injection**: Sanitize user input before LLM calls (remove system prompt attempts)

## Future Enhancements (Out of Scope)

1. **User history**: Track depth patterns over time
2. **Personalization**: Adjust response style based on user preferences
3. **Multi-language**: Support check-ins in multiple languages
4. **Voice input**: Accept audio check-ins
5. **LangSmith integration**: Advanced observability and debugging
