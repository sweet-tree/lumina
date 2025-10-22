"use server";

import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { PrismaClient } from "@/generated/prisma";
import { revalidatePath } from "next/cache";

const prisma = new PrismaClient();

export async function drawRandomCard() {
  const session = await getServerSession(authOptions);
  if (!session) {
    throw new Error("Unauthorized");
  }

  const cards = await prisma.card.findMany({
    where: { deck: "core" },
    orderBy: { order: "asc" },
  });

  if (cards.length === 0) {
    throw new Error("No cards found");
  }

  const randomIndex = Math.floor(Math.random() * cards.length);
  return cards[randomIndex];
}

export async function submitCardSession(cardId: string, answer: string) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.email) {
    throw new Error("Unauthorized");
  }

  const user = await prisma.user.findUnique({
    where: { email: session.user.email },
  });

  if (!user) {
    throw new Error("User not found");
  }

  const card = await prisma.card.findUnique({
    where: { id: cardId },
  });

  if (!card) {
    throw new Error("Card not found");
  }

  // Call AI backend
  const aiPrompt = `${card.reflectionPrompt}

Card: ${card.title} (${card.type})
User's Response: ${answer}

CRITICAL: 2-3 sentences...`;

  const aiResponse = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: aiPrompt,
    }),
  });

  if (!aiResponse.ok) {
    throw new Error("AI service error");
  }

  const aiData = await aiResponse.json();

  if (!aiData.success || !aiData.response) {
    throw new Error("AI service did not return valid response");
  }

  // Save session
  const cardSession = await prisma.cardSession.create({
    data: {
      userId: user.id,
      cardId: card.id,
      state: card.state,
      answer: answer.trim(),
      miniReflection: aiData.response,
    },
  });

  revalidatePath("/dashboard/practice");

  return {
    success: true,
    reflection: aiData.response,
    sessionId: cardSession.id,
    state: card.state,
  };
}
