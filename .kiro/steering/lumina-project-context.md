# Lumina Project Context

## Project Vision

Lumina is a consciousness practice app with an AI Plant Teacher guide. We're transitioning from a spiritual coach diary app to the full Lumina vision with breathing cards, pattern recognition, and card collection systems.

## Current Architecture

- **Frontend**: Next.js 15 with TypeScript, Tailwind CSS, Prisma
- **Backend**: Python FastAPI with RAG system (Qwen models on Nebius)
- **Database**: Prisma with user authentication (NextAuth)
- **Styling**: Tailwind CSS with Radix UI components

## Key Design Principles

- **Present moment focus** (Dzogchen: "short moments, many times")
- **Plant Teacher voice** (mystical, neither human nor machine)
- **Ceremonial container** (sacred practice, not productivity tool)
- **Visual beauty** (cards, animations, organic growth metaphors)

## Development Approach

- **Incremental transformation** (build on existing foundation)
- **Spec-driven development** (requirements → design → tasks)
- **One feature at a time** (breathing card first, then check-ins, then patterns)
- **User learning focus** (explain code concepts as we build)

## Code Standards

- Use TypeScript for all new code
- Prefer custom hooks for complex logic
- Use Tailwind for styling (avoid CSS modules)
- Follow Next.js 15 app directory patterns
- Implement accessibility from the start
