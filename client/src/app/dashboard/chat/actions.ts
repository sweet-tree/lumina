"use server";

// Import will be added later when we connect to the real chat service
// import { ChatService } from "@/../chat";

export async function sendMessage(message: string) {
  // For now, return a mock response
  // In the future, this will call the actual ChatService
  console.log("Message received in server action:", message);

  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  return {
    success: true,
    response:
      'This is a mock response to your message: "' +
      message +
      "\". In the next step, we'll connect this to the actual ChatService.",
  };
}
