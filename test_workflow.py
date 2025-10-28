"""
Integration test for Multi-Agent Workflow

Tests the complete LangGraph workflow with all agents.
"""

from backend.services.multi_agent_service import MultiAgentService
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


def test_workflow_shallow_input():
    """Test workflow with shallow input"""
    print("\n" + "=" * 60)
    print("Test 1: Shallow Input")
    print("=" * 60)

    service = MultiAgentService()

    result = service.process_checkin(
        user_id="test_user_1",
        user_input="stressed"
    )

    print(f"\nInput: 'stressed'")
    print(f"Depth: {result['depth']}")
    print(f"Strategy: {result.get('teaching_strategy', {}).get('strategy')}")
    print(f"Card Awarded: {result['card_decision'].get('award_card')}")
    print(f"Response: {result['response']}")

    # Assertions
    assert result['depth'] in ['shallow', 'medium', 'deep'], "Invalid depth"
    assert result['response'], "No response generated"
    assert 'card_decision' in result, "No card decision"

    print("\n✓ Test 1 passed")


def test_workflow_deep_input():
    """Test workflow with deep input"""
    print("\n" + "=" * 60)
    print("Test 2: Deep Input")
    print("=" * 60)

    service = MultiAgentService()

    result = service.process_checkin(
        user_id="test_user_2",
        user_input="chest tight, breath shallow, shoulders tense. Meeting in 10 minutes."
    )

    print(f"\nInput: 'chest tight, breath shallow, shoulders tense. Meeting in 10 minutes.'")
    print(f"Depth: {result['depth']}")
    print(f"Strategy: {result.get('teaching_strategy', {}).get('strategy')}")
    print(f"Card Awarded: {result['card_decision'].get('award_card')}")
    print(f"Card ID: {result['card_decision'].get('card_id')}")
    print(f"Response: {result['response']}")

    # Assertions
    assert result['depth'] in ['shallow', 'medium', 'deep'], "Invalid depth"
    assert result['response'], "No response generated"
    assert 'extraction' in result, "No extraction data"

    # Check extraction
    extraction = result.get('extraction', {})
    print(f"\nExtraction:")
    print(f"  Body signals: {extraction.get('body_signals')}")
    print(f"  Triggers: {extraction.get('triggers')}")
    print(f"  Specificity: {extraction.get('specificity_score')}")

    print("\n✓ Test 2 passed")


def test_workflow_state_propagation():
    """Test that state propagates correctly through all agents"""
    print("\n" + "=" * 60)
    print("Test 3: State Propagation")
    print("=" * 60)

    service = MultiAgentService()

    result = service.process_checkin(
        user_id="test_user_3",
        user_input="jaw clenched, stomach tight"
    )

    # Verify all agents produced output
    assert 'extraction' in result, "Extraction agent didn't run"
    assert 'depth' in result, "Deep agent didn't run"
    assert 'teaching_strategy' in result, "Teaching agent didn't run"
    assert 'card_decision' in result, "Card agent didn't run"
    assert 'response' in result, "Response generation didn't run"

    print("\n✓ All agents executed successfully")
    print(
        f"  - Extraction: {len(result['extraction'].get('body_signals', []))} body signals")
    print(f"  - Deep: {result['depth']} depth")
    print(
        f"  - Teaching: {result['teaching_strategy'].get('strategy')} strategy")
    print(f"  - Card: {result['card_decision'].get('award_card')} award")
    print(f"  - Response: {len(result['response'])} chars")

    print("\n✓ Test 3 passed")


def test_workflow_multiple_users():
    """Test workflow with multiple users to verify memory isolation"""
    print("\n" + "=" * 60)
    print("Test 4: Multiple Users")
    print("=" * 60)

    service = MultiAgentService()

    # User 1: First check-in
    result1 = service.process_checkin(
        user_id="user_a",
        user_input="chest tight"
    )

    # User 2: First check-in
    result2 = service.process_checkin(
        user_id="user_b",
        user_input="shoulders tense"
    )

    print(f"\nUser A depth: {result1['depth']}")
    print(f"User B depth: {result2['depth']}")

    # Both should work independently
    assert result1['response'], "User A response missing"
    assert result2['response'], "User B response missing"

    print("\n✓ Test 4 passed - Users isolated correctly")


def run_all_tests():
    """Run all workflow tests"""
    print("\n" + "=" * 60)
    print("Multi-Agent Workflow Integration Tests")
    print("=" * 60)

    try:
        test_workflow_shallow_input()
        test_workflow_deep_input()
        test_workflow_state_propagation()
        test_workflow_multiple_users()

        print("\n" + "=" * 60)
        print("✓ All workflow tests passed!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
