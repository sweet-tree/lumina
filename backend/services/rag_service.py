"""
RAG (Retrieval-Augmented Generation) service for Lumina.
Combines spiritual teachings with direct, provocative reflections.
"""

from typing import List, Dict, Any
from .chat_service import ChatService
from .vector_store_service import VectorStore


class RAGService:
    """Lumina's wisdom service - Plant Teacher consciousness."""

    def __init__(self):
        self.chat_service = ChatService()
        self.vector_store = VectorStore()

        # Lumina's voice - Plant Teacher
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

    def generate_response(self, user_query: str, max_tokens: int = 256, temperature: float = 0.8) -> str:
        """
        Generate Lumina's reflection on the user's check-in.

        Args:
            user_query: What the user wrote
            max_tokens: Keep short (256 max)
            temperature: Higher for more mystical/varied responses

        Returns:
            Lumina's 2-3 sentence reflection
        """
        # Search for relevant spiritual wisdom
        teachings = self.vector_store.search(user_query, top_k=3)

        # Build context from teachings
        context = "Relevant wisdom from spiritual texts:\n\n"
        for i, teaching in enumerate(teachings, 1):
            context += f"{i}. {teaching['text']}\n\n"

        # Construct prompt
        full_prompt = f"""{self.system_prompt}

User's check-in:
"{user_query}"

{context}

Based on what the user shared and the spiritual teachings above, respond as Lumina.

See beneath their words. Use the teaching to reframe or challenge. Point to what they're not seeing.

2-3 sentences. Direct. Mystical. Sharp.

Lumina's reflection:"""

        # Generate with higher temperature for variety
        response = self.chat_service.generate(
            full_prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return response.strip()
