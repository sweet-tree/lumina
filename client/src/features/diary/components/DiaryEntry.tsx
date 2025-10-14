"use client";

import { useState, useEffect } from "react";
import { DateTime } from "luxon";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { sendMessage, getEntryForDate } from "../actions";
import { LoadingState } from "./LoadingState";
import { ResponseDisplay } from "./ResponseDisplay";

export function DiaryEntry() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // Get date from URL or default to today
  const dateParam = searchParams.get("date");
  const [currentDate, setCurrentDate] = useState<DateTime>(
    dateParam ? DateTime.fromISO(dateParam) : DateTime.now()
  );

  const [entry, setEntry] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(false);
  const [response, setResponse] = useState<string | null>(null);
  const [existingEntry, setExistingEntry] = useState<{
    content: string;
    aiResponse: string | null;
  } | null>(null);
  // Fetch entry when date changes
  useEffect(() => {
    const fetchEntry = async () => {
      setIsFetching(true);
      const dateStr = currentDate.toISODate();
      const entry = await getEntryForDate(dateStr!);

      if (entry) {
        setExistingEntry(entry);
        setEntry(entry.content);
        setResponse(entry.aiResponse);
      } else {
        setExistingEntry(null);
        setEntry("");
        setResponse(null);
      }
      setIsFetching(false);
    };

    fetchEntry();
  }, [currentDate]);

  // Update URL when date changes
  useEffect(() => {
    const dateStr = currentDate.toISODate();
    const isToday = currentDate.hasSame(DateTime.now(), "day");

    if (isToday) {
      router.push("/dashboard/diary");
    } else {
      router.push(`/dashboard/diary?date=${dateStr}`);
    }
  }, [currentDate, router]);

  // Auto-save draft only for today
  useEffect(() => {
    const isToday = currentDate.hasSame(DateTime.now(), "day");
    if (!response && isToday) {
      const timer = setTimeout(() => {
        if (entry) {
          localStorage.setItem("diary_draft", entry);
        }
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [entry, response, currentDate]);

  // Load draft on mount (only for today)
  useEffect(() => {
    const isToday = currentDate.hasSame(DateTime.now(), "day");
    if (isToday && !existingEntry) {
      const draft = localStorage.getItem("diary_draft");
      if (draft) {
        setEntry(draft);
      }
    }
  }, [currentDate, existingEntry]);

  const handleSubmit = async () => {
    if (!entry.trim()) return;

    setIsLoading(true);

    try {
      const startTime = Date.now();
      const dateStr = currentDate.toISODate();
      const result = await sendMessage(entry, dateStr!);
      const elapsed = Date.now() - startTime;
      const remainingDelay = Math.max(0, 2000 - elapsed);

      await new Promise((resolve) => setTimeout(resolve, remainingDelay));

      if (result.success && result.response) {
        setResponse(result.response);
        setExistingEntry({ content: entry, aiResponse: result.response });
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
    setExistingEntry(null);
  };

  const goToPreviousDay = () => {
    setCurrentDate(currentDate.minus({ days: 1 }));
  };

  const goToNextDay = () => {
    const tomorrow = DateTime.now().plus({ days: 1 }).startOf("day");
    const nextDate = currentDate.plus({ days: 1 });

    // Don't go beyond tomorrow
    if (nextDate <= tomorrow) {
      setCurrentDate(nextDate);
    }
  };

  const goToToday = () => {
    setCurrentDate(DateTime.now());
  };

  const isToday = currentDate.hasSame(DateTime.now(), "day");
  const canGoNext = currentDate < DateTime.now().startOf("day");

  if (isFetching) {
    return (
      <div className="mx-auto max-w-3xl">
        <div className="flex items-center justify-center py-12">
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl">
      {/* Date Navigation */}
      <div className="mb-6 flex items-center justify-between">
        <button
          onClick={goToPreviousDay}
          className="rounded-lg p-2 transition-colors hover:bg-accent/10"
          aria-label="Previous day"
        >
          <ChevronLeft className="h-5 w-5 text-muted-foreground" />
        </button>

        <div className="flex flex-col items-center gap-1">
          <p className="text-sm text-muted-foreground">
            {currentDate.toFormat("MMMM d, yyyy")}
          </p>
          {!isToday && (
            <button
              onClick={goToToday}
              className="text-xs text-accent hover:underline"
            >
              Go to Today
            </button>
          )}
        </div>

        <button
          onClick={goToNextDay}
          disabled={!canGoNext}
          className="rounded-lg p-2 transition-colors hover:bg-accent/10 disabled:opacity-30 disabled:cursor-not-allowed"
          aria-label="Next day"
        >
          <ChevronRight className="h-5 w-5 text-muted-foreground" />
        </button>
      </div>

      {/* Entry Textarea */}
      <div className="mb-6">
        <textarea
          value={entry}
          onChange={(e) => setEntry(e.target.value)}
          placeholder={
            existingEntry
              ? "Your entry..."
              : isToday
              ? "How are you feeling right now?"
              : `Write an entry for ${currentDate.toFormat("MMMM d")}...`
          }
          disabled={isLoading || (!!response && !!existingEntry)}
          className="min-h-[300px] w-full resize-none rounded-lg border-0 bg-card p-6 font-serif text-lg leading-relaxed text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent/50 disabled:opacity-50"
          autoFocus={!existingEntry}
        />
      </div>

      {/* Action Buttons */}
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
