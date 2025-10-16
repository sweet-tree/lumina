"use client";

import { useState, useEffect } from "react";
import { sendMessage, getEntriesForDate } from "../actions";
import { LoadingState } from "./LoadingState";
import { DateTime } from "luxon";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";

type Entry = {
  id: string;
  content: string;
  aiResponse: string | null;
  createdAt: Date | string;
};

type View = "practice" | "timeline";

export function DiaryEntry() {
  const [view, setView] = useState<View>("practice");
  const [content, setContent] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentReflection, setCurrentReflection] = useState<string | null>(
    null
  );
  const [todayEntries, setTodayEntries] = useState<Entry[]>([]);
  const [isFetchingTimeline, setIsFetchingTimeline] = useState(false);

  // Fetch today's entries count
  useEffect(() => {
    const fetchCount = async () => {
      const today = DateTime.now().toISODate();
      const entries = await getEntriesForDate(today!);
      setTodayEntries(entries);
    };
    fetchCount();
  }, [view]);

  const handleSubmit = async () => {
    if (!content.trim()) return;
    setIsSubmitting(true);

    try {
      const startTime = Date.now();
      const today = DateTime.now().toISODate();
      const result = await sendMessage(content, today!);
      const elapsed = Date.now() - startTime;
      const remainingDelay = Math.max(0, 2000 - elapsed);

      await new Promise((resolve) => setTimeout(resolve, remainingDelay));

      if (result.success && result.response) {
        setCurrentReflection(result.response);
        setContent(""); // Clear form

        // Refresh count
        const entries = await getEntriesForDate(today!);
        setTodayEntries(entries);
      } else {
        alert(result.error || "Failed to get response");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNewCheckIn = () => {
    setContent("");
    setCurrentReflection(null);
    setView("practice");
  };

  const handleViewTimeline = async () => {
    setIsFetchingTimeline(true);
    setView("timeline");
    const today = DateTime.now().toISODate();
    const entries = await getEntriesForDate(today!);
    setTodayEntries(entries);
    setIsFetchingTimeline(false);
  };

  // Practice View - Resizable Split Layout
  if (view === "practice") {
    return (
      <div className="h-[calc(100vh-8rem)]">
        <PanelGroup direction="horizontal" autoSaveId="practice-layout">
          {/* Left Panel - Entry Input */}
          <Panel defaultSize={50} minSize={30}>
            <div className="flex h-full flex-col p-4">
              <p className="mb-4 text-center text-sm text-muted-foreground">
                Right now...
              </p>

              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="How are you feeling right now?"
                disabled={isSubmitting}
                className="min-h-0 flex-1 resize-none rounded-lg border bg-card p-6 font-serif text-lg leading-relaxed text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-accent/50 disabled:opacity-50"
                autoFocus
              />

              <div className="mt-6 flex flex-col gap-3">
                <button
                  onClick={handleSubmit}
                  disabled={!content.trim() || isSubmitting}
                  className="rounded-lg bg-accent px-8 py-3 font-medium text-accent-foreground transition-all hover:bg-accent/90 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isSubmitting ? "Reflecting..." : "Reflect"}
                </button>

                {todayEntries.length > 0 && (
                  <button
                    onClick={handleViewTimeline}
                    className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                  >
                    View Today ({todayEntries.length})
                  </button>
                )}
              </div>
            </div>
          </Panel>

          {/* Resize Handle */}
          {currentReflection && (
            <>
              <PanelResizeHandle className="w-px bg-border hover:bg-accent transition-colors" />

              {/* Right Panel - AI Reflection */}
              <Panel defaultSize={50} minSize={30}>
                <div className="flex h-full flex-col">
                  {isSubmitting ? (
                    <div className="flex h-full items-center justify-center p-4">
                      <LoadingState />
                    </div>
                  ) : (
                    <div className="flex h-full flex-col rounded-lg border bg-card m-4">
                      <div className="border-b p-4">
                        <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                          ✨ Reflection
                        </p>
                      </div>
                      <div className="flex-1 overflow-y-auto p-6">
                        <p className="whitespace-pre-wrap font-serif text-base leading-relaxed text-foreground">
                          {currentReflection}
                        </p>
                      </div>
                      <div className="border-t p-4">
                        <button
                          onClick={handleNewCheckIn}
                          className="w-full rounded-lg bg-accent/10 px-6 py-2 text-sm font-medium text-accent transition-colors hover:bg-accent/20"
                        >
                          New Check-In
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </Panel>
            </>
          )}
        </PanelGroup>
      </div>
    );
  }

  // Timeline View
  if (view === "timeline") {
    if (isFetchingTimeline) {
      return (
        <div className="mx-auto max-w-2xl">
          <div className="flex items-center justify-center py-12">
            <p className="text-muted-foreground">Loading...</p>
          </div>
        </div>
      );
    }

    return (
      <div className="mx-auto max-w-2xl">
        <button
          onClick={() => setView("practice")}
          className="mb-6 flex items-center gap-2 text-sm text-muted-foreground transition-colors hover:text-foreground"
        >
          ← Practice
        </button>

        <h2 className="mb-6 text-lg font-medium">Today</h2>

        <div className="space-y-6">
          {todayEntries.map((entry) => {
            const timestamp =
              typeof entry.createdAt === "string"
                ? DateTime.fromISO(entry.createdAt)
                : DateTime.fromJSDate(entry.createdAt);

            return (
              <div key={entry.id} className="rounded-lg border bg-card p-6">
                <p className="mb-4 text-sm text-muted-foreground">
                  {timestamp.toFormat("h:mm a")}
                </p>

                <p className="mb-4 whitespace-pre-wrap font-serif text-base leading-relaxed">
                  {entry.content}
                </p>

                {entry.aiResponse && (
                  <div className="rounded-lg bg-accent/10 p-4">
                    <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      ✨ Reflection
                    </p>
                    <p className="whitespace-pre-wrap text-sm leading-relaxed text-foreground/90">
                      {entry.aiResponse}
                    </p>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-8 flex justify-center">
          <button
            onClick={() => setView("practice")}
            className="rounded-lg bg-accent px-8 py-3 font-medium text-accent-foreground transition-all hover:bg-accent/90"
          >
            New Check-In
          </button>
        </div>
      </div>
    );
  }

  return null;
}
