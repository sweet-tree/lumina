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

### Active Spec: Multi-Agent Depth System

**Location:** `.kiro/specs/multi-agent-depth-system/` (to be created)

**Status:** Architecture finalized, ready for spec creation

**Previous Implementation:** Basic LangGraph depth evaluation (completed)

**Key Architecture Decisions:**

1. ✅ Four-agent system: Extraction, Deep (Memory), Teaching, Card
2. ✅ Depth is relative to user baseline, not absolute
3. ✅ LangGraph Store for long-term user memory
4. ✅ Teaching Agent guides users deeper when stuck
5. ✅ Card Agent decides rewards (earned, not automatic)
6. ✅ Separation of concerns (each agent has one job)

---

## Multi-Agent Depth System Architecture

### Overview

Four specialized agents work together to evaluate depth, maintain user memory, guide users deeper, and award cards.

### Agent 1: Extraction Agent

**Responsibility:** Extract structured signal from user input

**Input:** Raw user text

**Output:**

```json
{
  "body_signals": ["location: sensation"],
  "triggers": ["what's causing this"],
  "temporal": "past/present/future",
  "specificity_score": 0-10
}
```

**Implementation:**

- Single LLM call with structured output
- Prompt includes examples (few-shot learning)
- Fast execution (~0.5s)

---

### Agent 2: Deep Agent (Memory)

**Responsibility:** Maintain user model, detect patterns, evaluate relative depth

**Uses LangGraph Store:**

```
/memories/user_{id}/
  body_patterns.txt      # Body locations + frequencies
  triggers.txt           # What causes patterns
  loops_doorways.txt     # Detected patterns
  baseline.txt           # User's typical specificity
  progression.txt        # Trajectory over time
```

**Key Logic:**

```python
# Depth is relative to user
if current_specificity > user_baseline + 2:
    depth = "deep"
elif current_specificity < user_baseline - 2:
    depth = "shallow"
else:
    depth = "medium"
```

**Pattern Detection:**

- **Loops:** Recurring sequences (tension → depleted → foggy)
- **Doorways:** What breaks loops (awareness → ease)
- **Triggers:** What causes patterns (meetings, Mondays)
- **Baseline:** User's typical specificity (rolling average)

---

### Agent 3: Teaching Agent

**Responsibility:** Decide pedagogical strategy

**Strategies:**

1. **Reflect** - Mirror awareness (when doing well)
2. **Question** - Guide deeper (when stuck shallow)
3. **Teach** - Explain pattern (when pattern detected)
4. **Challenge** - Point out regression (when they were deeper)

**Decision Logic:**

```python
if stuck_shallow_5_days:
    strategy = "question"  # "Where in your body?"
elif pattern_detected:
    strategy = "teach"     # "This is the third time..."
elif regressing:
    strategy = "challenge" # "You were deeper before..."
else:
    strategy = "reflect"   # "The body speaks..."
```

**Why it matters:**

- Prevents stagnation
- Guides users toward embodiment
- Creates teacher-student relationship
- Lumina as guide, not just mirror

---

### Agent 4: Card Agent

**Responsibility:** Decide if card earned, which card, what rarity

**Award Criteria:**

**Award card when:**

- Deep reflection (specificity > user_baseline + 2)
- Multiple check-ins today (commitment)
- Breakthrough moment (loop broken)
- Consistent practice (3+ day streak)

**Don't award card when:**

- Shallow check-in (below threshold)
- First attempt of day (give chance to go deeper)
- Regressing without awareness

**Card Rarity:**

- **Common:** Daily deep check-ins
- **Rare:** Weekly pattern detected
- **Epic:** Monthly consciousness map
- **Legendary:** Major breakthrough

**Why it matters:**

- Gamification without being "gamey"
- Rewards depth, not just participation
- Creates dialogue (no card → question → deeper → card)

---

### Complete Flow

```
User Input
    ↓
Extraction Agent
    ↓
Deep Agent (reads/updates Store)
    ↓
    ├─→ Teaching Agent (parallel)
    └─→ Card Agent (parallel)
         ↓
Response Generation (uses Teaching strategy + RAG)
         ↓
Output: Response + Card (if awarded)
```

---

### Key Principles

1. **Depth is Relative:** Compare to user's baseline, not absolute scale
2. **Memory Enables Personalization:** Store tracks patterns over time
3. **Guidance Over Judgment:** Teaching Agent prevents stagnation
4. **Earned Rewards:** Cards motivate depth
5. **Separation of Concerns:** Each agent has one job

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
