# Breathing Card Feature Design

## Overview

The breathing card feature introduces users to Lumina through an interactive breathing practice that appears only on their first app experience. It serves as the bridge between the current dashboard-based app and the new Lumina consciousness practice vision, establishing the Plant Teacher relationship and creating the "this is different" moment.

## Architecture

### High-Level Flow

```
User Opens Practice → Check Database Status → Show Breathing Card (First-Time) → Complete 3 Cycles → Update Database → Continue to Practice
```

### Integration Points

- **Entry Point**: Integrated within `/dashboard/practice` route for first-time users
- **State Management**: Uses database as source of truth with localStorage as fallback
- **Exit Point**: Continues to practice content after completion (no redirect)
- **Current Integration**: Seamlessly integrated into practice flow

## Components and Interfaces

### 1. BreathingCardPage Component

**Location**: `client/src/app/dashboard/practice/page.tsx`
**Purpose**: Integrated breathing card within practice flow
**Responsibilities**:

- Check database for first-time user status
- Show breathing card before practice content
- Handle completion and continue to practice

### 2. BreathingCard Component

**Location**: `client/src/features/breathing-card/components/BreathingCard.tsx`
**Purpose**: Interactive breathing card with animation
**Props**:

```typescript
interface BreathingCardProps {
  onComplete: () => void;
}
```

**State**:

```typescript
type BreathingState = "idle" | "inhaling" | "exhaling" | "complete";

interface BreathingCardState {
  state: BreathingState;
  currentCycle: number; // 1, 2, or 3
  scale: number; // 0.8 to 1.2
  glowOpacity: number; // 0.4 to 0.8
}
```

### 3. useBreathingCard Hook

**Location**: `client/src/features/breathing-card/hooks/useBreathingCard.ts`
**Purpose**: Manages breathing animation logic and timing
**Returns**:

```typescript
interface UseBreathingCardReturn {
  state: BreathingState;
  currentCycle: number;
  scale: number;
  glowOpacity: number;
  currentText: string;
  startBreathing: () => void;
  isComplete: boolean;
}
```

### 4. useBreathingCardState Hook

**Location**: `client/src/features/breathing-card/hooks/useBreathingCardState.ts`
**Purpose**: Manages breathing card state with database integration and TanStack Query
**Returns**:

```typescript
interface UseBreathingCardStateReturn {
  isFirstTime: boolean;
  markBreathingComplete: () => Promise<{
    success: boolean;
    completedAt: Date | null;
  }>;
  isLoading: boolean;
  error: string | null;
}
```

## Data Models

### Database Schema (Primary)

```typescript
// User model in Prisma schema
model User {
  hasCompletedBreathingCard Boolean   @default(false)
  breathingCardCompletedAt  DateTime?
  // ... other fields
}
```

### Server Action

```typescript
// Server Action for completion
export async function completeBreathingCard() {
  // Updates database with completion status
  // Returns success status and completion timestamp
}
```

### Local Storage Schema (Fallback)

```typescript
interface LuminaUserState {
  hasCompletedBreathingCard: boolean;
  completedAt?: string; // ISO date string
}
```

**Storage Key**: `lumina-user-state`
**Purpose**: Fallback when database is unavailable

### Animation Timing Constants

```typescript
const BREATHING_CONFIG = {
  INHALE_DURATION: 4000, // 4 seconds
  EXHALE_DURATION: 6000, // 6 seconds
  TOTAL_CYCLES: 3,
  IDLE_SCALE: 0.8,
  EXPANDED_SCALE: 1.2,
  IDLE_GLOW: 0.4,
  ACTIVE_GLOW: 0.8,
  TEXT_FADE_DURATION: 500, // 0.5 seconds
} as const;
```

## Error Handling

### Animation Interruption

- **Scenario**: User leaves app mid-breath
- **Solution**: Reset to idle state on component mount
- **Implementation**: Check if animation was in progress and reset

### Performance Issues

- **Scenario**: Animation drops below 60fps
- **Solution**: Use CSS transforms and will-change property
- **Fallback**: Reduce animation complexity on slower devices

### Storage Failures

- **Scenario**: localStorage unavailable or full
- **Solution**: Graceful degradation - show breathing card every time
- **Implementation**: Try-catch around localStorage operations

## Testing Strategy

### Unit Tests

- **useBreathingCard Hook**: Test state transitions and timing
- **useFirstTimeUser Hook**: Test localStorage operations
- **BreathingCard Component**: Test prop handling and event emission

### Integration Tests

- **Full Flow**: First-time user → breathing card → completion → redirect
- **Repeat User**: Returning user bypasses breathing card
- **Animation Timing**: Verify 30-second total duration

### Manual Testing Checklist

- [ ] Smooth 60fps animation on mobile/desktop
- [ ] Correct timing (4s inhale, 6s exhale, 3 cycles)
- [ ] Text transitions are clear and readable
- [ ] Keyboard accessibility (spacebar to start)
- [ ] Works with different screen sizes
- [ ] localStorage persistence across sessions

## Visual Design Specifications

### Layout Structure

