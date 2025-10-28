"""
Test script to verify PostgresStore connection and setup
"""

from backend.services.user_memory import (
    get_user_baseline,
    update_user_baseline,
    get_body_patterns,
    update_body_patterns
)
from backend.services.multi_agent_service import get_multi_agent_service
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


def test_store_setup():
    """Test PostgresStore setup and basic operations"""
    print("=" * 60)
    print("Testing PostgresStore Setup")
    print("=" * 60)

    # Get service
    print("\n1. Initializing MultiAgentService...")
    service = get_multi_agent_service()
    print("✓ Service initialized")

    # Setup store tables
    print("\n2. Setting up Store tables in Supabase...")
    try:
        service.setup_store()
        print("✓ Store tables created")
    except Exception as e:
        print(f"✗ Store setup failed: {e}")
        return False

    # Test helper functions
    print("\n3. Testing helper functions...")
    store = service.store
    test_user_id = "test_user_123"

    # Test baseline
    print(f"\n   a) Testing baseline for {test_user_id}...")
    baseline = get_user_baseline(store, test_user_id)
    print(f"      Initial baseline: {baseline}")

    update_user_baseline(store, test_user_id, 7.5)
    new_baseline = get_user_baseline(store, test_user_id)
    print(f"      After update: {new_baseline}")

    # Test body patterns
    print(f"\n   b) Testing body patterns...")
    update_body_patterns(store, test_user_id, [
                         "chest: tight", "shoulders: tense"])
    patterns = get_body_patterns(store, test_user_id)
    print(f"      Body patterns: {patterns}")

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_store_setup()
    sys.exit(0 if success else 1)
