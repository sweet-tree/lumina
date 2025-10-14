-- AlterTable
ALTER TABLE "DiaryEntry" ADD COLUMN     "entryDate" DATE NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- CreateIndex
CREATE INDEX "DiaryEntry_userId_entryDate_idx" ON "DiaryEntry"("userId", "entryDate");
