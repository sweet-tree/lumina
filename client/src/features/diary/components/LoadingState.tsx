export function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="mb-4 h-12 w-12 animate-pulse rounded-full bg-accent/20" />
      <p className="text-sm text-muted-foreground">
        Your words are being received...
      </p>
    </div>
  );
}
