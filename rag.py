"""
RAG (Retrieval-Augmented Generation) service for the spiritual coach app.
Combines retrieved spiritual teachings with chat generation to provide personalized guidance.
"""

from typing import List, Dict, Any
from chat import ChatService
from vector_store import VectorStore


class RAGService:
    """Service that combines retrieval and generation for spiritual guidance."""

    def __init__(self):
        self.chat_service = ChatService()
        self.vector_store = VectorStore()

        # Define system prompt for spiritual coaching
        self.system_prompt = """You are a compassionate spiritual coach that combines psychological principles with authentic spiritual teachings. Your role is to help users live in the present moment, develop good habits, and work toward enlightenment.
        
When providing guidance:
1. First, acknowledge the user's experience with empathy
2. Then, share relevant spiritual teachings that address their situation, using the specific traditions mentioned in the retrieved teachings
3. Finally, offer practical advice for integrating these teachings into daily life
        
Always be kind, patient, and non-judgmental. Help the user see their challenges as opportunities for growth."""

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


def main():
    """Test the RAG service with sample queries."""
    print("Initializing RAG Service...")
    rag_service = RAGService()

    # Test queries simulating diary entries or questions
    test_queries = [
        "I'm feeling anxious about the future and can't stop worrying about what might happen",
        "I want to be more present in my daily life but my mind keeps wandering to the past and future",
        "I'm struggling with attachment to outcomes in my work and relationships",
        "I find it hard to work with difficult emotions like anger and sadness when they arise",
        "I'm on a spiritual path and want to understand what enlightenment really means"
    ]

    print("\nTesting RAG Service with sample queries:")
    print("-" * 50)

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("Generating response...")
        response = rag_service.generate_response(query)
        print(f"Response: {response}")
        print("\n" + "="*80)

    print("\nRAG Service test completed successfully!")


if __name__ == "__main__":
    main()
