Lumina AI - Implementation Plan: Diary Entry & Sidebar
Overview
Building the core diary entry experience with navigation sidebar. Landing experience will come later - focus is on making the writing ritual feel sacred and intentional.

Phase 1: Base Sidebar Navigation (1-1.5 hours)
Goal
Create a clean, minimal sidebar for navigation between core pages.
Components to Build

1. Sidebar Component (components/Sidebar.tsx)
   Features:

- Fixed position on left side
- Collapsed on mobile (hamburger menu)
- Navigation items:
  - 🏠 Today (diary entry page)
  - 📖 Your Journey (past entries)
  - 👤 Profile
  - ⚙️ Settings
- User info at bottom (avatar, name, sign out)
- Active state highlighting
- Smooth transitions

```

#### 2. Layout Wrapper (`components/DashboardLayout.tsx`)
```

Features:

- Wraps all authenticated pages
- Contains Sidebar + main content area
- Responsive: sidebar collapses to hamburger on mobile
- Main content has proper padding/margins

```

### Technical Details
- Use client component for interactivity
- Mobile breakpoint: 768px
- Sidebar width: 240px (desktop), full screen (mobile)
- Z-index management for overlay
- Use Lucide React for icons

### File Structure
```

src/
├── components/
│ ├── Sidebar.tsx
│ ├── DashboardLayout.tsx
│ └── ui/
│ └── (shadcn components if using)
└── app/
└── dashboard/
└── layout.tsx (uses DashboardLayout)

```

---

## Phase 2: Diary Entry Page Redesign (2-3 hours)

### Goal
Transform the chat interface into a sacred writing space that feels like a ritual.

### Visual Design

#### Color Palette
```

Primary: #2D3561 (Deep indigo - calm, introspection)
Secondary: #E8DCC4 (Warm sand - grounding)
Accent: #C9A969 (Soft gold - wisdom)
Background: #FAF9F6 (Off-white - gentle)
Text: #1A1A1A (Near black)
Text Secondary: #6B7280 (Gray)

```

#### Typography
```

Body: Serif font (Georgia or 'Crimson Text' from Google Fonts)
Headings: Sans-serif (Inter)
Entry text: 18px, line-height: 1.8
Generous spacing between elements

```

### Page Layout (`app/dashboard/today/page.tsx` or similar)

#### Structure
```

┌────────────────────────────────────────┐
│ October 14, 2025 · 8:47 PM │ ← Header (date/time)
├────────────────────────────────────────┤
│ │
│ [Large textarea] │ ← Writing space
│ - Serif font │
│ - Generous line height │
│ - Subtle paper texture background │
│ - Auto-resizes with content │
│ - Min height: 300px │
│ - No visible border (just subtle │
│ shadow on focus) │
│ │
│ │
│ │
├────────────────────────────────────────┤
│ [Reflect Button] │ ← Action area
│ - Centered │
│ - Soft gold color │
│ - Gentle glow on hover │
│ - Says "Reflect" not "Submit" │
└────────────────────────────────────────┘

```

### Features to Implement

#### 1. Date/Time Display
- Show current date and time
- Format: "October 14, 2025 · 8:47 PM"
- Updates on page load (not real-time)
- Subtle color (#6B7280)

#### 2. Writing Textarea
- Autosize (expands as user types)
- Placeholder: "How are you feeling right now?"
- Min height: 300px
- Max height: none (grows infinitely)
- Auto-focus on page load
- Auto-save to localStorage every 3 seconds (prevents data loss)

#### 3. Reflect Button
- Disabled when textarea empty
- Shows loading state when processing
- Text changes: "Reflect" → "Contemplating..." → "Reflect"
- Smooth transitions

#### 4. Loading State (2-3 seconds artificial delay)
```

Phase 1: User clicks "Reflect"

- Button disabled
- Show: "Your words are being received..."
- Gentle animation (pulsing icon or subtle shimmer)

Phase 2: Processing

- Keep loading state
- Call backend API
- Wait minimum 2 seconds (even if response faster)

Phase 3: Response appears

- Fade in from bottom
- Smooth transition

```

#### 5. AI Response Display
```

Design:
┌────────────────────────────────────────┐
│ 💫 Spiritual Guidance │ ← Header with icon
├────────────────────────────────────────┤
│ │
│ [AI response here] │ ← Response text
│ - Formatted with paragraphs │
│ - Line breaks preserved │
│ - Readable font size │
│ - Proper spacing │
│ │
│ ──────────────── │ ← Divider
│ │
│ Related wisdom: │ ← Optional quote
│ "Quote from spiritual text..." │
│ │
└────────────────────────────────────────┘

Features:

- Appears below textarea after response
- Gentle fade-in animation
- Background: subtle different shade
- Rounded corners
- Padding: generous (24px)
- Can copy text
- "Start new entry" button at bottom
  Technical Implementation
  Components Needed

DiaryEntry.tsx - Main entry component
ResponseDisplay.tsx - AI response display
LoadingState.tsx - Contemplation animation

State Management
typescript- entryText: string (textarea content)

- isLoading: boolean (submitting state)
- aiResponse: string | null (received response)
- autoSaveStatus: 'saved' | 'saving' | 'error'
  Auto-save Logic
  typescript- Use useEffect with debounce (3 seconds)
