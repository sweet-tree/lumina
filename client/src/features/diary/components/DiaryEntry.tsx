"use client";

import { useState, useEffect } from "react";
import { DateTime } from "luxon";
import { sendMessage } from "../actions";
import { LoadingState } from "./LoadingState";
import { ResponseDisplay } from "./ResponseDisplay";

export function DiaryEntry() {
  const [entry, setEntry] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<string | null>(null);
  const [currentDateTime, setCurrentDateTime] = useState("");

  // Set date/time on mount
  useEffect(() => {
    setCurrentDateTime(DateTime.now().toFormat("MMMM d, yyyy · h:mm a"));
  }, []);

  // Auto-save to localStorage
  useEffect(() => {
    if (!response) {
      const timer = setTimeout(() => {
        if (entry) {
          localStorage.setItem("diary_draft", entry);
        }
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [entry, response]);

  // Load draft on mount
  useEffect(() => {
    const draft = localStorage.getItem("diary_draft");
    if (draft) {
      setEntry(draft);
    }
  }, []);

  const handleSubmit = async () => {
    if (!entry.trim()) return;

    setIsLoading(true);

    try {
      // Artificial minimum delay for UX
      const startTime = Date.now();
      const result = await sendMessage(entry);
      const elapsed = Date.now() - startTime;
      const remainingDelay = Math.max(0, 2000 - elapsed);

      await new Promise((resolve) => setTimeout(resolve, remainingDelay));

      if (result.success && result.response) {
        setResponse(result.response);
        localStorage.removeItem("diary_draft");
      } else {
        alert(result.error || "Failed to get response");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewEntry = () => {
    setEntry("");
    setResponse(null);
    setCurrentDateTime(DateTime.now().toFormat("MMMM d, yyyy · h:mm a"));
  };

  return (
    <div className="mx-auto max-w-3xl">
      {/* Date/Time Header */}
      <div className="mb-6">
        <p className="text-sm text-muted-foreground">{currentDateTime}</p>
      </div>

      {/* Entry Textarea */}
      <div className="mb-6">
        <textarea
          value={entry}
          onChange={(e) => setEntry(e.target.value)}
          placeholder="How are you feeling right now?"
          disabled={isLoading || response !== null}
          className="min-h-[300px] w-full resize-none rounded-lg border-0 bg-card p-6 font-serif text-lg leading-relaxed text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent/50 disabled:opacity-50"
          autoFocus
        />
      </div>

      {/* Reflect Button */}
      {!response && (
        <div className="flex justify-center">
          <button
            onClick={handleSubmit}
            disabled={!entry.trim() || isLoading}
            className="rounded-lg bg-accent px-8 py-3 font-medium text-accent-foreground transition-all hover:bg-accent/90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {isLoading ? "Contemplating..." : "Reflect"}
          </button>
        </div>
      )}

      {/* Loading State */}
      {isLoading && <LoadingState />}

      {/* AI Response */}
      {response && (
        <ResponseDisplay response={response} onNewEntry={handleNewEntry} />
      )}
    </div>
  );
}
