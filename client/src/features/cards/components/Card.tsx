"use client";

import { useState } from "react";

// Types
type Question = {
  prompt: string;
  inputType: "text" | "voice" | "choice" | "slider";
  options?: string[];
};

type CardData = {
  id: string;
  title: string;
  type: "body" | "energy" | "mind" | "integration";
  state: string;
  questions: Question[];
  guidingPrompt: string;
  icon: string;
  color: string;
};

type CardProps = {
  card: CardData;
  onComplete: (answer: string, cardId: string) => void;
  isLoading?: boolean;
  reflection?: string | null;
};

// Helper to get type-specific styles
const getTypeStyles = (type: string) => {
  switch (type) {
    case "body":
      return {
        bg: "bg-red-50 dark:bg-red-950/20",
        border: "border-red-200 dark:border-red-800",
        text: "text-red-700 dark:text-red-400",
        icon: "bg-red-100 dark:bg-red-900/40 text-red-600 dark:text-red-400",
      };
    case "energy":
      return {
        bg: "bg-amber-50 dark:bg-amber-950/20",
        border: "border-amber-200 dark:border-amber-800",
        text: "text-amber-700 dark:text-amber-400",
        icon: "bg-amber-100 dark:bg-amber-900/40 text-amber-600 dark:text-amber-400",
      };
    case "mind":
      return {
        bg: "bg-blue-50 dark:bg-blue-950/20",
        border: "border-blue-200 dark:border-blue-800",
        text: "text-blue-700 dark:text-blue-400",
        icon: "bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400",
      };
    case "integration":
      return {
        bg: "bg-purple-50 dark:bg-purple-950/20",
        border: "border-purple-200 dark:border-purple-800",
        text: "text-purple-700 dark:text-purple-400",
        icon: "bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400",
      };
    default:
      return {
        bg: "bg-gray-50 dark:bg-gray-950/20",
        border: "border-gray-200 dark:border-gray-800",
        text: "text-gray-700 dark:text-gray-400",
        icon: "bg-gray-100 dark:bg-gray-900/40 text-gray-600 dark:text-gray-400",
      };
  }
};

export function Card({ card, onComplete, isLoading, reflection }: CardProps) {
  const [answer, setAnswer] = useState("");
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const styles = getTypeStyles(card.type);

  const handleSubmit = () => {
    if (!answer.trim()) return;
    setHasSubmitted(true); // Trigger flip immediately
    onComplete(answer, card.id);
  };

  return (
    <div
      className="relative w-full max-w-md mx-auto h-auto"
      style={{ perspective: "1000px" }}
    >
      {/* Card Container - rotates as one piece */}
      <div
        className="relative w-full h-auto transition-transform duration-700 ease-in-out"
        style={{
          transformStyle: "preserve-3d",
          transform:
            reflection || hasSubmitted ? "rotateY(180deg)" : "rotateY(0deg)",
        }}
      >
        {/* Front of Card - Questions */}
        <div
          className={`w-full rounded-2xl border-2 ${styles.border} ${
            styles.bg
          } shadow-lg overflow-hidden ${reflection ? "invisible" : "visible"}`}
          style={{
            backfaceVisibility: "hidden",
            WebkitBackfaceVisibility: "hidden",
          }}
        >
          {/* Header */}
          <div className="p-6 pb-4">
            <div className="flex items-center gap-3 mb-4">
              <div
                className={`${styles.icon} p-3 rounded-xl text-2xl flex items-center justify-center`}
              >
                {card.icon}
              </div>
              <h2 className={`text-xl font-semibold ${styles.text}`}>
                {card.title}
              </h2>
            </div>

            {/* Guiding Prompt */}
            <p className="text-base text-foreground/80 font-serif leading-relaxed mb-4">
              {card.guidingPrompt}
            </p>

            {/* Optional Guiding Questions */}
            {card.questions && card.questions.length > 0 && (
              <div className="space-y-2">
                <p className="text-sm text-muted-foreground font-medium">
                  Consider:
                </p>
                <ul className="space-y-1.5 ml-1">
                  {card.questions.map((q, idx) => (
                    <li
                      key={idx}
                      className="text-sm text-muted-foreground flex items-start gap-2"
                    >
                      <span className="text-xs mt-0.5">•</span>
                      <span className="flex-1">{q.prompt}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="p-6 pt-0">
            <textarea
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type or speak your response..."
              disabled={isLoading}
              className="w-full min-h-[160px] p-4 rounded-xl border-2 border-border bg-background/50 backdrop-blur-sm font-serif text-base leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent transition-all disabled:opacity-50 disabled:cursor-not-allowed placeholder:text-muted-foreground/50"
              autoFocus
            />
          </div>

          {/* Submit Button */}
          <div className="p-6 pt-0">
            <button
              onClick={handleSubmit}
              disabled={!answer.trim() || isLoading}
              className="w-full py-3 px-6 rounded-xl bg-accent text-accent-foreground font-medium transition-all hover:bg-accent/90 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-accent disabled:active:scale-100 shadow-sm"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg
                    className="animate-spin h-4 w-4"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Reflecting...
                </span>
              ) : (
                "Reflect"
              )}
            </button>
          </div>
        </div>

        {/* Back of Card - Reflection */}
        <div
          className={`w-full rounded-2xl border-2 border-purple-200 dark:border-purple-800 bg-purple-50 dark:bg-purple-950/20 shadow-lg overflow-hidden absolute inset-0 `}
          style={{
            backfaceVisibility: "hidden",
            WebkitBackfaceVisibility: "hidden",
            transform: "rotateY(180deg)",
          }}
        >
          {/* Always show content on back */}
          {reflection ? (
            <>
              {/* Header */}
              <div className="p-6 pb-4">
                <div className="flex items-center gap-3 mb-4">
                  <div className="bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400 p-3 rounded-xl text-2xl flex items-center justify-center">
                    ✨
                  </div>
                  <h2 className="text-xl font-semibold text-purple-700 dark:text-purple-400">
                    Reflection
                  </h2>
                </div>
              </div>

              {/* Reflection Content */}
              <div className="px-6 pb-6">
                <div className="p-5 rounded-xl bg-background/50 backdrop-blur-sm border border-border">
                  <p className="text-base font-serif leading-relaxed text-foreground/90 whitespace-pre-wrap">
                    {reflection}
                  </p>
                </div>
              </div>

              {/* Action Button */}
              <div className="p-6 pt-0">
                <button
                  onClick={() => window.location.reload()}
                  className="w-full py-3 px-6 rounded-xl bg-purple-600 dark:bg-purple-700 text-white font-medium transition-all hover:bg-purple-700 dark:hover:bg-purple-600 active:scale-[0.98] shadow-sm"
                >
                  New Check-In
                </button>
              </div>
            </>
          ) : (
            // Loading state
            <div className="flex flex-col items-center justify-center h-full p-6">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mb-4"></div>
              <p className="text-purple-700 dark:text-purple-400 font-serif">
                Reflecting on your response...
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
