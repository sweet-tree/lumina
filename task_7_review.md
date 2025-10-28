# Task 7 Review: LangGraph Workflow Implementation

## Current Status - What We've Built

### ✅ Completed Agents (Tasks 1-6)

#### 1. **Extraction Agent** (Task 2)

- **File:** `backend/services/extraction_agent.py`
- **Node Function:** `extraction_agent_node(state: Dict) -> Dict`
- **Output:** `{"extraction": {body_signals, triggers, temporal, specificity_score}}`
- **Status:** ✅ Complete with 11 passing tests

#### 2. **Deep Agent** (Task 3)

- **File:** `backend/services/deep_agent.py`
- **Node Function:** `deep_agent_node(state: Dict, *, store: BaseStore) -> Dict`
- **Output:** `{"user_model": {...}, "relative_depth": "shallow|medium|deep"}`
- **Special:** Requires `store` parameter (injected by LangGraph)
- **Status:** ✅ Complete with 10 passing tests

#### 3. **Teaching Agent** (Task 4)

- **File:** `backend/services/teaching_agent.py`
- **Node Function:** `teaching_agent_node(state: Dict[str, Any]) -> Dict[str, Any]`
- **Output:** `{"teaching_strategy": {strategy, guidance, reason}}`
- **Status:** ✅ Complete with 8 passing tests

#### 4. **Card Agent** (Task 5)

- **File:** `backend/services/card_agent.py`
- **Node Function:** `card_agent_node(state: Dict[str, Any]) -> Dict[str, Any]`
- **Output:** `{"card_decision": {award_card, card_id, rarity, reason}}`
- **Status:** ✅ Complete with 15 passing tests

#### 5. **Response Generation** (Task 6)

- **File:** `backend/services/response_generation.py`
- **Node Function:** `response_generation_node(state: Dict[str, Any]) -> Dict[str, Any]`
- **Output:** `{"rag_contexts": [...], "final_response": "..."}`
- **Status:** ✅ Complete with 10 passing tests

---

## Task 7 Requirements Analysis

### 7.1 Create StateGraph with all agents

**Required:**

- Define `MultiAgentState` TypedDict
- Add all 5 agent nodes to graph
- Initialize PostgresStore for Deep Agent

**Current Alignment:**
✅ All node functions exist and follow LangGraph conventions
✅ Deep Agent already uses `store` parameter correctly
⚠️ Need to define `MultiAgentState` TypedDict with proper annotations
⚠️ Need to initialize PostgresStore and pass to graph

**State Schema (from design):**

```python
class MultiAgentState(TypedDict):
    # Input
    user_id: str
    user_input: str
    session_id: str

    # Extraction Agent output
    extraction: dict

    # Deep Agent output
    user_model: dict
    relative_depth: str

    # Teaching Agent output
    teaching_strategy: dict

    # Card Agent output
    card_decision: dict

    # Response generation
    rag_contexts: Annotated[list[dict], add]  # Uses reducer for parallel
    final_response: str
```

---

### 7.2 Configure workflow edges

**Required Flow:**

1. **Sequential:** Extraction → Deep Agent
2. **Parallel:** Deep Agent → (Teaching Agent + Card Agent)
3. **Convergence:** (Teaching + Card) → Response Generation
4. **End:** Response Generation → END

**Implementation Notes:**

- Use `add_edge()` for sequential connections
- Use `add_edge()` from Deep Agent to both Teaching and Card (LangGraph handles parallel)
- Both Teaching and Card must complete before Response Generation
- No conditional edges needed (all paths are deterministic)

**Workflow Diagram:**

```
START
  ↓
extraction_agent_node
  ↓
deep_agent_node (with store)
  ↓
  ├─→ teaching_agent_node ─┐
  └─→ card_agent_node ──────┤
                            ↓
                  response_generation_node
                            ↓
                          END
```

---

### 7.3 Compile and test workflow

**Required:**

