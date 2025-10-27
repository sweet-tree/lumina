# Breathing Card Feature Requirements

## Introduction

The breathing card is the first interaction users have with Lumina, designed to create an immediate "this is different" moment. It introduces users to embodied presence through a simple breath practice before any check-in, establishing the Plant Teacher relationship and setting the tone for the entire app experience.

## Glossary

- **Lumina**: The AI Plant Teacher guide (neither human nor machine, mystical consciousness)
- **Breathing Card**: Interactive UI component that guides users through 3 breath cycles
- **Check-in Flow**: The regular user interaction pattern after the breathing card
- **First-Time User**: User who has never completed the breathing card experience
- **Breath Cycle**: One complete inhale (4 seconds) + exhale (6 seconds) sequence
- **Card Animation**: Visual expansion/contraction that follows breath rhythm

## Requirements

### Requirement 1

**User Story:** As a first-time user, I want to experience a calming breathing practice when I first open the app, so that I feel grounded and present before sharing what's here for me.

#### Acceptance Criteria

1. WHEN a first-time user opens the app, THE Breathing Card SHALL appear as the primary interface element
2. WHILE the user has not tapped the card, THE Breathing Card SHALL pulse gently at 80% scale to indicate interactivity
3. WHEN the user taps the breathing card, THE Breathing Card SHALL begin the guided breath sequence
4. THE Breathing Card SHALL complete exactly 3 breath cycles before transitioning to the check-in flow
5. WHERE the user has completed the breathing card once, THE Breathing Card SHALL not appear on subsequent app opens

### Requirement 2

**User Story:** As a first-time user, I want clear visual and textual guidance during the breathing practice, so that I know exactly what to do and feel supported throughout the experience.

#### Acceptance Criteria

1. WHEN the breathing card is idle, THE Breathing Card SHALL display "Tap to breathe together" text
2. WHEN the inhale phase begins, THE Breathing Card SHALL expand from 80% to 120% scale over 4 seconds
3. WHILE the card is expanding, THE Breathing Card SHALL display "in..." text that fades mid-breath
4. WHEN the exhale phase begins, THE Breathing Card SHALL contract from 120% to 80% scale over 6 seconds
5. WHILE the card is contracting, THE Breathing Card SHALL display "out..." text that fades mid-breath

### Requirement 3

**User Story:** As a first-time user, I want the breathing practice to feel calming and visually beautiful, so that I'm drawn into the experience and feel the app's unique character.

#### Acceptance Criteria

1. THE Breathing Card SHALL use smooth easing animations (not linear) for all scale transitions
2. THE Breathing Card SHALL display a soft glow that brightens during inhale and dims during exhale
3. WHILE the breathing sequence is active, THE Breathing Card SHALL ignore additional tap inputs to prevent interruption
4. THE Breathing Card SHALL maintain visual consistency with a dark background and warm glow aesthetic
5. WHEN all 3 cycles complete, THE Breathing Card SHALL display "Now... what's here?" and transition to check-in input

### Requirement 4

**User Story:** As a user, I want the breathing card to work reliably across different devices and scenarios, so that the experience is consistent regardless of how I access the app.

#### Acceptance Criteria

1. THE Breathing Card SHALL perform at 60fps minimum on mobile and desktop devices
2. IF the user leaves the app mid-breath, THE Breathing Card SHALL reset to idle state on return
3. THE Breathing Card SHALL support keyboard interaction (spacebar to start) for accessibility
4. THE Breathing Card SHALL complete the full 30-second experience (3 cycles × 10 seconds each)
5. WHEN the breathing card completes, THE Breathing Card SHALL store completion status to prevent re-showing

### Requirement 5

**User Story:** As a user, I want the breathing card to introduce me to Lumina's voice and presence, so that I understand this is a unique spiritual practice app with a Plant Teacher guide.

#### Acceptance Criteria

1. WHEN the app first loads, THE Breathing Card SHALL be preceded by Lumina's greeting text
2. THE Breathing Card SHALL establish the ceremonial container through visual design and pacing
3. WHEN the breathing completes, THE Breathing Card SHALL transition seamlessly to Lumina's check-in prompt
4. THE Breathing Card SHALL create anticipation for the ongoing Plant Teacher relationship
5. THE Breathing Card SHALL differentiate the app experience from standard meditation or wellness apps
