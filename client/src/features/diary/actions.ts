"use server";

import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { PrismaClient } from "@/generated/prisma";

const prisma = new PrismaClient();

export async function sendMessage(message: string) {
  console.log("Message received in server action:", message);

  try {
    // 1. Check authentication
    const session = await getServerSession(authOptions);
    if (!session?.user?.email) {
      return {
        success: false,
        response: null,
        error: "Unauthorized - please sign in",
      };
    }

    // 2. Get user from database
    const user = await prisma.user.findUnique({
      where: { email: session.user.email },
    });

    if (!user) {
      return {
        success: false,
        response: null,
        error: "User not found",
      };
    }

    // 3. Call the backend chat API
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();

    // 4. Save to database if AI response was successful
    if (data.success && data.response) {
      await prisma.diaryEntry.create({
        data: {
          userId: user.id,
          content: message,
          aiResponse: data.response,
        },
      });
      console.log("Entry saved to database");
    }

    // 5. Return the response
    return {
      success: data.success,
      response: data.response,
      error: data.error,
    };
  } catch (error) {
    console.error("Error calling chat API:", error);
    return {
      success: false,
      response: null,
      error: "Failed to connect to the chat service",
    };
  }
}
