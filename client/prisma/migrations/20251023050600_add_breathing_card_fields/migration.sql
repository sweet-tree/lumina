-- AlterTable
ALTER TABLE "User" ADD COLUMN     "breathingCardCompletedAt" TIMESTAMP(3),
ADD COLUMN     "hasCompletedBreathingCard" BOOLEAN NOT NULL DEFAULT false;
