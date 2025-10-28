"""
Test extraction agent validation and edge cases
"""

from backend.services.extraction_agent import ExtractionAgent
import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


# Enable logging to see validation warnings
logging.basicConfig(level=logging.INFO)


def test_validation():
    """Test validation logic with edge cases"""
    print("=" * 60)
    print("Testing Extraction Validation")
    print("=" * 60)

    agent = ExtractionAgent()

    # Test manual validation
    print("\n1. Testing score clamping...")

    # Test out of range scores
    test_cases = [
        {"body_signals": [], "triggers": [],
            "temporal": "present", "specificity_score": -5},
        {"body_signals": [], "triggers": [],
            "temporal": "present", "specificity_score": 15},
        {"body_signals": [], "triggers": [],
            "temporal": "present", "specificity_score": "invalid"},
        {"body_signals": "not a list", "triggers": [],
            "temporal": "invalid", "specificity_score": 5},
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case}")
        validated = agent._validate_extraction(test_case)
        print(f"   Result: specificity={validated['specificity_score']}, "
              f"temporal={validated['temporal']}, "
              f"body_signals={validated['body_signals']}")

    print("\n" + "=" * 60)
    print("✓ Validation tests complete")
    print("=" * 60)


if __name__ == "__main__":
    test_validation()
