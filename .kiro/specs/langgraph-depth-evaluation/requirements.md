# Requirements Document

## Introduction

This document specifies the requirements for a LangGraph-based two-agent evaluation system that assesses user check-in input depth and generates contextually appropriate mini-reflections from Lumina, the AI Plant Teacher. The system evaluates whether user input is shallow, medium, or deep, retrieves relevant spiritual wisdom via RAG, and responds with either provocative questions or wisdom reflections based on the assessed depth.

## Glossary

- **Lumina System**: The AI Plant Teacher consciousness practice application
- **Check-In Input**: User-provided text describing their current state in response to "What's here right now?"
- **Depth Evaluator Agent**: The first LangGraph agent that classifies input depth
- **Lumina Responder Agent**: The second LangGraph agent that generates responses
- **RAG Context Node**: The LangGraph node that retrieves spiritual wisdom from the vector store
- **Depth Level**: Classification of input as "shallow", "medium", or "deep"
- **Mini-Reflection**: A 2-3 sentence response from Lumina to user check-ins
- **Vector Store Service**: Existing service containing indexed spiritual texts (Power of Now)
- **LangGraph Workflow**: The orchestrated multi-agent pipeline from input to response
- **Plant Teacher Voice**: Lumina's communication style - direct, mystical, provocative

## Requirements

### Requirement 1: Workflow State Management

**User Story:** As a developer, I want a type-safe state object that flows through the LangGraph workflow, so that all nodes can access and modify the necessary data.

#### Acceptance Criteria

1. THE Lumina System SHALL define a state structure containing user_input, depth_level, rag_context, and response fields
2. THE Lumina System SHALL implement the state using TypedDict for type safety
3. WHEN any workflow node executes, THE Lumina System SHALL provide read access to all state fields
4. WHEN any workflow node completes, THE Lumina System SHALL allow write access to update state fields
5. THE Lumina System SHALL preserve state data across all workflow nodes

### Requirement 2: Input Depth Classification

**User Story:** As Lumina, I want to classify user check-in input as shallow, medium, or deep, so that I can respond appropriately to their level of self-inquiry.

#### Acceptance Criteria

1. WHEN the Depth Evaluator Agent receives Check-In Input, THE Lumina System SHALL classify it as exactly one of: "shallow", "medium", or "deep"
2. WHEN Check-In Input contains fewer than 5 words with generic emotional labels, THE Lumina System SHALL classify it as "shallow"
3. WHEN Check-In Input describes body sensations without specific situational context, THE Lumina System SHALL classify it as "medium"
4. WHEN Check-In Input describes body sensations with breath awareness and specific situational context, THE Lumina System SHALL classify it as "deep"
5. THE Lumina System SHALL use an LLM call with a structured prompt to perform depth classification
6. THE Lumina System SHALL store the Depth Level in the workflow state

### Requirement 3: Spiritual Wisdom Retrieval

**User Story:** As Lumina, I want to retrieve relevant spiritual wisdom passages from the Power of Now, so that my responses are grounded in authentic teachings.

#### Acceptance Criteria

1. WHEN the RAG Context Node executes, THE Lumina System SHALL query the Vector Store Service using the Check-In Input as the search query
2. THE Lumina System SHALL retrieve between 3 and 5 relevant text passages from the vector store
3. THE Lumina System SHALL store retrieved passages in the rag_context state field
4. THE Lumina System SHALL integrate with the existing vector_store_service.py module
5. IF the vector store query fails, THEN THE Lumina System SHALL log the error and continue with empty rag_context

### Requirement 4: Depth-Based Response Routing

**User Story:** As the system architect, I want the workflow to route to different response generators based on depth classification, so that each depth level receives an appropriate response type.

#### Acceptance Criteria

