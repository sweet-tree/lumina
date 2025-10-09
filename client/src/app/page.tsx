export default function Home() {
  return (
    <div className="container px-4 py-12">
      <div className="flex flex-col items-center justify-center space-y-8">
        <h1 className="text-3xl font-bold">Welcome to Lumina AI</h1>
        <p className="text-center text-muted-foreground max-w-md">
          An AI-powered platform for document processing and analysis. Upload
          your documents to get started.
        </p>
      </div>
    </div>
  );
}
