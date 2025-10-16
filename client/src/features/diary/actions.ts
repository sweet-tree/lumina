"use server";

import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { PrismaClient } from "@/generated/prisma";
import { DateTime } from "luxon";

const prisma = new PrismaClient();

export async function sendMessage(message: string, entryDate?: string) {
  console.log("Message received:", message, "for date:", entryDate);

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

    // 3. Determine entry date (use provided date or today)
    const dateForEntry = entryDate
      ? DateTime.fromISO(entryDate).startOf("day")
      : DateTime.now().startOf("day");

    // 4. Call the backend chat API
    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();

    // 5. Save to database if AI response was successful
    if (data.success && data.response) {
      const createdEntry = await prisma.diaryEntry.create({
        data: {
          userId: user.id,
          content: message,
          aiResponse: data.response,
          createdAt: DateTime.utc().toJSDate(), // When written (now)
          entryDate: dateForEntry.toJSDate(), // Which day it represents
        },
      });
      console.log("Entry saved for date:", dateForEntry.toISODate());

      // Return the created entry so we can add it to the UI
      return {
        success: true,
        response: data.response,
        entry: {
          id: createdEntry.id,
          content: createdEntry.content,
          aiResponse: createdEntry.aiResponse,
          createdAt: createdEntry.createdAt.toISOString(),
        },
      };
    }

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

// UPDATED: Fetch all entries for specific date (returns array)
export async function getEntriesForDate(date: string) {
  try {
    const session = await getServerSession(authOptions);
    if (!session?.user?.email) {
      return [];
    }

    const user = await prisma.user.findUnique({
      where: { email: session.user.email },
    });

    if (!user) {
      return [];
    }

    // Parse date and get start/end of day
    const targetDate = DateTime.fromISO(date).startOf("day");
    const nextDay = targetDate.plus({ days: 1 });

    // Fetch ALL entries for this specific date
    const entries = await prisma.diaryEntry.findMany({
      where: {
        userId: user.id,
        entryDate: {
          gte: targetDate.toJSDate(),
          lt: nextDay.toJSDate(),
        },
      },
      orderBy: {
        createdAt: "asc", // Chronological order (oldest first)
      },
    });

    return entries;
  } catch (error) {
    console.error("Error fetching entries:", error);
    return [];
  }
}
