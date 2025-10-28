# Depth Evaluation Algorithm: Revised Architecture

**Date:** 2025-10-28  
**Status:** Final Architecture - Ready for Implementation  
**Purpose:** Multi-agent system with memory for personalized consciousness guidance

---

## 📊 Current Algorithm (Simple LLM Classification)

### How It Works:

```
User Input → LLM with prompt → "shallow"/"medium"/"deep"
```

**Implementation:**

- Single LLM call with classification criteria
- Temperature: 0.3 (low for consistency)
- Max tokens: 10 (just need one word)
- Fallback: defaults to "medium" if invalid

**Strengths:**

- ✅ Fast (~0.7s)
- ✅ Simple
- ✅ Works reasonably well

**Weaknesses:**

- ❌ No self-reflection
- ❌ No learning from user progression
- ❌ Absolute scale (not relative to user)
- ❌ No context from previous check-ins
- ❌ Can't detect patterns over time
- ❌ No guidance to help users go deeper
- ❌ No card reward logic

---

## 🎯 Core Insight: Depth is Relative, Not Absolute

**Key realization:** "Stressed" is shallow for an experienced user, but might be deep for someone just starting.

**Depth = Information density relative to user's baseline**

- User A (baseline: "stressed") → "chest tight" = DEEP
- User B (baseline: "left shoulder blade, sharp pulling") → "chest tight" = SHALLOW

**This changes everything.**

---

## 🏗️ New Architecture: Four-Agent System

### Overview:

```
User Input
    ↓
1. Extraction Agent (extract structured signal)
    ↓
2. Deep Agent (user model + memory + patterns)
    ↓
    ├─→ 3. Teaching Agent (pedagogical strategy)
    └─→ 4. Card Agent (reward decision)
         ↓
Response Generation + Card (if earned)
```

---

## Agent 1: Extraction Agent

**Job:** Extract structured signal from user input

**Input:** Raw user text

**Output:**

```json
{
  "body_signals": ["chest: tight", "breath: shallow"],
  "triggers": ["meeting"],
  "temporal": "future (10 min)",
  "specificity_score": 8
}
```

**Why it matters:**

- Objective measurement (no judgment)
- Structured data for pattern detection
- Foundation for all other agents

**Implementation:**

- Single LLM call with structured output
- Prompt: "Extract body signals, triggers, temporal context, specificity (0-10)"
- Fast (~0.5s)

---

## Agent 2: Deep Agent (Memory)

**Job:** Maintain user model, detect patterns, evaluate relative depth

**Input:** Extraction output + user_id

**Output:**

```json
{
  "user_baseline": 3.2,
  "current_depth": "deep",
  "patterns": {
    "loops": ["tension → depleted → foggy"],
    "doorways": ["awareness → ease"],
    "triggers": { "meetings": 31, "mondays": 18 }
  },
  "trajectory": "stuck_shallow_5_days",
  "in_loop": true
}
```

**Uses LangGraph Store:**

```
/memories/user_123/
  body_patterns.txt
  triggers.txt
  loops_doorways.txt
  baseline.txt
  progression.txt
```

**Why it matters:**

