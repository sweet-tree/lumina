import { Sparkles } from "lucide-react";

interface ResponseDisplayProps {
  response: string;
  onNewEntry: () => void;
}

export function ResponseDisplay({
  response,
  onNewEntry,
}: ResponseDisplayProps) {
  return (
    <div className="mt-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="rounded-lg border border-accent/20 bg-secondary/30 p-6">
        {/* Header */}
        <div className="mb-4 flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-accent" />
          <h3 className="font-semibold text-foreground">Spiritual Guidance</h3>
        </div>

        {/* Response Content */}
        <div className="prose prose-sm max-w-none">
          <p className="whitespace-pre-wrap leading-relaxed text-foreground/90">
            {response}
          </p>
        </div>

        {/* Divider */}
        <div className="my-6 border-t border-accent/10" />

        {/* New Entry Button */}
        <button
          onClick={onNewEntry}
          className="w-full rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-foreground transition-colors hover:bg-accent/90"
        >
          Start New Entry
        </button>
      </div>
    </div>
  );
}
