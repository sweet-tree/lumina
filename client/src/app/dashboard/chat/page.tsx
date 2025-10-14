"use client";

import { useSession } from "next-auth/react";
import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { sendMessage } from "./actions";

export default function ChatPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const [messages, setMessages] = useState<
    Array<{ type: "user" | "ai"; content: string }>
  >([
    {
      type: "ai",
      content: "Hello! I'm your AI assistant. How can I help you today?",
    },
  ]);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/signin");
    }
  }, [status, router]);

  if (status === "loading") {
    return (
      <div className="container px-4 py-12">
        <div className="flex flex-col items-center justify-center space-y-8">
          <h1 className="text-3xl font-bold">Loading...</h1>
        </div>
      </div>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (inputRef.current && inputRef.current.value.trim()) {
      const userMessage = inputRef.current.value;

      // Add user message to chat
      setMessages((prev) => [...prev, { type: "user", content: userMessage }]);

      // Clear input
      inputRef.current.value = "";
      setIsProcessing(true);

      try {
        // Call server action
        const result = await sendMessage(userMessage);

        // Add AI response to chat
        if (result.success) {
          setMessages((prev) => [
            ...prev,
            { type: "ai", content: result.response },
          ]);
        }
      } catch (error) {
        console.error("Error sending message:", error);
        setMessages((prev) => [
          ...prev,
          {
            type: "ai",
            content: "Sorry, I encountered an error processing your request.",
          },
        ]);
      } finally {
        setIsProcessing(false);
      }
    }
  };

  return (
    <div className="container px-4 py-12">
      <h1 className="text-3xl font-bold mb-8">Chat Interface</h1>
      <div className="flex flex-col w-full max-w-3xl mx-auto">
        <div className="flex-1 overflow-y-auto mb-4 space-y-4 h-96">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.type === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`rounded-lg px-4 py-2 max-w-xs lg:max-w-md ${
                  msg.type === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-800"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="flex">
          <input
            ref={inputRef}
            type="text"
            placeholder={
              isProcessing ? "Thinking..." : "Type your message here..."
            }
            disabled={isProcessing}
            className="flex-1 p-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isProcessing}
            className="bg-blue-600 text-white p-3 rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? "Sending..." : "Send"}
          </button>
        </form>
      </div>
    </div>
  );
}
