# Implementation Plan

- [x] 1. Set up LangGraph dependencies and state definition

  - Add langgraph, langchain-core, and tenacity to requirements.txt
  - Create LuminaState TypedDict in langgraph_service.py with user_input, depth_level, rag_contexts (list with reducer), and response fields
  - Use Annotated[list[dict], operator.add] for rag_contexts to support future parallel retrieval from multiple sources
  - Verify type safety with mypy or similar type checker
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 2. Implement depth evaluator agent

  - Create backend/services/depth_evaluator.py with evaluate_depth function
  - Integrate ChatService for LLM calls with temperature=0.3 and max_tokens=10
  - Write system prompt defining shallow/medium/deep classification criteria
  - Implement validation to default to "medium" if LLM returns invalid depth
  - Add logging for depth classification results
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 10.1, 10.5_

- [ ] 3. Implement RAG context retrieval node

  - Create retrieve_context function in langgraph_service.py
  - Integrate existing VectorStoreService to search "spiritual-library" namespace
  - Extract top 3 text passages and structure as dict with source and passages keys
  - Return as list of dicts to support future multi-source retrieval
  - Implement error handling to set empty rag_contexts list on failure
  - Add logging for number of passages retrieved
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 10.3_

- [ ] 4. Implement conditional routing logic

  - Create route_by_depth function that returns depth_level from state
  - Configure LangGraph conditional edges mapping shallow/medium/deep to response nodes
  - Add logging for routing decisions
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 10.2_

- [ ] 5. Implement Lumina responder agents

  - Create backend/services/lumina_responder.py with Plant Teacher system prompt
  - Implement respond_shallow function generating 1-2 sentence provocative questions using RAG context for mystical style
  - Implement respond_medium function generating wisdom + question (2-3 sentences) using RAG context
  - Implement respond_deep function generating pure wisdom reflection (2-3 sentences) heavily using RAG context
  - Configure temperature=0.8 for shallow/medium, 0.9 for deep responses
  - Add logging for response generation timing
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 10.1_

- [ ] 6. Build and compile LangGraph workflow

  - Create LangGraphService class in langgraph_service.py
  - Initialize StateGraph with LuminaState
  - Add all nodes: evaluate_depth, retrieve_context, respond_shallow, respond_medium, respond_deep
  - Configure edges: START → evaluate_depth → retrieve_context → conditional routing → response nodes → END
  - Compile workflow into executable app
  - Implement process_checkin method that invokes workflow and returns response + depth
  - Add workflow-level logging with total execution time
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 10.4_

- [ ] 7. Implement error handling and retries

  - Add tenacity retry decorator to LLM calls with 3 attempts and exponential backoff
  - Implement fallback responses for each depth level when LLM fails
  - Add timeout handling (5 seconds) for entire workflow execution
  - Log all errors and fallback usage at WARNING/ERROR levels
  - _Requirements: 9.4, 10.1_

- [ ] 8. Create FastAPI checkin endpoint

  - Create backend/routes/checkin.py with CheckinRequest and CheckinResponse models
  - Implement POST /api/checkin endpoint that calls LangGraphService.process_checkin
  - Add input validation limiting user_input to 500 characters
  - Implement error handling returning 500 on workflow failures and 504 on timeouts
  - Register router in main FastAPI app
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]\* 9. Write unit tests for core components

  - Write tests for depth_evaluator.py covering shallow/medium/deep classification and edge cases
  - Write tests for lumina_responder.py validating response format, length, and Plant Teacher voice
  - Mock ChatService.generate() to return controlled outputs
  - Verify all responses are 1-3 sentences and shallow responses contain questions
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 5.1, 5.2, 5.3, 5.4, 5.5, 6.2, 6.3, 6.4_

- [ ]\* 10. Write integration and API tests
  - Write end-to-end workflow tests for shallow/medium/deep input paths
  - Test workflow behavior with vector store failures (empty rag_context)
  - Test workflow behavior with LLM failures (fallback responses)
  - Write API tests for /api/checkin endpoint covering valid requests, validation errors, and error responses
  - Verify response time is under 5 seconds
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
