"use client";

import { Card } from "@/features/cards/components/Card";
import { useState } from "react";

export default function TestCardPage() {
  const [reflection, setReflection] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const mockCard = {
    id: "test-1",
    title: "Body Tension",
    type: "body" as const,
    state: "tension",
    icon: "🫀",
    color: "#EF4444",
    questions: [
      {
        prompt: "Where are you holding tension right now?",
        inputType: "text" as const,
      },
      {
        prompt: "What's creating this holding pattern?",
        inputType: "text" as const,
      },
    ],
  };

  const handleComplete = (answers: string[], cardId: string) => {
    console.log("Answers:", answers);
    setIsLoading(true);

    // Simulate AI response after 2 seconds
    setTimeout(() => {
      setReflection(
        "Your body is holding tension as a protective mechanism. Notice where this pattern began and what it might be guarding you from."
      );
      setIsLoading(false);
    }, 2000);
  };

  return (
    <div className="container mx-auto py-8">
      <h1 className="mb-8 text-center text-2xl font-bold">
        Card Component Test
      </h1>
      <Card
        card={mockCard}
        onComplete={handleComplete}
        isLoading={isLoading}
        reflection={reflection}
      />
    </div>
  );
}