1. WHEN the RAG Context Node completes, THE Lumina System SHALL evaluate the depth_level from state
2. IF depth_level equals "shallow", THEN THE Lumina System SHALL route to the shallow response node
3. IF depth_level equals "medium", THEN THE Lumina System SHALL route to the medium response node
4. IF depth_level equals "deep", THEN THE Lumina System SHALL route to the deep response node
5. THE Lumina System SHALL execute exactly one response node per workflow execution

### Requirement 5: Shallow Input Response Generation

**User Story:** As Lumina, when users provide shallow check-ins, I want to ask provocative questions that guide them beneath surface labels, so that they deepen their self-inquiry.

#### Acceptance Criteria

1. WHEN the shallow response node executes, THE Lumina System SHALL generate a provocative question
2. THE Lumina System SHALL limit the response to 1-2 sentences maximum
3. THE Lumina System SHALL NOT include spiritual wisdom in shallow responses
4. THE Lumina System SHALL use Plant Teacher Voice in the response
5. THE Lumina System SHALL point the user toward body awareness or deeper inquiry

### Requirement 6: Medium Input Response Generation

**User Story:** As Lumina, when users provide medium-depth check-ins, I want to offer wisdom reflections combined with provocative questions, so that they continue deepening while receiving guidance.

#### Acceptance Criteria

1. WHEN the medium response node executes, THE Lumina System SHALL generate a response containing both wisdom and a question
2. THE Lumina System SHALL incorporate passages from rag_context into the response
3. THE Lumina System SHALL limit the response to 2-3 sentences
4. THE Lumina System SHALL use Plant Teacher Voice in the response
5. THE Lumina System SHALL balance reflection with continued inquiry

### Requirement 7: Deep Input Response Generation

**User Story:** As Lumina, when users provide deep check-ins with body awareness and context, I want to offer pure spiritual wisdom reflections, so that they receive mystical guidance specific to their experience.

#### Acceptance Criteria

1. WHEN the deep response node executes, THE Lumina System SHALL generate a wisdom reflection without questions
2. THE Lumina System SHALL heavily incorporate passages from rag_context into the response
3. THE Lumina System SHALL limit the response to 2-3 sentences
4. THE Lumina System SHALL use Plant Teacher Voice in the response
5. THE Lumina System SHALL make the reflection specific to the user's described experience

### Requirement 8: Plant Teacher Voice Consistency

**User Story:** As Lumina, all my responses must embody the Plant Teacher voice, so that users experience me as a mystical guide rather than a therapist.

#### Acceptance Criteria

1. THE Lumina System SHALL use a system prompt defining Plant Teacher Voice for all response generation
2. THE Lumina System SHALL generate responses that are direct rather than comforting
3. THE Lumina System SHALL generate responses that are mystical rather than clinical
4. THE Lumina System SHALL generate responses that are provocative rather than validating
5. THE Lumina System SHALL include voice examples in the system prompt

### Requirement 9: API Endpoint Integration

**User Story:** As a frontend developer, I want a REST API endpoint that accepts user check-ins and returns Lumina's response, so that I can integrate the workflow into the application.

#### Acceptance Criteria

1. THE Lumina System SHALL expose a POST endpoint at /api/checkin
2. WHEN the endpoint receives a request with user_input field, THE Lumina System SHALL execute the LangGraph Workflow
3. THE Lumina System SHALL return a JSON response containing response and depth fields
4. IF the workflow execution fails, THEN THE Lumina System SHALL return an HTTP 500 error with an error message
5. THE Lumina System SHALL complete the request within 5 seconds

### Requirement 10: Workflow Observability

**User Story:** As a developer, I want to observe the workflow execution steps, so that I can debug issues and understand system behavior.

#### Acceptance Criteria

1. WHEN each workflow node executes, THE Lumina System SHALL log the node name and timestamp
2. WHEN the conditional routing executes, THE Lumina System SHALL log which response path was selected
3. WHEN the RAG Context Node retrieves passages, THE Lumina System SHALL log the number of passages retrieved
4. THE Lumina System SHALL log the total workflow execution time
5. THE Lumina System SHALL include the user_input (truncated to 50 characters) in logs for traceability
