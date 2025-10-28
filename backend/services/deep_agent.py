"""
Deep Agent

Maintains user memory, detects patterns, and evaluates relative depth.
Uses PostgresStore for long-term memory and personalizes depth evaluation
based on user's baseline.
"""

import logging
from typing import Dict
from langgraph.store.base import BaseStore

from .user_memory import (
    get_user_baseline,
    update_user_baseline,
    get_user_patterns,
    update_body_patterns,
    update_triggers,
    get_body_patterns,
    get_triggers
)

logger = logging.getLogger("lumina.deep_agent")


class DeepAgent:
    """Agent for user memory, pattern detection, and relative depth evaluation"""

    def __init__(self, store: BaseStore):
        """
        Initialize Deep Agent.

        Args:
            store: LangGraph Store instance for user memory
        """
        self.store = store

    def evaluate(self, user_id: str, extraction: Dict) -> Dict:
        """
        Evaluate depth relative to user's baseline and update memory.

        Args:
            user_id: User identifier
            extraction: Extraction agent output {body_signals, triggers, temporal, specificity_score}

        Returns:
            dict: {user_model, relative_depth}
        """
        logger.info(f"Evaluating depth for user {user_id}")

        # Load user baseline
        baseline = get_user_baseline(self.store, user_id)
        current_specificity = extraction['specificity_score']

        logger.info(
            f"User baseline: {baseline:.2f}, Current: {current_specificity}")

        # Calculate relative depth
        relative_depth = self._calculate_relative_depth(
            current_specificity, baseline)

        # Load user patterns and history
        patterns = get_user_patterns(self.store, user_id)
        body_patterns = get_body_patterns(self.store, user_id)
        triggers = get_triggers(self.store, user_id)

        # Calculate trajectory
        trajectory = self._calculate_trajectory(
            user_id, current_specificity, baseline)

        # Build user model
        user_model = {
            "baseline": baseline,
            "patterns": patterns,
            "body_patterns": body_patterns,
            "triggers": triggers,
            "trajectory": trajectory,
            "in_loop": trajectory.get("stuck_shallow_count", 0) >= 3
        }

        # Update memory (done after evaluation to include current check-in)
        self._update_memory(user_id, extraction)

        logger.info(
            f"Depth evaluation: {relative_depth} (baseline: {baseline:.2f})")

        return {
            "user_model": user_model,
            "relative_depth": relative_depth
        }

    def _calculate_relative_depth(self, current_specificity: float, baseline: float) -> str:
        """
        Calculate depth relative to user's baseline.

        Args:
            current_specificity: Current specificity score
            baseline: User's baseline specificity

        Returns:
            str: "shallow" | "medium" | "deep"
        """
        # Depth is relative to user's baseline
        if current_specificity > baseline + 2:
            return "deep"
        elif current_specificity < baseline - 2:
            return "shallow"
        else:
            return "medium"

    def _calculate_trajectory(self, user_id: str, current_specificity: float, baseline: float) -> Dict:
        """
        Calculate user's trajectory (stuck, progressing, regressing).

        Args:
            user_id: User identifier
            current_specificity: Current specificity score
            baseline: User's baseline

        Returns:
            dict: Trajectory information with stuck_shallow_count, regressing, progressing
        """
        from .user_memory import get_recent_scores

        # Get recent check-in scores to detect trends
        recent_scores = get_recent_scores(self.store, user_id, limit=5)

        trajectory = {
            "stuck_shallow_count": 0,
            "regressing": False,
            "progressing": False
        }

        # Calculate stuck_shallow_count: consecutive shallow check-ins
        if recent_scores:
            stuck_count = 0
            for score in reversed(recent_scores):  # Most recent first
                if score < baseline - 2:  # Shallow relative to baseline
                    stuck_count += 1
                else:
                    break  # Stop at first non-shallow
            trajectory["stuck_shallow_count"] = stuck_count
        else:
            # First check-in or no history
            if current_specificity < baseline - 2:
                trajectory["stuck_shallow_count"] = 1

        # Detect regression: current is lower than average of previous 3
        if len(recent_scores) >= 3:
            previous_avg = sum(recent_scores[-3:]) / 3
            if current_specificity < previous_avg - 1.5:
                trajectory["regressing"] = True

        # Detect progression: current is higher than baseline by significant margin
        if current_specificity > baseline + 3:
            trajectory["progressing"] = True

        logger.info(
            f"Trajectory: stuck={trajectory['stuck_shallow_count']}, regressing={trajectory['regressing']}, progressing={trajectory['progressing']}")

        return trajectory

    def _update_memory(self, user_id: str, extraction: Dict) -> None:
        """
        Update user memory with current check-in data.

        Args:
            user_id: User identifier
            extraction: Extraction output
        """
        # Update baseline with rolling average
        update_user_baseline(self.store, user_id,
                             extraction['specificity_score'])

        # Update body patterns
        if extraction['body_signals']:
            update_body_patterns(self.store, user_id,
                                 extraction['body_signals'])

        # Update triggers
        if extraction['triggers']:
            update_triggers(self.store, user_id, extraction['triggers'])

        logger.info(f"Updated memory for user {user_id}")


# Node function for LangGraph
def deep_agent_node(state: Dict, *, store: BaseStore) -> Dict:
    """
    LangGraph node function for Deep Agent.

    Args:
        state: MultiAgentState dict
        store: LangGraph Store (injected by LangGraph)

    Returns:
        dict: Updated state with user_model and relative_depth
    """
    agent = DeepAgent(store)
    result = agent.evaluate(state["user_id"], state["extraction"])

    return result
