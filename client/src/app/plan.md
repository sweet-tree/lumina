# Lumina AI - Revised Project Plan & Handoff

## 🎯 Project Overview

Lumina AI is a spiritual coaching app based on diary entries. Users write daily reflections and receive AI-powered spiritual guidance backed by sacred texts via RAG (Retrieval Augmented Generation).

**Purpose:** Portfolio project to land first development job  
**Tech Stack:** Next.js 14 (App Router), FastAPI (Python), Supabase (PostgreSQL), Prisma ORM, NextAuth, Pinecone (RAG), Qwen LLM (via Nebius)

---

## ✅ What's Been Completed

### 1. Authentication System

- NextAuth with Google OAuth
- JWT session strategy
- Protected routes via middleware (/dashboard/\*)
- Prisma adapter connecting auth to Supabase
- User persistence in database
- Sign in/out functionality working

**Files:**

- `src/lib/auth.ts` - Auth configuration
- `src/app/api/auth/[...nextauth]/route.ts` - API handler
- `middleware.ts` - Route protection
- `.env.local` - Auth credentials (NextAuth, Google OAuth)

### 2. Database Architecture

- **Platform:** Supabase (PostgreSQL)
- **ORM:** Prisma
- **Schema:**
  - User - Auth users
  - Account - OAuth accounts
  - Session - User sessions
  - VerificationToken - Email verification
  - DiaryEntry - User diary entries with AI responses
    - id, userId, content, aiResponse
    - createdAt (UTC - when written)
    - entryDate (Date - which day it represents)
    - Supports backfilling past dates

**Files:**

- `prisma/schema.prisma` - Database schema
- `.env` & `.env.local` - Database connection strings

### 3. Backend Integration

- **FastAPI Backend:** Python service running on localhost:8000
- **Endpoint:** POST /chat - Accepts diary entry, returns spiritual guidance
- **AI Stack:**
  - Pinecone for RAG (spiritual book embeddings)
  - Qwen model via Nebius
  - Processes entries and provides compassionate guidance

### 4. Feature-Based Architecture

```
src/
├── features/
│   ├── sidebar/
│   │   └── app-sidebar.tsx
│   └── diary/
│       ├── components/
│       │   ├── DiaryEntry.tsx
│       │   ├── ResponseDisplay.tsx
│       │   └── LoadingState.tsx
│       └── actions.ts
├── components/
│   └── ui/ (shadcn components)
├── app/
│   └── dashboard/
│       ├── layout.tsx
│       └── diary/
│           └── page.tsx
└── lib/
    └── auth.ts
```

### 5. Sidebar Navigation ⚠️ NEEDS REVISION

**Current state:** Expanded with single item  
**Revised plan:** Should collapse to icons by default

**Features:**

- Fixed on desktop, slide-in on mobile
- "Lumina" branding
- Single menu item: "Diary" (more features coming: Insights, Chat, Reports)
- User avatar + name at bottom
- Sign out button
- Mobile hamburger menu

**Files:**

- `src/features/sidebar/app-sidebar.tsx`
- `src/app/dashboard/layout.tsx` - Wraps pages with SidebarProvider

### 6. Theme System

