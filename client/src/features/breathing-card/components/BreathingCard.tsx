"use client";

import { useBreathingCard } from "../hooks/useBreathingCard";

interface BreathingCardProps {
  onComplete: () => void;
}

export function BreathingCard({ onComplete }: BreathingCardProps) {
  const { state, startBreathing } = useBreathingCard({ onComplete });

  const handleCardClick = () => {
    if (state === "idle") {
      startBreathing();
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.code === "Space" && state === "idle") {
      event.preventDefault();
      startBreathing();
    }
  };

  return (
    <div className="flex flex-col items-center">
      {/* Progress indicator */}
      {state === "breathing" && (
        <div className="mb-8 text-white/60 text-sm">Breathing...</div>
      )}

      {/* Breathing Card */}
      <div
        className={`
          relative cursor-pointer select-none outline-none
          w-80 h-60 rounded-3xl
          bg-gradient-to-br from-gray-800 to-gray-900
          border border-white/20
          flex items-center justify-center
          focus:ring-2 focus:ring-white/30 focus:ring-offset-2 focus:ring-offset-gray-950
          
          ${
            state === "idle"
              ? "animate-pulse hover:scale-105 transition-transform duration-200"
              : ""
          }
          ${state === "breathing" ? "breathing-animation" : ""}
          ${state === "complete" ? "scale-100" : ""}
        `}
        onClick={handleCardClick}
        onKeyDown={handleKeyDown}
        tabIndex={0}
        role="button"
        aria-label={
          state === "idle"
            ? "Start breathing practice"
            : "Breathing in progress"
        }
      >
        {/* Card Text */}
        <div className="text-center">
          <p className="text-white/80 text-lg font-medium">
            {state === "idle" && "Tap to breathe together"}
            {state === "breathing" && (
              <span className="breathing-text">breathe...</span>
            )}
            {state === "complete" && "Now... what's here?"}
          </p>
        </div>

        {/* Glow effect */}
        <div
          className={`
            absolute inset-0 rounded-3xl pointer-events-none
            ${state === "breathing" ? "breathing-glow" : "opacity-5"}
          `}
        />
      </div>

      {/* Instructions */}
      {state === "idle" && (
        <p className="mt-6 text-white/60 text-sm text-center">
          Tap the card or press spacebar to begin
        </p>
      )}
    </div>
  );
}
