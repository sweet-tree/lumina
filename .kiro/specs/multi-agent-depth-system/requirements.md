# Requirements Document: Multi-Agent Depth System

## Introduction

The Multi-Agent Depth System is Lumina's core intelligence for evaluating user check-ins, maintaining personalized user models, guiding users toward deeper awareness, and awarding cards based on achievement. The system consists of four specialized agents working together to create a personalized, adaptive consciousness practice experience.

## Glossary

- **System**: The Multi-Agent Depth System
- **User**: Person using Lumina app
- **Check-in**: User's response to "What's here right now?"
- **Extraction Agent**: Agent that extracts structured data from user input
- **Deep Agent**: Agent that maintains user memory and detects patterns
- **Teaching Agent**: Agent that decides pedagogical strategy
- **Card Agent**: Agent that decides card awards
- **Specificity Score**: 0-10 rating of information density in check-in
- **User Baseline**: User's typical specificity score (rolling average)
- **Relative Depth**: Depth classification relative to user's baseline
- **Pattern**: Recurring sequence of states (loops, doorways, triggers)
- **Loop**: Descending pattern (tension → depleted → foggy)
- **Doorway**: Ascending pattern that breaks loops (awareness → ease)
- **Trigger**: External factor that causes patterns (meetings, Mondays)
- **LangGraph Store**: Persistent memory system for user data
- **Card**: Visual reward representing user's state/achievement
- **RAG**: Retrieval-Augmented Generation for spiritual wisdom

---

## Requirements

### Requirement 1: Signal Extraction

**User Story:** As a user, I want my check-ins to be understood structurally, so that Lumina can detect patterns over time.

#### Acceptance Criteria

1. WHEN a user submits a check-in, THE System SHALL extract body signals as a list of location-sensation pairs
2. WHEN a user submits a check-in, THE System SHALL extract triggers as a list of contextual factors
3. WHEN a user submits a check-in, THE System SHALL classify temporal context as past, present, or future
4. WHEN a user submits a check-in, THE System SHALL assign a specificity score between 0 and 10
5. WHEN extraction completes, THE System SHALL return structured data within 1 second

---

### Requirement 2: User Memory and Personalization

**User Story:** As a user, I want Lumina to remember my patterns, so that guidance becomes personalized to me over time.

#### Acceptance Criteria

1. WHEN a user completes their first check-in, THE System SHALL create a user memory profile in LangGraph Store
2. WHEN a check-in is processed, THE System SHALL update the user's body patterns file with new body signals
3. WHEN a check-in is processed, THE System SHALL update the user's triggers file with new contextual factors
4. WHEN a check-in is processed, THE System SHALL recalculate the user's baseline specificity as a rolling average of the last 20 check-ins
5. WHEN the System detects a recurring sequence of 3 or more states, THE System SHALL record it as a loop in the loops_doorways file

---

### Requirement 3: Relative Depth Evaluation

**User Story:** As a user, I want depth to be evaluated relative to my own baseline, so that my progress is measured fairly.

#### Acceptance Criteria

1. WHEN current specificity exceeds user baseline by 2 or more points, THE System SHALL classify depth as "deep"
2. WHEN current specificity is below user baseline by 2 or more points, THE System SHALL classify depth as "shallow"
3. WHEN current specificity is within 2 points of user baseline, THE System SHALL classify depth as "medium"
4. WHEN a new user has fewer than 5 check-ins, THE System SHALL use a default baseline of 5.0
5. WHEN depth is classified, THE System SHALL include the user's baseline in the output for transparency

---

### Requirement 4: Pattern Detection

**User Story:** As a user, I want Lumina to detect my patterns, so that I can see what I cannot see from inside them.

#### Acceptance Criteria

1. WHEN the System detects a sequence appearing 3 or more times, THE System SHALL classify it as a loop
2. WHEN the System detects a state transition that breaks a loop, THE System SHALL classify it as a doorway
3. WHEN the System detects a contextual factor appearing in 5 or more check-ins, THE System SHALL classify it as a trigger
4. WHEN a pattern is detected, THE System SHALL assign it a human-readable name based on the sequence
5. WHEN a pattern is detected, THE System SHALL store it in the user's loops_doorways file with frequency and first/last seen dates