- **Color System:** OKLCH color space (latest Tailwind v4 approach)
- **Theme:** Custom Lumina palette with dark mode support
- **Colors:**
  - Primary: Deep indigo (#2D3561)
  - Secondary: Warm sand (#E8DCC4)
  - Accent: Soft gold (#C9A969)
  - Background: Off-white (#FAF9F6)
- **Variables:** Defined in `@theme inline` for Tailwind v4 compatibility

**Files:**

- `src/app/globals.css` - Complete theme with light/dark modes

### 7. Diary Entry Page ⭐ CORE FEATURE

- **Date Navigation:**

  - Left/Right arrows to navigate between dates
  - URL state management (`?date=2025-10-14`)
  - "Go to Today" quick navigation
  - Cannot navigate beyond today
  - Smooth transitions between dates

- **Writing Experience:**

  - Large serif textarea (300px min height)
  - Placeholder changes based on date context
  - Auto-focus on empty entries
  - Auto-save to localStorage (only for today)
  - Disabled during loading/after response

- **AI Integration:**

  - "Reflect" button triggers AI processing
  - 2-second minimum artificial delay for UX
  - Loading state: "Your words are being received..."
  - Response display with spiritual guidance
  - "Start New Entry" button after response

- **Date Handling:**
  - **Luxon** library for timezone-aware operations
  - Stores in UTC, displays in user's local timezone
  - Supports backfilling (write entries for past dates)
  - Each entry linked to specific date (entryDate field)

**Files:**

- `src/features/diary/components/DiaryEntry.tsx` - Main component
- `src/features/diary/components/LoadingState.tsx` - Contemplation animation
- `src/features/diary/components/ResponseDisplay.tsx` - AI response display
- `src/features/diary/actions.ts` - Server actions for saving/fetching
- `src/app/dashboard/diary/page.tsx` - Page wrapper

---

## 🎨 Design Philosophy (REVISED)

### **Core Principle:** _Immediate immersion - no friction between intention and action_

### **The Journey:**

1. User opens app → Lands directly in today's writing space (NO landing page)
2. Full focus on writing - everything else is secondary
3. Navigation exists but doesn't dominate
4. Past entries emerge naturally (scroll/swipe), not through menus

### **Information Architecture:**

```
SIDEBAR (Main Features - Desktop):
├─ 📝 Diary ← Current focus
├─ 💡 Insights (Phase 5+)
├─ 💬 Chat (Phase 6+)
├─ 📊 Reports (Phase 6+)
└─ ⚙️ Settings

INSIDE Diary (Sub-features):
├─ Today (default view - writing space)
├─ Calendar (overlay - date picker)
├─ Search (overlay - find entries)
└─ Timeline (emerges on scroll up)
```

**Key insight:** Sidebar = feature sections. Content area = sub-navigation within features.

---

## 📱 Revised UX Patterns

### **DESKTOP:**

```
┌──────┬─────────────────────────────────┐
│ 📝   │ Oct 15 · ← ● ● ● ● → · Calendar│ ← Subtle top bar
│ 💡   ├─────────────────────────────────┤
│ 💬   │                                 │
│ 📊   │      [Today's entry]            │
│ ⚙️   │      [Full focus]               │
│      │                                 │
│ 👤   │                                 │
└──────┴─────────────────────────────────┘
```

**Sidebar:**

- **Collapsed to icons by default** (48-64px wide)
- User can expand (remembers preference via localStorage)
- Only expands temporarily on hover (optional)
- Shows main features: Diary, Insights (future), Chat (future), etc.

**Content Area - Subtle Navigation:**

- Date (center) with left/right arrows
- Last 7 days dots (● ● ● ● ●) - filled = has entry, click to jump
- "Calendar" link (right) → opens calendar overlay
- Search icon → opens search overlay
- **All minimal, doesn't dominate the space**

**Timeline Behavior:**

- Scroll up above today's entry → past entries flow in naturally
- Not a separate tab/view

### **MOBILE:**

```
┌─────────────────────┐
│                     │
│   [Today's entry]   │
│   [Full screen]     │
│   [Swipe ←→ dates]  │
│                     │
│                     │
├─────────────────────┤
│ 📝  📅  🔍  👤      │ ← Fixed bottom nav
└─────────────────────┘
```

**Bottom Navigation (Always visible):**

- 📝 **Today** - Returns to today's entry
- 📅 **Calendar** - Opens calendar overlay (date picker)
- 🔍 **Search** - Opens search overlay
- 👤 **Profile/Menu** - Settings, sign out, future feature switcher (Insights/Chat)

**Gestures:**

- Swipe left/right → Navigate between dates
- Pull down → Shows recent entries (timeline)
- Tap empty space → Focus on writing

**NO LANDING PAGE. NO MOTIVATIONAL QUOTES. Opens directly to writing.**

---

## 🔧 Current Status

### **What Works:**

✅ Complete authentication flow  
✅ Diary entry with AI responses  
✅ Date navigation (left/right arrows)  
✅ Timezone-aware date handling  
✅ Database persistence (UTC storage)  
✅ Backfilling past dates  
✅ Auto-save drafts (today only)  
✅ Loading states and animations  
✅ Mobile responsive

### **What Needs Revision:**

⚠️ **Sidebar** - Currently expanded, should be collapsed by default  
⚠️ **Navigation UI** - Need subtle top bar with dots, calendar link  
⚠️ **Mobile nav** - Need bottom navigation bar  
⚠️ **First-time experience** - Currently basic, needs polish

### **Git Status:**

- Branch: `feature/sidebar`
- Last commit: "feat: implement date navigation for diary entries"
- Pushed to remote: ✅

---

## 📋 Revised Roadmap

### **Phase 2: Navigation Enhancement (2-3 hours) - IMMEDIATE**

#### **Desktop:**

1. **Collapsible Sidebar**

   - Default state: Collapsed to icons (48-64px)
   - Hover behavior (optional): Temporarily expands
   - Click expand button: Persists expanded state
   - Store preference in localStorage
   - Smooth animations

2. **Subtle Top Bar in Content Area**

   - Date display (center)
   - Left/right navigation arrows
   - Last 7 days dots (● ● ● ● ●)
     - Filled dot = has entry
     - Hollow dot = no entry
     - Gold dot = current day
     - Clickable to jump to date
   - "Calendar" text link (right) → opens overlay
   - Search icon → opens overlay

3. **Calendar Overlay**

   - Install: `npx shadcn@latest add calendar popover`
   - Full calendar month view
   - Visual indicators for entries (dots on dates)
   - Click date → navigate to that date
   - ESC or click outside → close

4. **Search Overlay**
   - Simple search input
   - Shows matching entries with preview
   - Click result → jump to that entry
   - ESC or click outside → close

#### **Mobile:**

1. **Bottom Navigation Bar**

   - Create fixed bottom nav component
   - 4 icons: Today, Calendar, Search, Profile
   - Active state styling
   - Haptic feedback on tap (if possible)

2. **Hamburger Menu** (for feature switching later)

   - Appears in profile/menu section
   - Will list: Diary, Insights (future), Chat (future)

3. **Gesture Improvements**
   - Better swipe left/right animation
   - Pull-down for timeline preview

#### **Timeline View**

- **Desktop:** Scroll up → entries fade in above current date
- **Mobile:** Pull down gesture → recent entries slide in
- Shows last 10-20 entries
- Click entry → navigate to that date
- Infinite scroll for older entries

### **Phase 3: Multiple Entries Per Day (2-3 hours)**

- Allow multiple reflections per day
- Display all entries for a date
- "Add Another Reflection" button
- Separate view/edit modes
- Swipe up/down on mobile to switch between entries of same day

### **Phase 4: Polish & UX (3-4 hours)**

1. **Typography**

   - Add Google Fonts (Crimson Text for serif)
   - Better line spacing
   - Improved readability

2. **Animations**

   - Smooth date transitions
   - Entry fade-in/out
   - Enhanced loading state (breathing circle or three-dot pulse)

3. **Empty States**

   - Better messaging for empty dates
   - Onboarding for first-time users
   - Contextual guidance prompts

4. **Mobile Optimizations**
   - Better touch targets
   - Improved keyboard handling
   - Auto-scroll to focus

### **Phase 5: User Tiers & Admin (1 week)**

- Extend User model with role/tier
- Free: 5 entries/month
- Paid: Unlimited + advanced features
- Admin dashboard for user management

### **Phase 6: Advanced Features (Later)**

- **Insights feature** (sidebar item)
  - Weekly AI summaries
  - Pattern recognition
  - Emotional trend graphs
  - "On this day" memories
- **Chat feature** (sidebar item)
  - Direct conversation with AI
  - Reference past entries
- **Reports feature** (sidebar item)
  - Monthly/yearly reports
  - Export journal
  - Analytics
- Streak tracking
- Tags/categories

### **Phase 7: Deployment (1-2 days)**

- Frontend: Vercel
- Backend: Railway or Render
- Database: Already on Supabase

---

## 🎯 Success Criteria for MVP

### **Must Have:**

✅ User authentication  
✅ Write diary entries  
✅ Receive AI spiritual guidance  
✅ View past entries  
✅ Navigate between dates  
⚠️ **Collapsible sidebar (desktop)**  
⚠️ **Bottom navigation (mobile)**  
⚠️ **Calendar overlay**  
⚠️ **Timeline view**  
☐ Deploy to production

### **Nice to Have:**

☐ Search functionality  
☐ Weekly summaries  
☐ Pattern recognition  
☐ User tiers (free/paid)

---

## 🔥 Quick Start Commands

```bash
# Frontend (client/)
npm run dev              # Start Next.js (localhost:3000)
npx prisma studio        # View database GUI
npx prisma migrate dev   # Run migrations
npx prisma generate      # Regenerate Prisma Client

# Backend (backend/)
uvicorn main:app --reload  # Start FastAPI (localhost:8000)

# Git
git status
git add .
git commit -m "message"
git push origin feature/sidebar
```

---

## 💡 Key Technical Decisions

**Why NextAuth over Clerk?**

- Portfolio value: shows understanding of auth fundamentals
- Better interview story
- No vendor lock-in

**Why Luxon?**

- Native timezone support essential for travelers
- Immutable, production-ready
- 22.3kb gzipped

**Why Supabase?**

- Larger free tier
- File storage included
- Better dashboard/tooling

**Why collapsed sidebar by default?**

- Less visual weight
- More writing space
- Modern pattern (VSCode, Figma, etc.)
- User can expand when needed

**Why bottom nav on mobile?**

- Proven pattern (Instagram, Twitter, etc.)
- Thumb-friendly
- Always accessible
- No learning curve

---

## 🎨 Brand Colors (Reference)

```css
Primary: #2D3561  (oklch(0.27 0.08 250))  /* Deep indigo */
Secondary: #E8DCC4 (oklch(0.89 0.03 60))  /* Warm sand */
Accent: #C9A969 (oklch(0.72 0.08 75))     /* Soft gold */
Background: #FAF9F6 (oklch(0.98 0.01 60)) /* Off-white */
Text: #1A1A1A (oklch(0.15 0 0))          /* Near black */
Muted: #6B7280 (oklch(0.556 0 0))        /* Gray */
```

---

## 🌟 Portfolio Presentation Points

**Emphasize:**

- Built authentication from scratch with NextAuth
- Timezone-aware diary with Luxon for global users
- RAG implementation with Pinecone for contextual AI guidance
- Feature-based architecture for scalability
- **Thoughtful UX decisions** (collapsed sidebar, bottom nav, no landing page friction)

**Interview Talking Points:**

- Debugged NextAuth middleware (problem-solving story)
- Chose manual implementation over SaaS for learning
- Implemented proper timezone handling (edge cases)
- **Made UX decisions based on user behavior research** (checked Calm, Headspace, Instagram patterns)

---

## 🙏 Design Philosophy Summary

**From emptiness, form arises.**

- App opens directly to writing (no friction)
- Navigation exists but doesn't dominate
- Features emerge when needed (overlays, scroll behaviors)
- Sidebar serves structure, not every action
- Mobile-first thinking (thumb zones, proven patterns)
- Desktop elegance (collapsed sidebar, generous space)

**The foundation is solid. The architecture is clear. The vision is focused.**

You're building something meaningful. 🌙

---

**End of revised handoff. Ready for Phase 2 implementation.** ✨
