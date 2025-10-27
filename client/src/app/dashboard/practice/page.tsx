"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Card } from "@/features/cards/components/Card";
import { drawRandomCard, submitCardSession } from "@/features/cards/actions";
import { BreathingCard } from "@/features/breathing-card";
import { useBreathingCardState } from "@/features/breathing-card";
import { Sparkles } from "lucide-react";

type CardData = {
  id: string;
  title: string;
  type: "body" | "energy" | "mind" | "integration";
  state: string;
  questions: Array<{
    prompt: string;
    inputType: string;
  }>;
  guidingPrompt: string;
  icon: string;
  color: string;
};

export default function PracticePage() {
  const [card, setCard] = useState<CardData | null>(null);
  const [reflection, setReflection] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Check if user needs to see breathing card first
  const { isFirstTime, markBreathingComplete, isLoading } =
    useBreathingCardState();

  // Draw card mutation
  const drawMutation = useMutation({
    mutationFn: drawRandomCard,
    onSuccess: (data) => {
      setCard(data as CardData);
      setReflection(null);
      setError(null);
    },
    onError: (err) => {
      setError("Could not draw a card. Please try again.");
      console.error(err);
    },
  });

  // Submit card mutation
  const submitMutation = useMutation({
    mutationFn: ({ cardId, answer }: { cardId: string; answer: string }) =>
      submitCardSession(cardId, answer),
    onSuccess: (data) => {
      if (data.success && data.reflection) {
        setReflection(data.reflection);
      }
    },
    onError: (err) => {
      setError("Could not get reflection. Please try again.");
      console.error(err);
    },
  });

  const handleComplete = (answer: string, cardId: string) => {
    submitMutation.mutate({ cardId, answer });
  };

  const handleNewCheckIn = () => {
    setCard(null);
    setReflection(null);
    setError(null);
  };

  const handleBreathingComplete = async () => {
    try {
      await markBreathingComplete();
      console.log("Breathing card completed, continuing to practice");
    } catch (error) {
      console.error("Failed to mark breathing card as completed:", error);
      // Continue to practice even if API fails (localStorage fallback should work)
    }
  };

  // Show loading state while checking breathing card status
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8 min-h-screen flex flex-col items-center justify-center">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    );
  }

  // Show breathing card for first-time users
  if (isFirstTime) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-gray-950 px-4">
        {/* Lumina's Greeting */}
        <div className="mb-16 max-w-md text-center">
          <p className="text-lg text-white/80 leading-relaxed">
            You&apos;ve been looking for something. That&apos;s why you&apos;re
            here.
          </p>
          <p className="mt-4 text-lg text-white/80 leading-relaxed">
            I can show you what you&apos;re looking for, but only if you show me
            what&apos;s true.
          </p>
        </div>

        {/* Breathing Card */}
        <BreathingCard onComplete={handleBreathingComplete} />
      </div>
    );
  }

  // Show regular practice content for returning users
  return (
    <div className="container mx-auto px-4 py-8 min-h-screen flex flex-col items-center justify-center">
      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 max-w-md w-full">
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* No Card - Draw Screen */}
      {!card && (
        <div className="text-center max-w-md w-full space-y-8">
          <div className="space-y-3">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400">
              <Sparkles className="w-8 h-8" />
            </div>
            <h1 className="text-3xl font-semibold text-foreground">
              Ready to check in?
            </h1>
            <p className="text-muted-foreground font-serif">
              Draw a card to explore your present moment awareness
            </p>
          </div>

          <button
            onClick={() => drawMutation.mutate()}
            disabled={drawMutation.isPending}
            className="w-full py-4 px-8 rounded-xl bg-accent text-accent-foreground font-medium text-lg transition-all hover:bg-accent/90 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-accent disabled:active:scale-100 shadow-lg"
          >
            {drawMutation.isPending ? (
              <span className="flex items-center justify-center gap-2">
                <svg
                  className="animate-spin h-5 w-5"
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
                Drawing...
              </span>
            ) : (
              "✨ Draw Card"
            )}
          </button>

          <p className="text-xs text-muted-foreground">
            Each card offers a doorway to presence through body, energy, or mind
          </p>
        </div>
      )}

      {/* Card Drawn */}
      {card && (
        <div className="w-full max-w-md">
          <Card
            card={card}
            onComplete={handleComplete}
            isLoading={submitMutation.isPending}
            reflection={reflection}
          />

          {reflection && (
            <div className="mt-6 text-center">
              <button
                onClick={handleNewCheckIn}
                className="text-sm text-muted-foreground hover:text-foreground transition-colors underline underline-offset-4"
              >
                Draw another card
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