- Save to localStorage: `diary_draft_${userId}_${date}`
- Show tiny "Saved" indicator
- Load draft on mount if exists
- Clear draft after successful submission
  API Integration
  typescript- Call existing sendMessage() server action
- Add artificial 2-second minimum delay for UX
- Handle errors gracefully
- Show error message if API fails

```

### Styling Approach
- Use Tailwind CSS for layout
- Custom CSS for specific effects (paper texture, animations)
- CSS variables for colors (easy theme switching later)
- Responsive: stack vertically on mobile

### Mobile Considerations
- Full-width textarea
- Larger touch targets (48px minimum)
- Bottom padding for keyboard
- Sticky "Reflect" button on mobile
- Simplified animations (performance)

---

## Phase 3: Quick Polish (30-45 min)

### Micro-improvements
1. **Transitions**
   - All state changes fade (200-300ms)
   - Page transitions smooth
   - Hover states on buttons

2. **Focus States**
   - Textarea subtle glow on focus
   - Button outline for accessibility
   - Remove default browser outlines, add custom

3. **Empty States**
   - If no past entries: gentle message
   - Loading skeletons where appropriate

4. **Feedback**
   - Success message after save
   - Error messages styled consistently
   - Toast notifications (optional)

---

## File Structure
```

src/
├── app/
│ ├── dashboard/
│ │ ├── layout.tsx (wraps with DashboardLayout)
│ │ ├── today/
│ │ │ └── page.tsx (diary entry page)
│ │ ├── journey/
│ │ │ └── page.tsx (past entries - Phase 4)
│ │ └── settings/
│ │ └── page.tsx (placeholder)
│ └── actions/
│ └── diaryActions.ts (server actions)
├── components/
│ ├── Sidebar.tsx
│ ├── DashboardLayout.tsx
│ ├── DiaryEntry.tsx
│ ├── ResponseDisplay.tsx
│ ├── LoadingState.tsx
│ └── ui/
│ └── (reusable UI components)
└── lib/
└── utils.ts (helper functions)

Dependencies to Install
bashnpm install date-fns # For date formatting
npm install lucide-react # For icons
npm install class-variance-authority # For component variants (optional)
npm install clsx tailwind-merge # For className utilities

Design Assets Needed
Icons (use Lucide React)

Home
BookOpen
User
Settings
LogOut
Sparkles (for AI response)
Send (for submit)

Fonts (Google Fonts)
html<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">

Testing Checklist
Functionality

Sidebar navigation works
Active page highlights in sidebar
Textarea auto-resizes
Auto-save works (check localStorage)
Submit calls API correctly
Loading state shows for 2+ seconds
Response displays correctly
"Start new entry" clears form
Sign out works

Responsive

Sidebar collapses on mobile
Hamburger menu works
Textarea full width on mobile
Buttons touchable (48px min)
No horizontal scroll

Accessibility

Keyboard navigation works
Focus states visible
Screen reader friendly
Color contrast meets WCAG AA
Alt text on icons (aria-label)

Polish

Animations smooth (60fps)
No layout shift
Loading states clear
Error messages helpful
Success feedback clear

Priority Order

Sidebar (foundation for navigation)
Diary entry page redesign (core experience)
Loading states (polish the interaction)
Response display (complete the loop)
Auto-save (safety feature)
Polish (micro-interactions)

Expected Timeline

Sidebar: 1-1.5 hours
Entry page redesign: 2-3 hours
Polish: 30-45 minutes
Testing: 30 minutes

Total: 4-6 hours for complete Phase 1 & 2

Notes for Implementation
CSS Custom Properties (in globals.css)
css:root {
--color-primary: #2D3561;
--color-secondary: #E8DCC4;
--color-accent: #C9A969;
--color-background: #FAF9F6;
--color-text: #1A1A1A;
--color-text-secondary: #6B7280;

--font-serif: 'Crimson Text', Georgia, serif;
--font-sans: 'Inter', system-ui, sans-serif;
}
Artificial Delay Implementation
typescriptconst MIN_LOADING_TIME = 2000; // 2 seconds

const startTime = Date.now();
const response = await sendMessage(text);
const elapsed = Date.now() - startTime;
const remainingDelay = Math.max(0, MIN*LOADING_TIME - elapsed);
await new Promise(resolve => setTimeout(resolve, remainingDelay));
Auto-save Implementation
typescriptuseEffect(() => {
const timer = setTimeout(() => {
if (entryText) {
localStorage.setItem(`diary_draft*${userId}`, entryText);
setAutoSaveStatus('saved');
}
}, 3000);

return () => clearTimeout(timer);
}, [entryText, userId]);

Success Criteria
✅ User can navigate via sidebar
✅ Writing experience feels intentional and calm
✅ Loading states create anticipation
✅ Response display is beautiful and readable
✅ Auto-save prevents data loss
✅ Mobile experience is polished
✅ Accessible to all users
✅ Performance is smooth (no jank)

Future Enhancements (Not in this phase)

Weekly/monthly summaries
Pattern recognition
Search functionality
Export journal
Custom themes
Daily prompts
Streak tracking
Analytics dashboard

Ready to Start?
Begin with Sidebar component, then move to diary entry redesign. Each component should be tested before moving to the next. Commit frequently.

End of Implementation Plan
