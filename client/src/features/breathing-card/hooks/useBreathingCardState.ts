"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { completeBreathingCard } from "../actions/breathing-card-actions";

interface BreathingCardStatusResponse {
  hasCompleted: boolean;
  completedAt?: string;
}

interface UseBreathingCardStateReturn {
  isFirstTime: boolean;
  markBreathingComplete: () => Promise<{
    success: boolean;
    completedAt: Date | null;
  }>;
  isLoading: boolean;
  error: string | null;
}

// Query key for breathing card status
const BREATHING_CARD_QUERY_KEY = ["user", "breathing-card-status"];

// Server Action to fetch breathing card status
async function fetchBreathingCardStatus(): Promise<BreathingCardStatusResponse> {
  // We'll use the user's session to check their database status
  // For now, we'll create a simple server action to check this
  const { getBreathingCardStatus } = await import(
    "../actions/breathing-card-actions"
  );
  return await getBreathingCardStatus();
}

export function useBreathingCardState(): UseBreathingCardStateReturn {
  const queryClient = useQueryClient();

  // Query for breathing card status from database
  const {
    data,
    isLoading: queryLoading,
    error: queryError,
  } = useQuery({
    queryKey: BREATHING_CARD_QUERY_KEY,
    queryFn: fetchBreathingCardStatus,
    retry: 1,
    // Fallback to localStorage if database query fails
    placeholderData: () => {
      try {
        const stored = localStorage.getItem("lumina-user-state");
        if (stored) {
          const userState = JSON.parse(stored);
          return {
            hasCompleted: userState.hasCompletedBreathingCard || false,
            completedAt: userState.completedAt,
          };
        }
      } catch (err) {
        console.warn("localStorage fallback failed:", err);
      }
      return { hasCompleted: false };
    },
  });

  // Mutation for completing breathing card
  const completeMutation = useMutation({
    mutationFn: completeBreathingCard,
    onSuccess: (result) => {
      console.log("Breathing card marked as completed successfully");

      // Optimistically update the query cache
      queryClient.setQueryData(BREATHING_CARD_QUERY_KEY, {
        hasCompleted: true,
        completedAt: result.completedAt?.toISOString(),
      });

      // Update localStorage as backup
      try {
        const userState = {
          hasCompletedBreathingCard: true,
          completedAt:
            result.completedAt?.toISOString() || new Date().toISOString(),
        };
        localStorage.setItem("lumina-user-state", JSON.stringify(userState));
      } catch (err) {
        console.warn("Failed to update localStorage backup:", err);
      }
    },
    onError: (error) => {
      console.error("Failed to complete breathing card:", error);

      // Fallback to localStorage if Server Action fails
      try {
        const userState = {
          hasCompletedBreathingCard: true,
          completedAt: new Date().toISOString(),
        };
        localStorage.setItem("lumina-user-state", JSON.stringify(userState));

        // Update the cache with localStorage data
        queryClient.setQueryData(BREATHING_CARD_QUERY_KEY, {
          hasCompleted: true,
          completedAt: new Date().toISOString(),
        });

        console.log("Used localStorage fallback for breathing card completion");
      } catch (localStorageError) {
        console.error("localStorage fallback failed:", localStorageError);
      }
    },
  });

  return {
    isFirstTime: !data?.hasCompleted,
    markBreathingComplete: completeMutation.mutateAsync,
    isLoading: queryLoading || completeMutation.isPending,
    error: queryError?.message || completeMutation.error?.message || null,
  };
}
