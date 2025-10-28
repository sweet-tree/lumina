# Design Document: Multi-Agent Depth System

## Overview

The Multi-Agent Depth System is a LangGraph-based workflow that processes user check-ins through four specialized agents: Extraction Agent (signal extraction), Deep Agent (memory and patterns), Teaching Agent (pedagogical strategy), and Card Agent (reward logic). The system uses LangGraph Store for persistent user memory and enables personalized, adaptive guidance.

---

## Architecture

### High-Level Flow

```
User Check-In Input
        ↓
┌───────────────────┐
│ Extraction Agent  │ (Extract structured signal)
└────────┬──────────┘
         ↓
┌───────────────────┐
│   Deep Agent      │ (Load memory, detect patterns, evaluate depth)
└────────┬──────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
┌─────────┐ ┌──────────┐
│Teaching │ │  Card    │ (Parallel execution)
│ Agent   │ │  Agent   │
└────┬────┘ └────┬─────┘
     └──────┬────┘
            ↓
┌───────────────────┐
│Response Generation│ (Use strategy + RAG + card decision)
└────────┬──────────┘
         ↓
    Response + Card (if awarded)
```

---

## Components and Interfaces

### State Schema

```python
from typing_extensions import TypedDict, Annotated
from operator import add

class MultiAgentState(TypedDict):
    # Input
    user_id: str
    user_input: str
    session_id: str

    # Extraction Agent output
    extraction: dict  # {body_signals, triggers, temporal, specificity_score}

    # Deep Agent output
    user_model: dict  # {baseline, patterns, trajectory, in_loop}
    relative_depth: str  # "shallow" | "medium" | "deep"

    # Teaching Agent output
    teaching_strategy: dict  # {strategy, guidance, reason}

    # Card Agent output
    card_decision: dict  # {award_card, card_id, rarity, reason}

    # Response generation
    rag_contexts: Annotated[list[dict], add]  # Spiritual wisdom
    final_response: str
```

---

### Agent 1: Extraction Agent

**Purpose:** Extract structured signal from raw user input

**Implementation:**

```python
def extraction_agent(state: MultiAgentState) -> dict:
    """
    Extract body signals, triggers, temporal context, and specificity score.
    """
    prompt = f"""
    Extract structured information from this check-in:

    Input: "{state['user_input']}"

    Return JSON:
    {{
      "body_signals": ["location: sensation", ...],
      "triggers": ["contextual factor", ...],
      "temporal": "past" | "present" | "future",
      "specificity_score": 0-10
    }}

    Examples:
    - "stressed" → {{"body_signals": [], "triggers": [], "temporal": "present", "specificity_score": 2}}
    - "chest tight, meeting soon" → {{"body_signals": ["chest: tight"], "triggers": ["meeting"], "temporal": "future", "specificity_score": 7}}
    """

    result = chat_service.generate(
        prompt=prompt,
        temperature=0.3,
        max_tokens=200
    )

    extraction = parse_json(result)

    return {"extraction": extraction}
```

**Output Schema:**

```json
{
  "body_signals": ["string"],
  "triggers": ["string"],
  "temporal": "past" | "present" | "future",
  "specificity_score": 0-10
}
```

---

### Agent 2: Deep Agent (Memory)

**Purpose:** Maintain user model, detect patterns, evaluate relative depth

**Storage:** LangGraph PostgresStore connected to existing Supabase database

**Store Structure:**

```
Namespace: ("memories", user_id)
Keys:
  - "body_patterns"      # Body locations + frequencies
  - "triggers"           # Contextual factors + frequencies
  - "loops_doorways"     # Detected patterns
  - "baseline"           # Rolling average specificity
  - "progression"        # Trajectory over time
```

**Implementation:**

