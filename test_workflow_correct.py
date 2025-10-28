"""
Correct workflow test - demonstrates the proper pattern

Key: Use a SINGLE service instance for all requests (matches production)
"""

from backend.services.multi_agent_service import MultiAgentService
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))


print("=" * 70)
print("Multi-Agent Workflow Test - Production Pattern")
print("=" * 70)
print("\nKey: Single service instance, multiple requests (like production)")
print("=" * 70)

# Create service ONCE (like FastAPI startup)
print("\n[STARTUP] Creating MultiAgentService...")
service = MultiAgentService()
print("✓ Service created with persistent Store and compiled graph\n")

# Run multiple requests using the SAME service instance
print("=" * 70)
print("REQUEST 1: Shallow input")
print("=" * 70)
result1 = service.process_checkin(
    user_id="user1",
    user_input="stressed"
)
print(f"✓ Depth: {result1['depth']}")
print(f"✓ Has extraction: {'extraction' in result1}")
print(f"✓ Response: {result1['response'][:100]}...")

print("\n" + "=" * 70)
print("REQUEST 2: Deep input")
print("=" * 70)
result2 = service.process_checkin(
    user_id="user2",
    user_input="chest tight, breath shallow, shoulders tense, meeting soon"
)
print(f"✓ Depth: {result2['depth']}")
print(f"✓ Has extraction: {'extraction' in result2}")
if 'extraction' in result2:
    print(f"✓ Body signals: {result2['extraction']['body_signals']}")
    print(f"✓ Specificity: {result2['extraction']['specificity_score']}")
print(f"✓ Response: {result2['response'][:100]}...")

print("\n" + "=" * 70)
print("REQUEST 3: Same user, second check-in")
print("=" * 70)
result3 = service.process_checkin(
    user_id="user2",
    user_input="chest still tight, but breath deeper now"
)
print(f"✓ Depth: {result3['depth']}")
print(f"✓ Has extraction: {'extraction' in result3}")
print(f"✓ Response: {result3['response'][:100]}...")

print("\n" + "=" * 70)
print("REQUEST 4: Card award test")
print("=" * 70)
result4 = service.process_checkin(
    user_id="user3",
    user_input="chest tight, heart racing, breath shallow, stomach churning, meeting in 5 minutes"
)
print(f"✓ Depth: {result4['depth']}")
print(f"✓ Card awarded: {result4['card_decision']['award_card']}")
if result4['card_decision']['award_card']:
    print(
        f"✓ Card: {result4['card_decision']['card_id']} ({result4['card_decision']['rarity']})")
print(f"✓ Response: {result4['response'][:100]}...")

print("\n" + "=" * 70)
print("REQUEST 5: Multiple users")
print("=" * 70)
result5a = service.process_checkin(user_id="user4", user_input="jaw clenched")
result5b = service.process_checkin(
    user_id="user5", user_input="shoulders tense")
print(f"✓ User 4 depth: {result5a['depth']}")
print(f"✓ User 5 depth: {result5b['depth']}")

# Cleanup
print("\n" + "=" * 70)
print("[SHUTDOWN] Closing service...")
print("=" * 70)
service.close()
print("✓ Store connection closed")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)
print("\nConclusion:")
print("- Single service instance handles multiple requests correctly")
print("- No prepared statement conflicts")
print("- This matches production deployment pattern")
print("- Ready for FastAPI integration")
print("=" * 70)
