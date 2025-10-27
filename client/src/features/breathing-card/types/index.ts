export type BreathingState = "idle" | "inhaling" | "exhaling" | "complete";

export interface BreathingCardProps {
  onComplete: () => void;
}

export interface UseBreathingCardProps {
  onComplete: () => void;
}

export interface UseBreathingCardReturn {
  state: BreathingState;
  currentCycle: number;
  currentText: string;
  startBreathing: () => void;
  isComplete: boolean;
}

export interface UseBreathingCardStateReturn {
  isFirstTime: boolean;
  markBreathingComplete: () => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

export interface BreathingCardStatusResponse {
  hasCompleted: boolean;
  completedAt?: string;
}

export interface BreathingCardCompletionRequest {
  // No body needed for completion request
}

export interface BreathingCardCompletionResponse {
  success: boolean;
  completedAt: string;
}

export const BREATHING_CONFIG = {
  INHALE_DURATION: 4000, // 4 seconds
  EXHALE_DURATION: 6000, // 6 seconds
  TOTAL_CYCLES: 3,
} as const;
