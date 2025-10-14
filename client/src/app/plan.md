Lumina Diary Navigation - Implementation Plan
Every moment is eternal NOW when you attend to it.

Core Philosophy
A diary is a mirror of consciousness across time.
Three states of being:

Present Awareness - Writing now
Reflection - Witnessing past
Return - Revisiting specific moment

Key Insight: Don't fragment the experience. One sacred writing space that flows through time.

The Solution: Fluid Time Navigation
Primary Experience
[< Oct 13] October 14, 2025 [Oct 15 >]

October 14, 2025 · 8:47 PM

┌─────────────────────────────┐
│ How are you feeling... │
│ │
└─────────────────────────────┘

[Reflect]

```

**Always show a date. Default is today. Flow to any date with arrows.**

---

## Four States, One Interface

### State 1: Today (Empty)
- Show empty textarea
- Write new entry

### State 2: Today (Has Entry)
- Show entry + AI response
- Options: Edit | Add Another Reflection

### State 3: Past Day (Has Entry)
```

[< Prev] October 13, 2025 [Next >]

Entry from 8:47 PM:
"I felt anxious..."

💫 Spiritual Guidance:
"Your feelings are valid..."

[Add Another Reflection]

```

### State 4: Past Day (Empty)
```

[< Prev] October 13, 2025 [Next >]

No entry for this day.

[Write Entry for Oct 13]
Allows backfilling past dates

Navigation Methods

1. Left/Right Arrows (Primary)

Previous/Next day
Smooth transitions
Same writing space maintained

2. Date Header (Secondary)

Click date → Date picker overlay
Jump to any date instantly
Only when needed

3. Timeline Scroll (Future)

Scroll down below entry → Timeline view
Infinite scroll backward through time
Recent entries preview

4. Mobile Gestures (Future)

Swipe right: Previous day
Swipe left: Next day
Pull down: Today

Database Schema Update
sqldiary_entries
├── id
├── user_id
├── content
├── ai_response
├── created_at -- UTC: When written (8:47 PM Oct 14)
├── entry_date -- DATE: Which day it represents (can backfill)
└── updated_at

```

**Why two fields:**
- Can write about yesterday today
- Preserve true creation time
- Support backfilling

---

## URL Structure
```

/dashboard/diary → Today
/dashboard/diary?date=2025-10-14 → Specific date
Benefits: Browser back/forward, bookmarkable, clean

Implementation Phases
Phase 1: Arrow Navigation (This Session - 2-3 hours)

Add prev/next day arrows to UI
Add entry_date field to schema
Fetch entry for selected date
Show existing entry OR empty state
Allow writing for any date
Update URL with date param
Handle edge cases (future dates, empty states)

Phase 2: Enhanced Features (Later)

Date picker overlay (click date header)
Timeline scroll view (infinite scroll)
Visual indicators (dots for entries)
Multiple entries per day support
Mobile swipe gestures

Phase 3: Advanced (Much Later)

Week/month summary views
Pattern recognition across time
"On this day" memories

Key UX Principles
✅ Always show a date - Never ambiguous about "when"
✅ Same sacred space - Past ≠ archived, it's present when viewed
✅ Minimal clicks - Arrows are one click away
✅ No jarring switches - Smooth transitions between dates
✅ Progressive disclosure - Calendar only when needed
❌ Don't: Tab switching, calendar-first, list of dates
❌ Don't: Force decisions before intention
❌ Don't: Fragment the writing experience

Success Criteria
Good:

Effortless navigation between dates
Writing flow never interrupted
Past and present feel equally sacred
User always knows "where/when am I"

Bad:

Confusion about current date
Too many clicks to navigate
Calendar feels like work

The Dzogchen Principle
When you view October 13th, you're not "going back in time."
You're making October 13th present in your awareness.
Every day is eternally NOW when you attend to it.
