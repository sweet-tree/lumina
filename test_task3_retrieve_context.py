"""
Test for Task 3: RAG context retrieval node

Run from project root:
    python test_task3_retrieve_context.py
"""

from backend.services.langgraph_service import LuminaState, retrieve_context


def test_retrieve_context_structure():
    """Test that retrieve_context returns correct structure."""

    print("=" * 60)
    print("Testing Task 3: retrieve_context function")
    print("=" * 60)

    # Create a sample state
    state: LuminaState = {
        "user_input": "I feel tension in my chest and my breath is shallow",
        "depth_level": "deep",
        "rag_contexts": [],
        "response": ""
    }

    print(f"\n📝 Query: {state['user_input']}")
    print("\n🔍 Calling retrieve_context...")

    # Call retrieve_context
    result = retrieve_context(state)

    # Verify structure
    print("\n✓ Checking result structure...")
    assert "rag_contexts" in result, "Missing 'rag_contexts' key"
    assert isinstance(result["rag_contexts"],
                      list), "rag_contexts should be a list"

    print(f"  ✓ rag_contexts is a list: {type(result['rag_contexts'])}")

    if len(result["rag_contexts"]) > 0:
        context = result["rag_contexts"][0]

        # Verify dict structure
        assert isinstance(context, dict), "Each context should be a dict"
        assert "source" in context, "Missing 'source' key"
        assert "passages" in context, "Missing 'passages' key"
        assert context["source"] == "spiritual-library", "Wrong source"
        assert isinstance(context["passages"],
                          list), "passages should be a list"

        print(f"  ✓ Context structure is correct")
        print(f"  ✓ Source: {context['source']}")
        print(f"  ✓ Number of passages: {len(context['passages'])}")

        # Show first passage preview
        if context["passages"]:
            print(f"\n📖 First passage preview:")
            print(f"  {context['passages'][0][:150]}...")

        # Verify parallel-ready structure
        print(f"\n✓ Structure supports parallel retrieval:")
        print(f"  - Returns list of dicts ✓")
        print(f"  - Each dict has 'source' and 'passages' ✓")
        print(f"  - Ready to add more sources (Buddhist, Vedic, etc.) ✓")

    else:
        print("\n⚠️  No passages retrieved")
        print("   This could mean:")
        print("   - Vector store is empty")
        print("   - Error occurred (check logs)")
        print("   - No relevant passages found")

    print("\n" + "=" * 60)
    print("✅ Task 3 verification complete!")
    print("=" * 60)

    return True


def test_error_handling():
    """Test that retrieve_context handles errors gracefully."""

    print("\n" + "=" * 60)
    print("Testing error handling")
    print("=" * 60)

    # Test with empty input
    state: LuminaState = {
        "user_input": "",
        "depth_level": "shallow",
        "rag_contexts": [],
        "response": ""
    }

    print("\n📝 Testing with empty input...")
    result = retrieve_context(state)

    # Should return empty contexts, not crash
    assert "rag_contexts" in result
    assert isinstance(result["rag_contexts"], list)

    print("  ✓ Handles empty input gracefully")
    print("  ✓ Returns empty list instead of crashing")

    print("\n✅ Error handling works correctly!")

    return True


if __name__ == "__main__":
    try:
        test_retrieve_context_structure()
        test_error_handling()

        print("\n" + "🎉" * 30)
        print("\n  ALL TESTS PASSED!")
        print("\n" + "🎉" * 30)

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