```
┌─────────────────────────────────┐
│                                 │
│  [Lumina's Greeting Text]       │
│  (top third, centered)          │
│                                 │
│      ┌─────────────────┐        │
│      │                 │        │
│      │  [Breathing     │        │
│      │   Card]         │        │
│      │                 │        │
│      │  "Tap to        │        │
│      │   breathe       │        │
│      │   together"     │        │
│      │                 │        │
│      └─────────────────┘        │
│                                 │
└─────────────────────────────────┘
```

### CSS Classes and Styling

```css
.breathing-card {
  /* Base card styling */
  width: 70vw;
  max-width: 400px;
  aspect-ratio: 4/3;
  border-radius: 20px;
  background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
  border: 1px solid rgba(255, 254, 245, 0.2);

  /* Animation properties */
  transform-origin: center;
  will-change: transform, box-shadow;
  transition: transform 0.1s ease-out;
}

.breathing-card--pulsing {
  animation: gentle-pulse 3s ease-in-out infinite;
}

.breathing-card__glow {
  box-shadow: 0 0 40px rgba(255, 254, 245, var(--glow-opacity));
}

.breathing-card__text {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.125rem;
  text-align: center;
  transition: opacity 0.5s ease;
}
```

### Animation Implementation

- **CSS Transforms**: Use `transform: scale()` for performance
- **Easing Function**: `cubic-bezier(0.4, 0, 0.2, 1)` for natural breathing feel
- **GPU Acceleration**: `will-change: transform` and `transform3d()`

## Technical Implementation Details

### Practice Page Integration Logic

```typescript
// In /dashboard/practice/page.tsx
export default function PracticePage() {
  const { isFirstTime, markBreathingComplete, isLoading } =
    useBreathingCardState();

  // Show loading while checking database
  if (isLoading) return <LoadingState />;

  // Show breathing card for first-time users
  if (isFirstTime) {
    return <BreathingCardExperience onComplete={markBreathingComplete} />;
  }

  // Show practice content for returning users
  return <PracticeContent />;
}
```

### Animation State Machine

```typescript
const breathingStateMachine = {
  idle: {
    on: { START: "inhaling" },
  },
  inhaling: {
    on: { INHALE_COMPLETE: "exhaling" },
    duration: 4000,
  },
  exhaling: {
    on: {
      EXHALE_COMPLETE: [
        { target: "inhaling", cond: "hasMoreCycles" },
        { target: "complete", cond: "allCyclesComplete" },
      ],
    },
    duration: 6000,
  },
  complete: {
    type: "final",
  },
};
```

### Performance Optimizations

- **React.memo**: Prevent unnecessary re-renders
- **useCallback**: Memoize event handlers
- **CSS Animations**: Prefer CSS over JavaScript for transforms
- **Preload**: Ensure smooth first animation

## Future Enhancements

### Phase 2 Considerations

- **Audio Integration**: Optional breath sounds
- **Haptic Feedback**: Gentle vibration on mobile
- **Customizable Timing**: 4-7-8 breathing, box breathing
- **Analytics**: Track completion rates and drop-off points

### Integration with Full Lumina Vision

- **Practice Flow**: Seamlessly integrated into practice experience
- **Lumina Voice**: Enhanced AI responses after breathing
- **Card System**: Natural transition to card drawing after breathing
- **Pattern Recognition**: Begin user journey tracking from first practice

## Dependencies and Libraries

### Required Packages

- **Existing**: React, Next.js, TypeScript, Tailwind CSS
- **Animation**: CSS-only (no additional libraries needed)
- **State**: React hooks (useState, useEffect, useCallback)
- **Storage**: Browser localStorage API

### Browser Support

- **Modern Browsers**: Chrome 60+, Firefox 55+, Safari 12+
- **Mobile**: iOS Safari 12+, Chrome Mobile 60+
- **Fallbacks**: Graceful degradation for older browsers

## Security and Privacy

### Data Storage

- **Database Primary**: Breathing card completion stored in user database
- **Cross-device Sync**: Status persists across all user devices
- **localStorage Fallback**: Backup storage when database unavailable
- **User Control**: Admin can reset user states via database

### Privacy Considerations

- **No Tracking**: Breathing patterns not recorded
- **Anonymous**: No personal data associated with breathing practice
- **Consent**: Implicit consent through app usage

## Modern Implementation Architecture

### Server Actions Integration

The breathing card uses Next.js Server Actions instead of API routes for better performance and type safety:

```typescript
// Server Action
"use server";
export async function completeBreathingCard() {
  const session = await getServerSession(authOptions);
  // Update database directly
  await prisma.user.update({
    where: { email: session.user.email },
    data: { hasCompletedBreathingCard: true },
  });
}
```

### TanStack Query Integration

State management follows project patterns using TanStack Query:

```typescript
const completeMutation = useMutation({
  mutationFn: completeBreathingCard,
  onSuccess: () => {
    // Optimistic updates and localStorage fallback
  },
});
```

### Feature-Based Architecture

All breathing card code is organized in a feature directory:

```
src/features/breathing-card/
├── components/
│   ├── BreathingCard.tsx
│   └── BreathingCardExperience.tsx
├── hooks/
│   ├── useBreathingCard.ts
│   └── useBreathingCardState.ts
├── actions/
│   └── breathing-card-actions.ts
├── types/
│   └── index.ts
└── index.ts
```

This design provides a solid foundation for implementing the breathing card feature while maintaining integration with the existing Next.js architecture and preparing for the future Lumina vision.
