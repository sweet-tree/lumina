import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { PrismaClient } from "@/generated/prisma";

const prisma = new PrismaClient();

export async function GET() {
  try {
    // 1. Check authentication
    const session = await getServerSession(authOptions);
    if (!session) {
      return NextResponse.json(
        { error: "Unauthorized - please sign in" },
        { status: 401 }
      );
    }

    // 2. Fetch all cards from 'core' deck
    const cards = await prisma.card.findMany({
      where: { deck: "core" },
      orderBy: { order: "asc" },
    });

    if (cards.length === 0) {
      return NextResponse.json(
        { error: "No cards found in database" },
        { status: 404 }
      );
    }

    // 3. Select random card
    const randomIndex = Math.floor(Math.random() * cards.length);
    const randomCard = cards[randomIndex];

    return NextResponse.json(randomCard);
  } catch (error) {
    console.error("Error fetching random card:", error);
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    );
  }
}
