# Implementation Plan: Multi-Agent Depth System

## Overview

This implementation plan breaks down the Multi-Agent Depth System into discrete, actionable tasks. Each task builds incrementally on previous work, ending with a fully integrated system.

---

## Tasks

- [x] 1. Set up LangGraph PostgresStore and state schema

  - Install `langgraph-checkpoint-postgres` for PostgresStore support
  - Create new file `backend/services/multi_agent_service.py`
  - Define `MultiAgentState` TypedDict with all required fields
  - Initialize PostgresStore connected to existing Supabase database (use DATABASE_URL from backend/.env)
  - Run `store.setup()` once to create Store tables in Supabase
  - Create `backend/services/user_memory.py` with helper functions:
    - `get_user_baseline(store, user_id) -> float`
    - `update_user_baseline(store, user_id, score) -> None`
    - `get_user_patterns(store, user_id) -> dict`
    - `update_body_patterns(store, user_id, signals) -> None`
    - `update_triggers(store, user_id, triggers) -> None`
  - _Requirements: 2.1, 10.5_

- [ ] 2. Implement Extraction Agent

  - [x] 2.1 Create extraction agent node function

    - Write prompt template for signal extraction
    - Include few-shot examples in prompt
    - Parse JSON output from LLM
    - Handle malformed JSON with fallback
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [x] 2.2 Add specificity scoring logic

    - Implement 0-10 scoring in prompt
    - Validate score is within range
    - Log extraction results
    - _Requirements: 1.4, 1.5_

  - [ ]\* 2.3 Write unit tests for extraction agent
    - Test with shallow input ("stressed")
    - Test with deep input ("chest tight, breath shallow, meeting soon")
    - Test with edge cases (empty input, very long input)
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 3. Implement Deep Agent with memory

  - [ ] 3.1 Create user memory file structure

    - Define memory file paths for each user
    - Create baseline.txt schema
    - Create body_patterns.txt schema
    - Create triggers.txt schema
    - Create loops_doorways.txt schema
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ] 3.2 Implement memory read/write operations

    - Write `load_baseline()` function
    - Write `update_baseline()` function (rolling average)
    - Write `update_body_patterns()` function
    - Write `update_triggers()` function
    - Handle missing files (new users)
    - _Requirements: 2.2, 2.3, 2.4_

  - [ ] 3.3 Implement relative depth evaluation

    - Calculate depth relative to user baseline
    - Handle new users (< 5 check-ins) with default baseline
    - Return depth classification with baseline for transparency
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [ ] 3.4 Implement pattern detection

    - Write `detect_loops()` function (recurring sequences)
    - Write `detect_doorways()` function (loop-breaking transitions)
    - Write `detect_triggers()` function (frequent contextual factors)
    - Assign human-readable names to patterns
    - Store patterns in loops_doorways.txt
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ]\* 3.5 Write unit tests for Deep Agent
    - Test baseline calculation
    - Test relative depth evaluation
    - Test pattern detection with mock history
    - Test new user handling
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3_

- [ ] 4. Implement Teaching Agent

  - [ ] 4.1 Create teaching strategy decision logic

    - Implement "question" strategy (stuck shallow 5+ days)
    - Implement "challenge" strategy (regressing)
    - Implement "teach" strategy (pattern detected)
    - Implement "reflect" strategy (default)
    - Return strategy with guidance and reason
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ] 4.2 Create trajectory calculation helper

    - Calculate stuck_shallow_count from recent check-ins
    - Detect regression (current < previous 3 average)
    - Return trajectory summary
    - _Requirements: 5.1, 5.2_

  - [ ]\* 4.3 Write unit tests for Teaching Agent
    - Test each strategy activation condition
    - Test trajectory calculation
    - Test strategy selection logic
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 5. Implement Card Agent

  - [ ] 5.1 Create card award decision logic

    - Award card for deep reflection
    - Award card for multiple check-ins today
    - Award rare card for pattern detection
    - Award rare card for loop breaking
    - Don't award card for shallow first attempt
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ] 5.2 Implement card selection logic

    - Select card based on extraction signals
    - Map signals to card library
    - Determine rarity (common/rare/epic/legendary)
    - Return card decision with reason
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [ ]\* 5.3 Write unit tests for Card Agent
    - Test each award criterion
    - Test card selection logic
    - Test rarity determination
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 6. Implement Response Generation

  - [ ] 6.1 Create response generation function

    - Build prompts for each teaching strategy
    - Integrate RAG retrieval for spiritual wisdom
    - Generate response using strategy + RAG + user input
    - Handle different strategies (question, reflect, teach, challenge)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ] 6.2 Integrate with existing RAG system

    - Use existing VectorStoreService
    - Retrieve relevant passages based on user input and strategy
    - Format RAG contexts for prompt
    - _Requirements: 7.5_

  - [ ]\* 6.3 Write unit tests for response generation
    - Test each strategy prompt
    - Test RAG integration
    - Test response quality (manual review)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 7. Build LangGraph workflow

  - [ ] 7.1 Create StateGraph with all agents

    - Define MultiAgentState schema
    - Add Extraction Agent node
    - Add Deep Agent node
    - Add Teaching Agent node
    - Add Card Agent node
    - Add Response Generation node
    - _Requirements: 10.1, 10.2_

  - [ ] 7.2 Configure workflow edges

    - Sequential: Extraction → Deep Agent
    - Parallel: Deep Agent → (Teaching Agent + Card Agent)
    - Convergence: (Teaching + Card) → Response Generation
    - Add conditional edges if needed
    - _Requirements: 10.1_

  - [ ] 7.3 Compile and test workflow
    - Compile StateGraph
    - Test with sample inputs
    - Verify state propagation
    - Check parallel execution
    - _Requirements: 10.1, 10.2_

