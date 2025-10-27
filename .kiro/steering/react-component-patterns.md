---
inclusion: fileMatch
fileMatchPattern: "*.tsx"
---

# React Component Patterns for Lumina

## Component Structure

Always structure React components in this order:

1. Imports (React, Next.js, then local)
2. Type definitions
3. Component function
4. Export statement

## Custom Hooks

- Prefix with `use` (e.g., `useBreathingCard`)
- Keep logic separate from UI components
- Return objects with clear property names
- Handle loading and error states

## Animation Patterns

- Prefer CSS transitions over JavaScript animation
- Use `will-change` for performance
- Implement smooth easing functions
- Always consider 60fps performance

## Accessibility Requirements

- Include proper ARIA labels
- Support keyboard navigation
- Provide screen reader announcements
- Test with actual assistive technology

## Example Component Template

```tsx
"use client";

import { useState, useCallback } from "react";
import { SomeType } from "@/types";

interface ComponentProps {
  onAction: () => void;
  data: SomeType;
}

export function ComponentName({ onAction, data }: ComponentProps) {
  const [state, setState] = useState(false);

  const handleClick = useCallback(() => {
    // Handle interaction
    onAction();
  }, [onAction]);

  return <div className="component-wrapper">{/* Component content */}</div>;
}
```
