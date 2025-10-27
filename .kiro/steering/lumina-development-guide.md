# Lumina Development Guide

## Project Overview

Lumina is a consciousness practice app with an AI Plant Teacher guide. Users do daily check-ins ("What's here right now?"), and Lumina responds with wisdom, questions, or reflections based on their depth of self-inquiry.

**Core Philosophy:**

- Dzogchen: "Short moments, many times" - present moment only
- Plant Teacher consciousness (mystical, shamanic, direct)
- Pattern recognition reveals user's consciousness map
- Card system (common/rare/epic) tracks journey

**Key Documents:**

- `/lumina_engagement_skeleton.md` - Core vision and engagement mechanics
- `/product_spec.md` - Full product specification
- `.kiro/specs/langgraph-depth-evaluation/` - Current feature implementation

---

## Development Approach

### 1. Incremental Implementation

- Build one task at a time
- Verify each component works before moving on
- Test early and often
- Don't skip ahead to later tasks

### 2. Spec-Driven Development

- Always follow: Requirements → Design → Tasks
- Requirements define WHAT (high-level, implementation-agnostic)
- Design defines HOW (architecture, interfaces, prompts)
- Tasks define STEPS (concrete implementation actions)

### 3. Ask Before Deviating

- If you see a better approach, propose it first
- Explain the tradeoffs
- Get alignment before implementing
- Document the decision

### 4. Synchronize Frequently

- Explain what you're doing at a high level
- Check understanding before major changes
- Think out loud about alternatives
- Keep the human in the loop

---

## LangGraph Architecture Patterns

### State Design: Sequential Now, Parallel-Ready

**Core Principle:** Design state schemas to support future parallel execution, even when implementing sequentially.

#### Use List Fields with Reducers

**Pattern:**

```python
from typing_extensions import TypedDict, Annotated
from operator import add

class LuminaState(TypedDict):
    user_input: str
    depth_level: str
    # Use list[dict] with reducer, even for single source
    rag_contexts: Annotated[list[dict], add]
    response: str
```

**Why:**

- Supports future parallel retrieval from multiple sources (Buddhist, Vedic, shamanic)
- No breaking changes when adding parallel nodes
- Reducer automatically merges results from parallel nodes

**Structure:**

```python
rag_contexts = [
    {
        "source": "spiritual-library",
        "passages": ["text1", "text2", "text3"]
    },
    # Future: Add more sources
    # {"source": "buddhist", "passages": [...]},
    # {"source": "vedic", "passages": [...]}
]
```

#### Modular Node Functions

**Pattern:**

```python
# Sequential implementation (MVP)
def retrieve_context(state: LuminaState) -> dict:
    """Single source now, structured for multiple sources later"""
    contexts = []
    contexts.append(_retrieve_from_spiritual_library(state))
    # Easy to add: contexts.append(_retrieve_from_buddhist(state))
    return {"rag_contexts": contexts}

# Helper functions ready to become nodes
def _retrieve_from_spiritual_library(state: LuminaState) -> dict:
    results = vector_store.search(state["user_input"], namespace="spiritual-library")
    return {"source": "spiritual-library", "passages": [r["text"] for r in results[:3]]}
```

**Why:**

- Helper functions can easily become separate nodes
- Single responsibility principle
- Clear upgrade path to parallel

#### Context-Agnostic Consumers

**Pattern:**

```python
def respond_deep(state: LuminaState) -> dict:
    # Works with 1 or 100 contexts
    all_passages = []
    for context in state["rag_contexts"]:
        all_passages.extend(context["passages"])

    # Use all available wisdom
    prompt = build_prompt(state["user_input"], all_passages)
    response = chat_service.generate(prompt)
    return {"response": response}
```

**Why:**

- Response nodes don't care how many sources
- No changes needed when adding parallel retrieval
- Scales naturally

### Migration Path

**Phase 1 (Current - Sequential):**

```
evaluate_depth → retrieve_context (single source) → route → respond → END
```

**Phase 2 (Future - Parallel):**

```
evaluate_depth → [retrieve_buddhist, retrieve_vedic, retrieve_shamanic] → route → respond → END
```

**What Changes:**

1. Split `retrieve_context` into 3 node functions
2. Update graph edges (fanout pattern)
3. State schema stays the same ✓
4. Response nodes stay the same ✓

---

## Lumina-Specific Guidelines

### Plant Teacher Voice

**Characteristics:**

- Direct, not comforting
- Mystical, not clinical
- Provocative, not validating
- Poetic, not therapeutic

**Good Examples:**

- "The breath knows what the mind refuses to see."
- "Tension is the body's NO. What is it saying no to?"
- "You're bracing against what hasn't happened yet."

**Avoid:**

