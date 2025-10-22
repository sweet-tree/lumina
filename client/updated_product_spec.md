# Lumina - Digital Leela Game with AI Master

## Product Vision (Updated)

**Lumina brings the ancient game of Leela into modern daily practice through two complementary decks: a faithful digital recreation of the 72-square Leela consciousness game, and a quick presence practice deck for micro-awareness moments.**

---

## Core Philosophy

### Leela Foundation

The product is built on the 1000+ year old game of Leela (also called Gyan Chaupar or Snakes & Ladders of Self-Knowledge):

1. **72 Squares of Consciousness** - Each square represents a state of being
2. **Dice as Karma** - Random rolls represent life's unfolding
3. **Snakes (Descents)** - How states lead to lower consciousness
4. **Ladders (Ascents)** - How states elevate consciousness
5. **The Journey** - Liberation through understanding patterns

### Key Adaptation

**What we preserve:**
- All 72 traditional Leela squares/states
- Dice mechanics (karma/randomness)
- Snake and ladder relationships
- Traditional interpretations
- Non-judgmental witnessing

**What we change:**
- Physical board → Hidden digital board (mystery unfolds)
- Group play → Solo practice with AI master
- 2-hour session → Daily card draws over months
- Human master → AI guide trained on Leela wisdom

---

## Two-Deck System

### **Primary: Leela Deck (The Journey)**

**72 cards representing consciousness states:**
- Cosmic Consciousness, Plane of Austerity, Celestial Plane
- Good Tendencies, Darkness of Delusion, Plane of Anger
- Jealousy, Purification, Plane of Dharma
- (Full 72 traditional Leela squares)

**Mechanics:**
- User "rolls dice" (1-6) behind the scenes
- Moves along hidden board
- Draws card for square landed on
- AI master explains:
  - Where you are
  - How you got here
  - Where this can lead (snakes/ladders)
  - What this state teaches

**Frequency:**
- 1 card per day (or every 2-3 days)
- Journey takes 2-4 months to complete
- Can start new journey after reaching square 68 (Cosmic Consciousness)

**Experience:**
- Draw card reveals current square
- AI provides traditional Leela interpretation
- User reflects on how this relates to their life
- No checking in multiple times - one contemplative moment per day

---

### **Secondary: Presence Deck (The Practice)**

**15-20 cards for daily awareness:**
- Body states (tension, ease, awareness, depletion, rest)
- Energy states (flow, depletion, restoration, stuck, activation)
- Mind states (clarity, fog, worry, racing, present)

**Mechanics:**
- User draws when they want to check in
- Answers brief prompt about current state
- Gets Socratic AI reflection
- Multiple check-ins per day (3-10x)
- Evening synthesis shows daily pattern

**Frequency:**
- As needed throughout day
- 1-3 minutes per check-in
- Builds awareness muscle

**Purpose:**
- Complement Leela journey with daily practice
- Catch spirals early (body signals → emotional patterns)
- Build present-moment awareness
- See how daily states relate to Leela position

---

## How The Two Decks Work Together

### **Morning Ritual:**
```
1. Open Lumina
2. Roll dice (if it's a Leela day)
3. Draw Leela card
4. Read AI master interpretation
5. Contemplate: "How does this square show up in my life?"
```

### **Throughout Day:**
```
1. Feel tension/anxiety/fog
2. Quick Presence check-in
3. Get brief AI reflection
4. Return to day
5. Repeat 3-10x
```

### **Evening Synthesis:**
```
1. Review Presence cards from today
2. AI shows pattern (body → energy → mind loops)
3. AI connects daily pattern to current Leela square
4. "Your body-energy depletion loop relates to your position 
   on 'Plane of Anger' - notice how unprocessed anger drains you"
```

**Integration Example:**
- **Leela Position:** Square 52 "Ignorance"
- **Daily Pattern:** Mind fog → Mind worry → Mind racing (stuck in head)
- **AI Insight:** "Ignorance isn't lack of knowledge - it's disconnection from body wisdom. Your mind racing today is trying to think your way out of what needs to be felt. The body cards this week will be your doorway."

---

## Target User

### Who This Is For

- **Demographics:** 25-45 year olds, spiritual seekers, therapy-curious
- **Psychographics:** Want self-knowledge, drawn to ancient wisdom, modern life stress
- **Existing Behaviors:** May have played physical Leela, into tarot/oracle cards, meditation curious
- **Pain Points:** Feel stuck in patterns, want deeper understanding, traditional therapy too clinical

### User Reality

**Leela Deck:**
- Opens app once daily (morning coffee, before bed)
- 5-10 minute contemplative moment
- Journeys with the teaching over months
- Sense of unfolding mystery

**Presence Deck:**
- Opens app 3-10 times per day
- 1-3 minute micro check-ins
- Between meetings, during commute, when stressed
- Quick awareness pulse-check