- Compile StateGraph to CompiledGraph
- Test with sample inputs (shallow, medium, deep)
- Verify state propagation through all nodes
- Check parallel execution of Teaching + Card agents
- Verify timing requirements (< 3s total)

---

## Key Implementation Considerations

### 1. **PostgresStore Integration**

- Deep Agent requires `store` parameter
- Must use `StateGraph` with `store` parameter in compile
- Store is injected automatically by LangGraph

**Example:**

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver

# Initialize store
store = PostgresSaver.from_conn_string(DATABASE_URL)
store.setup()

# Create graph with store
graph = StateGraph(MultiAgentState)
# ... add nodes ...
compiled = graph.compile(checkpointer=store)
```

### 2. **Parallel Execution**

- Teaching Agent and Card Agent run in parallel after Deep Agent
- Both must complete before Response Generation
- Use `rag_contexts` with `Annotated[list[dict], add]` reducer
- This allows future parallel RAG retrieval if needed

### 3. **State Propagation**

- Each node returns a dict that updates the state
- State is passed through all nodes automatically
- Final state contains all outputs from all agents

### 4. **Error Handling**

- Each agent already has internal error handling
- Fallback responses implemented in Response Generation
- Task 8 will add retry logic and additional error handling

---

## Potential Issues & Solutions

### Issue 1: Deep Agent Store Parameter

**Problem:** Deep Agent node requires `store` parameter, others don't
**Solution:** LangGraph supports mixed signatures - store is injected only where needed

### Issue 2: Parallel Node Coordination

**Problem:** Need to ensure both Teaching and Card complete before Response
**Solution:** LangGraph automatically waits for all parallel branches before continuing

### Issue 3: State Type Consistency

**Problem:** Some nodes use `Dict`, others use `Dict[str, Any]`
**Solution:** TypedDict will enforce consistency, but runtime is flexible

### Issue 4: Session ID

**Problem:** State schema includes `session_id` but not used yet
**Solution:** Include in state schema for future use, not required for MVP

---

## Recommended Implementation Order

### Step 1: Define State Schema

- Create `MultiAgentState` TypedDict in `multi_agent_service.py`
- Use proper annotations (especially `Annotated[list[dict], add]` for rag_contexts)

### Step 2: Initialize PostgresStore

- Get DATABASE_URL from config
- Create PostgresSaver instance
- Run setup() once

### Step 3: Build StateGraph

- Create StateGraph with MultiAgentState
- Add all 5 nodes in order
- Configure edges (sequential + parallel)

### Step 4: Compile Graph

- Compile with checkpointer (PostgresSaver)
- This enables persistence and store injection

### Step 5: Test Workflow

- Test with shallow input ("stressed")
- Test with medium input ("chest tight")
- Test with deep input ("chest tight, breath shallow, meeting soon")
- Verify all agents execute
- Check timing (< 3s)

---

## Success Criteria

✅ All 5 agents integrated into single workflow
✅ State propagates correctly through all nodes
✅ Parallel execution works (Teaching + Card)
✅ PostgresStore connected and working
✅ Sample inputs produce complete responses
✅ Total latency < 3 seconds
✅ No errors or exceptions in happy path

---

## Next Steps After Task 7

- **Task 8:** Add retry logic and enhanced error handling
- **Task 9:** Create FastAPI endpoint integration
- **Task 10:** Data privacy and security
- **Task 11:** Performance optimization
- **Task 12:** Documentation and deployment

---

## Conclusion

**Alignment Status: ✅ READY**

All prerequisite tasks (1-6) are complete and properly structured for LangGraph integration. The node functions follow LangGraph conventions, state outputs are consistent, and the workflow design is clear.

**Key Points:**

1. All agents have node functions ready
2. Deep Agent correctly uses store parameter
3. State schema is well-defined in design doc
4. Workflow edges are straightforward (no complex conditionals)
5. Parallel execution pattern is standard LangGraph

**Recommendation:** Proceed with Task 7 implementation. The foundation is solid.
