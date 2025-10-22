import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { PrismaClient } from "@/generated/prisma";

const prisma = new PrismaClient();

export async function POST(request: Request) {
  try {
    // 1. Check authentication
    const session = await getServerSession(authOptions);
    if (!session?.user?.email) {
      return NextResponse.json(
        { error: "Unauthorized - please sign in" },
        { status: 401 }
      );
    }

    // 2. Get user from database
    const user = await prisma.user.findUnique({
      where: { email: session.user.email },
    });

    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 });
    }

    // 3. Parse request body
    const { cardId, answer } = await request.json();

    if (!cardId || !answer || !answer.trim()) {
      return NextResponse.json(
        { error: "cardId and answer are required" },
        { status: 400 }
      );
    }

    // 4. Get card details for reflection prompt
    const card = await prisma.card.findUnique({
      where: { id: cardId },
    });

    if (!card) {
      return NextResponse.json({ error: "Card not found" }, { status: 404 });
    }

    // 5. Prepare AI prompt with context
    const aiPrompt = `${card.reflectionPrompt}

Card: ${card.title} (${card.type})
Guiding Prompt: ${card.guidingPrompt}

User's Response:
${answer}

Provide a brief, warm reflection (2-3 sentences). Be Socratic if the response is surface-level, or reflective if they went deep. Reference specifics from their answer.`;

    // 6. Call AI backend
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
      throw new Error(`AI service returned ${aiResponse.status}`);
    }

    const aiData = await aiResponse.json();

    if (!aiData.success || !aiData.response) {
      throw new Error("AI service did not return a valid response");
    }

    // 7. Save card session to database
    const cardSession = await prisma.cardSession.create({
      data: {
        userId: user.id,
        cardId: card.id,
        state: card.state,
        answer: answer.trim(),
        miniReflection: aiData.response,
      },
    });

    // 8. Return reflection
    return NextResponse.json({
      success: true,
      reflection: aiData.response,
      sessionId: cardSession.id,
      state: card.state,
    });
  } catch (error) {
    console.error("Error creating card session:", error);
    return NextResponse.json(
      {
        error: "Failed to process card session",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}
