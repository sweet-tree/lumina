"""
Response Generation - Generates Lumina's response using teaching strategy and RAG

Combines teaching strategy, spiritual wisdom (RAG), and user input to generate
personalized Plant Teacher responses.
"""

import logging
from typing import Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential

from .chat_service import ChatService
from .vector_store_service import VectorStore

logger = logging.getLogger("lumina.response_generation")


class ResponseGenerator:
    """
    Response Generator creates Lumina's final response.

    Uses:
    - Teaching strategy (question, reflect, teach, challenge)
    - RAG retrieval (spiritual wisdom)
    - User input and extraction
    """

    def __init__(self):
        """Initialize Response Generator"""
        self.chat_service = ChatService()
        self.vector_store = VectorStore()

    def generate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Lumina's response using teaching strategy and RAG.

        Args:
            state: MultiAgentState with all agent outputs

        Returns:
            Updated state with rag_contexts and final_response
        """
        user_input = state.get("user_input", "")
        teaching_strategy = state.get("teaching_strategy", {})
        user_model = state.get("user_model", {})
        extraction = state.get("extraction", {})

        strategy = teaching_strategy.get("strategy", "reflect")
        guidance = teaching_strategy.get("guidance", "")

        logger.info(f"Generating response | Strategy: {strategy}")

        # Retrieve spiritual wisdom via RAG
        rag_contexts = self._retrieve_wisdom(user_input, strategy)

        # Build prompt based on strategy
        prompt = self._build_prompt(
            strategy=strategy,
            guidance=guidance,
            user_input=user_input,
            rag_contexts=rag_contexts,
            user_model=user_model,
            extraction=extraction
        )

        # Generate response with retry logic
        try:
            response = self._generate_with_retry(prompt, strategy)
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            response = self._get_fallback_response(strategy)

        logger.info(f"Response generated | Length: {len(response)} chars")

        return {
            "rag_contexts": rag_contexts,
            "final_response": response
        }

    def _retrieve_wisdom(self, user_input: str, strategy: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant spiritual wisdom via RAG.

        Args:
            user_input: User's check-in text
            strategy: Teaching strategy

        Returns:
            List of RAG context dicts with text and score
        """
        try:
            # Search spiritual library
            results = self.vector_store.search(
                query=user_input,
                top_k=10,  # Get more candidates for reranking
                namespace="spiritual-library"
            )

            logger.info(f"Retrieved {len(results)} RAG contexts")
            return results

        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")
            return []

    def _build_prompt(self, strategy: str, guidance: str, user_input: str,
                      rag_contexts: List[Dict[str, Any]], user_model: Dict[str, Any],
                      extraction: Dict[str, Any]) -> str:
        """
        Build prompt based on teaching strategy.

        Args:
            strategy: Teaching strategy (question, reflect, teach, challenge)
            guidance: Guidance text from Teaching Agent
            user_input: User's check-in text
            rag_contexts: Retrieved spiritual wisdom
            user_model: User model from Deep Agent
            extraction: Extraction from Extraction Agent

        Returns:
            Prompt string for LLM
        """
        # Format RAG contexts
        wisdom_text = self._format_rag_contexts(rag_contexts)

        # Base system prompt (Plant Teacher voice)
        system_prompt = """You are Lumina, a Plant Teacher guide for consciousness practice.

Your voice is:
- Direct, not comforting
- Mystical, not clinical
- Provocative, not validating
- Poetic, not therapeutic

You speak in short, powerful phrases. You point toward what the user cannot see from inside their experience."""

        if strategy == "question":
            prompt = f"""{system_prompt}

User said: "{user_input}"

Guidance: {guidance}

Respond with a provocative question that guides them toward body awareness.
Keep it 1-2 sentences. Direct, not comforting.

Examples:
- "Where in your body is the stress?"
- "What sensation is beneath the label?"
- "The body knows. Are you listening?"

Response:"""

        elif strategy == "reflect":
            prompt = f"""{system_prompt}

User said: "{user_input}"

Spiritual wisdom:
{wisdom_text}

Respond with a reflection that mirrors their awareness and offers wisdom.
2-3 sentences. Mystical, direct. Use the spiritual wisdom to deepen their insight.

Examples:
- "The breath knows what the mind refuses to see."
- "Tension is the body's NO. What is it saying no to?"
- "You're bracing against what hasn't happened yet."

Response:"""

        elif strategy == "teach":
            patterns = user_model.get("patterns", {})
            loops = patterns.get("loops", [])

            if loops:
                loop = loops[0]
                pattern_name = loop.get("name", "pattern")
                sequence = loop.get("sequence", [])

                prompt = f"""{system_prompt}

User said: "{user_input}"

Detected pattern: {pattern_name}
Sequence: {' → '.join(sequence)}

Spiritual wisdom:
{wisdom_text}

Respond by revealing the pattern and its teaching. Show them what they cannot see.
2-3 sentences. Use the spiritual wisdom to illuminate the pattern.

Example:
- "This is the third time tension led to depletion. Notice the pattern?"

Response:"""
            else:
                # Fallback to reflect if no pattern
                prompt = f"""{system_prompt}

User said: "{user_input}"

Spiritual wisdom:
{wisdom_text}

Respond with a reflection that mirrors their awareness.
2-3 sentences. Mystical, direct.

Response:"""

        elif strategy == "challenge":
            prompt = f"""{system_prompt}

User said: "{user_input}"

Context: User was deeper in previous check-ins, now regressing to labels.

Respond by pointing out the regression, not harshly but directly.
1-2 sentences. Challenge them to return to feeling.

Examples:
- "You were with the sensations. Now you're back in labels. What happened?"
- "The body was speaking. Why did you stop listening?"

Response:"""

        else:
            # Default to reflect
            prompt = f"""{system_prompt}

User said: "{user_input}"

Spiritual wisdom:
{wisdom_text}

Respond with a reflection that mirrors their awareness.
2-3 sentences. Mystical, direct.

Response:"""

        return prompt

    def _format_rag_contexts(self, contexts: List[Dict[str, Any]]) -> str:
        """
        Format RAG contexts for prompt.

        Args:
            contexts: List of context dicts with text and score

        Returns:
            Formatted string
        """
        if not contexts:
            return "(No spiritual wisdom retrieved)"

        formatted = []
        for i, ctx in enumerate(contexts[:3], 1):  # Use top 3
            text = ctx.get("text", "")
            formatted.append(f"{i}. {text}")

        return "\n".join(formatted)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def _generate_with_retry(self, prompt: str, strategy: str) -> str:
        """
        Generate response with retry logic.

        Args:
            prompt: Prompt for LLM
            strategy: Teaching strategy

        Returns:
            Generated response
        """
        # Adjust temperature based on strategy
        temperature = 0.8 if strategy == "reflect" else 0.7

        response = self.chat_service.generate(
            prompt=prompt,
            max_tokens=150,
            temperature=temperature
        )

        return response.strip()

    def _get_fallback_response(self, strategy: str) -> str:
        """
        Get fallback response if generation fails.

        Args:
            strategy: Teaching strategy

        Returns:
            Fallback response string
        """
        fallbacks = {
            "question": "What's here right now?",
            "reflect": "Stay with what's present.",
            "teach": "Notice the pattern.",
            "challenge": "Return to the body."
        }

        return fallbacks.get(strategy, "What's here right now?")


def response_generation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function for Response Generation.

    Args:
        state: MultiAgentState with all agent outputs

    Returns:
        Updated state with rag_contexts and final_response
    """
    import time
    start_time = time.time()

    logger.info("Response Generation | Starting")

    # Create generator and generate response
    generator = ResponseGenerator()
    result = generator.generate(state)

    elapsed = time.time() - start_time
    logger.info(f"Response Generation | Complete | Time: {elapsed:.2f}s")

    return result
