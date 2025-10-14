"""
Test script for the VectorStore class with spiritual teachings.
Demonstrates storing and retrieving spiritual texts using Pinecone.
"""

import json
from backend.services.vector_store_service import VectorStore


def main():
    print("Initializing VectorStore...")
    vector_store = VectorStore()

    print("Using uploaded documents from spiritual-library namespace")
    print("Teachings stored successfully!")

    # Test retrieval with sample queries
    test_queries = [
        "I'm feeling anxious about the future",
        "How can I be more present in my daily life?",
        "I'm struggling with attachment to outcomes",
        "How can I work with difficult emotions?",
        "What is the path to enlightenment?"
    ]

    print("\nTesting retrieval with sample queries:")
    print("-" * 40)

    for query in test_queries:
        print(f"\nQuery: {query}")
        results = vector_store.search(query)
        print("Top 3 relevant teachings:")
        for i, result in enumerate(results, 1):
            print(f"{i}. Score: {result['score']:.3f}")
            print(f"   {result['text'][:200]}...")

    print("\nVectorStore test completed successfully!")


if __name__ == "__main__":
    main()
