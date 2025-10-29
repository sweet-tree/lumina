"use client";

import { useState } from "react";
import { Sparkles, Loader2 } from "lucide-react";

type MultiAgentResponse = {
  response: string;
  depth: string;
  card_decision: {
    award_card: boolean;
    reason: string;
  };
  teaching_strategy: Record<string, unknown>;
  extraction: Record<string, unknown>;
};

export default function MultiAgentTestPage() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<MultiAgentResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v2/checkin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_input: input,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to process check-in"
      );
      console.error("Multi-agent test error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewTest = () => {
    setInput("");
    setResult(null);
    setError(null);
  };

  return (
    <div className="container mx-auto px-4 py-8 min-h-screen">
      <div className="max-w-2xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-3">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-purple-100 dark:bg-purple-900/40 text-purple-600 dark:text-purple-400">
            <Sparkles className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-semibold text-foreground">
            Multi-Agent System Test
          </h1>
          <p className="text-muted-foreground">
            Test the new multi-agent depth evaluation system
          </p>
        </div>

        {/* Input Form */}
        {!result && (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label
                htmlFor="checkin-input"
                className="text-sm font-medium text-foreground"
              >
                What&apos;s here right now?
              </label>
              <textarea
                id="checkin-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Try: 'chest tight, breath shallow, meeting soon' or just 'stressed'"
                className="w-full min-h-[120px] p-4 rounded-xl border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="w-full py-4 px-8 rounded-xl bg-accent text-accent-foreground font-medium text-lg transition-all hover:bg-accent/90 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-accent disabled:active:scale-100 shadow-lg"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing...
                </span>
              ) : (
                "✨ Process Check-in"
              )}
            </button>
          </form>
        )}

        {/* Error Display */}
        {error && (
          <div className="p-4 rounded-lg bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800">
            <p className="text-sm text-red-700 dark:text-red-400">
              <strong>Error:</strong> {error}
            </p>
          </div>
        )}

        {/* Results Display */}
        {result && (
          <div className="space-y-6">
            {/* Lumina's Response */}
            <div className="p-6 rounded-xl bg-purple-50 dark:bg-purple-950/20 border border-purple-200 dark:border-purple-800">
              <h2 className="text-sm font-semibold text-purple-900 dark:text-purple-300 mb-3">
                Lumina&apos;s Response
              </h2>
              <p className="text-lg text-purple-950 dark:text-purple-100 leading-relaxed font-serif">
                {result.response}
              </p>
            </div>

            {/* Depth Evaluation */}
            <div className="p-6 rounded-xl bg-blue-50 dark:bg-blue-950/20 border border-blue-200 dark:border-blue-800">
              <h2 className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-3">
                Depth Evaluation
              </h2>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-bold text-blue-950 dark:text-blue-100 capitalize">
                  {result.depth}
                </span>
                <span className="text-sm text-blue-700 dark:text-blue-400">
                  {result.depth === "deep" && "🌟 Deep inquiry"}
                  {result.depth === "medium" && "💫 Medium depth"}
                  {result.depth === "shallow" && "✨ Surface level"}
                </span>
              </div>
            </div>

            {/* Card Decision */}
            <div className="p-6 rounded-xl bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800">
              <h2 className="text-sm font-semibold text-amber-900 dark:text-amber-300 mb-3">
                Card Decision
              </h2>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="text-lg font-semibold text-amber-950 dark:text-amber-100">
                    {result.card_decision.award_card
                      ? "✅ Card Awarded"
                      : "❌ No Card"}
                  </span>
                </div>
                <p className="text-sm text-amber-700 dark:text-amber-400">
                  {result.card_decision.reason}
                </p>
              </div>
            </div>

            {/* Debug Info */}
            <details className="p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-200 dark:border-gray-800">
              <summary className="text-sm font-semibold text-gray-900 dark:text-gray-300 cursor-pointer">
                Debug Info (Raw Response)
              </summary>
              <pre className="mt-3 text-xs text-gray-700 dark:text-gray-400 overflow-auto">
                {JSON.stringify(result, null, 2)}
              </pre>
            </details>

            {/* New Test Button */}
            <button
              onClick={handleNewTest}
              className="w-full py-3 px-6 rounded-xl border border-border bg-background text-foreground font-medium transition-all hover:bg-accent/10 active:scale-[0.98]"
            >
              Test Another Check-in
            </button>
          </div>
        )}

        {/* Example Inputs */}
        {!result && !isLoading && (
          <div className="p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-200 dark:border-gray-800">
            <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-300 mb-2">
              Try these examples:
            </h3>
            <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-400">
              <li>
                <button
                  onClick={() => setInput("stressed")}
                  className="hover:text-purple-600 dark:hover:text-purple-400 underline"
                >
                  • Shallow: &quot;stressed&quot;
                </button>
              </li>
              <li>
                <button
                  onClick={() => setInput("chest tight, breath shallow")}
                  className="hover:text-purple-600 dark:hover:text-purple-400 underline"
                >
                  • Medium: &quot;chest tight, breath shallow&quot;
                </button>
              </li>
              <li>
                <button
                  onClick={() =>
                    setInput(
                      "chest tight, breath shallow, meeting in 10 minutes, noticing the tension wants to brace against what hasn't happened yet"
                    )
                  }
                  className="hover:text-purple-600 dark:hover:text-purple-400 underline"
                >
                  • Deep: &quot;chest tight, breath shallow, meeting in 10
                  minutes, noticing the tension wants to brace...&quot;
                </button>
              </li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
