"use client";

import { useState, useEffect } from "react";

type BreathingState = "idle" | "breathing" | "complete";

interface UseBreathingCardProps {
  onComplete: () => void;
}

interface UseBreathingCardReturn {
  state: BreathingState;
  currentCycle: number;
  startBreathing: () => void;
}

export function useBreathingCard({
  onComplete,
}: UseBreathingCardProps): UseBreathingCardReturn {
  const [state, setState] = useState<BreathingState>("idle");
  const [currentCycle, setCurrentCycle] = useState(1);

  const startBreathing = () => {
    if (state !== "idle") return;

    setState("breathing");
    setCurrentCycle(1);

    // Total time: 3 cycles × 10 seconds = 30 seconds
    setTimeout(() => {
      setState("complete");
      setTimeout(() => {
        onComplete();
      }, 2000); // Show "Now... what's here?" for 2 seconds
    }, 30000); // 30 seconds total
  };

  return {
    state,
    currentCycle,
    startBreathing,
  };
}