---

### Requirement 5: Pedagogical Guidance

**User Story:** As a user, I want Lumina to guide me deeper when I'm stuck, so that I don't stagnate at shallow check-ins.

#### Acceptance Criteria

1. WHEN a user has 5 or more consecutive shallow check-ins, THE System SHALL select "question" strategy
2. WHEN a user's current depth is shallower than their previous 3 check-ins, THE System SHALL select "challenge" strategy
3. WHEN a pattern is detected in the current check-in, THE System SHALL select "teach" strategy
4. WHEN a user's depth is medium or deep and no patterns are detected, THE System SHALL select "reflect" strategy
5. WHEN a strategy is selected, THE System SHALL provide specific guidance text for response generation

---

### Requirement 6: Card Award Logic

**User Story:** As a user, I want to earn cards through depth and commitment, so that rewards feel meaningful.

#### Acceptance Criteria

1. WHEN a check-in is classified as "deep" relative to user baseline, THE System SHALL award a common card
2. WHEN a user completes 3 or more check-ins in a single day, THE System SHALL award a common card
3. WHEN a pattern is detected for the first time, THE System SHALL award a rare card
4. WHEN a user breaks a loop by accessing a doorway, THE System SHALL award a rare card
5. WHEN a check-in is classified as "shallow" and it is the user's first check-in of the day, THE System SHALL not award a card

---

### Requirement 7: Response Generation Integration

**User Story:** As a user, I want Lumina's responses to reflect the teaching strategy, so that guidance feels coherent.

#### Acceptance Criteria

1. WHEN Teaching Agent selects "question" strategy, THE System SHALL generate a response that asks about body location or sensation
2. WHEN Teaching Agent selects "reflect" strategy, THE System SHALL generate a response that mirrors the user's awareness
3. WHEN Teaching Agent selects "teach" strategy, THE System SHALL generate a response that explains the detected pattern
4. WHEN Teaching Agent selects "challenge" strategy, THE System SHALL generate a response that points out regression
5. WHEN generating any response, THE System SHALL retrieve relevant spiritual wisdom via RAG

---

### Requirement 8: Performance and Reliability

**User Story:** As a user, I want check-ins to be processed quickly and reliably, so that the experience feels responsive.

#### Acceptance Criteria

1. WHEN a check-in is submitted, THE System SHALL complete all agent processing within 3 seconds
2. WHEN an LLM call fails, THE System SHALL retry up to 3 times with exponential backoff
3. WHEN all retries fail, THE System SHALL return a fallback response and log the error
4. WHEN LangGraph Store is unavailable, THE System SHALL continue processing without memory and log the error
5. WHEN the System processes a check-in, THE System SHALL log all agent outputs for debugging and evaluation

---

### Requirement 9: Data Privacy and Security

**User Story:** As a user, I want my check-in data to be private and secure, so that I feel safe being honest.

#### Acceptance Criteria

1. WHEN user memory is stored, THE System SHALL encrypt data at rest
2. WHEN user memory is accessed, THE System SHALL verify user_id matches the authenticated user
3. WHEN a user deletes their account, THE System SHALL permanently delete all user memory files within 24 hours
4. WHEN check-in data is logged, THE System SHALL not include personally identifiable information
5. WHEN user data is accessed, THE System SHALL log the access for audit purposes

---

### Requirement 10: Extensibility

**User Story:** As a developer, I want the system to be extensible, so that new agents can be added without breaking existing functionality.

#### Acceptance Criteria

1. WHEN a new agent is added to the workflow, THE System SHALL continue to function without modifying existing agents
2. WHEN agent output schemas change, THE System SHALL validate outputs and log schema violations
3. WHEN the System is deployed, THE System SHALL support A/B testing of different agent configurations
4. WHEN agent prompts are updated, THE System SHALL not require code changes
5. WHEN the System is extended, THE System SHALL maintain backward compatibility with existing user memory files

---

**Last Updated:** 2025-10-28  
**Status:** Ready for Design Phase