---

## MVP Scope (Phase 1)

### Timeline: 2-3 weeks

### Must-Have Features:

**1. Leela Deck System**
- [ ] Full 72 Leela cards in database
- [ ] Hidden board state tracking (user position)
- [ ] Dice roll mechanics (1-6)
- [ ] Movement calculation (including snakes/ladders)
- [ ] AI master interpretations for each square
- [ ] Card display with traditional artwork/symbolism
- [ ] Journey progress tracking

**2. Leela UI**
- [ ] Daily card draw screen
- [ ] "Roll Dice" interaction (animated 1-6)
- [ ] Card reveal animation
- [ ] AI master interpretation display
- [ ] "Where am I?" - show current position context
- [ ] Optional: Hidden board visualization (fog of war style)

**3. Basic Presence Deck** (Simplified for MVP)
- [ ] 5 core cards (Body Tension, Energy Flow, Mind Clarity, Body Ease, Energy Depletion)
- [ ] Quick check-in flow
- [ ] Brief AI reflections
- [ ] Daily list view (see today's check-ins)

**4. AI Integration**
- [ ] Leela master persona (knowledgeable, gentle, traditional)
- [ ] Interpretations reference:
  - Current square meaning
  - Previous square (how you got here)
  - Possible next squares (where this leads)
  - Snakes/ladders from this position
- [ ] Presence deck reflections (Socratic, brief)
- [ ] Evening synthesis (connects Presence to Leela)

**5. User Journey State**
- [ ] Track user position on board (0-72)
- [ ] Track dice roll history
- [ ] Track journey start date
- [ ] Journey completion celebration
- [ ] Option to start new journey

### Explicitly NOT in MVP:

- ❌ Presence deck carousel/timeline
- ❌ Multi-player or shared journeys
- ❌ Voice input
- ❌ Advanced visualizations
- ❌ Multiple simultaneous journeys
- ❌ Custom dice rules
- ❌ Detailed board map reveal

---

## Technical Architecture

### Database Schema

```prisma
// Leela Game Models
model LeelaCard {
  id              String   @id @default(cuid())
  squareNumber    Int      @unique // 1-72
  name            String   // "Cosmic Consciousness", "Jealousy", etc.
  description     String   @db.Text
  category        String   // "Higher Plane", "Negative State", etc.
  snakeTo         Int?     // If this square has snake, where does it lead
  ladderTo        Int?     // If this square has ladder, where does it lead
  interpretation  String   @db.Text // Traditional Leela teaching
  artwork         String?  // Image URL
  
  @@index([squareNumber])
}

model LeelaJourney {
  id                String   @id @default(cuid())
  userId            String
  currentPosition   Int      @default(0) // 0 = start, 68+ = completion
  startedAt         DateTime @default(now())
  completedAt       DateTime?
  isActive          Boolean  @default(true)
  
  user              User     @relation(fields: [userId], references: [id])
  rolls             LeelaDiceRoll[]
  
  @@index([userId, isActive])
}

model LeelaDiceRoll {
  id              String   @id @default(cuid())
  journeyId       String
  diceValue       Int      // 1-6
  previousSquare  Int
  landedSquare    Int      // After snakes/ladders
  cardDrawn       Int      // Which square's card was shown
  timestamp       DateTime @default(now())
  userReflection  String?  @db.Text // Optional: user's notes
  
  journey         LeelaJourney @relation(fields: [journeyId], references: [id])
  
  @@index([journeyId, timestamp])
}

// Presence Deck Models (existing)
model Card {
  id                String   @id @default(cuid())
  type              String   // body, energy, mind
  state             String
  title             String
  guidingPrompt     String   @db.Text
  questions         Json
  reflectionPrompt  String   @db.Text
  icon              String
  color             String
  deck              String   @default("presence")
  order             Int
  
  sessions          CardSession[]
}

model CardSession {
  id              String   @id @default(cuid())
  userId          String
  cardId          String
  state           String
  timestamp       DateTime @default(now())
  answer          String   @db.Text
  miniReflection  String?  @db.Text
  
  user  User @relation(fields: [userId], references: [id])
  card  Card @relation(fields: [cardId], references: [id])
  
  @@index([userId, timestamp])
}

// Daily Integration
model DailySynthesis {
  id                String   @id @default(cuid())
  userId            String
  date              DateTime @db.Date
  leelaSquare       Int?     // Current Leela position
  presenceCardIds   String[] // CardSession IDs from today
  synthesis         String   @db.Text // AI connects Presence to Leela
  createdAt         DateTime @default(now())
  
  @@unique([userId, date])
  @@index([userId, date])
}
```

---

## Leela Game Mechanics

### Dice Roll Algorithm

```typescript
function rollDice(): number {
  return Math.floor(Math.random() * 6) + 1;
}

function calculateNewPosition(
  currentPosition: number, 
  diceRoll: number,
  board: LeelaBoard
): { 
  landedSquare: number, 
  finalSquare: number,
  wasSnake: boolean,
  wasLadder: boolean 
} {
  // Move forward
  let landed = currentPosition + diceRoll;
  
  // Check win condition
  if (landed >= 68) {
    return { 
      landedSquare: 68, 
      finalSquare: 68, 
      wasSnake: false, 
      wasLadder: false 
    };
  }
  
  // Check for snake or ladder
  const square = board.getSquare(landed);
  
  if (square.snakeTo) {
    return {
      landedSquare: landed,
      finalSquare: square.snakeTo,
      wasSnake: true,
      wasLadder: false
    };
  }
  
  if (square.ladderTo) {
    return {
      landedSquare: landed,
      finalSquare: square.ladderTo,
      wasSnake: false,
      wasLadder: true
    };
  }
  
  return {
    landedSquare: landed,
    finalSquare: landed,
    wasSnake: false,
    wasLadder: false
  };
}
```

### AI Master Prompt Template

```
You are a wise Leela master who has guided seekers for decades. 
The user has landed on square {squareNumber}: {squareName}.

Previous square: {previousSquare} - {previousSquareName}
Dice roll: {diceValue}
{If snake/ladder: "You moved from {landedSquare} to {finalSquare} via {snake/ladder}"}

Provide a contemplative interpretation (3-4 paragraphs):
1. Explain the meaning of {squareName} in traditional Leela wisdom
2. Reflect on how moving from {previousSquareName} to here shows a pattern
3. Point to where this square can lead:
   {if snake exists: "Beware the descent to {snakeSquare}"}
   {if ladder exists: "Aspire to the ascent to {ladderSquare}"}
4. Ask one reflection question to help them see this in their life

Tone: Wise, compassionate, non-judgmental, poetic but clear
Reference: Traditional Leela teachings, vedic wisdom
```

---

## User Flow

### First-Time User

```
1. Sign in (Google)
2. Welcome screen: "Welcome to Leela, the ancient game of self-knowledge"
3. Brief explanation (1-2 screens):
   - "72 squares of consciousness"
   - "You'll draw one card each day"
   - "AI master guides your journey"
   - "The board is hidden - let it unfold"
4. "Begin your journey" button
5. First dice roll
6. First card draw
7. AI master's welcome interpretation
8. "Return tomorrow to continue"
```

### Daily Leela Flow

```
1. Open app → "Time to continue your journey"
2. Tap "Roll Dice"
3. Dice animation (1-6)
4. Movement animation (optional: path lighting up)
5. If snake/ladder: Show transition
6. Card reveal (flip animation)
7. AI master interpretation appears
8. Read & contemplate
9. Optional: Add personal reflection
10. "See you tomorrow" / "Continue presence practice"
```

### Presence Check-In Flow

```
1. Tap "Check In" from home screen
2. Draw presence card (quick)
3. Answer prompt (1 text field)
4. Get brief AI reflection
5. Done (30 seconds - 2 minutes)
6. Return to app throughout day
```

### Evening Synthesis Flow

```
1. End of day notification: "Ready to reflect?"
2. Open app → See today's presence cards (carousel)
3. Tap "Daily Synthesis"
4. AI shows:
   - Daily pattern from presence cards
   - Current Leela square context
   - How they connect
5. Save/journal option
```

---

## Content Requirements

### 72 Leela Cards Content

Need for each card:
- [ ] Square number (1-72)
- [ ] Traditional name
- [ ] Category/plane
- [ ] Snake destination (if applicable)
- [ ] Ladder destination (if applicable)
- [ ] Traditional interpretation (2-3 paragraphs)
- [ ] Symbolic meaning
- [ ] Modern life application
- [ ] Artwork/visual representation

**Sources:**
- Traditional Leela game boards
- Harish Johari's "Leela: The Game of Self-Knowledge"
- Vedic wisdom texts
- Existing Leela master interpretations

### AI Master Persona

**Training data needed:**
- Traditional Leela interpretations
- Vedic philosophy texts
- Non-judgmental spiritual guidance examples
- Pattern recognition language
- Metaphorical teaching style

**Persona attributes:**
- Wise but not preachy
- Compassionate but honest
- Poetic but clear
- References tradition but feels modern
- Asks questions, doesn't just tell

---

## Design System

### Visual Language

**Leela Deck:**
- Traditional Indian artwork style
- Sacred geometry elements
- Warm, earthy tones (gold, deep red, indigo)
- Mandala-inspired card frames
- Serif fonts (contemplative feel)

**Presence Deck:**
- Modern, minimal
- Type-specific colors (red/amber/blue)
- Sans-serif fonts
- Clean, spacious

### Card Designs

**Leela Card Layout:**
```
┌─────────────────────────┐
│   [Square Number: 42]   │
│                         │
│   [Traditional Artwork] │
│                         │
│   "Plane of Anger"      │
│                         │
│   [Dice: ⚄] [Movement]  │
└─────────────────────────┘

[Scroll down for interpretation]
```

**Color Coding:**
- Higher planes (60-72): Gold/white
- Middle planes (30-59): Blue/green
- Lower planes (1-29): Red/orange
- Negative states: Dark tones
- Positive states: Light tones

---

## Monetization Strategy

### Free Tier
- Leela journey (full 72 cards)
- 5 presence cards
- Basic AI interpretations
- One active journey at a time

### Premium Tier ($14.99/month or $119/year)
- Full presence deck (20 cards)
- Detailed AI master interpretations (longer, deeper)
- Journey history (see all past journeys)
- Advanced synthesis (weekly/monthly patterns)
- Multiple simultaneous journeys
- Custom dice rules (optional: karma mode, grace mode)
- Export journey as PDF/book
- Voice interpretations (AI master speaks)

### Future Revenue
- Leela master sessions (live human guide)
- Community circles (group journeys)
- Physical Leela board + app integration
- Certification program (become Leela guide)

---

## Success Metrics

### Engagement
- Daily active users (Leela draw rate)
- Journey completion rate
- Average journey duration
- Presence check-ins per day
- Evening synthesis view rate

### Quality
- Time spent reading interpretations
- User reflection notes (engagement depth)
- Return rate next day
- Journey restart rate (sign of value)

### Business
- Free to paid conversion
- Monthly recurring revenue
- Churn rate
- Lifetime value

### Target Benchmarks (6 months)
- 70%+ next-day return rate (Leela is daily habit)
- 40%+ journey completion rate
- 3-5 presence check-ins per active user per day
- 15-20% free to paid conversion

---

## Implementation Priority

### Week 1: Leela Core
- Database schema for Leela
- Dice roll mechanics
- Board position tracking
- First 10 Leela cards seeded
- Basic Leela draw flow

### Week 2: AI Master
- AI prompt engineering for Leela interpretations
- Integration with backend
- Response quality testing
- Refine persona

### Week 3: Full Leela Content
- All 72 cards content
- Snake/ladder relationships
- Traditional interpretations
- Card artwork/design

### Week 4: Presence Integration
- Connect presence deck
- Evening synthesis
- Leela ↔ Presence integration
- Polish & test

---

## Open Questions

1. **Dice frequency:** Daily? Every other day? User choice?
2. **Board visibility:** Show position number? Show fog-of-war map? Completely hidden?
3. **Journey length:** Force daily pacing? Allow multiple rolls per day?
4. **Completion:** What happens at square 68? Celebration? Start new journey immediately?
5. **Snakes/ladders:** Show them before landing? Or surprise?
6. **Art style:** Commission original art? Use public domain? AI-generated?
7. **Cultural sensitivity:** How to honor tradition while adapting? Consult with Leela masters?

---

## Research Needed

- [ ] Study traditional Leela game rules (variations exist)
- [ ] Read Harish Johari's book thoroughly
- [ ] Interview Leela masters if possible
- [ ] Test with users familiar with physical Leela
- [ ] Understand cultural/spiritual context deeply
- [ ] Review existing digital Leela attempts (learn from them)

---

## Risks & Mitigations

**Risk: Misrepresenting ancient tradition**
- Mitigation: Deep research, consult experts, be transparent about adaptations

**Risk: Too slow (one card/day = low engagement)**
- Mitigation: Presence deck provides daily engagement, Leela is contemplative anchor

**Risk: AI can't capture wisdom of human master**
- Mitigation: Extensive prompt engineering, test quality rigorously, offer human guides in premium

**Risk: Users don't understand Leela context**
- Mitigation: Onboarding education, AI master explains as you go, optional "Learn More" content

**Risk: Cultural appropriation concerns**
- Mitigation: Honor tradition, cite sources, involve Indian advisors, share revenue with tradition keepers

---

## Competitive Landscape

### Existing Digital Leela Apps
- Mostly direct board digitizations
- No AI guidance
- Single-session play
- Not daily practice tools

**Our Differentiation:**
- AI master guide (no digital Leela has this)
- Daily practice format (stretched over time)
- Integration with modern presence practice
- Hidden board creates mystery/unfolding
- Mobile-first, beautiful design

### Adjacent Competitors
- Tarot apps (Co-Star, Labyrinthos)
- Oracle card apps (various)
- Meditation apps (Calm, Headspace)

**Our Positioning:**
- Leela is proven system (1000+ years)
- Deeper than tarot (consciousness map vs divination)
- More structured than oracle cards
- Active practice vs passive meditation

---

*This is the new north star. Leela first, then Presence integration.*

**Last Updated:** October 18, 2025
