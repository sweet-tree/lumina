"use server";

import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { PrismaClient } from "@/generated/prisma";

const prisma = new PrismaClient();

export async function getBreathingCardStatus() {
  try {
    const session = await getServerSession(authOptions);

    if (!session?.user?.email) {
      throw new Error("Unauthorized");
    }

    // Get user's breathing card completion status
    const user = await prisma.user.findUnique({
      where: { email: session.user.email },
      select: {
        hasCompletedBreathingCard: true,
        breathingCardCompletedAt: true,
      },
    });

    if (!user) {
      throw new Error("User not found");
    }

    return {
      hasCompleted: user.hasCompletedBreathingCard,
      completedAt: user.breathingCardCompletedAt?.toISOString(),
    };
  } catch (error) {
    console.error("Error fetching breathing card status:", error);
    throw new Error("Failed to fetch breathing card status");
  }
}

export async function completeBreathingCard() {
  try {
    const session = await getServerSession(authOptions);

    if (!session?.user?.email) {
      throw new Error("Unauthorized");
    }

    // Update user's breathing card completion status
    const updatedUser = await prisma.user.update({
      where: { email: session.user.email },
      data: {
        hasCompletedBreathingCard: true,
        breathingCardCompletedAt: new Date(),
      },
      select: {
        hasCompletedBreathingCard: true,
        breathingCardCompletedAt: true,
      },
    });

    return {
      success: true,
      completedAt: updatedUser.breathingCardCompletedAt,
    };
  } catch (error) {
    console.error("Error completing breathing card:", error);
    throw new Error("Failed to complete breathing card");
  }
}
