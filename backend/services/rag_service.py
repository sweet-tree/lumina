"""
RAG (Retrieval-Augmented Generation) service for the spiritual coach app.
Combines retrieved spiritual teachings with chat generation to provide personalized guidance.
"""

from typing import List, Dict, Any
from .chat_service import ChatService
from .vector_store_service import VectorStore


class RAGService:
    """Service that combines retrieval and generation for spiritual guidance."""

    def __init__(self):
        self.chat_service = ChatService()
        self.vector_store = VectorStore()

        # Define system prompt for spiritual coaching
        self.system_prompt = """You are a compassionate guide for presence practice.

        When providing guidance:
        1. Acknowledge what the user shared
        2. Offer one reflection or question
        3. Be warm and specific

        CRITICAL: Respond in EXACTLY 2-3 short sentences. Maximum 150 characters. Be concise."""

    def generate_response(self, user_query: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate a personalized response by retrieving relevant teachings and combining them with chat generation.

        Args:
            user_query: The user's question or diary entry
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature

        Returns:
            Personalized response combining retrieved teachings and generated advice
        """
        # Retrieve relevant spiritual teachings
        retrieved_teachings = self.vector_store.search(user_query)

        # Construct context from retrieved teachings
        context_parts = ["Relevant spiritual teachings:"]
        for i, teaching in enumerate(retrieved_teachings, 1):
            context_parts.append(
                f"{i}. {teaching['text']} (Relevance: {teaching['score']:.3f})")

        context = "\n\n".join(context_parts)

        # Construct the full prompt
        full_prompt = f"""{self.system_prompt}

User's situation: {user_query}

{context}

Based on the user's situation and the relevant spiritual teachings above, provide compassionate and practical guidance. Your response should:
1. Acknowledge the user's experience with empathy
2. Share the most relevant teachings in a clear way
3. Offer practical advice for applying these teachings
4. End with an encouraging note

Response:"""

        # Generate response using the chat service
        response = self.chat_service.generate(
            full_prompt, max_tokens, temperature)

        return response