- Personalization (knows THIS user)
- Pattern recognition (sees what they can't)
- Relative evaluation (deep for them, not absolute)
- Long-term memory (learns over time)

**Key logic:**

```python
if current_specificity > user_baseline + 2:
    depth = "deep"
elif current_specificity < user_baseline - 2:
    depth = "shallow"
else:
    depth = "medium"
```

---

## Agent 3: Teaching Agent

**Job:** Decide pedagogical strategy (when to guide, when to reflect)

**Input:** Deep Agent output

**Output:**

```json
{
  "strategy": "question",
  "guidance": "Ask about body location",
  "reason": "Stuck shallow 5 days, needs guidance"
}
```

**Strategies:**

1. **Reflect** - Mirror their awareness (when doing well)

   - "The chest tightness knows something. What is it showing you?"

2. **Question** - Guide deeper (when stuck shallow)

   - "Where in your body is the stress?"

3. **Teach** - Explain pattern (when pattern detected)

   - "This is the third time tension led to depletion. Notice the pattern?"

4. **Challenge** - Point out regression (when they were deeper before)
   - "You were with the sensations. Now you're back in labels. What happened?"

**When each strategy activates:**

- **Stuck shallow (5+ check-ins):** Question
- **Consistent medium:** Expand awareness
- **Regressing:** Challenge
- **Deep/progressing:** Reflect

**Why it matters:**

- Guides users toward embodiment
- Prevents stagnation
- Creates dialogue (not just logging)
- Lumina as teacher, not just mirror

---

## Agent 4: Card Agent

**Job:** Decide if card earned, which card, what rarity

**Input:** Extraction + Deep Agent output

**Output:**

```json
{
  "award_card": true,
  "card_id": "body_tension",
  "rarity": "common",
  "reason": "Deep reflection, specificity > threshold"
}
```

**Card award criteria:**

**Award card when:**

- Deep reflection (specificity > user_baseline + 2)
- Multiple check-ins today (commitment)
- Breakthrough moment (pattern broken, loop exited)
- Consistent practice (3+ days streak)

**Don't award card when:**

- Shallow check-in (specificity < threshold)
- First attempt of day (give chance to go deeper)
- Regressing without awareness

**Card rarity logic:**

- **Common:** Daily deep check-ins
- **Rare:** Weekly pattern detected
- **Epic:** Monthly consciousness map
- **Legendary:** Major breakthrough (loop broken)

**Why it matters:**

- Gamification without being "gamey"
- Rewards depth, not just participation
- Creates incentive to go deeper
- Dialogue mechanic (no card → question → try again → card)

---

## 🚀 Why This Architecture Works

### 1. Separation of Concerns

- Each agent has ONE job
- Easy to tune independently
- Clear responsibilities

### 2. Personalization

- Deep Agent knows user's baseline
- Depth is relative, not absolute
- Learns patterns over time

### 3. Guidance

- Teaching Agent prevents stagnation
- Actively guides users deeper
- Creates teacher-student relationship

### 4. Engagement

- Card Agent creates reward system
- Earned, not automatic
- Incentivizes depth

### 5. Scalability

- Add new agents easily (e.g., Pattern Prediction Agent)
- Parallel execution (Teaching + Card agents)
- LangGraph handles orchestration

---

## 🔄 Complete Flow Example

### Scenario 1: Shallow User

**Input:** "stressed"

**Extraction Agent:**

```json
{ "body_signals": [], "triggers": [], "specificity_score": 2 }
```

**Deep Agent:**

```json
{
  "user_baseline": 3.2,
  "current_depth": "shallow",
  "trajectory": "stuck_shallow_5_days"
}
```

**Teaching Agent:**

```json
{ "strategy": "question", "guidance": "Ask about body location" }
```

**Card Agent:**

```json
{ "award_card": false, "reason": "Too shallow, guide deeper first" }
```

**Response:** "Where in your body is the stress?"

**No card shown** (incentive to go deeper)

---

### Scenario 2: User Goes Deeper

**Input:** "chest tight, shoulders tense"

**Extraction Agent:**

```json
{ "body_signals": ["chest: tight", "shoulders: tense"], "specificity_score": 7 }
```

**Deep Agent:**

```json
{ "user_baseline": 3.2, "current_depth": "deep", "trajectory": "progressing" }
```

**Teaching Agent:**

```json
{ "strategy": "reflect", "guidance": "Mirror awareness" }
```

**Card Agent:**

```json
{ "award_card": true, "card_id": "body_tension", "rarity": "common" }
```

**Response:** "The body speaks. Chest and shoulders holding. What are they protecting?"

**Card reveals** (reward for depth)

---

### Scenario 3: Pattern Detected

**Input:** "tired again" (after 5 check-ins showing tension → depleted pattern)

**Deep Agent:**

```json
{ "patterns": { "loops": ["tension → depleted"] }, "in_loop": true }
```

**Teaching Agent:**

```json
{ "strategy": "teach", "guidance": "Reveal pattern" }
```

**Response:** "This is the fifth time tension led to depletion. The pattern is showing itself. What if the tiredness is the body's response to holding?"

**Rare card awarded** (pattern recognition milestone)

---

## 🚀 State-of-the-Art Improvements (Archived for Reference)

### 1. Reflection & Self-Critique Loop ⭐⭐⭐⭐⭐

**Pattern:** Agent evaluates its own classification

```
Input → Initial Classification → Self-Critique → Final Classification
```

**Implementation:**

- First pass: LLM classifies depth
- Second pass: LLM critiques its own decision
- Questions: "Did I miss body awareness? Is there hidden context?"
- Final decision based on reflection

**Why it matters for enlightenment:**

- Mirrors meditation practice (observe the observer)
- Catches subtle cues (breath mentions, body sensations)
- More accurate depth detection = better guidance

**Effort:** Medium | **Impact:** High

**References:**

- LangChain Deep Agents: Self-reflection capabilities
- Evaluation patterns: Agent trajectory analysis

---

### 2. Multi-Dimensional Evaluation ⭐⭐⭐⭐⭐

**Pattern:** Evaluate multiple aspects, not just depth

```
Input → [Body Awareness, Breath Awareness, Context, Emotion, Pattern] → Composite Score
```

**Dimensions to track:**

- **Body awareness**: 0-10 (none → specific sensations)
- **Breath awareness**: 0-10 (not mentioned → detailed)
- **Contextual specificity**: 0-10 (vague → precise situation)
- **Emotional vs somatic**: Ratio
- **Present moment**: Past/future vs now

**Why it matters for enlightenment:**

- Dzogchen principle: "Short moments, many times"
- Track actual progress toward embodiment
- Guide users from thinking → feeling → being

**Effort:** Medium | **Impact:** Very High

---

### 3. User Progression Tracking (Long-term Memory) ⭐⭐⭐⭐⭐

**Pattern:** Deep Agents with persistent memory

```
Check-in → Evaluate with history → Update user profile → Personalized response
```

**What to track:**

- Baseline depth (where they usually start)
- Progression over time (shallow → medium → deep)
- Patterns (always tense on Mondays)
- Doorways (what helps them go deeper)
- Loops (recurring patterns)

**Implementation (from Deep Agents docs):**

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    store=store,
    use_longterm_memory=True,
    system_prompt="""Read /memories/user_profile.txt to understand:
    - User's baseline depth
    - Common patterns
    - What helps them deepen

    Update this file as you learn."""
)
```

**Why it matters for enlightenment:**

- Personalized guidance (not one-size-fits-all)
- Recognizes growth (celebrates progress)
- Identifies stuck points (where they need help)
- Builds relationship (Lumina knows them)

**Effort:** High | **Impact:** Transformative

**References:**

- Deep Agents: Long-term memory with LangGraph Store
- Self-improving instructions pattern

---

### 4. Trajectory Evaluation (Not Just Final Response) ⭐⭐⭐⭐

**Pattern:** Evaluate the path, not just the destination

```
Week of check-ins → Analyze trajectory → Identify patterns → Intervention
```

**What to evaluate:**

- Are they going deeper over time?
- Do they regress after certain events?
- What triggers shallow vs deep check-ins?
- Are they stuck in a loop?

**Implementation (from LangSmith docs):**

- Create datasets of user check-ins
- Run trajectory evaluations weekly
- LLM-as-judge: "Is this user progressing?"
- Trigger interventions (Lumina suggests practices)

**Why it matters for enlightenment:**

- Consciousness development isn't linear
- Patterns reveal unconscious habits
- Intervention at right time = breakthrough

**Effort:** Medium | **Impact:** High

**References:**

- LangSmith: Agent trajectory evaluation
- Evaluation concepts: Multi-turn evaluation

---

### 5. Multi-Agent Depth Evaluation ⭐⭐⭐⭐

**Pattern:** Specialized agents for different aspects

```
Input → [Body Agent, Breath Agent, Context Agent, Integration Agent] → Consensus
```

**Agents:**

- **Body Agent**: Detects somatic awareness
- **Breath Agent**: Evaluates breath mentions
- **Context Agent**: Assesses situational specificity
- **Emotion Agent**: Distinguishes feeling vs sensation
- **Integration Agent**: Synthesizes all inputs

**Why it matters for enlightenment:**

- Holistic evaluation (not reductionist)
- Each agent is expert in its domain
- Catches nuances single LLM misses

**Effort:** High | **Impact:** High

**References:**

- Multi-agent systems: Specialized agents for complex tasks
- Context engineering: What each agent sees

---

### 6. Few-Shot Learning with Examples ⭐⭐⭐

**Pattern:** Show LLM examples of each depth level

```
Prompt with 5 examples per depth → Classify new input
```

**Examples to include:**

- **Shallow**: "I'm ok", "tired", "stressed"
- **Medium**: "shoulders tight", "chest heavy"
- **Deep**: "chest tight, breath shallow, meeting soon"

**Why it matters:**

- More consistent classifications
- Reduces ambiguity
- Aligns with your vision of depth

**Effort:** Low | **Impact:** Medium

---

### 7. Semantic Embeddings + Clustering ⭐⭐⭐

**Pattern:** Use embeddings to find similar check-ins

```
Input → Embed → Find similar past check-ins → Use their depth as reference
```

**How it works:**

- Embed all check-ins
- New check-in → find 5 most similar
- If 4/5 were "deep", likely this is too
- Combine with LLM classification

**Why it matters:**

- Consistency across similar inputs
- Learns from patterns
- Less reliant on single LLM call

**Effort:** Medium | **Impact:** Medium

---

### 8. Chain-of-Thought Reasoning ⭐⭐⭐⭐

**Pattern:** Make LLM explain its reasoning

```
Input → LLM thinks step-by-step → Classification with reasoning
```

**Prompt:**

```
Think step by step:
1. Is there body awareness mentioned? (yes/no + evidence)
2. Is there breath awareness? (yes/no + evidence)
3. Is there specific context? (yes/no + evidence)
4. Based on above, classify as shallow/medium/deep
```

**Why it matters:**

- More accurate (reasoning improves LLM performance)
- Debuggable (see why it classified that way)
- Teachable (can improve prompts based on reasoning)

**Effort:** Low | **Impact:** Medium-High

---

### 9. Confidence Scoring ⭐⭐⭐

**Pattern:** LLM provides confidence with classification

```
Input → Classification + Confidence (0-100%) → Handle uncertainty
```

**Use confidence:**

- Low confidence → ask clarifying question
- High confidence → proceed with classification
- Medium confidence → default to "medium"

**Why it matters:**

- Handles edge cases gracefully
- Opportunity for dialogue (ask user to clarify)
- More honest (admits uncertainty)

**Effort:** Low | **Impact:** Medium

---

### 10. Contextual Depth (Time of Day, Streak, etc.) ⭐⭐⭐

**Pattern:** Consider external factors

```
Input + Context (time, streak, last depth) → Adjusted classification
```

**Context to consider:**

- Time of day (morning vs evening)
- Streak (day 1 vs day 30)
- Previous depth (progression or regression)
- Day of week (patterns)

**Why it matters:**

- Depth is contextual
- Celebrates progress (deeper on day 30 than day 1)
- Identifies patterns (always shallow on Mondays)

**Effort:** Low | **Impact:** Medium

---

## 🎯 Implementation Roadmap

### Phase 1: Core Four-Agent System (Week 1-2)

**Build:**

1. Extraction Agent (structured signal extraction)
2. Deep Agent with LangGraph PostgresStore (user model + memory)
3. Teaching Agent (pedagogical strategy)
4. Card Agent (reward logic)

**Storage:**

- LangGraph PostgresStore connected to existing Supabase database
- Helper functions in `backend/services/user_memory.py`
- JSON-based memory storage (baseline, patterns, triggers)

**Deliverables:**

- New service file: `backend/services/multi_agent_service.py`
- PostgresStore setup in Supabase (run `store.setup()` once)
- User memory helper functions (get/update baseline, patterns, triggers)
- LangGraph workflow with 4 agents
- Basic pattern detection (loops, triggers)
- Card award logic

**Expected Impact:**

- Personalized depth evaluation (relative to user baseline)
- User guidance system (Teaching Agent)
- Pattern recognition foundation
- Persistent memory across sessions

---

### Phase 2: Memory & Patterns (Week 3-4)

**Enhance:**

1. Deep Agent memory operations (body_patterns, triggers, loops, doorways in PostgresStore)
2. Pattern detection algorithms (loop identification, doorway discovery)
3. Baseline calculation (rolling average of last 20 check-ins)
4. Trajectory tracking (progression over time)

**Deliverables:**

- Persistent user profiles
- Pattern naming ("The Monday Morning Spiral")
- Doorway identification (what breaks loops)
- Weekly synthesis (rare card generation)

**Expected Impact:**

- "Wow" moments (pattern revelation)
- Personalized insights
- Rare card system working

---

### Phase 3: Advanced Teaching (Month 2)

**Add:**

1. Predictive patterns (anticipate loops)
2. Proactive interventions (suggest doorways)
3. Confidence scoring (when to ask for clarification)
4. Multi-turn dialogue (follow-up questions)

**Deliverables:**

- "You're entering the loop again" predictions
- "Try your doorway?" suggestions
- Clarifying questions when ambiguous
- Dialogue flow (not just one-shot)

**Expected Impact:**

- Proactive guidance
- Breakthrough acceleration
- Deeper user relationship

---

### Phase 4: Optimization (Month 3+)

**Optimize:**

1. Chain-of-thought in agent prompts (better reasoning)
2. Few-shot examples (consistency)
3. Semantic embeddings (find similar check-ins)
4. A/B testing framework (tune thresholds)

**Deliverables:**

- Improved agent accuracy
- Faster pattern detection
- Optimized card award criteria
- Data-driven tuning

**Expected Impact:**

- Higher accuracy
- Faster time-to-pattern
- Better user experience

---

## 💡 Key Principles

### 1. Depth is Relative

Not "is this deep?" but "is this deep for THIS user?"

### 2. Guidance Over Judgment

Don't just classify—guide them deeper when stuck.

### 3. Patterns Over Points

One check-in is data. Ten check-ins reveal patterns.

### 4. Memory Enables Personalization

Without memory, every check-in is the first check-in.

### 5. Separation of Concerns

Each agent has one job. Easy to tune, easy to understand.

### 6. Earned Rewards

Cards are earned through depth, not just participation.

### 7. Teacher, Not Tool

Lumina guides, challenges, teaches—not just mirrors.

---

## 📚 References & Research

### LangChain/LangGraph Documentation:

- Deep Agents: https://docs.langchain.com/oss/python/deepagents/overview
- Long-term Memory: https://docs.langchain.com/oss/python/deepagents/long-term-memory
- Multi-agent Systems: https://docs.langchain.com/oss/python/langchain/multi-agent
- Agent Evaluation: https://docs.langchain.com/langsmith/evaluate-complex-agent
- Trajectory Evaluation: https://docs.langchain.com/langsmith/evaluation-approaches

### Consciousness & Meditation:

- Dzogchen: "Short moments, many times" - present moment awareness
- Rigpa: Direct experience of the ultimate ground of existence
- Embodiment: Moving from conceptual to somatic awareness

### Current Implementation:

- Location: `backend/services/depth_evaluator.py`
- Method: Single LLM call with classification prompt
- Temperature: 0.3, Max tokens: 10
- Fallback: "medium" on invalid response

---

## 🚀 Next Steps

1. **Create implementation spec** (`.kiro/specs/multi-agent-depth-system/`)
2. **Define requirements** (user stories for 4-agent system)
3. **Design architecture** (LangGraph flow, state schema, agent interfaces)
4. **Build Phase 1** (core 4-agent system)
5. **Test with real users** (measure pattern detection, card awards, guidance quality)
6. **Iterate** based on data

---

**Last Updated:** 2025-10-28  
**Author:** Architecture discussion & refinement  
**Status:** Final architecture - Ready for spec creation
