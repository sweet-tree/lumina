"""
Test script for Extraction Agent
"""

from backend.services.extraction_agent import ExtractionAgent
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


def test_extraction():
    """Test extraction agent with various inputs"""
    print("=" * 60)
    print("Testing Extraction Agent")
    print("=" * 60)

    agent = ExtractionAgent()

    test_cases = [
        ("stressed", "Shallow - vague label"),
        ("shoulders tight", "Medium - some body awareness"),
        ("chest tight, breath shallow, meeting in 10 min", "Deep - specific + context"),
        ("jaw clenched, shoulders up to ears, about to call mom", "Deep - very specific"),
        ("was anxious yesterday", "Shallow - past tense, emotional label"),
    ]

    for user_input, description in test_cases:
        print(f"\n{description}")
        print(f"Input: \"{user_input}\"")
        print("-" * 60)

        try:
            result = agent.extract(user_input)
            print(f"Body signals: {result['body_signals']}")
            print(f"Triggers: {result['triggers']}")
            print(f"Temporal: {result['temporal']}")
            print(f"Specificity: {result['specificity_score']}/10")
        except Exception as e:
            print(f"ERROR: {e}")

    print("\n" + "=" * 60)
    print("✓ Extraction tests complete")
    print("=" * 60)


if __name__ == "__main__":
    test_extraction()