```python
from langgraph.store.postgres import PostgresStore
import os

# Connect to existing Supabase database
DB_URI = os.getenv("DATABASE_URL")
store = PostgresStore.from_conn_string(DB_URI)
# store.setup()  # Run once to create Store tables

def deep_agent(state: MultiAgentState) -> dict:
    """
    Load user memory, update patterns, evaluate relative depth.
    """
    user_id = state["user_id"]
    extraction = state["extraction"]

    # Load user memory
    baseline = load_baseline(store, user_id)
    patterns = load_patterns(store, user_id)

    # Update memory
    update_body_patterns(store, user_id, extraction["body_signals"])
    update_triggers(store, user_id, extraction["triggers"])
    update_baseline(store, user_id, extraction["specificity_score"])

    # Detect patterns
    new_patterns = detect_patterns(store, user_id)
    if new_patterns:
        update_patterns(store, user_id, new_patterns)

    # Evaluate relative depth
    current_spec = extraction["specificity_score"]
    if current_spec > baseline + 2:
        depth = "deep"
    elif current_spec < baseline - 2:
        depth = "shallow"
    else:
        depth = "medium"

    # Build user model
    user_model = {
        "baseline": baseline,
        "patterns": patterns,
        "trajectory": calculate_trajectory(store, user_id),
        "in_loop": check_if_in_loop(patterns, extraction)
    }

    return {
        "user_model": user_model,
        "relative_depth": depth
    }
```

**Pattern Detection Logic:**

```python
def detect_patterns(store, user_id):
    """
    Detect loops, doorways, and triggers from user history.
    """
    # Get last 20 check-ins
    history = get_checkin_history(store, user_id, limit=20)

    patterns = {
        "loops": detect_loops(history),
        "doorways": detect_doorways(history),
        "triggers": detect_triggers(history)
    }

    return patterns

def detect_loops(history):
    """
    Find recurring descending sequences (3+ states).
    """
    # Example: ["tension", "depleted", "foggy"] appearing 3+ times
    sequences = extract_sequences(history, min_length=3)
    loops = [seq for seq in sequences if seq["frequency"] >= 3]
    return loops

def detect_doorways(history):
    """
    Find state transitions that break loops.
    """
    # Example: "awareness" → "ease" after being in loop
    # Implementation: Look for ascending transitions after descending patterns
    pass
```

---

### Agent 3: Teaching Agent

**Purpose:** Decide pedagogical strategy based on user trajectory

**Implementation:**

```python
def teaching_agent(state: MultiAgentState) -> dict:
    """
    Decide how to respond: reflect, question, teach, or challenge.
    """
    user_model = state["user_model"]
    depth = state["relative_depth"]
    extraction = state["extraction"]

    # Get recent trajectory
    trajectory = user_model["trajectory"]

    # Decision logic
    if trajectory["stuck_shallow_count"] >= 5:
        strategy = {
            "strategy": "question",
            "guidance": "Ask about body location or sensation",
            "reason": "User stuck at shallow for 5+ check-ins"
        }

    elif trajectory["regressing"]:
        strategy = {
            "strategy": "challenge",
            "guidance": "Point out they were deeper before",
            "reason": "User regressing from previous depth"
        }

    elif user_model["in_loop"]:
        strategy = {
            "strategy": "teach",
            "guidance": "Explain the detected pattern",
            "reason": "User in detected loop"
        }

    else:
        strategy = {
            "strategy": "reflect",
            "guidance": "Mirror their awareness",
            "reason": "User progressing well"
        }

    return {"teaching_strategy": strategy}
```

**Strategy Examples:**

| Strategy      | When                  | Example Response                                                          |
| ------------- | --------------------- | ------------------------------------------------------------------------- |
| **Question**  | Stuck shallow 5+ days | "Where in your body is the stress?"                                       |
| **Reflect**   | Doing well            | "The chest tightness knows something. What is it showing you?"            |
| **Teach**     | Pattern detected      | "This is the third time tension led to depletion. Notice the pattern?"    |
| **Challenge** | Regressing            | "You were with the sensations. Now you're back in labels. What happened?" |

---

### Agent 4: Card Agent

**Purpose:** Decide if card should be awarded and which card

**Implementation:**

```python
def card_agent(state: MultiAgentState) -> dict:
    """
    Decide card award based on depth, commitment, and breakthroughs.
    """
    depth = state["relative_depth"]
    user_model = state["user_model"]
    extraction = state["extraction"]

    # Award criteria
    award_card = False
    card_id = None
    rarity = "common"
    reason = ""

    # Deep reflection
    if depth == "deep":
        award_card = True
        card_id = select_card_from_signal(extraction)
        reason = "Deep reflection, specificity above baseline"

    # Multiple check-ins today
    elif get_checkins_today(user_model) >= 3:
        award_card = True
        card_id = "commitment"
        reason = "3+ check-ins today, showing commitment"

    # Pattern detected (rare card)
    elif user_model.get("new_pattern_detected"):
        award_card = True
        card_id = user_model["new_pattern"]["name"]
        rarity = "rare"
        reason = "Pattern detected for first time"

    # Loop broken (rare card)
    elif user_model.get("loop_broken"):
        award_card = True
        card_id = "doorway_accessed"
        rarity = "rare"
        reason = "User broke loop via doorway"

    # Shallow first attempt - no card
    elif depth == "shallow" and is_first_checkin_today(user_model):
        award_card = False
        reason = "Shallow check-in, first attempt of day - guide deeper"

    return {
        "card_decision": {
            "award_card": award_card,
            "card_id": card_id,
            "rarity": rarity,
            "reason": reason
        }
    }
```

