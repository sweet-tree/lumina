"""
Card Agent - Decides card awards based on depth, commitment, and breakthroughs

The Card Agent analyzes user performance to decide if a card should be awarded,
which card to give, and what rarity it should be.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("lumina.card_agent")


class CardAgent:
    """
    Card Agent decides card awards.

    Award criteria:
    - Deep reflection (specificity > baseline + 2)
    - Multiple check-ins today (3+)
    - Pattern detected for first time (rare)
    - Loop broken via doorway (rare)
    - No card for shallow first attempt
    """

    def __init__(self):
        """Initialize Card Agent"""
        pass

    def decide_award(self, user_model: Dict[str, Any], relative_depth: str,
                     extraction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide if card should be awarded and which card.

        Args:
            user_model: User's memory and patterns from Deep Agent
            relative_depth: "shallow" | "medium" | "deep"
            extraction: Extracted signals from Extraction Agent

        Returns:
            {
                "award_card": bool,
                "card_id": str | None,
                "rarity": "common" | "rare" | "epic" | "legendary",
                "reason": str
            }
        """
        patterns = user_model.get("patterns", {})
        trajectory = user_model.get("trajectory", {})

        # Priority 1: Loop broken (rare card)
        if self._check_loop_broken(user_model):
            return {
                "award_card": True,
                "card_id": "doorway_accessed",
                "rarity": "rare",
                "reason": "User broke loop by accessing doorway"
            }

        # Priority 2: New pattern detected (rare card)
        if self._check_new_pattern_detected(patterns):
            loop = patterns["loops"][0]
            return {
                "award_card": True,
                "card_id": self._pattern_to_card_id(loop),
                "rarity": "rare",
                "reason": f"New pattern detected: {loop.get('name', 'pattern')}"
            }

        # Priority 3: Deep reflection (common card)
        if relative_depth == "deep":
            card_id = self._select_card_from_signals(extraction)
            return {
                "award_card": True,
                "card_id": card_id,
                "rarity": "common",
                "reason": "Deep reflection, specificity above baseline"
            }

        # Priority 4: Multiple check-ins today (common card)
        checkins_today = self._get_checkins_today(user_model)
        if checkins_today >= 3:
            return {
                "award_card": True,
                "card_id": "commitment",
                "rarity": "common",
                "reason": f"{checkins_today} check-ins today, showing commitment"
            }

        # Priority 5: Shallow first attempt - no card (guide deeper)
        if relative_depth == "shallow" and self._is_first_checkin_today(user_model):
            return {
                "award_card": False,
                "card_id": None,
                "rarity": "common",
                "reason": "Shallow check-in, first attempt of day - guide deeper"
            }

        # Default: No card for medium depth or shallow non-first attempts
        return {
            "award_card": False,
            "card_id": None,
            "rarity": "common",
            "reason": f"No card criteria met (depth: {relative_depth})"
        }

    def _check_loop_broken(self, user_model: Dict[str, Any]) -> bool:
        """
        Check if user broke a loop by accessing a doorway.

        Args:
            user_model: User model with patterns

        Returns:
            bool: True if loop was broken
        """
        patterns = user_model.get("patterns", {})
        doorways = patterns.get("doorways", [])

        # Check if any doorway was recently accessed
        # For now, simplified: check if doorways exist and user was in loop
        was_in_loop = user_model.get("in_loop", False)
        has_doorways = len(doorways) > 0

        # If user was in loop and has doorways, they may have broken it
        # More sophisticated: track if doorway was just accessed
        return False  # Simplified for MVP - will enhance later

    def _check_new_pattern_detected(self, patterns: Dict[str, Any]) -> bool:
        """
        Check if a pattern was detected for the first time.

        Args:
            patterns: User patterns from Deep Agent

        Returns:
            bool: True if new pattern detected (frequency == 3)
        """
        loops = patterns.get("loops", [])

        if loops:
            # Check if most recent loop has frequency of exactly 3 (first detection)
            loop = loops[0]
            if loop.get("frequency", 0) == 3:
                return True

        return False

    def _get_checkins_today(self, user_model: Dict[str, Any]) -> int:
        """
        Get number of check-ins completed today.

        Args:
            user_model: User model with baseline data

        Returns:
            int: Number of check-ins today
        """
        # For MVP, simplified: return 1 (current check-in)
        # TODO: Track check-ins per day in Store
        return 1

    def _is_first_checkin_today(self, user_model: Dict[str, Any]) -> bool:
        """
        Check if this is the first check-in today.

        Args:
            user_model: User model

        Returns:
            bool: True if first check-in today
        """
        # For MVP, simplified: assume it's first check-in
        # TODO: Track check-ins per day in Store
        return True

    def _select_card_from_signals(self, extraction: Dict[str, Any]) -> str:
        """
        Select card based on extracted body signals.

        Args:
            extraction: Extraction output with body_signals

        Returns:
            str: Card ID
        """
        body_signals = extraction.get("body_signals", [])

        if not body_signals:
            return "awareness"

        # Map body locations to cards
        # Extract location from "location: sensation" format
        locations = []
        for signal in body_signals:
            if ":" in signal:
                location = signal.split(":")[0].strip().lower()
                locations.append(location)

        # Simple mapping (can be enhanced with card library)
        card_mapping = {
            "chest": "heart_opening",
            "shoulders": "burden_release",
            "jaw": "tension_awareness",
            "stomach": "gut_knowing",
            "breath": "breath_awareness",
            "throat": "voice_truth",
            "head": "mind_clarity",
            "back": "support_strength"
        }

        # Return card for first recognized location
        for location in locations:
            if location in card_mapping:
                return card_mapping[location]

        # Default card
        return "presence"

    def _pattern_to_card_id(self, loop: Dict[str, Any]) -> str:
        """
        Convert pattern to card ID.

        Args:
            loop: Loop pattern dict

        Returns:
            str: Card ID for the pattern
        """
        name = loop.get("name", "pattern")

        # Convert pattern name to card ID (snake_case)
        card_id = name.lower().replace(" ", "_")

        return card_id


def card_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function for Card Agent.

    Args:
        state: MultiAgentState with user_model, relative_depth, extraction

    Returns:
        Updated state with card_decision
    """
    import time
    start_time = time.time()

    user_model = state.get("user_model", {})
    relative_depth = state.get("relative_depth", "medium")
    extraction = state.get("extraction", {})

    logger.info(f"Card Agent | Depth: {relative_depth}")

    # Create agent and decide award
    agent = CardAgent()
    decision = agent.decide_award(user_model, relative_depth, extraction)

    elapsed = time.time() - start_time
    logger.info(
        f"Card Agent | Award: {decision['award_card']} | Card: {decision.get('card_id')} | Rarity: {decision['rarity']} | Time: {elapsed:.2f}s")

    return {"card_decision": decision}
