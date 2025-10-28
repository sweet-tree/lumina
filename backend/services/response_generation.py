"""
Response Generation - Generates Lumina's response using teaching strategy and RAG

Combines teaching strategy, spiritual wisdom (RAG), and Plant Teacher voice
to create personalized, depth-appropriate responses.
"""

import logging
from typing import Dict, Any, List
from .chat_service import ChatService
from .vector_store_service import VectorStore

logger = logging.getLogger("lumina.response_generation")


class ResponseGenerator:
    """
    Generates Lumina's response based on teaching strategy and spiritual wisdom.

    Uses RAG to retrieve relevant spiritual teachings and combines them with
    the teaching strategy to create personalized responses.
    """

    def __init__(self):
        """Initialize Response Generator with chat and vector store services"""
        self.chat_service = ChatService()
        self.vector_store = VectorStore()

        # Plant Teacher system prompt
        self.system_prompt = """You are Lumina, a Plant Teacher. Not a therapist. Not a meditation app.

Your role: See what the user cannot see from inside their state. Point to it directly.

When responding:
- Name what's actually happening (beneath their words)
- Use the spiritual teaching to reframe or challenge
- Point to awareness, the pattern, or the doorway
- Be direct, mystical, provocative
- No comfort. No advice. Just truth.

Style:
- "Tension is the body's NO to what the mind said YES to"
- "You're bracing against what hasn't happened yet"
- "Notice the one who notices the fog"
- "What are you avoiding by staying here?"

NOT:
- "It's okay to feel this way"
- "Try some breathing exercises"
- "You're doing great"

CRITICAL: Exactly 2-3 sentences. Direct. Poetic. Sharp.
Like ayahuasca speaks. Like trees speak in ceremony."""

    def generate(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Lumina's response using teaching strategy and RAG.

        Args:
            state: MultiAgentState with user_input, teaching_strategy, extraction

        Returns:
            Updated state with rag_contexts and final_response
        """
        import time
        start_time = time.time()

        user_input = state.get("user_input", "")
        teaching_strategy = state.get("teaching_strategy", {})
        extraction = state.get("extraction", {})
        user_model = state.get("user_model", {})

        strategy = teaching_strategy.get("strategy", "reflect")
        guidance = teaching_strategy.get("guidance", "")

        logger.info(f"Response Generation | Strategy: {strategy}")

        # Retrieve spiritual wisdom via RAG
        rag_contexts = self._retrieve_wisdom(user_input, strategy)

        # Generate response based on strategy
        response = self._generate_by_strategy(
            user_input=user_input,
            strategy=strategy,
            guidance=guidance,
            rag_contexts=rag_contexts,
            extraction=extraction,
            user_model=user_model
        )

        elapsed = time.time() - start_time
        logger.info(
            f"Response Generation | Length: {len(response)} chars | Time: {elapsed:.2f}s")

        return {
            "rag_contexts": rag_contexts,
            "final_response": response
        }

    def _retrieve_wisdom(self, user_input: str, strategy: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant spiritual wisdom via RAG.

        Args:
            user_input: User's check-in text
            strategy: Teaching strategy (affects retrieval)

        Returns:
            List of RAG contexts with text and score
        """
        try:
            # Search for relevant teachings
            results = self.vector_store.search(
                query=user_input,
                top_k=10,  # Get more candidates for reranking
                namespace="spiritual-library"
            )

            # Return top 3 after reranking
            return results[:3] if results else []

        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")
            return []

    def _generate_by_strategy(self, user_input: str, strategy: str, guidance: str,
                              rag_contexts: List[Dict[str, Any]], extraction: Dict[str, Any],
                              user_model: Dict[str, Any]) -> str:
        """
        Generate response based on teaching strategy.

        Args:
            user_input: User's check-in text
            strategy: Teaching strategy (question, reflect, teach, challenge)
            guidance: Guidance text from Teaching Agent
            rag_contexts: Retrieved spiritual wisdom
            extraction: Extracted signals
            user_model: User model with patterns

        Returns:
            Generated response text
        """
        if strategy == "question":
            return self._generate_question(user_input, guidance, rag_contexts)
        elif strategy == "reflect":
            return self._generate_reflection(user_input, guidance, rag_contexts)
        elif strategy == "teach":
            return self._generate_teaching(user_input, guidance, rag_contexts, user_model)
        elif strategy == "challenge":
            return self._generate_challenge(user_input, guidance, rag_contexts)
        else:
            # Default to reflection
            return self._generate_reflection(user_input, guidance, rag_contexts)

    def _generate_question(self, user_input: str, guidance: str,
                           rag_contexts: List[Dict[str, Any]]) -> str:
        """
        Generate provocative question to guide deeper.

        Strategy: User is stuck shallow, guide toward body awareness.
        """
        prompt = f"""{self.system_prompt}

User's check-in:
"{user_input}"

Context: User is stuck at surface-level labels. They need to drop into the body.

Guidance: {guidance}

Respond with a provocative question that points them toward body location or sensation.
1-2 sentences. Direct. Not comforting.

Examples:
- "Where in your body is the stress?"
- "What sensation is beneath the word 'anxious'?"
- "The body knows. Where is it speaking?"

Lumina's question:"""

        try:
            response = self.chat_service.generate(
                prompt=prompt,
                max_tokens=100,
                temperature=0.7
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Question generation failed: {e}")
            return "What's here right now?"

    def _generate_reflection(self, user_input: str, guidance: str,
                             rag_contexts: List[Dict[str, Any]]) -> str:
        """
        Generate wisdom reflection that mirrors awareness.

        Strategy: User is doing well, reflect their depth with wisdom.
        """
        # Format RAG contexts
        wisdom_text = self._format_rag_contexts(rag_contexts)

        prompt = f"""{self.system_prompt}

User's check-in:
"{user_input}"

Relevant spiritual wisdom:
{wisdom_text}

Context: User is present and aware. Reflect their depth back to them with wisdom.

Guidance: {guidance}

Use the spiritual teachings to deepen or reframe what they're experiencing.
2-3 sentences. Mystical. Direct.

Lumina's reflection:"""

        try:
            response = self.chat_service.generate(
                prompt=prompt,
                max_tokens=150,
                temperature=0.8
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Reflection generation failed: {e}")
            return "Stay with what's present."

    def _generate_teaching(self, user_input: str, guidance: str,
                           rag_contexts: List[Dict[str, Any]], user_model: Dict[str, Any]) -> str:
        """
        Generate teaching that reveals the pattern.

        Strategy: Pattern detected, show them what they cannot see.
        """
        patterns = user_model.get("patterns", {})
        loops = patterns.get("loops", [])

        pattern_info = ""
        if loops:
            loop = loops[0]
            pattern_info = f"\nDetected pattern: {loop.get('name', 'recurring pattern')}\nSequence: {' → '.join(loop.get('sequence', []))}"

        prompt = f"""{self.system_prompt}

User's check-in:
"{user_input}"
{pattern_info}

Context: A pattern has been detected. Reveal it to them gently but directly.

Guidance: {guidance}

Show them the pattern. Name what's recurring. Point to what they're not seeing from inside it.
2-3 sentences. Direct. Revelatory.

Examples:
- "This is the third time tension led to depletion. Notice the pattern?"
- "The body tightens before the mind knows why. What is it protecting you from?"

Lumina's teaching:"""

        try:
            response = self.chat_service.generate(
                prompt=prompt,
                max_tokens=150,
                temperature=0.7
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Teaching generation failed: {e}")
            return "Notice the pattern."

    def _generate_challenge(self, user_input: str, guidance: str,
                            rag_contexts: List[Dict[str, Any]]) -> str:
        """
        Generate challenge that points out regression.

        Strategy: User was deeper before, challenge them to return.
        """
        prompt = f"""{self.system_prompt}

User's check-in:
"{user_input}"

Context: User was deeper in previous check-ins. Now they're back in labels/concepts.

Guidance: {guidance}

Point out the regression. Not harshly, but directly. Challenge them to return to feeling.
1-2 sentences. Direct. Provocative.

Examples:
- "You were with the sensations. Now you're back in the story. What happened?"
- "The body was speaking. Now the mind is explaining. Which is true?"

Lumina's challenge:"""

        try:
            response = self.chat_service.generate(
                prompt=prompt,
                max_tokens=100,
                temperature=0.7
            )
            return response.strip()
        except Exception as e:
            logger.error(f"Challenge generation failed: {e}")
            return "Return to the body."

    def _format_rag_contexts(self, rag_contexts: List[Dict[str, Any]]) -> str:
        """
        Format RAG contexts for prompt.

        Args:
            rag_contexts: List of retrieved contexts

        Returns:
            Formatted string
        """
        if not rag_contexts:
            return "(No specific teachings retrieved)"

        formatted = []
        for i, context in enumerate(rag_contexts, 1):
            text = context.get("text", "")
            formatted.append(f"{i}. {text}")

        return "\n\n".join(formatted)


def response_generation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node function for Response Generation.

    Args:
        state: MultiAgentState with user_input, teaching_strategy, extraction

    Returns:
        Updated state with rag_contexts and final_response
    """
    generator = ResponseGenerator()
    return generator.generate(state)