- [ ] 8. Add error handling and retries

  - [ ] 8.1 Add retry logic to LLM calls

    - Use tenacity for exponential backoff
    - Retry up to 3 times
    - Log retry attempts
    - _Requirements: 8.2_

  - [ ] 8.2 Implement fallback responses

    - Define fallback for each teaching strategy
    - Handle Store unavailable errors
    - Handle LLM failures gracefully
    - Log all errors
    - _Requirements: 8.3, 8.4_

  - [ ]\* 8.3 Write error handling tests
    - Test LLM failure scenarios
    - Test Store unavailable scenarios
    - Test fallback responses
    - _Requirements: 8.2, 8.3, 8.4_

- [ ] 9. Create FastAPI endpoint

  - [ ] 9.1 Update checkin endpoint

    - Integrate MultiAgentService
    - Pass user_id and user_input to workflow
    - Return response + card decision
    - Handle errors and return appropriate status codes
    - _Requirements: 8.1, 8.5_

  - [ ] 9.2 Add logging and monitoring

    - Log all agent outputs
    - Log timing for each agent
    - Log card decisions
    - Enable LangSmith tracing
    - _Requirements: 8.5_

  - [ ]\* 9.3 Write integration tests for endpoint
    - Test full workflow via API
    - Test error scenarios
    - Test performance (< 3s latency)
    - _Requirements: 8.1_

- [ ] 10. Data privacy and security

  - [ ] 10.1 Implement user_id verification

    - Verify authenticated user matches user_id
    - Return 403 if mismatch
    - _Requirements: 9.2_

  - [ ] 10.2 Add data encryption

    - Encrypt Store data at rest
    - Use secure key management
    - _Requirements: 9.1_

  - [ ] 10.3 Implement data deletion

    - Create endpoint for account deletion
    - Delete all user memory files
    - Log deletion for audit
    - _Requirements: 9.3_

  - [ ] 10.4 Remove PII from logs
    - Sanitize user input in logs
    - Redact sensitive information
    - _Requirements: 9.4_

- [ ] 11. Performance optimization

  - [ ] 11.1 Measure and optimize latency

    - Profile each agent execution time
    - Optimize slow agents
    - Ensure < 3s total latency
    - _Requirements: 8.1_

  - [ ] 11.2 Optimize Store operations

    - Batch Store reads/writes where possible
    - Cache frequently accessed data
    - _Requirements: 8.1_

  - [ ]\* 11.3 Load testing
    - Test with concurrent users
    - Identify bottlenecks
    - Optimize as needed
    - _Requirements: 8.1_

- [ ] 12. Documentation and deployment

  - [ ] 12.1 Write API documentation

    - Document endpoint parameters
    - Document response format
    - Include example requests/responses
    - _Requirements: 10.3_

  - [ ] 12.2 Update development guide

    - Document agent architecture
    - Document Store structure
    - Document testing approach
    - _Requirements: 10.4_

  - [ ] 12.3 Deploy to staging
    - Configure production Store (persistent)
    - Set up monitoring and alerts
    - Test with real users
    - _Requirements: 10.5_

---

**Total Tasks:** 12 top-level, 38 sub-tasks (8 optional test tasks)

**Estimated Timeline:** 3-4 weeks

**Dependencies:** langgraph, langchain-core, langgraph-checkpoint, tenacity

---

**Last Updated:** 2025-10-28  
**Status:** Ready for Implementation