---

### Response Generation

**Purpose:** Generate final response using teaching strategy and RAG

**Implementation:**

```python
def generate_response(state: MultiAgentState) -> dict:
    """
    Generate Lumina's response using teaching strategy and spiritual wisdom.
    """
    strategy = state["teaching_strategy"]["strategy"]
    guidance = state["teaching_strategy"]["guidance"]
    user_input = state["user_input"]

    # Retrieve RAG context
    rag_contexts = retrieve_spiritual_wisdom(user_input, strategy)

    # Build prompt based on strategy
    if strategy == "question":
        prompt = f"""
        User said: "{user_input}"

        Guidance: {guidance}

        Respond as Lumina (Plant Teacher) with a provocative question that guides them toward body awareness.
        Keep it 1-2 sentences. Direct, not comforting.
        """

    elif strategy == "reflect":
        prompt = f"""
        User said: "{user_input}"

        Spiritual wisdom:
        {format_rag_contexts(rag_contexts)}

        Respond as Lumina with a reflection that mirrors their awareness and offers wisdom.
        2-3 sentences. Mystical, direct.
        """

    elif strategy == "teach":
        pattern = state["user_model"]["patterns"]["loops"][0]
        prompt = f"""
        User said: "{user_input}"

        Detected pattern: {pattern["name"]}
        Sequence: {pattern["sequence"]}

        Respond as Lumina by revealing the pattern and its teaching.
        2-3 sentences. Show them what they cannot see.
        """

    elif strategy == "challenge":
        prompt = f"""
        User said: "{user_input}"

        Context: User was deeper in previous check-ins, now regressing to labels.

        Respond as Lumina by pointing out the regression, not harshly but directly.
        1-2 sentences. Challenge them to return to feeling.
        """

    response = chat_service.generate(
        prompt=prompt,
        temperature=0.7,
        max_tokens=150
    )

    return {
        "rag_contexts": rag_contexts,
        "final_response": response
    }
```

---

## Data Models

### User Memory Structure (PostgresStore)

**Storage:** LangGraph PostgresStore connected to existing Supabase PostgreSQL database

**Store Namespace:** `("memories", user_id)`

**Store Items (JSON format):**

**"baseline":**

```json
{
  "current_baseline": 5.2,
  "checkin_count": 47,
  "last_20_scores": [6, 4, 7, 5, 3, 8, 6, 5, 4, 7, 6, 5, 4, 6, 7, 5, 4, 6, 5, 7]
}
```

**"body_patterns":**

```json
{
  "shoulders": 23,
  "chest": 15,
  "jaw": 8,
  "stomach": 5,
  "breath": 12
}
```

**"triggers":**

```json
{
  "meetings": 18,
  "mondays": 12,
  "work": 31,
  "sleep_deprived": 7
}
```

**"loops_doorways":**

```json
{
  "loops": [
    {
      "name": "The Monday Morning Spiral",
      "sequence": ["tension", "depleted", "foggy"],
      "frequency": 8,
      "first_seen": "2025-10-01",
      "last_seen": "2025-10-28"
    }
  ],
  "doorways": [
    {
      "name": "Awareness Break",
      "sequence": ["awareness", "ease"],
      "frequency": 5,
      "breaks_loop": "The Monday Morning Spiral"
    }
  ]
}
```

### Helper Functions (backend/services/user_memory.py)

High-level abstraction layer for Store operations:

