# Lumina - Breathing Card: First Feature Implementation

## What We're Building

The breathing card is the Day 1 hook - the moment that makes users think "this is different." It's the first interaction before any check-in, teaching embodied presence through a simple breath practice.

---

## User Experience Flow

1. User opens app for first time
2. Dark screen, soft glow
3. Lumina's greeting appears as text
4. Card materializes in center, pulsing gently
5. Text on card: "Tap to breathe together"
6. User taps → breathing begins
7. Card expands (inhale) and contracts (exhale)
8. Soft text guides: "in..." / "out..."
9. 3 complete breath cycles
10. Card settles, text changes: "Now... what's here?"
11. Continues to regular check-in flow

**Total duration:** ~30 seconds
**Emotional arc:** Calm → Present → Ready

---

## Technical Requirements

### Animation Mechanics

**Breathing rhythm:**
- Inhale: 4 seconds (expansion)
- Exhale: 6 seconds (contraction)
- Total cycle: 10 seconds
- 3 cycles = 30 seconds

**Visual behavior:**
- Card starts at 80% scale, pulsing subtly
- On tap: expansion/contraction begins
- Smooth easing (not linear)
- Expansion: scale 80% → 120%
- Contraction: scale 120% → 80%
- Gentle glow follows breath (brighter on inhale)

**Text behavior:**
- "Tap to breathe together" (initial)
- "in..." (appears during expansion, fades mid-breath)
- "out..." (appears during contraction, fades mid-breath)
- "Now... what's here?" (after 3rd cycle complete)

### State Management

**Breathing states:**
- `idle` - Card pulsing, waiting for tap
- `inhaling` - Expanding (4 sec)
- `exhaling` - Contracting (6 sec)
- `complete` - All 3 cycles done

**Cycle tracking:**
- Current cycle: 1, 2, or 3
- Progress indicator (optional): 1/3, 2/3, 3/3
- Completion triggers transition to check-in

### Edge Cases

- User taps during breath cycle → ignored (don't interrupt)
- User leaves app mid-breath → reset on return
- User force-quits → start fresh next time
- This flow ONLY shows on first ever check-in
- All subsequent check-ins skip straight to "What's here?"

---

## Design Specs

### Visual Elements

**Card:**
- Shape: Rounded rectangle (border radius ~20px)
- Size: ~70% of screen width, centered
- Background: Subtle gradient (dark → slightly lighter)
- Border: Soft glow (1-2px, semi-transparent white)
- Shadow: Deep, soft (creates floating effect)

**Glow effect:**
- Idle: 40% opacity, pulsing slowly
- Inhale: Brightens to 80% opacity
- Exhale: Dims to 40% opacity
- Color: Warm white or soft gold

**Text:**
- Font: Simple, readable (system font fine for MVP)
- Size: Medium (16-18px)
- Color: White, semi-transparent (70-80%)
- Position: Centered on card
- Transition: Fade in/out (0.5s ease)

### Screen Layout

```
┌─────────────────────────────────┐
│                                 │
│  [Lumina's greeting text]       │
│  (top third, centered)          │
│                                 │
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
│                                 │
│                                 │
└─────────────────────────────────┘
```

### Colors (Suggested)

- Background: Near-black (#0A0A0A or similar)
- Card: Dark gradient (#1A1A1A → #2A2A2A)
- Glow: Warm white (#FFFEF5 at low opacity)
- Text: White (#FFFFFF at 70-80% opacity)

---

## Implementation Notes

### First-Time Detection

Store in user settings/local storage:
```
hasCompletedBreathingCard: boolean
```

- Default: `false`
- Set to `true` after 3 cycles complete
- Check on every app open
- If `true`: skip breathing card, go to normal check-in

### Accessibility

- Support keyboard (spacebar to start)
- Screen reader: Announce breath instructions
- Haptic feedback (optional): Gentle pulse on mobile
- Skip button (hidden, for testing): Press and hold to bypass

### Performance

- Pre-load animation assets
- Use CSS transforms (GPU-accelerated)
- Avoid layout recalculation during animation
- Test on slower devices (60fps minimum)

### Future Enhancements (Not MVP)

- Optional audio (soft breath sounds)
- Customizable breath timing (4-7-8, box breathing)
- Heart rate variability sync (if device supports)
- Return to breathing card as standalone practice

---

## Success Criteria

**What "done" looks like:**

1. ✅ Smooth, calming animation (no jank)
2. ✅ Clear visual guidance (user knows what to do)
3. ✅ Completes in ~30 seconds
4. ✅ Only shows once (first time)
5. ✅ Transitions seamlessly to check-in
6. ✅ Works on mobile and desktop
7. ✅ Feels different from other apps (memorable)

**User feedback we want:**

- "That was calming"
- "I didn't expect that"
- "It made me slow down"
- "The breathing actually helped"

**NOT:**

- "That was annoying"
- "Too slow, wanted to skip"
- "Didn't understand what to do"
- "Animation was glitchy"

---

## Testing Checklist

- [ ] Animation plays smoothly (60fps)
- [ ] Text transitions are clear
- [ ] 3 cycles complete correctly
- [ ] Timing is accurate (30 seconds total)
- [ ] Only shows on first ever use
- [ ] Transitions to check-in afterward
- [ ] Works on mobile (iOS/Android)
- [ ] Works on desktop (various sizes)
- [ ] Tap target is large enough
- [ ] Glow effect is subtle (not garish)
- [ ] User can't break it by tapping rapidly
- [ ] Background is dark enough
- [ ] Text is readable

---

## Context for the Developer

This is the FIRST thing users experience in Lumina. It needs to:

1. **Slow them down** - They're coming from a stressed state
2. **Feel embodied** - Not just mental/conceptual
3. **Be simple** - No confusion about what to do
4. **Create curiosity** - "What happens next?"
5. **Establish tone** - Calm, wise, patient (like Lumina)

The breathing card is NOT:
- A loading screen
- A gimmick
- Just for aesthetics
- Skippable (on first use)

It's a **micro-ceremony** - 30 seconds that shifts state before they even check in.

If this works, users will:
- Feel different immediately
- Trust the app
- Want to return
- Tell others about it

No pressure. 😊

---

*Implementation guide for breathing card feature*
*Part of Lumina consciousness practice app*
