# Card System Testing Checklist

**Project:** Lumina - Card-based Presence Practice  
**Date Started:** October 18, 2025  
**Testing Status:** In Progress 🟡

---

## 1. Basic Functionality ✅

**Status:** COMPLETE  
**Tested:** October 18, 2025

- [x] Draw random card works
- [x] Card displays correctly
- [x] Can type answer in textarea
- [x] Reflect button works
- [x] AI reflection appears
- [x] Session saved to database

**Notes:** All core functionality working end-to-end.

---

## 2. Visual & Animation Testing ⬜

**Status:** NOT TESTED  
**Priority:** HIGH

### Card Flip Animation

- [ ] Card flips smoothly (300ms transition)
- [ ] 3D rotation effect works (Y-axis flip)
- [ ] Front fades out cleanly
- [ ] Back appears without flicker
- [ ] No visual glitches during flip

### Color System

- [ ] Body cards show red (#EF4444) theme
- [ ] Energy cards show amber (#F59E0B) theme
- [ ] Mind cards show blue (#3B82F6) theme
- [ ] Integration cards show purple theme
- [ ] Icon backgrounds match type color
- [ ] Text color contrast is readable

### Reflection Display

- [ ] Reflection appears on card back
- [ ] Purple theme on back side
- [ ] ✨ icon displays correctly
- [ ] Text is readable and well-formatted
- [ ] Background blur effect works
- [ ] Border styling looks good

### Loading States

- [ ] Loading spinner appears on submit
- [ ] "Reflecting..." text shows
- [ ] Button is disabled during loading
- [ ] Spinner animates smoothly
- [ ] Loading state clears after response

### Card Design

- [ ] Card shadow looks good
- [ ] Border radius is consistent
- [ ] Padding/spacing feels right
- [ ] Icon size is appropriate
- [ ] Typography hierarchy is clear
- [ ] Guiding prompt is readable (serif font)
- [ ] "Consider:" hints are visible but not overwhelming

---

## 3. Mobile Responsiveness ⬜

**Status:** NOT TESTED  
**Priority:** HIGH (mobile-first design)

### Viewport Testing

- [ ] Test at 375px width (iPhone SE)
- [ ] Test at 390px width (iPhone 12/13/14)
- [ ] Test at 428px width (iPhone 14 Pro Max)
- [ ] Test at 360px width (Galaxy S20)
- [ ] Test at 768px width (iPad)

### Mobile Layout

- [ ] Card width is 90% of viewport (not too wide)
- [ ] Textarea is large enough to type comfortably
- [ ] Buttons are touch-friendly (min 44px height)
- [ ] No horizontal scrolling
- [ ] Text is readable without zooming
- [ ] Spacing feels comfortable on small screens

### Touch Interactions

- [ ] Can tap textarea to focus
- [ ] Can tap Reflect button
- [ ] Can tap New Check-In button
- [ ] No double-tap zoom issues
- [ ] Buttons have proper active states
- [ ] Touch targets don't overlap

### Mobile Animations

- [ ] Card flip animation is smooth (no lag)
- [ ] No performance issues on mobile
- [ ] Animations don't cause layout shift
- [ ] Loading spinner works on mobile

---

## 4. Multiple Cards Flow ⬜

**Status:** NOT TESTED  
**Priority:** MEDIUM

### Sequential Card Drawing

- [ ] Can draw first card successfully
- [ ] Can complete first card and get reflection
- [ ] Can click "Draw another card" (or refresh)
- [ ] Second card draws successfully
- [ ] Can complete second card
- [ ] Can draw 3rd, 4th, 5th cards in sequence

### Card Variety

- [ ] Draw and complete a Body card
- [ ] Draw and complete an Energy card
- [ ] Draw and complete a Mind card
- [ ] Verify different cards have different content
- [ ] Verify randomization works (not same card repeatedly)

### State Management

- [ ] Previous card data clears when drawing new card
- [ ] Previous reflection clears
- [ ] Textarea resets to empty
- [ ] No data leaking between cards

---

## 5. Database Integrity ⬜

**Status:** NOT TESTED  
**Priority:** HIGH

### Prisma Studio Verification

- [ ] Open Prisma Studio: `npx prisma studio`
- [ ] Navigate to CardSession table
- [ ] Verify sessions are being created

### Data Fields Check

- [ ] `id` field populated (cuid)
- [ ] `userId` matches authenticated user
- [ ] `cardId` matches the card drawn
- [ ] `state` field contains correct state (e.g., "tension")
- [ ] `timestamp` is current time
- [ ] `answer` contains user's typed response
- [ ] `miniReflection` contains AI response

### Data Quality

- [ ] No NULL values in required fields
- [ ] Timestamps are in correct timezone (UTC)
- [ ] Answer text is properly stored (check special characters, line breaks)
- [ ] AI reflection is complete (not truncated)

### Multiple Sessions

- [ ] Create 3-5 card sessions
- [ ] Verify all are saved separately
- [ ] Verify userId is same for all (your user)
- [ ] Verify different cardIds for different cards
- [ ] Check order by timestamp (most recent first)

---

## 6. AI Response Quality ⬜

**Status:** NOT TESTED  
**Priority:** HIGH

### Response Length

- [ ] Reflections are 2-3 sentences (not too long)
- [ ] Reflections are not too short (not just one word)
- [ ] Consistent length across different cards

### Contextual Relevance

- [ ] AI references specific details from user's answer
- [ ] Body card reflections mention body/physical aspects
- [ ] Energy card reflections mention energy/emotion
- [ ] Mind card reflections mention thoughts/mental states

### Tone & Style

- [ ] Warm and non-judgmental
- [ ] Socratic (asks good questions) when answer is surface-level
- [ ] Reflective (offers insight) when answer is deep
- [ ] No clinical/diagnostic language
- [ ] No prescriptive "you should" statements

### Test Cases

#### Test Case 1: Short Surface Answer

- Card: Body Tension
- Answer: "Shoulders"
- Expected: Socratic question to deepen awareness
- [ ] AI asks a follow-up question
- [ ] Question is open-ended and curious

#### Test Case 2: Deep Detailed Answer

- Card: Body Tension
- Answer: "My shoulders and neck are incredibly tight, like rocks. I think it's from sitting at my desk for 8 hours straight working on this deadline. I notice I'm also clenching my jaw."
- Expected: Reflective response acknowledging specifics
- [ ] AI references shoulders, neck, jaw
- [ ] AI connects to desk work and deadline
- [ ] Offers insight or pattern recognition

#### Test Case 3: Energy Card

- Card: Energy Depletion
- Answer: "Completely drained. Meetings all day sucked the life out of me. Feel like 2/10."
- Expected: Acknowledges depletion, asks about restoration
- [ ] AI acknowledges meetings drained energy
- [ ] AI references the 2/10 rating
- [ ] Asks about what energy needs

#### Test Case 4: Mind Card

- Card: Mind Worry
- Answer: "Worried about money. Bills coming up and not sure I have enough."
- Expected: Explores beneath the worry
- [ ] AI asks what's beneath the money worry
- [ ] Non-judgmental tone
- [ ] Helps user go deeper

---

## 7. Error Handling ⬜

**Status:** NOT TESTED  
**Priority:** HIGH

### Input Validation

- [ ] Cannot submit empty answer (button disabled)
- [ ] Cannot submit whitespace-only answer
- [ ] Very long answers (1000+ characters) work
- [ ] Special characters don't break anything
- [ ] Line breaks in answer are preserved

### Backend Errors

- [ ] Stop AI backend → Try to reflect
- [ ] Error message appears to user
- [ ] Error is user-friendly (not technical)
- [ ] Can recover and try again
- [ ] Error doesn't break the UI

### Network Errors

- [ ] Turn off internet → Try to reflect
- [ ] Appropriate error message shows
- [ ] UI doesn't crash

### Database Errors

- [ ] (Hard to test) What if database is down?
- [ ] (Hard to test) What if user is logged out?

### Edge Cases

- [ ] Draw card when not authenticated (should redirect)
- [ ] Very slow API response (30+ seconds)
- [ ] Rapid clicking of Reflect button
- [ ] Browser back button behavior

---

## 8. Authentication & Authorization ⬜

**Status:** NOT TESTED  
**Priority:** HIGH

### Auth Flow

- [ ] User must be signed in to access /dashboard/practice
- [ ] Unauthenticated user redirects to sign in
- [ ] After sign in, redirects to practice page

### Session Ownership

- [ ] CardSessions are created with correct userId
- [ ] User A cannot see User B's sessions
- [ ] Sessions persist across browser refresh

---

## 9. Performance Testing ⬜

**Status:** NOT TESTED  
**Priority:** MEDIUM

### Load Times

- [ ] Practice page loads in < 1 second
- [ ] Draw card response in < 500ms
- [ ] AI reflection response in < 5 seconds
- [ ] Card flip animation is 60fps

### Multiple Sessions

- [ ] Complete 10 cards in a row
- [ ] Check for memory leaks
- [ ] Check for slowdowns
- [ ] Database queries are efficient

---

## 10. Cross-Browser Testing ⬜

**Status:** NOT TESTED  
**Priority:** MEDIUM

### Desktop Browsers

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Mobile Browsers

- [ ] Safari iOS
- [ ] Chrome Android
- [ ] Firefox Mobile

### Browser Features

- [ ] 3D card flip works in all browsers
- [ ] CSS animations smooth
- [ ] Textarea focus behavior consistent
- [ ] Button styles consistent

---

## 11. Accessibility ⬜

**Status:** NOT TESTED  
**Priority:** LOW (but important)

### Keyboard Navigation

- [ ] Can tab to textarea
- [ ] Can tab to buttons
- [ ] Enter key submits form
- [ ] Focus indicators visible

### Screen Reader

- [ ] Card title is announced
- [ ] Guiding prompt is readable
- [ ] Button states are clear
- [ ] Error messages are announced

### Color Contrast

- [ ] Text meets WCAG AA standards
- [ ] Color-blind friendly (don't rely only on color)

---

## 12. Content Quality ⬜

**Status:** NOT TESTED  
**Priority:** MEDIUM

### Card Content Review

- [ ] Review all 15 cards
- [ ] Guiding prompts are clear
- [ ] Question hints are helpful
- [ ] No typos or grammatical errors
- [ ] Tone is consistent across cards
- [ ] Icons are appropriate

### State Mapping

- [ ] Body Tension → correctly tagged as "tension" state
- [ ] Energy Flow → correctly tagged as "flow" state
- [ ] Mind Clarity → correctly tagged as "clarity" state
- [ ] All 15 states are unique

---

## Priority Summary

### 🔴 CRITICAL (Must Test Now)

1. Visual & Animation Testing
2. Mobile Responsiveness
3. Database Integrity
4. AI Response Quality
5. Error Handling
6. Authentication

### 🟡 IMPORTANT (Test Soon)

7. Multiple Cards Flow
8. Performance Testing
9. Content Quality

### 🟢 NICE TO HAVE (Test Later)

10. Cross-Browser Testing
11. Accessibility

---

## Testing Log

| Date         | Tester | Area Tested         | Status  | Notes                     |
| ------------ | ------ | ------------------- | ------- | ------------------------- |
| Oct 18, 2025 | User   | Basic Functionality | ✅ PASS | All core features working |
|              |        |                     |         |                           |
|              |        |                     |         |                           |

---

## Known Issues

_None yet_

---

## Next Steps

1. **Start with Visual & Animation Testing** - Quick visual check
2. **Then Mobile Responsiveness** - Critical for UX
3. **Then Database Integrity** - Verify data is saving correctly
4. **Then AI Quality** - Make sure reflections are good

**Estimated Testing Time:** 2-3 hours for full checklist

---

**Last Updated:** October 18, 2025
