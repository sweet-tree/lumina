# Depth Evaluation Algorithm: Current State & Improvements

**Date:** 2025-10-27  
**Status:** Research & Recommendations  
**Purpose:** Guide evolution of Lumina's depth evaluation toward state-of-the-art consciousness guidance

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
- ❌ Binary decision (no nuance)
- ❌ No context from previous check-ins
- ❌ Can't detect patterns over time

---

## 🚀 State-of-the-Art Improvements (Ranked by Impact)

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

## 🎯 Recommended Implementation Roadmap

### Phase 1: Quick Wins (Week 1-2)

1. **Chain-of-Thought Reasoning** - Improve accuracy immediately
2. **Few-Shot Learning** - Add examples to prompt
3. **Confidence Scoring** - Handle edge cases

**Expected Impact:** 20-30% improvement in classification accuracy

---

### Phase 2: Reflection (Week 3-4)

4. **Reflection Loop** - Self-critique classification
5. **Multi-Dimensional Evaluation** - Track body/breath/context separately

**Expected Impact:** Richer data for pattern recognition, foundation for personalization

---

### Phase 3: Personalization (Month 2)

6. **User Progression Tracking** - Long-term memory with Deep Agents
7. **Trajectory Evaluation** - Weekly pattern analysis

**Expected Impact:** Personalized guidance, breakthrough moments

---

### Phase 4: Advanced (Month 3+)

8. **Multi-Agent System** - Specialized evaluators
9. **Semantic Embeddings** - Consistency via similarity
10. **Contextual Depth** - Time/streak awareness

**Expected Impact:** State-of-the-art consciousness guidance system

---

## 💡 The Enlightenment Path

### Key Insight:

Enlightenment isn't about better classification—it's about **guiding users from thinking → feeling → being**.

### The Real Innovation:

- Track **progression** (are they going deeper over time?)
- Identify **doorways** (what helps them access presence?)
- Recognize **loops** (where they get stuck)
- Intervene **precisely** (right teaching at right time)

### This Requires:

- Long-term memory (know the user)
- Pattern recognition (see what they can't)
- Personalized guidance (not generic)
- Relationship (Lumina as teacher, not tool)

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

1. **Review this document** with the team
2. **Prioritize improvements** based on impact vs effort
3. **Start with Phase 1** (quick wins)
4. **Measure impact** using LangSmith evaluation datasets
5. **Iterate** based on real user data

---

**Last Updated:** 2025-10-27  
**Author:** Research via LangChain MCP + Web Search  
**Status:** Ready for implementation planning
