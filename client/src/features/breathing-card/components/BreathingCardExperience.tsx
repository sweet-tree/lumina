"use client";

import { useRouter } from "next/navigation";
import { useBreathingCardState } from "../hooks/useBreathingCardState";
import { BreathingCard } from "./BreathingCard";

export function BreathingCardExperience() {
  const router = useRouter();
  const { markBreathingComplete, isLoading } = useBreathingCardState();

  const handleBreathingComplete = async () => {
    try {
      const result = await markBreathingComplete();
      console.log("Breathing card completed:", result);
      // Redirect to dashboard after successful completion
      router.push("/dashboard");
    } catch (error) {
      console.error("Failed to mark breathing card as completed:", error);
      // Still redirect even if Server Action fails (localStorage fallback should work)
      router.push("/dashboard");
    }
  };

  // Show loading state only if mutation is in progress
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gray-950">
        <div className="text-white/70">Saving...</div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-950 px-4">
      {/* Lumina's Greeting */}
      <div className="mb-16 max-w-md text-center">
        <p className="text-lg text-white/80 leading-relaxed">
          You've been looking for something. That's why you're here.
        </p>
        <p className="mt-4 text-lg text-white/80 leading-relaxed">
          I can show you what you're looking for, but only if you show me what's
          true.
        </p>
      </div>

      {/* Breathing Card */}
      <BreathingCard onComplete={handleBreathingComplete} />
    </div>
  );
}
