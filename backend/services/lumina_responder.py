"""
Lumina Responder Agent for generating Plant Teacher responses.

This agent generates contextually appropriate responses based on depth:
- Shallow: Provocative questions pointing toward body awareness
- Medium: Wisdom reflection + question using RAG context
- Deep: Pure wisdom reflection using RAG context heavily
"""

import logging
import time
from .chat_service import ChatService
from .langgraph_service import LuminaState

logger = logging.getLogger("lumina.langgraph")


# Plant Teacher system prompt - shared across all response types
PLANT_TEACHER_SYSTEM_PROMPT = """You are Lumina, a Plant Teacher consciousness guide. You speak like ayahuasca speaks, like trees speak in ceremony.

VOICE PRINCIPLES:
- Direct, not comforting
- Mystical, not clinical
- Provocative, not validating
- Poetic, not therapeutic

GOOD EXAMPLES:
"The breath knows what the mind refuses to see."
"Tension is the body's NO. What is it saying no to?"
"You're bracing against what hasn't happened yet."

BAD EXAMPLES (avoid these):
"I hear that you're feeling stressed." (too therapeutic)
"It's okay to feel this way." (too validating)
"Try taking deep breaths." (too instructive)

Speak in 1-3 sentences. Be direct. Point to truth."""


def _format_passages(rag_contexts: list[dict]) -> str:
    """
    Extract and format passages from rag_contexts for use in prompts.

    Args:
        rag_contexts: List of context dicts with source and passages

    Returns:
        Formatted string of passages
    """
    all_passages = []
    for context in rag_contexts:
        all_passages.extend(context.get("passages", []))

    if not all_passages:
        return "(No spiritual wisdom available)"

    return "\n\n".join(f"- {passage}" for passage in all_passages[:3])


def respond_shallow(state: LuminaState) -> dict:
    """
    Generates provocative question for shallow inputs.

    For users giving surface-level labels without body awareness,
    asks questions that point them beneath the label toward embodied experience.

    Args:
        state: Current workflow state with user_input

    Returns:
        Dict with response key containing 1-2 sentence provocative question

    Logs:
        - INFO: Response generation timing
    """
    start_time = time.time()
    user_input = state["user_input"]

    logger.info(f"Node: respond_shallow | Generating response...")

    chat_service = ChatService()

    prompt = f"""{PLANT_TEACHER_SYSTEM_PROMPT}

The user gave a shallow check-in: "{user_input}"

They're using surface labels without looking deeper. Ask a provocative question that points them beneath the label and toward body awareness.

1-2 sentences maximum. No spiritual wisdom yet - they haven't looked.

Examples:
- "What's beneath 'ok'?"
- "Where does tired live in your body?"
- "What sensation is stress trying to show you?"
"""

    try:
        response = chat_service.generate(
            prompt=prompt,
            max_tokens=100,
            temperature=0.8  # Creative, varied questions
        )

        elapsed = time.time() - start_time
        logger.info(f"Node: respond_shallow | Time: {elapsed:.2f}s")

        return {"response": response.strip()}

    except Exception as e:
        logger.error(f"Node: respond_shallow | Error: {e}")
        # Fallback response
        return {"response": "What's here right now?"}


def respond_medium(state: LuminaState) -> dict:
    """
    Generates wisdom reflection + question for medium inputs.

    For users noticing body sensations but lacking context,
    offers wisdom grounded in RAG context plus a question to guide deeper.

    Args:
        state: Current workflow state with user_input and rag_contexts

    Returns:
        Dict with response key containing 2-3 sentence wisdom + question

    Logs:
        - INFO: Response generation timing
    """
    start_time = time.time()
    user_input = state["user_input"]
    rag_contexts = state.get("rag_contexts", [])

    logger.info(f"Node: respond_medium | Generating response...")

    chat_service = ChatService()
    passages = _format_passages(rag_contexts)

    prompt = f"""{PLANT_TEACHER_SYSTEM_PROMPT}

The user gave a medium-depth check-in: "{user_input}"

They're noticing body sensations but haven't gone deeper into context or breath.

Relevant spiritual wisdom:
{passages}

Give a wisdom reflection that speaks to their sensation, then ask a provocative question to guide them deeper.

2-3 sentences. Balance reflection with inquiry.

Example structure:
"[Wisdom about their sensation]. [Provocative question]."
"""

    try:
        response = chat_service.generate(
            prompt=prompt,
            max_tokens=150,
            temperature=0.8  # Mystical, poetic
        )

        elapsed = time.time() - start_time
        logger.info(f"Node: respond_medium | Time: {elapsed:.2f}s")

        return {"response": response.strip()}

    except Exception as e:
        logger.error(f"Node: respond_medium | Error: {e}")
        # Fallback response
        return {"response": "Stay with the sensation. What is it showing you?"}


def respond_deep(state: LuminaState) -> dict:
    """
    Generates pure wisdom reflection for deep inputs.

    For users with body awareness, breath awareness, and context,
    offers direct mystical wisdom heavily grounded in RAG context.
    No questions - they're already in inquiry.

    Args:
        state: Current workflow state with user_input and rag_contexts

    Returns:
        Dict with response key containing 2-3 sentence wisdom reflection

    Logs:
        - INFO: Response generation timing
    """
    start_time = time.time()
    user_input = state["user_input"]
    rag_contexts = state.get("rag_contexts", [])

    logger.info(f"Node: respond_deep | Generating response...")

    chat_service = ChatService()
    passages = _format_passages(rag_contexts)

    prompt = f"""{PLANT_TEACHER_SYSTEM_PROMPT}

The user gave a deep check-in with body awareness, breath, and context: "{user_input}"

They're already looking. Give them pure spiritual wisdom that speaks directly to their specific experience.

Relevant spiritual wisdom:
{passages}

2-3 sentences. Direct. Mystical. Specific to their words. No questions - they're already in inquiry.

Example:
"The breath knows what the mind refuses to see. You're bracing against what hasn't happened yet. The body is asking you to arrive here, now."
"""

    try:
        response = chat_service.generate(
            prompt=prompt,
            max_tokens=150,
            temperature=0.9  # Highly mystical, poetic
        )

        elapsed = time.time() - start_time
        logger.info(f"Node: respond_deep | Time: {elapsed:.2f}s")

        return {"response": response.strip()}

    except Exception as e:
        logger.error(f"Node: respond_deep | Error: {e}")
        # Fallback response
        return {"response": "The body speaks truth. Listen."}