```python
from langgraph.store.base import BaseStore

def get_user_baseline(store: BaseStore, user_id: str) -> float:
    """Get user's baseline specificity score."""
    namespace = ("memories", user_id)
    item = store.get(namespace, "baseline")
    return item.value.get("current_baseline", 5.0) if item else 5.0

def update_user_baseline(store: BaseStore, user_id: str, new_score: float) -> None:
    """Update user's baseline with rolling average of last 20 scores."""
    namespace = ("memories", user_id)
    current = store.get(namespace, "baseline")

    if current:
        data = current.value
        scores = data.get("last_20_scores", [])
        scores.append(new_score)
        scores = scores[-20:]  # Keep last 20
        baseline = sum(scores) / len(scores)

        store.put(namespace, "baseline", {
            "current_baseline": baseline,
            "checkin_count": data.get("checkin_count", 0) + 1,
            "last_20_scores": scores
        })
    else:
        # First check-in
        store.put(namespace, "baseline", {
            "current_baseline": new_score,
            "checkin_count": 1,
            "last_20_scores": [new_score]
        })

def get_user_patterns(store: BaseStore, user_id: str) -> dict:
    """Get detected loops, doorways, and triggers."""
    namespace = ("memories", user_id)
    item = store.get(namespace, "loops_doorways")
    return item.value if item else {"loops": [], "doorways": []}

def update_body_patterns(store: BaseStore, user_id: str, body_signals: list) -> None:
    """Update body pattern frequencies."""
    namespace = ("memories", user_id)
    current = store.get(namespace, "body_patterns")
    patterns = current.value if current else {}

    for signal in body_signals:
        location = signal.split(":")[0].strip()
        patterns[location] = patterns.get(location, 0) + 1

    store.put(namespace, "body_patterns", patterns)

def update_triggers(store: BaseStore, user_id: str, triggers: list) -> None:
    """Update trigger frequencies."""
    namespace = ("memories", user_id)
    current = store.get(namespace, "triggers")
    trigger_counts = current.value if current else {}

    for trigger in triggers:
        trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1

    store.put(namespace, "triggers", trigger_counts)
```

---

## Error Handling

### LLM Failures

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_llm_with_retry(prompt: str) -> str:
    return chat_service.generate(prompt)
```

**Fallback responses by strategy:**

- Question: "What's here right now?"
- Reflect: "Stay with what's present."
- Teach: "Notice the pattern."
- Challenge: "Return to the body."

### Store Failures

```python
def deep_agent_with_fallback(state: MultiAgentState) -> dict:
    try:
        return deep_agent(state)
    except StoreUnavailableError:
        logger.error("LangGraph Store unavailable, using defaults")
        return {
            "user_model": get_default_user_model(),
            "relative_depth": "medium"
        }
```

---

## Testing Strategy

### Unit Tests

**Test each agent independently:**

```python
def test_extraction_agent():
    state = {"user_input": "chest tight, meeting soon"}
    result = extraction_agent(state)

    assert result["extraction"]["body_signals"] == ["chest: tight"]
    assert result["extraction"]["triggers"] == ["meeting"]
    assert result["extraction"]["specificity_score"] >= 6

def test_deep_agent_relative_depth():
    # Mock user with baseline 3.0
    state = {
        "user_id": "test_user",
        "extraction": {"specificity_score": 8}
    }

    result = deep_agent(state)
    assert result["relative_depth"] == "deep"  # 8 > 3 + 2
```

### Integration Tests

**Test full workflow:**

```python
def test_full_workflow_shallow_to_deep():
    # First check-in: shallow
    result1 = process_checkin(user_id="test", input="stressed")
    assert result1["card_decision"]["award_card"] == False
    assert result1["teaching_strategy"]["strategy"] == "question"

    # Second check-in: deeper
    result2 = process_checkin(user_id="test", input="chest tight, shoulders tense")
    assert result2["card_decision"]["award_card"] == True
    assert result2["teaching_strategy"]["strategy"] == "reflect"
```

### Manual Testing

**Test scenarios:**

1. New user journey (Day 1-7)
2. Pattern detection (loop appears 3+ times)
3. Regression handling (deep → shallow)
4. Card award logic (various criteria)
5. Teaching strategy transitions

---

## Performance Requirements

- **Total latency:** < 3 seconds end-to-end
- **Extraction Agent:** < 0.5s
- **Deep Agent:** < 0.5s (including Store operations)
- **Teaching + Card Agents:** < 0.5s (parallel)
- **Response Generation:** < 1.5s (including RAG)

---

## Security Considerations

1. **User isolation:** Verify user_id matches authenticated user
2. **Data encryption:** Encrypt Store data at rest
3. **PII handling:** No PII in logs
4. **Access logging:** Log all Store access for audit
5. **Data deletion:** Support GDPR right to be forgotten

---

**Last Updated:** 2025-10-28  
**Status:** Ready for Implementation
