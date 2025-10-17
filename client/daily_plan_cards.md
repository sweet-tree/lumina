# Daily Plan: Card System Foundation (Option A)

**Date:** [Today's Date]  
**Goal:** Build working card prototype - ONE complete flow end-to-end  
**Time Budget:** 3-4 hours  
**Status:** 🟡 In Progress

---

## Overview

Build the foundation for the card-based presence practice system. By end of day, we should be able to:
1. Draw a random card
2. Answer questions
3. Submit answers
4. Get AI mini-reflection
5. See card flip animation

---

## Hour 1: Card Component (60 mins)

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

### Task 1.1: Create Card Component File (10 mins)
- [ ] Create `src/features/cards/components/Card.tsx`
- [ ] Set up basic TypeScript types for Card props
- [ ] Import necessary dependencies (useState, etc.)

**Types Needed:**
```typescript
type Question = {
  prompt: string;
  inputType: 'text' | 'voice' | 'choice' | 'slider';
  options?: string[];
};

type CardData = {
  id: string;
  title: string;
  type: 'body' | 'energy' | 'mind' | 'integration';
  state: string;
  questions: Question[];
  icon: string;
  color: string;
};

type CardProps = {
  card: CardData;
  onComplete: (answers: string[], cardId: string) => void;
  isLoading?: boolean;
};
```

---

### Task 1.2: Build Card Front (Questions) (20 mins)
- [ ] Create card container with styling
- [ ] Display card header (icon + title)
- [ ] Map through questions and display
- [ ] Add text input for each question
- [ ] Store answers in state
- [ ] Add "Submit" button

**Key Elements:**
- Card should be mobile-friendly (90% width on mobile, max 500px on desktop)
- Use card type color for header
- Icon displayed prominently
- Questions use serif font for contemplative feel
- Text inputs are simple, clean

---

### Task 1.3: Build Card Back (Reflection) (15 mins)
- [ ] Create flipped state view
- [ ] Display AI reflection content
- [ ] Add "Done" or "New Check-In" button
- [ ] Style with accent background

**Design:**
- Different background color to indicate "back"
- ✨ icon to indicate reflection
- Serif font for reflection text
- Clear call-to-action button

---

### Task 1.4: Add Flip Animation (15 mins)
- [ ] Implement flip transition (CSS or Framer Motion)
- [ ] Trigger flip when answers submitted and reflection received
- [ ] 3D rotation effect (300ms duration)
- [ ] Smooth, polished feel

**Animation Requirements:**
- Card flips on Y-axis (horizontal flip)
- Front fades out, back fades in
- Should feel delightful, not jarring
- Mobile-friendly (no performance issues)

---

## Hour 2: Database + Seeding (60 mins)

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

### Task 2.1: Update Prisma Schema (15 mins)
- [ ] Open `prisma/schema.prisma`
- [ ] Verify Card model exists (if not, add it)
- [ ] Verify CardSession model exists (if not, add it)
- [ ] Add necessary fields (state, ascendingStates, descendingStates, etc.)
- [ ] Run `npx prisma generate` after changes

**Required Models:**
```prisma
model Card {
  id                String   @id @default(cuid())
  type              String   // body, energy, mind, integration
  state             String   // tension, flow, clarity, etc.
  title             String
  questions         Json     // Array of Question objects
  reflectionPrompt  String   @db.Text
  icon              String
  color             String
  deck              String   @default("core")
  order             Int
  
  // Leela relationships
  ascendingStates   String[]
  descendingStates  String[]
  breaksPatternOf   String[]
  
  sessions          CardSession[]
  createdAt         DateTime @default(now())
  
  @@index([deck])
}

model CardSession {
  id              String   @id @default(cuid())
  userId          String
  cardId          String
  state           String
  timestamp       DateTime @default(now())
  answers         Json     // Array of answer strings
  miniReflection  String?  @db.Text
  
  user  User @relation(fields: [userId], references: [id], onDelete: Cascade)
  card  Card @relation(fields: [cardId], references: [id])
  
  @@index([userId, timestamp])
  @@index([userId, state])
}
```

---

### Task 2.2: Create Seed Script (30 mins)
- [ ] Create `prisma/seed-cards.ts` (or update existing seed file)
- [ ] Write 2 complete cards (Body Tension + Energy Flow)
- [ ] Include all required fields
- [ ] Add to package.json seed script if needed

**Seed Data:**
```typescript
const cards = [
  {
    type: 'body',
    state: 'tension',
    title: 'Body Tension',
    questions: [
      {
        prompt: 'Where are you holding tension right now?',
        inputType: 'text'
      },
      {
        prompt: "What's creating this holding pattern?",
        inputType: 'text'
      }
    ],
    reflectionPrompt: 'The user is experiencing body tension. Provide a brief Socratic reflection (2-3 sentences) asking what the tension might be protecting or teaching them. Be warm and non-judgmental.',
    icon: '🫀',
    color: '#EF4444',
    deck: 'core',
    order: 1,
    ascendingStates: ['awareness', 'ease'],
    descendingStates: ['depletion'],
    breaksPatternOf: []
  },
  {
    type: 'energy',
    state: 'flow',
    title: 'Energy Flow',
    questions: [
      {
        prompt: "What's the quality of your energy right now?",
        inputType: 'text'
      },
      {
        prompt: 'When did you last feel it shift?',
        inputType: 'text'
      }
    ],
    reflectionPrompt: 'The user is experiencing energy flow. Provide a brief reflection (2-3 sentences) on what might have created this flow state and how they might sustain it. Be warm and encouraging.',
    icon: '⚡',
    color: '#F59E0B',
    deck: 'core',
    order: 2,
    ascendingStates: ['vitality', 'clarity'],
    descendingStates: [],
    breaksPatternOf: ['stuck']
  }
];
```

---

### Task 2.3: Run Migration & Seed (15 mins)
- [ ] Run `npx prisma migrate dev --name add_cards_system`
- [ ] Run `npx prisma db seed` (or your seed command)
- [ ] Verify cards in database (use Prisma Studio: `npx prisma studio`)
- [ ] Check that 2 cards exist with correct data

---

## Hour 3: API Routes + Page Integration (60 mins)

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

### Task 3.1: Create Random Card API Route (20 mins)
- [ ] Create `src/app/api/cards/random/route.ts`
- [ ] Implement GET handler
- [ ] Fetch all cards from 'core' deck
- [ ] Return random card
- [ ] Handle errors (no cards found, database error)

**Code Structure:**
```typescript
import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { PrismaClient } from '@/generated/prisma';

const prisma = new PrismaClient();

export async function GET() {
  try {
    const session = await getServerSession(authOptions);
    if (!session) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const cards = await prisma.card.findMany({
      where: { deck: 'core' }
    });

    if (cards.length === 0) {
      return NextResponse.json({ error: 'No cards found' }, { status: 404 });
    }

    const randomCard = cards[Math.floor(Math.random() * cards.length)];
    return NextResponse.json(randomCard);
  } catch (error) {
    console.error('Error fetching random card:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```

---

### Task 3.2: Create Card Session API Route (25 mins)
- [ ] Create `src/app/api/cards/session/route.ts`
- [ ] Implement POST handler
- [ ] Accept: cardId, answers
- [ ] Save CardSession to database
- [ ] Call AI backend for mini-reflection
- [ ] Return mini-reflection

**Code Structure:**
```typescript
export async function POST(request: Request) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user?.email) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const user = await prisma.user.findUnique({
      where: { email: session.user.email }
    });

    if (!user) {
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }

    const { cardId, answers } = await request.json();

    // Get card details for reflection prompt
    const card = await prisma.card.findUnique({
      where: { id: cardId }
    });

    if (!card) {
      return NextResponse.json({ error: 'Card not found' }, { status: 404 });
    }

    // Call AI backend
    const aiResponse = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: `Card: ${card.title}
Questions and Answers:
${card.questions.map((q: any, i: number) => `Q: ${q.prompt}\nA: ${answers[i]}`).join('\n\n')}

${card.reflectionPrompt}`
      })
    });

    const aiData = await aiResponse.json();

    // Save session
    const cardSession = await prisma.cardSession.create({
      data: {
        userId: user.id,
        cardId: card.id,
        state: card.state,
        answers: answers,
        miniReflection: aiData.response
      }
    });

    return NextResponse.json({
      success: true,
      reflection: aiData.response,
      sessionId: cardSession.id
    });
  } catch (error) {
    console.error('Error creating card session:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
```

---

### Task 3.3: Update Practice Page (15 mins)
- [ ] Open `src/app/dashboard/diary/page.tsx`
- [ ] Replace diary UI with card draw interface
- [ ] Add "Draw Card" button
- [ ] Fetch random card on button click
- [ ] Display Card component with fetched card
- [ ] Handle loading states

**Basic Structure:**
```typescript
'use client'

import { useState } from 'react';
import { Card } from '@/features/cards/components/Card';

export default function PracticePage() {
  const [card, setCard] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [reflection, setReflection] = useState(null);

  const drawCard = async () => {
    setIsLoading(true);
    const response = await fetch('/api/cards/random');
    const data = await response.json();
    setCard(data);
    setIsLoading(false);
  };

  const handleComplete = async (answers: string[], cardId: string) => {
    setIsLoading(true);
    const response = await fetch('/api/cards/session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cardId, answers })
    });
    const data = await response.json();
    setReflection(data.reflection);
    setIsLoading(false);
  };

  return (
    <div className="container mx-auto max-w-2xl py-8">
      {!card ? (
        <div className="text-center">
          <h1 className="mb-8 text-2xl font-semibold">Ready to check in?</h1>
          <button
            onClick={drawCard}
            disabled={isLoading}
            className="rounded-lg bg-accent px-8 py-3 font-medium text-accent-foreground"
          >
            {isLoading ? 'Drawing...' : 'Draw Card'}
          </button>
        </div>
      ) : (
        <Card
          card={card}
          onComplete={handleComplete}
          isLoading={isLoading}
          reflection={reflection}
        />
      )}
    </div>
  );
}
```

---

## Hour 4: Testing + Polish (60 mins)

**Status:** ⬜ Not Started | 🟡 In Progress | ✅ Complete

### Task 4.1: End-to-End Test (20 mins)
- [ ] Open app in browser
- [ ] Navigate to Practice page
- [ ] Click "Draw Card"
- [ ] Verify random card appears
- [ ] Answer both questions
- [ ] Click Submit
- [ ] Verify AI reflection appears
- [ ] Verify card flips
- [ ] Test on mobile viewport

**Test Cases:**
1. ✅ Card draws successfully
2. ✅ Questions display correctly
3. ✅ Can type in answer fields
4. ✅ Submit button works
5. ✅ Loading state shows during AI call
6. ✅ Reflection appears
7. ✅ Flip animation is smooth
8. ✅ Mobile responsive

---

### Task 4.2: Debug Issues (20 mins)
- [ ] Fix any console errors
- [ ] Check network requests in DevTools
- [ ] Verify database records created
- [ ] Test error cases (no cards, API down, etc.)

**Common Issues to Check:**
- Prisma client not generated
- Environment variables missing
- API routes not found (404)
- CORS issues
- JSON parsing errors
- Database connection issues

---

### Task 4.3: Polish UI (20 mins)
- [ ] Improve card styling
- [ ] Add subtle shadows/borders
- [ ] Smooth out animations
- [ ] Add loading spinners
- [ ] Improve mobile spacing
- [ ] Test dark mode (if applicable)

**Polish Checklist:**
- Card feels tactile/delightful
- Colors match type (body/energy)
- Typography is readable
- Spacing is comfortable
- Buttons are clear
- Loading states are friendly

---

## Success Criteria

By end of session, you should have:

✅ Working Card component with flip animation  
✅ 2 cards seeded in database  
✅ API route that returns random card  
✅ API route that saves session + gets AI reflection  
✅ Practice page that draws card and handles flow  
✅ Complete flow: Draw → Answer → Submit → Reflect → Flip  
✅ Tested on desktop + mobile  

---

## Blockers / Issues

**Track any problems here:**

| Issue | Description | Status | Resolution |
|-------|-------------|--------|------------|
| | | | |

---

## Next Steps (Tomorrow)

After today's foundation is complete:

1. **Add remaining 13 cards** to database
2. **Build Carousel view** for multiple cards
3. **Add Daily Synthesis** functionality
4. **Improve animations** and polish
5. **Add "New Check-In"** button to draw another card

---

## Notes

**Developer Notes:**
- Remember to run `npx prisma generate` after schema changes
- Backend AI must be running at localhost:8000
- Test with actual typing (not just clicking)
- Save frequently (commit after each major task)

**AI Worker Context:**
- This is Phase 1 (MVP) of card system
- We're building Leela-inspired consciousness mapping tool
- Philosophy: Present-moment awareness, no judgment
- Mobile-first design
- Card = state of consciousness (not just prompt)

---

**Last Updated:** [Timestamp]  
**Updated By:** [Developer Name/AI]