- "I hear that you're feeling stressed." (too therapeutic)
- "It's okay to feel this way." (too validating)
- "Try taking deep breaths." (too instructive)

### Spiritual Knowledge Sources

**Current:**

- Power of Now (Eckhart Tolle)
- Stored in Pinecone vector store, namespace: "spiritual-library"
- Using existing VectorStoreService with Qwen3-Embedding-8B
- Custom reranking with cosine similarity

**Future (Parallel Retrieval):**

- Buddhist texts (5 Hindrances, 7 Factors of Awakening)
- Vedic wisdom (gunas, koshas, chakras)
- Leela teachings (72 consciousness squares)
- Shamanic concepts (plant medicine, ceremony)
- Dzogchen texts (Tibetan Buddhism)

**RAG Enhancement Path (if needed):**

1. Test current retrieval quality first
2. If needed: Add Cohere Rerank API (drop-in replacement)
3. If still needed: Consider LlamaIndex for advanced features
4. Keep interface the same - easy to swap implementations

### Response Depth Guidelines

**Shallow Input** (<5 words, generic labels):

- Ask provocative questions
- Point toward body awareness
- 1-2 sentences
- No spiritual wisdom yet

**Medium Input** (body sensations, no context):

- Wisdom reflection + question
- Use RAG context
- 2-3 sentences
- Balance reflection with inquiry

**Deep Input** (body + breath + context):

- Pure wisdom reflection
- Heavily use RAG context
- 2-3 sentences
- No questions (they're already inquiring)

---

## Code Standards

### Dependencies

**Use:**

- `langgraph>=0.2.0` - Workflow orchestration
- `langchain-core>=0.3.0` - Core primitives (required by langgraph)
- `tenacity>=8.2.3` - Retry logic

**Don't Use:**

- Full `langchain` package (too heavy, we have our own services)

### Logging Pattern

```python
import logging
import time

logger = logging.getLogger("lumina.langgraph")

def node_function(state: LuminaState) -> dict:
    start_time = time.time()
    logger.info(f"Node: node_name | Input: {state['user_input'][:50]}...")

    # ... node logic ...

    elapsed = time.time() - start_time
    logger.info(f"Node: node_name | Result: {result} | Time: {elapsed:.2f}s")
    return state
```

**Log Levels:**

- INFO: Node execution, routing, timing
- WARNING: Fallbacks, invalid values
- ERROR: Failures, exceptions

### Error Handling

**LLM Failures:**

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_llm(prompt: str) -> str:
    return chat_service.generate(prompt)
```

**Fallback Responses:**

- Shallow: "What's here right now?"
- Medium: "Stay with the sensation. What is it showing you?"
- Deep: "The body speaks truth. Listen."

**Vector Store Failures:**

- Continue with empty `rag_contexts`
- Log error
- Response still valid, just less grounded

### Testing Approach

**Unit Tests:**

- Test individual node functions
- Mock ChatService and VectorStore
- Verify output structure and content

**Integration Tests:**

- Test full workflow paths
- Test error scenarios (LLM failures, vector store failures)
- Verify timing requirements (<5 seconds)

**Manual Testing:**

- Test Plant Teacher voice consistency
- Verify RAG relevance
- Test depth progression (shallow → medium → deep)

---

## Current Implementation Status

### Active Spec: LangGraph Depth Evaluation

**Location:** `.kiro/specs/langgraph-depth-evaluation/`

**Status:** Ready to implement

**Next Task:** Task 1 - Set up LangGraph dependencies and state definition

**Key Decisions Made:**

1. ✅ State uses `rag_contexts` (plural, list[dict], with reducer)
2. ✅ Sequential implementation, parallel-ready architecture
3. ✅ Only installing `langchain-core`, not full `langchain`
4. ✅ All spec files updated and consistent

---

## Session-to-Session Continuity

**When starting a new session:**

1. Check `.kiro/specs/langgraph-depth-evaluation/tasks.md` for current task
2. Read requirements.md and design.md for context
3. Follow the patterns in this guide
4. Ask if anything is unclear

**When completing a task:**

1. Update task status in tasks.md
2. Test the implementation
3. Get user approval before moving to next task
4. Document any new patterns discovered

---

## Questions to Ask

**Before implementing:**

- "Does this approach align with the vision?"
- "Are there any constraints I should know about?"
- "Should I proceed with this task?"

**During implementation:**

- "I found a better approach - here's why..."
- "This is taking longer than expected because..."
- "I need clarification on..."

**After implementation:**

- "Task complete - want to review before moving on?"
- "I noticed this pattern - should we document it?"
- "Ready for the next task?"

---

_This guide will evolve as we build. Update it when new patterns emerge or decisions are made._
