-- CreateTable
CREATE TABLE "Card" (
    "id" TEXT NOT NULL,
    "type" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "guidingPrompt" TEXT NOT NULL,
    "questions" JSONB NOT NULL,
    "reflectionPrompt" TEXT NOT NULL,
    "icon" TEXT NOT NULL,
    "color" TEXT NOT NULL,
    "deck" TEXT NOT NULL DEFAULT 'core',
    "order" INTEGER NOT NULL,
    "ascendingStates" TEXT[],
    "descendingStates" TEXT[],
    "breaksPatternOf" TEXT[],
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Card_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "CardSession" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "cardId" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "answer" TEXT NOT NULL,
    "miniReflection" TEXT,

    CONSTRAINT "CardSession_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "DailySynthesis" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "date" DATE NOT NULL,
    "cardSessionIds" TEXT[],
    "synthesis" TEXT NOT NULL,
    "journeyPattern" TEXT,
    "stateTransitions" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "DailySynthesis_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Card_deck_idx" ON "Card"("deck");

-- CreateIndex
CREATE INDEX "Card_state_idx" ON "Card"("state");

-- CreateIndex
CREATE INDEX "CardSession_userId_timestamp_idx" ON "CardSession"("userId", "timestamp");

-- CreateIndex
CREATE INDEX "CardSession_userId_state_idx" ON "CardSession"("userId", "state");

-- CreateIndex
CREATE INDEX "DailySynthesis_userId_date_idx" ON "DailySynthesis"("userId", "date");

-- CreateIndex
CREATE UNIQUE INDEX "DailySynthesis_userId_date_key" ON "DailySynthesis"("userId", "date");

-- AddForeignKey
ALTER TABLE "CardSession" ADD CONSTRAINT "CardSession_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CardSession" ADD CONSTRAINT "CardSession_cardId_fkey" FOREIGN KEY ("cardId") REFERENCES "Card"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
