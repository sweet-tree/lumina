"use client";

import { useState } from "react";
import { LoadingState } from "./LoadingState";

interface NewEntryFormProps {
  onSubmit: (content: string) => Promise<void>;
  onCancel?: () => void;
  isLoading: boolean;
  placeholder?: string;
}

export function NewEntryForm({
  onSubmit,
  onCancel,
  isLoading,
  placeholder = "How are you feeling right now?",
}: NewEntryFormProps) {
  const [content, setContent] = useState("");

  const handleSubmit = async () => {
    if (!content.trim()) return;
    await onSubmit(content);
    setContent(""); // Clear after submit
  };

  const handleCancel = () => {
    setContent("");
    onCancel?.();
  };

  return (
    <div className="rounded-lg border bg-card p-6">
      {/* Soft Prompts - TODO: Phase 3 */}
      {/* Will add collapsible Body/Energy/Mind prompts here */}

      {/* Text Area */}
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder={placeholder}
        disabled={isLoading}
        className="min-h-[300px] w-full resize-none border-0 bg-transparent font-serif text-lg leading-relaxed text-foreground placeholder:text-muted-foreground focus:outline-none disabled:opacity-50"
        autoFocus
      />

      {/* Actions */}
      <div className="mt-4 flex justify-end gap-3">
        {onCancel && (
          <button
            onClick={handleCancel}
            disabled={isLoading}
            className="rounded-lg px-6 py-2 font-medium text-muted-foreground transition-colors hover:bg-accent/10 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Cancel
          </button>
        )}
        <button
          onClick={handleSubmit}
          disabled={!content.trim() || isLoading}
          className="rounded-lg bg-accent px-8 py-2 font-medium text-accent-foreground transition-all hover:bg-accent/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isLoading ? "Reflecting..." : "Reflect"}
        </button>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="mt-6">
          <LoadingState />
        </div>
      )}
    </div>
  );
}
