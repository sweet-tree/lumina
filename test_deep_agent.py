"""
Test script for Deep Agent
"""

from backend.services.multi_agent_service import get_multi_agent_service
from backend.services.deep_agent import DeepAgent
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


def test_deep_agent():
    """Test Deep Agent with various scenarios"""
    print("=" * 60)
    print("Testing Deep Agent")
    print("=" * 60)

    # Get store from service
    service = get_multi_agent_service()
    store = service.store

    agent = DeepAgent(store)
    test_user_id = "test_deep_user_456"

    # Test Case 1: New user with shallow input
    print("\n1. New user - shallow input")
    print("-" * 60)
    extraction1 = {
        "body_signals": [],
        "triggers": [],
        "temporal": "present",
        "specificity_score": 2.0
    }
    result1 = agent.evaluate(test_user_id, extraction1)
    print(f"Baseline: {result1['user_model']['baseline']:.2f}")
    print(f"Relative depth: {result1['relative_depth']}")
    print(f"In loop: {result1['user_model']['in_loop']}")

    # Test Case 2: Same user with medium input
    print("\n2. Same user - medium input")
    print("-" * 60)
    extraction2 = {
        "body_signals": ["shoulders: tight"],
        "triggers": [],
        "temporal": "present",
        "specificity_score": 5.0
    }
    result2 = agent.evaluate(test_user_id, extraction2)
    print(f"Baseline: {result2['user_model']['baseline']:.2f}")
    print(f"Relative depth: {result2['relative_depth']}")
    print(f"Body patterns: {result2['user_model']['body_patterns']}")

    # Test Case 3: Same user with deep input
    print("\n3. Same user - deep input")
    print("-" * 60)
    extraction3 = {
        "body_signals": ["chest: tight", "breath: shallow"],
        "triggers": ["meeting"],
        "temporal": "future",
        "specificity_score": 8.0
    }
    result3 = agent.evaluate(test_user_id, extraction3)
    print(f"Baseline: {result3['user_model']['baseline']:.2f}")
    print(f"Relative depth: {result3['relative_depth']}")
    print(f"Body patterns: {result3['user_model']['body_patterns']}")
    print(f"Triggers: {result3['user_model']['triggers']}")
    print(f"Progressing: {result3['user_model']['trajectory']['progressing']}")

    # Test Case 4: Regression - back to shallow
    print("\n4. Same user - regression to shallow")
    print("-" * 60)
    extraction4 = {
        "body_signals": [],
        "triggers": [],
        "temporal": "present",
        "specificity_score": 1.0
    }
    result4 = agent.evaluate(test_user_id, extraction4)
    print(f"Baseline: {result4['user_model']['baseline']:.2f}")
    print(f"Relative depth: {result4['relative_depth']}")
    print(f"Regressing: {result4['user_model']['trajectory']['regressing']}")

    print("\n" + "=" * 60)
    print("✓ Deep Agent tests complete")
    print("=" * 60)


if __name__ == "__main__":
    test_deep_agent()
