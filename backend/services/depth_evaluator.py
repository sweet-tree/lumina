"""
Depth Evaluator Agent for Lumina check-in classification.

This agent evaluates the depth of user check-in input and classifies it as:
- shallow: Generic labels, <5 words, no body awareness
- medium: Body sensations mentioned but no specific context
- deep: Body sensations + breath awareness + specific situational context
"""

import logging
from typing import Literal
from backend.services.chat_service import ChatService
from backend.services.langgraph_service import LuminaState

logger = logging.getLogger("lumina.langgraph")


# System prompt defining depth classification criteria
DEPTH_CLASSIFICATION_PROMPT = """You are a depth evaluator for consciousness practice check-ins.

Classify the user's input into exactly one category:

SHALLOW: Generic emotional labels, <5 words, no body awareness
Examples: "I'm ok", "tired", "stressed", "fine", "anxious"

MEDIUM: Body sensations mentioned but no specific context
Examples: "shoulders tight", "chest heavy", "jaw clenched", "belly soft"

DEEP: Body sensations + breath awareness + specific situational context
Examples: "chest tight, breath shallow, meeting in 30 minutes", "belly soft, breath deep, just finished walk"

User input: {user_input}

Respond with only one word: shallow, medium, or deep"""


def evaluate_depth(state: LuminaState) -> dict:
    """
    Evaluates the depth of user input using LLM classification.

    This function classifies check-in input as shallow, medium, or deep
    based on the presence of body awareness, breath awareness, and context.

    Args:
        state: Current workflow state with user_input

    Returns:
        Dict with depth_level key containing classification result

    Logs:
        - INFO: Input text (truncated) and classification result
        - WARNING: Invalid depth value from LLM (defaults to "medium")
    """
    import time
    start_time = time.time()

    user_input = state["user_input"]
    logger.info(f"Node: evaluate_depth | Input: {user_input[:50]}...")

    # Initialize ChatService
    chat_service = ChatService()

    # Build prompt with user input
    prompt = DEPTH_CLASSIFICATION_PROMPT.format(user_input=user_input)

    # Call LLM with low temperature for consistent classification
    try:
        response = chat_service.generate(
            prompt=prompt,
            max_tokens=10,  # Only need one word
            temperature=0.3  # Low temperature for consistency
        )

        # Parse and validate response
        depth = response.strip().lower()

        # Validate depth value
        if depth not in ["shallow", "medium", "deep"]:
            logger.warning(
                f"Node: evaluate_depth | Invalid depth '{depth}' from LLM, defaulting to 'medium'"
            )
            depth = "medium"

        elapsed = time.time() - start_time
        logger.info(
            f"Node: evaluate_depth | Depth: {depth} | Time: {elapsed:.2f}s")

        return {"depth_level": depth}

    except Exception as e:
        logger.error(f"Node: evaluate_depth | Error: {e}")
        # Default to medium on error
        logger.warning(
            "Node: evaluate_depth | Defaulting to 'medium' due to error")
        return {"depth_level": "medium"}
