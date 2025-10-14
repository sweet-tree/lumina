"""
Minimal RAG project using Qwen models on Nebius.
Demonstrates chat completions and embedding generation.
"""

from backend.services.chat_service import ChatService
from backend.services.embedding_service import EmbeddingService


def main():
    """Main function to demonstrate both chat and embedding functionality."""

    print("Initializing Qwen RAG project...")

    # Initialize services
    chat_service = ChatService()
    embedding_service = EmbeddingService()

    # Test chat completion
    print("\n1. Testing Chat Completion:")
    print("-" * 30)

    prompt = "Explain the concept of Retrieval-Augmented Generation in simple terms."
    try:
        response = chat_service.generate(prompt, max_tokens=200)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error in chat completion: {e}")

    # Test embedding generation
    print("\n2. Testing Embedding Generation:")
    print("-" * 30)

    text = "Retrieval-Augmented Generation combines retrieval and generation for better responses."
    try:
        embedding = embedding_service.create_embedding(text)
        print(f"Text: {text}")
        print(f"Embedding dimension: {len(embedding)}")
        print(f"First 5 values: {embedding[:5]}")
        print(f"Last 5 values: {embedding[-5:]}")
    except Exception as e:
        print(f"Error in embedding generation: {e}")

    print("\nVerification complete. Both chat and embedding services are working.")


if __name__ == "__main__":
    main()
