"""
Teaching Agent - Decides pedagogical strategy based on user trajectory

The Teaching Agent analyzes the user's trajectory and patterns to decide
how Lumina should respond: reflect, question, teach, or challenge.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger("lumina.teaching_agent")


class TeachingAgent:
    """
    Teaching Agent decides pedagogical strategy.

    Strategies:
    - question: Guide deeper when stuck shallow
    - challenge: Point out regression
    - teach: Explain detected pattern
    - reflect: Mirror awareness (default)
    """

    def __init__(self):
        """Initialize Teaching Agent"""
        pass

    def decide_strategy(self, user_model: Dict[str, Any], relative_depth: str,
                        extraction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide teaching strategy based on user trajectory.

        Args:
            user_model: User's memory and patterns from Deep Agent
            relative_depth: "shallow" | "medium" | "deep"
            extraction: Extracted signals from Extraction Agent

        Returns:
            {
                "strategy": "question" | "reflect" | "teach" | "challenge",
                "guidance": str,  # Guidance for response generation
                "reason": str     # Why this strategy was chosen
            }
        """
        trajectory = user_model.get("trajectory", {})
        in_loop = user_model.get("in_loop", False)
        patterns = user_model.get("patterns", {})

        # Priority 1: Stuck shallow for 5+ check-ins
        stuck_shallow_count = trajectory.get("stuck_shallow_count", 0)
        if stuck_shallow_count >= 5:
            return {
                "strategy": "question",
                "guidance": "Ask about body location or sensation to guide deeper",
                "reason": f"User stuck at shallow for {stuck_shallow_count} check-ins"
            }

        # Priority 2: Regressing from previous depth
        if trajectory.get("regressing", False):
            return {
                "strategy": "challenge",
                "guidance": "Point out they were deeper before, challenge them to return to feeling",
                "reason": "User regressing from previous depth level"
            }

        # Priority 3: In a detected loop
        if in_loop and patterns.get("loops"):
            loop = patterns["loops"][0]  # Get most recent loop
            return {
                "strategy": "teach",
                "guidance": f"Explain the detected pattern: {loop.get('name', 'recurring pattern')}",
                "reason": f"User in detected loop: {loop.get('name', 'pattern')}"
            }

        # Priority 4: Pattern detected (but not in loop currently)
        if patterns.get("loops") and len(patterns["loops"]) > 0:
            # Check if pattern was recently detected
            loop = patterns["loops"][0]
            if loop.get("frequency", 0) == 3:  # First time detected (exactly 3 occurrences)
                return {
                    "strategy": "teach",
                    "guidance": f"Gently reveal the pattern: {loop.get('name', 'pattern')}",
                    "reason": f"New pattern detected: {loop.get('name', 'pattern')}"
                }

        # Default: Reflect their awareness
        return {
            "strategy": "reflect",
            "guidance": "Mirror their awareness and offer wisdom",
            "reason": "User progressing well, reflect their depth"
        }


def teaching_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function for Teaching Agent.

    Args:
        state: MultiAgentState with user_model, relative_depth, extraction

    Returns:
        Updated state with teaching_strategy
    """
    import time
    start_time = time.time()

    user_model = state.get("user_model", {})
    relative_depth = state.get("relative_depth", "medium")
    extraction = state.get("extraction", {})

    logger.info(
        f"Teaching Agent | Depth: {relative_depth} | In loop: {user_model.get('in_loop', False)}")

    # Create agent and decide strategy
    agent = TeachingAgent()
    strategy = agent.decide_strategy(user_model, relative_depth, extraction)

    elapsed = time.time() - start_time
    logger.info(
        f"Teaching Agent | Strategy: {strategy['strategy']} | Reason: {strategy['reason']} | Time: {elapsed:.2f}s")

    return {"teaching_strategy": strategy}
