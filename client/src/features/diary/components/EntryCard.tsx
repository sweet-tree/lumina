"use client";

import { DateTime } from "luxon";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface EntryCardProps {
  entry: {
    id: string;
    content: string;
    aiResponse: string | null;
    createdAt: Date | string;
  };
  isExpanded?: boolean;
}

export function EntryCard({ entry, isExpanded = true }: EntryCardProps) {
  const [expanded, setExpanded] = useState(isExpanded);

  const timestamp =
    typeof entry.createdAt === "string"
      ? DateTime.fromISO(entry.createdAt)
      : DateTime.fromJSDate(entry.createdAt);

  return (
    <div className="mb-4 rounded-lg border bg-card">
      {/* Header - Timestamp & Toggle */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex w-full items-center justify-between p-4 text-left transition-colors hover:bg-accent/5"
      >
        <span className="text-sm text-muted-foreground">
          {timestamp.toFormat("h:mm a")}
        </span>
        {expanded ? (
          <ChevronUp className="h-4 w-4 text-muted-foreground" />
        ) : (
          <ChevronDown className="h-4 w-4 text-muted-foreground" />
        )}
      </button>

      {/* Content - Collapsible */}
      {expanded && (
        <div className="border-t px-4 pb-4">
          {/* User Entry */}
          <div className="pt-4">
            <p className="whitespace-pre-wrap font-serif text-base leading-relaxed">
              {entry.content}
            </p>
          </div>

          {/* AI Response */}
          {entry.aiResponse && (
            <div className="mt-6 rounded-lg bg-accent/10 p-4">
              <p className="mb-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                Reflection
              </p>
              <p className="whitespace-pre-wrap text-sm leading-relaxed text-foreground/90">
                {entry.aiResponse}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Preview when collapsed */}
      {!expanded && (
        <div className="border-t px-4 py-3">
          <p className="truncate text-sm text-muted-foreground">
            {entry.content.slice(0, 60)}...
          </p>
        </div>
      )}
    </div>
  );
}
